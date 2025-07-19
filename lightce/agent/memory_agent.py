from typing import Dict, List, Any, Optional, TypedDict, Annotated, Union
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from pydantic import BaseModel, Field
import json
import logging
from datetime import datetime, timedelta
from ..config import (
    DEFAULT_MODEL_NAME, DEFAULT_TEMPERATURE, DEFAULT_TOP_P, DEFAULT_TOP_K, 
    DEFAULT_MAX_TOKENS, DEFAULT_PROVIDER, SUPPORTED_PROVIDERS,
    TEMPERATURE_MIN, TEMPERATURE_MAX, TOP_P_MIN, TOP_P_MAX, 
    TOP_K_MIN, MAX_TOKENS_MIN, LOG_LEVEL, LOG_FORMAT
)

# 配置日志
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)

class MemoryItem(BaseModel):
    """记忆项"""
    content: str = Field(description="记忆内容")
    timestamp: datetime = Field(default_factory=datetime.now, description="创建时间")
    importance: float = Field(default=0.5, ge=0.0, le=1.0, description="重要性评分")
    category: str = Field(default="general", description="记忆类别")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")

class Rule(BaseModel):
    """规则定义"""
    name: str = Field(description="规则名称")
    description: str = Field(description="规则描述")
    content: str = Field(description="规则内容")
    priority: int = Field(default=1, ge=1, le=10, description="优先级")
    active: bool = Field(default=True, description="是否激活")

class MemoryAgentState(TypedDict):
    """记忆Agent状态定义"""
    # 对话相关
    messages: Annotated[List[BaseMessage], "对话消息列表"]
    tools: Annotated[List[BaseTool], "可用工具列表"]
    
    # 记忆相关
    long_term_memory: Annotated[List[MemoryItem], "长期记忆"]
    short_term_memory: Annotated[List[BaseMessage], "短期对话记忆"]
    
    # 规则相关
    rules: Annotated[List[Rule], "行为规则"]
    
    # 工具相关
    tool_outputs: Annotated[List[Dict[str, Any]], "工具调用输出"]
    
    # 配置相关
    model_config: Annotated[Dict[str, Any], "模型配置参数"]
    current_step: Annotated[str, "当前执行步骤"]
    error: Annotated[Optional[str], "错误信息"]
    
    # 输出相关
    output_text: Annotated[Optional[str], "最终输出文本"]

class MemoryAgentConfig(BaseModel):
    """记忆Agent配置参数"""
    model_name: str = Field(default=DEFAULT_MODEL_NAME, description="模型名称")
    temperature: float = Field(default=DEFAULT_TEMPERATURE, description="温度参数", ge=TEMPERATURE_MIN, le=TEMPERATURE_MAX)
    top_p: float = Field(default=DEFAULT_TOP_P, description="Top-p参数", ge=TOP_P_MIN, le=TOP_P_MAX)
    top_k: int = Field(default=DEFAULT_TOP_K, description="Top-k参数", ge=TOP_K_MIN)
    max_tokens: int = Field(default=DEFAULT_MAX_TOKENS, description="最大token数", ge=MAX_TOKENS_MIN)
    provider: str = Field(default=DEFAULT_PROVIDER, description=f"模型提供商: {', '.join(SUPPORTED_PROVIDERS)}")
    
    # 记忆相关配置
    max_short_term_memory: int = Field(default=10, description="短期记忆最大条数")
    max_long_term_memory: int = Field(default=1000, description="长期记忆最大条数")
    memory_importance_threshold: float = Field(default=0.3, description="记忆重要性阈值")
    
    # 规则相关配置
    max_rules: int = Field(default=50, description="最大规则数量")
    
    # 工具相关配置
    max_tool_outputs: int = Field(default=20, description="最大工具输出数量")

