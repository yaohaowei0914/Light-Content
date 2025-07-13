#!/usr/bin/env python3
"""
LangGraph Agent 演示脚本
展示agent的各种功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lightce import run_agent, search_web, calculate, get_weather
from lightce.config import AGENT_NAME

def demo_tools():
    """演示工具功能"""
    print("=" * 60)
    print("工具功能演示")
    print("=" * 60)
    
    # 演示搜索工具
    print("\n1. 搜索工具演示:")
    search_result = search_web("人工智能")
    print(f"搜索 '人工智能': {search_result}")
    
    # 演示计算工具
    print("\n2. 计算工具演示:")
    calc_result = calculate("(10 + 5) * 2")
    print(f"计算 '(10 + 5) * 2': {calc_result}")
    
    # 演示天气工具
    print("\n3. 天气工具演示:")
    weather_result = get_weather("上海")
    print(f"查询上海天气: {weather_result}")

def demo_agent_conversation():
    """演示agent对话功能"""
    print("\n" + "=" * 60)
    print("Agent对话演示")
    print("=" * 60)
    
    # 示例对话
    conversations = [
        "你好，请介绍一下你自己",
        "请帮我计算 25 * 4 + 10",
        "北京今天天气怎么样？",
        "搜索一下Python编程语言的特点"
    ]
    
    for i, user_input in enumerate(conversations, 1):
        print(f"\n对话 {i}:")
        print(f"用户: {user_input}")
        
        try:
            # 运行agent
            messages = run_agent(user_input)
            
            # 显示最后一条AI消息
            for message in messages:
                if hasattr(message, 'type') and message.type == 'ai':
                    if hasattr(message, 'content') and message.content:
                        print(f"助手: {message.content}")
                    break
                    
        except Exception as e:
            print(f"助手: 抱歉，处理您的请求时出现错误: {str(e)}")
            print("(这通常是因为没有设置OpenAI API密钥)")

def main():
    """主演示函数"""
    print(f"欢迎使用 {AGENT_NAME} 演示程序!")
    print("这个演示将展示LangGraph Agent的各种功能")
    
    # 演示工具功能
    demo_tools()
    
    # 演示agent对话
    demo_agent_conversation()
    
    print("\n" + "=" * 60)
    print("演示完成!")
    print("=" * 60)
    print("\n要开始交互式对话，请运行: python main.py")
    print("要运行测试，请运行: python -m unittest tests/test_agent.py")

if __name__ == "__main__":
    main() 