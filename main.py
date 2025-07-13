#!/usr/bin/env python3
"""
LangGraph Agent 主程序
使用LangGraph构建的智能助手
"""

import os
import sys
from typing import List
from langchain_core.messages import BaseMessage

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lightce import run_agent, AGENT_NAME
from lightce.config import OPENAI_API_KEY

def print_messages(messages: List[BaseMessage]):
    """打印消息历史"""
    print("\n" + "="*50)
    print("对话历史:")
    print("="*50)
    
    for i, message in enumerate(messages):
        if hasattr(message, 'content') and message.content:
            role = "用户" if message.type == "human" else "助手"
            print(f"\n{role}: {message.content}")
        
        # 如果有工具调用，显示工具调用信息
        if hasattr(message, 'tool_calls') and message.tool_calls:
            print(f"\n[工具调用]:")
            for tool_call in message.tool_calls:
                print(f"  - 工具: {tool_call['name']}")
                print(f"    参数: {tool_call['args']}")

def main():
    """主函数"""
    print(f"欢迎使用 {AGENT_NAME}!")
    print("这是一个基于LangGraph构建的智能助手")
    print("支持的功能:")
    print("- 搜索网络信息")
    print("- 计算数学表达式") 
    print("- 获取天气信息")
    print("- 一般对话")
    print("\n输入 'quit' 或 'exit' 退出程序")
    print("-" * 50)
    
    # 检查API密钥
    if not OPENAI_API_KEY:
        print("错误: 未设置OPENAI_API_KEY环境变量")
        print("请在.env文件中设置您的OpenAI API密钥")
        return
    
    conversation_history = []
    
    while True:
        try:
            # 获取用户输入
            user_input = input("\n您: ").strip()
            
            # 检查退出命令
            if user_input.lower() in ['quit', 'exit', '退出']:
                print(f"\n感谢使用 {AGENT_NAME}，再见！")
                break
            
            if not user_input:
                continue
            
            print(f"\n{AGENT_NAME} 正在思考...")
            
            # 运行agent
            messages = run_agent(user_input)
            
            # 打印结果
            print_messages(messages)
            
            # 更新对话历史
            conversation_history.extend(messages)
            
        except KeyboardInterrupt:
            print(f"\n\n感谢使用 {AGENT_NAME}，再见！")
            break
        except Exception as e:
            print(f"\n发生错误: {str(e)}")
            print("请重试或联系技术支持")

if __name__ == "__main__":
    main()
