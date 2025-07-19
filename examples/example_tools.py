from langchain_core.tools import tool
from typing import Optional
import requests
import json
import datetime
import logging
from ..config import DEFAULT_TOOL_CATEGORIES

logger = logging.getLogger(__name__)

@tool
def get_current_time() -> str:
    """获取当前时间"""
    return f"当前时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

@tool
def calculate(expression: str) -> str:
    """
    计算数学表达式
    
    Args:
        expression: 数学表达式，如 "2 + 3 * 4"
    
    Returns:
        计算结果
    """
    try:
        # 安全地计算表达式
        allowed_names = {
            k: v for k, v in __builtins__.items() 
            if k in ['abs', 'round', 'min', 'max', 'sum', 'pow']
        }
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"计算结果: {expression} = {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"

@tool
def get_weather(city: str) -> str:
    """
    获取城市天气信息（模拟）
    
    Args:
        city: 城市名称
    
    Returns:
        天气信息
    """
    # 这里使用模拟数据，实际应用中可以调用真实的天气API
    weather_data = {
        "北京": {"温度": "20°C", "天气": "晴天", "湿度": "45%"},
        "上海": {"温度": "25°C", "天气": "多云", "湿度": "60%"},
        "广州": {"温度": "30°C", "天气": "阵雨", "湿度": "75%"},
        "深圳": {"温度": "28°C", "天气": "晴天", "湿度": "55%"}
    }
    
    if city in weather_data:
        weather = weather_data[city]
        return f"{city}天气: 温度{weather['温度']}, {weather['天气']}, 湿度{weather['湿度']}"
    else:
        return f"抱歉，没有找到{city}的天气信息"

@tool
def search_web(query: str) -> str:
    """
    搜索网络信息（模拟）
    
    Args:
        query: 搜索查询
    
    Returns:
        搜索结果
    """
    # 这里使用模拟数据，实际应用中可以调用搜索API
    return f"搜索 '{query}' 的结果: 这是模拟的搜索结果，实际应用中会调用真实的搜索API。"

@tool
def translate_text(text: str, target_language: str = "英语") -> str:
    """
    翻译文本（模拟）
    
    Args:
        text: 要翻译的文本
        target_language: 目标语言
    
    Returns:
        翻译结果
    """
    # 这里使用模拟数据，实际应用中可以调用翻译API
    translations = {
        "英语": f"English translation of '{text}': [模拟翻译结果]",
        "日语": f"日本語訳 '{text}': [模擬翻訳結果]",
        "法语": f"Traduction française de '{text}': [résultat de traduction simulé]"
    }
    
    return translations.get(target_language, f"翻译到{target_language}: [模拟翻译结果]")

@tool
def file_operation(operation: str, filename: str, content: Optional[str] = None) -> str:
    """
    文件操作（模拟）
    
    Args:
        operation: 操作类型 (read, write, delete)
        filename: 文件名
        content: 写入内容（仅write操作需要）
    
    Returns:
        操作结果
    """
    if operation == "read":
        return f"读取文件 {filename}: [模拟文件内容]"
    elif operation == "write":
        return f"写入文件 {filename}: 内容已保存"
    elif operation == "delete":
        return f"删除文件 {filename}: 文件已删除"
    else:
        return f"不支持的操作: {operation}"

# 预定义的工具列表
EXAMPLE_TOOLS = [
    get_current_time,
    calculate,
    get_weather,
    search_web,
    translate_text,
    file_operation
]

def get_tools_by_category(category: str) -> list:
    """
    根据类别获取工具
    
    Args:
        category: 工具类别 (time, math, weather, search, translate, file, all)
    
    Returns:
        工具列表
    """
    tool_categories = {
        "time": [get_current_time],
        "math": [calculate],
        "weather": [get_weather],
        "search": [search_web],
        "translate": [translate_text],
        "file": [file_operation],
        "all": EXAMPLE_TOOLS
    }
    
    if category not in DEFAULT_TOOL_CATEGORIES:
        logger.warning(f"未知的工具类别: {category}。支持的类别: {', '.join(DEFAULT_TOOL_CATEGORIES)}")
    
    return tool_categories.get(category, []) 