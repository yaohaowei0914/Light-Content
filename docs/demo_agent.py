#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用Agent演示程序
展示如何使用LangGraph创建的通用agent，支持工具调用和参数配置
"""

import os
from dotenv import load_dotenv
from lightce.agent.system import UniversalAgent, create_agent, ModelConfig
from lightce.tools.example_tools import EXAMPLE_TOOLS, get_tools_by_category

# 加载环境变量
load_dotenv()

def demo_basic_usage():
    """演示基本用法"""
    print("=== 基本用法演示 ===")
    
    # 方法1: 使用便捷函数创建agent
    agent = create_agent(
        tools=EXAMPLE_TOOLS
    )
    
    # 运行agent
    result = agent.run("请告诉我现在的时间")
    print(f"用户: 请告诉我现在的时间")
    print(f"Agent: {result['response']}")
    print(f"成功: {result['success']}")
    print()

def demo_parameter_config():
    """演示参数配置"""
    print("=== 参数配置演示 ===")
    
    # 方法2: 使用ModelConfig创建agent
    config = ModelConfig(
        temperature=0.1,  # 更低的温度，更确定性的回答
        top_p=0.9,
        top_k=20,
        max_tokens=500
    )
    
    agent = UniversalAgent(config)
    agent.add_tools(get_tools_by_category("math"))
    
    # 运行agent
    result = agent.run("请计算 15 * 23 + 8")
    print(f"用户: 请计算 15 * 23 + 8")
    print(f"Agent: {result['response']}")
    print(f"配置: {agent.get_config()}")
    print()

def demo_dynamic_config_update():
    """演示动态配置更新"""
    print("=== 动态配置更新演示 ===")
    
    agent = create_agent(
        tools=EXAMPLE_TOOLS
    )
    
    # 第一次运行
    result1 = agent.run("请用创意的方式描述今天的天气")
    print(f"用户: 请用创意的方式描述今天的天气")
    print(f"Agent (温度0.7): {result1['response']}")
    print()
    
    # 更新配置
    agent.update_model_config(temperature=1.2, max_tokens=2000)
    
    # 第二次运行
    result2 = agent.run("请用创意的方式描述今天的天气")
    print(f"用户: 请用创意的方式描述今天的天气")
    print(f"Agent (温度1.2): {result2['response']}")
    print(f"新配置: {agent.get_config()}")
    print()

def demo_tool_categories():
    """演示不同工具类别"""
    print("=== 工具类别演示 ===")
    
    # 只使用数学工具
    math_agent = create_agent(
        temperature=0.1,
        tools=get_tools_by_category("math")
    )
    
    result = math_agent.run("请计算 (25 + 15) * 2 / 5")
    print(f"用户: 请计算 (25 + 15) * 2 / 5")
    print(f"Agent: {result['response']}")
    print(f"可用工具: {math_agent.get_config()['tools']}")
    print()
    
    # 只使用天气工具
    weather_agent = create_agent(
        tools=get_tools_by_category("weather")
    )
    
    result = weather_agent.run("请告诉我北京的天气")
    print(f"用户: 请告诉我北京的天气")
    print(f"Agent: {result['response']}")
    print(f"可用工具: {weather_agent.get_config()['tools']}")
    print()

def demo_complex_interaction():
    """演示复杂交互"""
    print("=== 复杂交互演示 ===")
    
    agent = create_agent(
        temperature=0.8,
        tools=EXAMPLE_TOOLS
    )
    
    # 复杂查询
    result = agent.run("""
    请帮我完成以下任务：
    1. 告诉我现在的时间
    2. 计算 100 除以 7 的结果（保留两位小数）
    3. 查询北京的天气
    4. 将"你好世界"翻译成英语
    """)
    
    print(f"用户: 请帮我完成多个任务")
    print(f"Agent: {result['response']}")
    print(f"执行步骤: {result['current_step']}")
    print(f"消息数量: {len(result['messages'])}")
    print()

def demo_error_handling():
    """演示错误处理"""
    print("=== 错误处理演示 ===")
    
    # 创建没有工具的agent
    agent = create_agent()
    
    # 尝试使用不存在的工具
    result = agent.run("请计算 2 + 2")
    print(f"用户: 请计算 2 + 2")
    print(f"Agent: {result['response']}")
    print(f"成功: {result['success']}")
    print(f"错误: {result.get('error')}")
    print()

def demo_ollama_integration():
    """演示Ollama集成（如果可用）"""
    print("=== Ollama集成演示 ===")
    
    try:
        # 尝试使用Ollama
        agent = create_agent(
            model_name="llama2",
            provider="ollama",
            tools=get_tools_by_category("time")
        )
        
        result = agent.run("请告诉我现在的时间")
        print(f"用户: 请告诉我现在的时间")
        print(f"Agent: {result['response']}")
        print(f"成功: {result['success']}")
        
    except Exception as e:
        print(f"Ollama不可用: {str(e)}")
        print("请确保Ollama已安装并运行")
    
    print()

def main():
    """主函数"""
    print("通用Agent演示程序")
    print("=" * 50)
    
    # 检查API密钥
    if not os.getenv("OPENAI_API_KEY"):
        print("警告: 未设置OPENAI_API_KEY环境变量")
        print("请创建.env文件并设置您的OpenAI API密钥")
        print("示例: OPENAI_API_KEY=your_api_key_here")
        print()
    
    try:
        # 运行各种演示
        demo_basic_usage()
        demo_parameter_config()
        demo_dynamic_config_update()
        demo_tool_categories()
        demo_complex_interaction()
        demo_error_handling()
        demo_ollama_integration()
        
        print("演示完成！")
        
    except Exception as e:
        print(f"演示过程中出现错误: {str(e)}")
        print("请检查您的配置和网络连接")

if __name__ == "__main__":
    main() 