class MemoryAgent:
    """支持长期记忆、短期对话、工具输出、规则和输出文本的Agent"""
    
    def __init__(self, config: Optional[MemoryAgentConfig] = None):
        """
        初始化记忆Agent
        
        Args:
            config: Agent配置参数
        """
        self.config = config or MemoryAgentConfig()
        self.llm = self._create_llm()
        self.tools: List[BaseTool] = []
        self.rules: List[Rule] = []
        self.long_term_memory: List[MemoryItem] = []
        self.graph = self._build_graph()
        
    def _create_llm(self):
        """根据配置创建LLM实例"""
        if self.config.provider == "openai":
            return ChatOpenAI(
                model=self.config.model_name,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                top_p=self.config.top_p,
                top_k=self.config.top_k
            )
        elif self.config.provider == "ollama":
            return Ollama(
                model=self.config.model_name,
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                top_k=self.config.top_k
            )
        else:
            raise ValueError(f"不支持的模型提供商: {self.config.provider}。支持的提供商: {', '.join(SUPPORTED_PROVIDERS)}")
    
    def add_tool(self, tool: BaseTool):
        """添加工具到agent"""
        self.tools.append(tool)
        logger.info(f"添加工具: {tool.name}")
    
    def add_tools(self, tools: List[BaseTool]):
        """批量添加工具"""
        for tool in tools:
            self.add_tool(tool)
    
    def add_rule(self, rule: Rule):
        """添加规则"""
        if len(self.rules) >= self.config.max_rules:
            # 移除优先级最低的规则
            self.rules.sort(key=lambda x: x.priority)
            self.rules.pop(0)
        
        self.rules.append(rule)
        logger.info(f"添加规则: {rule.name}")
    
    def add_rules(self, rules: List[Rule]):
        """批量添加规则"""
        for rule in rules:
            self.add_rule(rule)
    
    def add_memory(self, content: str, importance: float = 0.5, category: str = "general", metadata: Dict[str, Any] = None):
        """添加长期记忆"""
        if len(self.long_term_memory) >= self.config.max_long_term_memory:
            # 移除最不重要的记忆
            self.long_term_memory.sort(key=lambda x: x.importance)
            self.long_term_memory.pop(0)
        
        memory_item = MemoryItem(
            content=content,
            importance=importance,
            category=category,
            metadata=metadata or {}
        )
        self.long_term_memory.append(memory_item)
        logger.info(f"添加记忆: {content[:50]}...")
    
    def get_relevant_memories(self, query: str, limit: int = 5) -> List[MemoryItem]:
        """获取相关记忆"""
        # 简单的关键词匹配，实际应用中可以使用向量搜索
        relevant_memories = []
        query_lower = query.lower()
        
        for memory in self.long_term_memory:
            if (query_lower in memory.content.lower() or 
                memory.importance >= self.config.memory_importance_threshold):
                relevant_memories.append(memory)
        
        # 按重要性排序并限制数量
        relevant_memories.sort(key=lambda x: x.importance, reverse=True)
        return relevant_memories[:limit]
    
    def update_model_config(self, **kwargs):
        """更新模型配置"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        
        # 重新创建LLM实例
        self.llm = self._create_llm()
        logger.info(f"更新模型配置: {kwargs}")
    
    def _should_continue(self, state: MemoryAgentState) -> str:
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
    
    def _prepare_context(self, state: MemoryAgentState) -> str:
        """准备上下文信息"""
        context_parts = []
        
        # 添加规则
        if state["rules"]:
            rules_text = "行为规则:\n"
            for rule in sorted(state["rules"], key=lambda x: x.priority, reverse=True):
                if rule.active:
                    rules_text += f"- {rule.name}: {rule.description}\n"
            context_parts.append(rules_text)
        
        # 添加相关记忆
        if state["long_term_memory"]:
            # 从最后一条用户消息中提取查询
            user_messages = [msg for msg in state["messages"] if isinstance(msg, HumanMessage)]
            if user_messages:
                query = user_messages[-1].content
                relevant_memories = self.get_relevant_memories(query)
                if relevant_memories:
                    memories_text = "相关记忆:\n"
                    for memory in relevant_memories:
                        memories_text += f"- {memory.content}\n"
                    context_parts.append(memories_text)
        
        # 添加工具输出
        if state["tool_outputs"]:
            outputs_text = "工具输出:\n"
            for output in state["tool_outputs"][-3:]:  # 最近3个输出
                outputs_text += f"- {output.get('tool_name', 'Unknown')}: {output.get('result', '')}\n"
            context_parts.append(outputs_text)
        
        return "\n".join(context_parts)
    
    def _call_model(self, state: MemoryAgentState) -> MemoryAgentState:
        """调用模型生成响应"""
        try:
            # 准备上下文
            context = self._prepare_context(state)
            
            # 创建系统消息
            system_content = f"""你是一个智能助手，具有以下特点：
