#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆Agent演示程序
展示如何使用支持长期记忆、短期对话、工具输出、规则和输出文本的Agent
"""

import os
from dotenv import load_dotenv
from lightce.agent.memory_agent import create_memory_agent, MemoryAgentConfig, Rule
from lightce.tools.example_tools import EXAMPLE_TOOLS, get_tools_by_category
from lightce.tools.example_rules import get_rules_by_category, create_custom_rule

# 加载环境变量
load_dotenv()

def demo_basic_memory_agent():
    """演示基本记忆Agent"""
    print("=== 基本记忆Agent演示 ===")
    
    # 创建记忆Agent
    agent = create_memory_agent(
        tools=EXAMPLE_TOOLS,
        rules=get_rules_by_category("basic")
    )
    
    # 添加一些初始记忆
    agent.add_memory("用户喜欢简洁明了的回答", importance=0.8, category="preference")
    agent.add_memory("用户经常询问技术问题", importance=0.7, category="behavior")
    
    # 运行Agent
    result = agent.run("请告诉我现在的时间")
    print(f"用户: 请告诉我现在的时间")
    print(f"Agent: {result['response']}")
    print(f"成功: {result['success']}")
    print(f"使用的记忆: {result['memories_used']}")
    print(f"应用的规则: {result['rules_applied']}")
    print(f"使用的工具: {result['tools_used']}")
    print()

def demo_memory_learning():
    """演示记忆学习功能"""
    print("=== 记忆学习演示 ===")
    
    agent = create_memory_agent(
        tools=get_tools_by_category("math"),
        rules=get_rules_by_category("learning")
    )
    
    # 第一次对话
    result1 = agent.run("请计算 15 * 23")
    print(f"用户: 请计算 15 * 23")
    print(f"Agent: {result1['response']}")
    print()
    
    # 添加记忆
    agent.add_memory("用户询问了数学计算问题", importance=0.6, category="interaction")
    
    # 第二次对话 - 应该能利用之前的记忆
    result2 = agent.run("再帮我计算一个类似的乘法")
    print(f"用户: 再帮我计算一个类似的乘法")
    print(f"Agent: {result2['response']}")
    print(f"使用的记忆: {result2['memories_used']}")
    print()

def demo_rule_application():
    """演示规则应用"""
    print("=== 规则应用演示 ===")
    
    # 创建自定义规则
    custom_rule = create_custom_rule(
        name="技术专家模式",
        description="以技术专家的身份回答问题",
        content="在回答技术问题时，使用专业术语，提供详细的技术解释，并给出最佳实践建议。",
        priority=8
    )
    
    agent = create_memory_agent(
        tools=EXAMPLE_TOOLS,
        rules=get_rules_by_category("professional") + [custom_rule]
    )
    
    result = agent.run("请解释什么是人工智能")
    print(f"用户: 请解释什么是人工智能")
    print(f"Agent: {result['response']}")
    print(f"应用的规则: {result['rules_applied']}")
    print()

def demo_tool_integration():
    """演示工具集成"""
    print("=== 工具集成演示 ===")
    
    agent = create_memory_agent(
        tools=EXAMPLE_TOOLS,
        rules=get_rules_by_category("basic")
    )
    
    # 添加记忆
    agent.add_memory("用户经常需要查询天气信息", importance=0.7, category="preference")
    
    result = agent.run("请告诉我北京的天气，然后计算今天的日期加上30天")
    print(f"用户: 请告诉我北京的天气，然后计算今天的日期加上30天")
    print(f"Agent: {result['response']}")
    print(f"使用的工具: {result['tools_used']}")
    print()

def demo_memory_management():
    """演示记忆管理"""
    print("=== 记忆管理演示 ===")
    
    agent = create_memory_agent()
    
    # 添加不同类型的记忆
    agent.add_memory("用户的名字是张三", importance=0.9, category="personal")
    agent.add_memory("用户喜欢编程", importance=0.8, category="interest")
    agent.add_memory("用户住在北京", importance=0.7, category="location")
    agent.add_memory("今天是晴天", importance=0.3, category="weather")
    
    # 查看记忆统计
    stats = agent.get_memory_stats()
    print(f"记忆统计:")
    print(f"- 总记忆数: {stats['total_memories']}")
    print(f"- 平均重要性: {stats['average_importance']:.2f}")
    print(f"- 类别分布: {stats['categories']}")
    print()
    
    # 测试记忆检索
    result = agent.run("你还记得我的信息吗？")
    print(f"用户: 你还记得我的信息吗？")
    print(f"Agent: {result['response']}")
    print(f"使用的记忆: {result['memories_used']}")
    print()

def demo_creative_writing():
    """演示创意写作"""
    print("=== 创意写作演示 ===")
    
    agent = create_memory_agent(
        rules=get_rules_by_category("creative")
    )
    
    # 添加创意相关的记忆
    agent.add_memory("用户喜欢科幻小说", importance=0.8, category="preference")
    agent.add_memory("用户之前写过关于太空探索的故事", importance=0.7, category="creative")
    
    result = agent.run("请帮我写一个关于人工智能的短故事")
    print(f"用户: 请帮我写一个关于人工智能的短故事")
    print(f"Agent: {result['response']}")
    print(f"应用的规则: {result['rules_applied']}")
    print()

def demo_error_handling():
    """演示错误处理"""
    print("=== 错误处理演示 ===")
    
    agent = create_memory_agent(
        rules=get_rules_by_category("error_handling")
    )
    
    # 尝试一个可能出错的任务
    result = agent.run("请告诉我一个不存在的信息")
    print(f"用户: 请告诉我一个不存在的信息")
    print(f"Agent: {result['response']}")
    print(f"应用的规则: {result['rules_applied']}")
    print()

def demo_memory_persistence():
    """演示记忆持久性"""
    print("=== 记忆持久性演示 ===")
    
    agent = create_memory_agent()
    
    # 第一次对话
    result1 = agent.run("我的名字是李四，我喜欢音乐")
    print(f"用户: 我的名字是李四，我喜欢音乐")
    print(f"Agent: {result1['response']}")
    print()
    
    # 第二次对话 - 应该记住之前的信息
    result2 = agent.run("你还记得我的名字吗？")
    print(f"用户: 你还记得我的名字吗？")
    print(f"Agent: {result2['response']}")
    print(f"使用的记忆: {result2['memories_used']}")
    print()

def demo_configuration():
    """演示配置管理"""
    print("=== 配置管理演示 ===")
    
    # 自定义配置
    config = MemoryAgentConfig(
        temperature=0.3,  # 更确定性的回答
        max_short_term_memory=5,
        max_long_term_memory=50,
        memory_importance_threshold=0.5
    )
    
    agent = create_memory_agent(
        config=config,
        tools=get_tools_by_category("time"),
        rules=get_rules_by_category("basic")
    )
    
    # 查看配置
    agent_config = agent.get_config()
    print(f"Agent配置:")
    print(f"- 模型: {agent_config['model_config']['model_name']}")
    print(f"- 温度: {agent_config['model_config']['temperature']}")
    print(f"- 工具数量: {len(agent_config['tools'])}")
    print(f"- 规则数量: {len(agent_config['rules'])}")
    print(f"- 记忆数量: {agent_config['memory_count']}")
    print()

def main():
    """主函数"""
    print("记忆Agent演示程序")
    print("=" * 50)
    
    # 检查API密钥
    if not os.getenv("OPENAI_API_KEY"):
        print("警告: 未设置OPENAI_API_KEY环境变量")
        print("请创建.env文件并设置您的OpenAI API密钥")
        print("示例: OPENAI_API_KEY=your_api_key_here")
        print()
        print("注意: 以下演示需要有效的API密钥才能正常运行")
        print()
    
    try:
        # 运行各种演示
        demo_basic_memory_agent()
        demo_memory_learning()
        demo_rule_application()
        demo_tool_integration()
        demo_memory_management()
        demo_creative_writing()
        demo_error_handling()
        demo_memory_persistence()
        demo_configuration()
        
        print("记忆Agent演示完成！")
        print("\n特点总结:")
        print("- ✅ 长期记忆管理")
        print("- ✅ 短期对话记忆")
        print("- ✅ 工具调用集成")
        print("- ✅ 规则系统")
        print("- ✅ 输出文本生成")
        print("- ✅ 记忆检索和利用")
        print("- ✅ 配置管理")
        
    except Exception as e:
        print(f"演示过程中出现错误: {str(e)}")
        print("请检查您的配置和网络连接")

if __name__ == "__main__":
    main() 