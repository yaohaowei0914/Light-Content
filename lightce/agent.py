from typing import Dict, List, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import json
from .config import OPENAI_API_KEY, OPENAI_MODEL, TEMPERATURE
from .tools.mini_contents import get_text_length, compress_text, analyze_and_compress
from .tools.get_llm import get_llm_parameters, list_available_models, compare_models

# 定义状态类型
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "对话历史"]
    tools: Annotated[List[Dict], "可用工具列表"]
    tool_results: Annotated[List[Dict], "工具执行结果"]
    current_step: Annotated[str, "当前步骤"]
    iteration_count: Annotated[int, "迭代次数"]

# 定义工具
@tool
def search_web(query: str) -> str:
    """搜索网络信息"""
    return f"搜索结果: {query} - 这是模拟的搜索结果"

@tool
def calculate(expression: str) -> str:
    """计算数学表达式"""
    try:
        result = eval(expression)
        return f"计算结果: {expression} = {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"

@tool
def get_weather(city: str) -> str:
    """获取天气信息"""
    return f"{city}的天气: 晴天，温度25°C，湿度60%"

# 创建工具列表
tools = [
    search_web, calculate, get_weather, 
    get_text_length, compress_text, analyze_and_compress,
    get_llm_parameters, list_available_models, compare_models
]

def create_llm():
    """创建LLM实例"""
    return ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=OPENAI_MODEL,
        temperature=TEMPERATURE
    )

def create_tool_node():
    """创建工具节点"""
    return ToolNode(tools)

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个智能助手，可以帮助用户完成各种任务。
    你可以使用以下工具:
    - search_web: 搜索网络信息
    - calculate: 计算数学表达式
    - get_weather: 获取天气信息
    - get_text_length: 获取文本的长度统计信息（字符数、词数、行数等）
    - compress_text: 根据压缩倍数智能压缩文本内容
    - analyze_and_compress: 分析文本并压缩的综合工具
    - get_llm_parameters: 获取LLM模型的参数信息（max_tokens、推理能力、Top-k、Top-p、temperature等）
    - list_available_models: 列出指定API类型的所有可用模型
    - compare_models: 比较两个模型的参数
    
    请根据用户的需求选择合适的工具，或者直接回答用户的问题。
    如果用户的问题需要工具帮助，请使用相应的工具。
    如果不需要工具，请直接回答。"""),
    MessagesPlaceholder(variable_name="messages"),
    MessagesPlaceholder(variable_name="tool_results")
])

# 创建LLM节点
def llm_node(state: AgentState) -> AgentState:
    """LLM处理节点"""
    messages = state["messages"]
    tool_results = state["tool_results"]
    
    # 构建输入
    inputs = {
        "messages": messages,
        "tool_results": tool_results
    }
    
    # 创建LLM并调用
    llm = create_llm()
    response = llm.invoke(prompt.format_messages(**inputs))
    
    # 更新状态
    new_messages = messages + [response]
    return {
        **state,
        "messages": new_messages,
        "current_step": "llm_response"
    }

# 创建工具调用节点
def tool_calling_node(state: AgentState) -> AgentState:
    """工具调用节点"""
    messages = state["messages"]
    last_message = messages[-1]
    
    # 检查是否需要调用工具
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        # 创建工具节点并调用
        tool_node = create_tool_node()
        tool_results = tool_node.invoke(state)
        return {
            **state,
            "tool_results": tool_results["tool_results"],
            "current_step": "tool_execution"
        }
    else:
        # 不需要工具调用
        return {
            **state,
            "tool_results": [],
            "current_step": "no_tools_needed"
        }

# 创建路由函数
def route_after_llm(state: AgentState) -> str:
    """LLM响应后的路由"""
    messages = state["messages"]
    last_message = messages[-1]
    
    # 检查是否需要工具调用
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tool_calling"
    else:
        return END

def route_after_tools(state: AgentState) -> str:
    """工具执行后的路由"""
    iteration_count = state["iteration_count"]
    
    # 检查是否超过最大迭代次数
    if iteration_count >= 10:
        return END
    else:
        return "llm"

# 构建图
def create_agent_graph() -> StateGraph:
    """创建agent图"""
    workflow = StateGraph(AgentState)
    
    # 添加节点
    workflow.add_node("llm", llm_node)
    workflow.add_node("tool_calling", tool_calling_node)
    
    # 设置入口点
    workflow.set_entry_point("llm")
    
    # 添加条件边
    workflow.add_conditional_edges(
        "llm",
        route_after_llm,
        {"tool_calling": "tool_calling", "end": END}
    )
    workflow.add_conditional_edges(
        "tool_calling",
        route_after_tools,
        {"llm": "llm", "end": END}
    )
    
    # 编译图
    return workflow.compile()

# 创建agent实例
agent_graph = create_agent_graph()

def run_agent(user_input: str, max_iterations: int = 10) -> List[BaseMessage]:
    """运行agent"""
    # 初始化状态
    initial_state = {
        "messages": [HumanMessage(content=user_input)],
        "tools": tools,
        "tool_results": [],
        "current_step": "start",
        "iteration_count": 0
    }
    
    # 运行图
    result = agent_graph.invoke(initial_state)
    
    return result["messages"] 