1. 遵循给定的行为规则
2. 利用相关记忆提供更好的回答
3. 根据需要使用工具完成任务
4. 保持对话的连贯性和上下文理解

{context}

请根据用户的问题和上下文信息提供准确、有用的回答。"""
            
            system_message = SystemMessage(content=system_content)
            
            # 绑定工具到LLM
            llm_with_tools = self.llm.bind_tools(self.tools)
            
            # 准备消息列表
            messages = [system_message] + state["messages"]
            
            # 调用模型
            response = llm_with_tools.invoke(messages)
            
            # 添加AI响应到消息列表
            state["messages"].append(response)
            state["current_step"] = "model_response"
            
            # 更新短期记忆
            state["short_term_memory"].extend(state["messages"][-2:])  # 最近两条消息
            if len(state["short_term_memory"]) > self.config.max_short_term_memory:
                state["short_term_memory"] = state["short_term_memory"][-self.config.max_short_term_memory:]
            
            logger.info("模型响应生成成功")
            return state
            
        except Exception as e:
            error_msg = f"模型调用失败: {str(e)}"
            logger.error(error_msg)
            state["error"] = error_msg
            return state
    
    def _call_tools(self, state: MemoryAgentState) -> MemoryAgentState:
        """调用工具"""
        try:
            # 使用ToolNode处理工具调用
            tool_node = ToolNode(self.tools)
            result = tool_node.invoke(state)
            
            # 更新状态
            state["messages"] = result["messages"]
            state["current_step"] = "tool_execution"
            
            # 记录工具输出
            last_message = state["messages"][-1]
            if isinstance(last_message, ToolMessage):
                tool_output = {
                    "tool_name": last_message.tool_name,
                    "result": last_message.content,
                    "timestamp": datetime.now().isoformat()
                }
                state["tool_outputs"].append(tool_output)
                
                # 限制工具输出数量
                if len(state["tool_outputs"]) > self.config.max_tool_outputs:
                    state["tool_outputs"] = state["tool_outputs"][-self.config.max_tool_outputs:]
            
            logger.info("工具执行完成")
            return state
            
        except Exception as e:
            error_msg = f"工具调用失败: {str(e)}"
            logger.error(error_msg)
            state["error"] = error_msg
            return state
    
    def _generate_output(self, state: MemoryAgentState) -> MemoryAgentState:
        """生成最终输出文本"""
        try:
            # 从最后一条AI消息中提取内容
            ai_messages = [msg for msg in state["messages"] if isinstance(msg, AIMessage)]
            if ai_messages:
                last_ai_message = ai_messages[-1]
                state["output_text"] = last_ai_message.content
            else:
                state["output_text"] = "无法生成响应"
            
            # 将重要信息添加到长期记忆
            if state["output_text"] and len(state["output_text"]) > 10:
                # 简单的记忆重要性评估
                importance = 0.5
                if any(keyword in state["output_text"].lower() for keyword in ["重要", "关键", "记住", "注意"]):
                    importance = 0.8
                
                self.add_memory(
                    content=state["output_text"],
                    importance=importance,
                    category="conversation"
                )
            
            state["current_step"] = "output_generated"
            logger.info("输出文本生成完成")
            return state
            
        except Exception as e:
            error_msg = f"输出生成失败: {str(e)}"
            logger.error(error_msg)
            state["error"] = error_msg
            return state
    
    def _build_graph(self) -> StateGraph:
        """构建LangGraph工作流"""
        workflow = StateGraph(MemoryAgentState)
        
        # 添加节点
        workflow.add_node("agent", self._call_model)
        workflow.add_node("tools", self._call_tools)
        workflow.add_node("output", self._generate_output)
        
        # 设置入口点
        workflow.set_entry_point("agent")
        
        # 添加条件边
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "tools": "tools",
                END: "output"
            }
        )
        
        workflow.add_conditional_edges(
            "tools",
            self._should_continue,
            {
                "agent": "agent",
                END: "output"
            }
        )
        
        # 输出节点直接结束
        workflow.add_edge("output", END)
        
        return workflow.compile()
    
    def run(self, message: str, tools: Optional[List[BaseTool]] = None) -> Dict[str, Any]:
        """
        运行记忆Agent
        
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
        initial_state = MemoryAgentState(
            messages=[HumanMessage(content=message)],
            tools=current_tools,
            long_term_memory=self.long_term_memory.copy(),
            short_term_memory=[],
            rules=self.rules.copy(),
            tool_outputs=[],
            model_config=self.config.dict(),
            current_step="start",
            error=None,
            output_text=None
        )
        
        try:
            # 执行工作流
            result = self.graph.invoke(initial_state)
            
            return {
                "success": True,
                "response": result["output_text"],
                "messages": result["messages"],
                "current_step": result["current_step"],
                "error": result.get("error"),
                "memories_used": len([m for m in result["long_term_memory"] if m in self.long_term_memory]),
                "rules_applied": len([r for r in result["rules"] if r.active]),
                "tools_used": len(result["tool_outputs"])
            }
            
        except Exception as e:
            error_msg = f"记忆Agent执行失败: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "response": None,
                "messages": initial_state["messages"],
                "current_step": "error",
                "error": error_msg,
                "memories_used": 0,
                "rules_applied": 0,
                "tools_used": 0
            }
    
    def get_config(self) -> Dict[str, Any]:
        """获取当前配置"""
        return {
            "model_config": self.config.dict(),
            "tools": [tool.name for tool in self.tools],
            "rules": [rule.name for rule in self.rules if rule.active],
            "memory_count": len(self.long_term_memory),
            "graph_nodes": list(self.graph.nodes.keys())
        }
    
    def clear_memory(self, category: Optional[str] = None):
        """清除记忆"""
        if category:
            self.long_term_memory = [m for m in self.long_term_memory if m.category != category]
            logger.info(f"清除类别 '{category}' 的记忆")
        else:
            self.long_term_memory.clear()
            logger.info("清除所有记忆")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """获取记忆统计信息"""
        categories = {}
        for memory in self.long_term_memory:
            categories[memory.category] = categories.get(memory.category, 0) + 1
        
        return {
            "total_memories": len(self.long_term_memory),
            "categories": categories,
            "average_importance": sum(m.importance for m in self.long_term_memory) / len(self.long_term_memory) if self.long_term_memory else 0
        }

# 便捷函数
def create_memory_agent(
    model_name: str = DEFAULT_MODEL_NAME,
    temperature: float = DEFAULT_TEMPERATURE,
    top_p: float = DEFAULT_TOP_P,
    top_k: int = DEFAULT_TOP_K,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    provider: str = DEFAULT_PROVIDER,
    tools: Optional[List[BaseTool]] = None,
    rules: Optional[List[Rule]] = None
) -> MemoryAgent:
    """
    创建记忆Agent的便捷函数
    
    Args:
        model_name: 模型名称
        temperature: 温度参数
        top_p: Top-p参数
        top_k: Top-k参数
        max_tokens: 最大token数
        provider: 模型提供商
        tools: 工具列表
        rules: 规则列表
    
    Returns:
        MemoryAgent实例
    """
    config = MemoryAgentConfig(
        model_name=model_name,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        max_tokens=max_tokens,
        provider=provider
    )
    
    agent = MemoryAgent(config)
    
    if tools:
        agent.add_tools(tools)
    
    if rules:
        agent.add_rules(rules)
    
    return agent 