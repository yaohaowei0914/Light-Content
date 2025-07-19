from typing import Dict, List, Any, Optional, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from pydantic import BaseModel, Field
import json
import logging
from ..config import (
    DEFAULT_MODEL_NAME, DEFAULT_TEMPERATURE, DEFAULT_TOP_P, DEFAULT_TOP_K, 
    DEFAULT_MAX_TOKENS, DEFAULT_PROVIDER, SUPPORTED_PROVIDERS,
    TEMPERATURE_MIN, TEMPERATURE_MAX, TOP_P_MIN, TOP_P_MAX, 
    TOP_K_MIN, MAX_TOKENS_MIN, LOG_LEVEL, LOG_FORMAT
)

# 配置日志
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)

class AgentState(TypedDict):
    """Agent状态定义"""
    messages: Annotated[List[BaseMessage], "对话消息列表"]
    tools: Annotated[List[BaseTool], "可用工具列表"]
    model_config: Annotated[Dict[str, Any], "模型配置参数"]
    current_step: Annotated[str, "当前执行步骤"]
    error: Annotated[Optional[str], "错误信息"]

class ModelConfig(BaseModel):
    """模型配置参数"""
    model_name: str = Field(default=DEFAULT_MODEL_NAME, description="模型名称")
    temperature: float = Field(default=DEFAULT_TEMPERATURE, description="温度参数", ge=TEMPERATURE_MIN, le=TEMPERATURE_MAX)
    top_p: float = Field(default=DEFAULT_TOP_P, description="Top-p参数", ge=TOP_P_MIN, le=TOP_P_MAX)
    top_k: int = Field(default=DEFAULT_TOP_K, description="Top-k参数", ge=TOP_K_MIN)
    max_tokens: int = Field(default=DEFAULT_MAX_TOKENS, description="最大token数", ge=MAX_TOKENS_MIN)
    provider: str = Field(default=DEFAULT_PROVIDER, description=f"模型提供商: {', '.join(SUPPORTED_PROVIDERS)}")

class UniversalAgent:
    """通用Agent类，支持工具调用和参数配置"""
    
    def __init__(self, model_config: Optional[ModelConfig] = None):
        """
        初始化通用Agent
        
        Args:
            model_config: 模型配置参数
        """
        self.model_config = model_config or ModelConfig()
        self.llm = self._create_llm()
        self.tools: List[BaseTool] = []
        self.graph = self._build_graph()
        
    def _create_llm(self):
        """根据配置创建LLM实例"""
        if self.model_config.provider == "openai":
            return ChatOpenAI(
                model=self.model_config.model_name,
                temperature=self.model_config.temperature,
                max_tokens=self.model_config.max_tokens,
                top_p=self.model_config.top_p
                # 移除top_k参数，因为OpenAI API不支持
            )
        elif self.model_config.provider == "ollama":
            return Ollama(
                model=self.model_config.model_name,
                temperature=self.model_config.temperature,
                top_p=self.model_config.top_p,
                top_k=self.model_config.top_k
            )
        else:
            raise ValueError(f"不支持的模型提供商: {self.model_config.provider}。支持的提供商: {', '.join(SUPPORTED_PROVIDERS)}")
    
    def add_tool(self, tool: BaseTool):
        """添加工具到agent"""
        self.tools.append(tool)
        logger.info(f"添加工具: {tool.name}")
    
    def add_tools(self, tools: List[BaseTool]):
        """批量添加工具"""
        for tool in tools:
            self.add_tool(tool)
    
    def update_model_config(self, **kwargs):
        """更新模型配置"""
        for key, value in kwargs.items():
            if hasattr(self.model_config, key):
                setattr(self.model_config, key, value)
        
        # 重新创建LLM实例
        self.llm = self._create_llm()
        logger.info(f"更新模型配置: {kwargs}")
    
    def _should_continue(self, state: AgentState) -> str:
        """判断是否继续执行"""
        last_message = state["messages"][-1]
        
        # 如果最后一条消息是工具调用，继续执行
        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            return "tools"
        
        # 如果最后一条消息是工具结果，继续执行
        if isinstance(last_message, ToolMessage):
            return "agent"
        
        # 否则结束
        return END
    
    def _call_model(self, state: AgentState) -> AgentState:
        """调用模型生成响应"""
        try:
            # 绑定工具到LLM
            llm_with_tools = self.llm.bind_tools(self.tools)
            
            # 调用模型
            response = llm_with_tools.invoke(state["messages"])
            
            # 添加AI响应到消息列表
            state["messages"].append(response)
            state["current_step"] = "model_response"
            
            logger.info("模型响应生成成功")
            return state
            
        except Exception as e:
            error_msg = f"模型调用失败: {str(e)}"
            logger.error(error_msg)
            state["error"] = error_msg
            return state
    
    def _call_tools(self, state: AgentState) -> AgentState:
        """调用工具"""
        try:
            # 使用ToolNode处理工具调用
            tool_node = ToolNode(self.tools)
            result = tool_node.invoke(state)
            
            # 更新状态
            state["messages"] = result["messages"]
            state["current_step"] = "tool_execution"
            
            logger.info("工具执行完成")
            return state
            
        except Exception as e:
            error_msg = f"工具调用失败: {str(e)}"
            logger.error(error_msg)
            state["error"] = error_msg
            return state
    
    def _build_graph(self) -> StateGraph:
        """构建LangGraph工作流"""
        workflow = StateGraph(AgentState)
        
        # 添加节点
        workflow.add_node("agent", self._call_model)
        workflow.add_node("tools", self._call_tools)
        
        # 设置入口点
        workflow.set_entry_point("agent")
        
        # 添加条件边
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "tools": "tools",
                END: END
            }
        )
        
        workflow.add_conditional_edges(
            "tools",
            self._should_continue,
            {
                "agent": "agent",
                END: END
            }
        )
        
        return workflow.compile()
    
    def run(self, message: str, tools: Optional[List[BaseTool]] = None) -> Dict[str, Any]:
        """
        运行agent
        
        Args:
            message: 用户输入消息
            tools: 可选的工具列表（会覆盖已添加的工具）
        
        Returns:
            执行结果
        """
        # 准备工具列表
        if tools is not None:
            current_tools = tools
        else:
            current_tools = self.tools
        
        # 初始化状态
        initial_state = AgentState(
            messages=[HumanMessage(content=message)],
            tools=current_tools,
            model_config=self.model_config.dict(),
            current_step="start",
            error=None
        )
        
        try:
            # 执行工作流
            result = self.graph.invoke(initial_state)
            
            # 提取最终响应
            final_message = result["messages"][-1]
            if isinstance(final_message, AIMessage):
                response_content = final_message.content
            else:
                response_content = "执行完成"
            
            return {
                "success": True,
                "response": response_content,
                "messages": result["messages"],
                "current_step": result["current_step"],
                "error": result.get("error")
            }
            
        except Exception as e:
            error_msg = f"Agent执行失败: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "response": None,
                "messages": initial_state["messages"],
                "current_step": "error",
                "error": error_msg
            }
    
    def get_config(self) -> Dict[str, Any]:
        """获取当前配置"""
        return {
            "model_config": self.model_config.dict(),
            "tools": [tool.name for tool in self.tools],
            "graph_nodes": list(self.graph.nodes.keys())
        }

# 便捷函数
def create_agent(
    model_name: str = DEFAULT_MODEL_NAME,
    temperature: float = DEFAULT_TEMPERATURE,
    top_p: float = DEFAULT_TOP_P,
    top_k: int = DEFAULT_TOP_K,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    provider: str = DEFAULT_PROVIDER,
    tools: Optional[List[BaseTool]] = None
) -> UniversalAgent:
    """
    创建通用Agent的便捷函数
    
    Args:
        model_name: 模型名称
        temperature: 温度参数
        top_p: Top-p参数
        top_k: Top-k参数
        max_tokens: 最大token数
        provider: 模型提供商
        tools: 工具列表
    
    Returns:
        UniversalAgent实例
    """
    config = ModelConfig(
        model_name=model_name,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        max_tokens=max_tokens,
        provider=provider
    )
    
    agent = UniversalAgent(config)
    
    if tools:
        agent.add_tools(tools)
    
    return agent
