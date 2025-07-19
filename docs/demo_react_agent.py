#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
React Agent演示程序
展示如何使用能够根据环境变化和用户反馈动态调整行为的智能Agent
"""

import os
from dotenv import load_dotenv
from lightce.agent.react_agent import create_react_agent, ReactAgentConfig, ReactionType
from lightce.tools.example_tools import EXAMPLE_TOOLS, get_tools_by_category
from lightce.tools.example_adaptive_rules import get_adaptive_rules_by_category, get_behavior_patterns_by_category, create_custom_adaptive_rule

# 加载环境变量
load_dotenv()

def demo_basic_react_agent():
    """演示基本React Agent"""
    print("=== 基本React Agent演示 ===")
    
    # 创建React Agent
    agent = create_react_agent(
        tools=EXAMPLE_TOOLS,
        adaptive_rules=get_adaptive_rules_by_category("all"),
        behavior_patterns=get_behavior_patterns_by_category("all")
    )
    
    # 运行Agent
    result = agent.run("请告诉我现在的时间")
    print(f"用户: 请告诉我现在的时间")
    print(f"Agent: {result['response']}")
    print(f"成功: {result['success']}")
    print(f"适应水平: {result['adaptation_level']:.2f}")
    print(f"应用的反应: {result['reaction_applied']}")
    print()

def demo_environment_adaptation():
    """演示环境适应"""
    print("=== 环境适应演示 ===")
    
    agent = create_react_agent(
        tools=get_tools_by_category("time"),
        adaptive_rules=get_adaptive_rules_by_category("emergency")
    )
    
    # 添加环境事件
    agent.add_environment_event(
        event_type="系统错误",
        description="检测到系统性能下降",
        severity=0.8,
        metadata={"component": "database", "error_code": "DB001"}
    )
    
    # 运行Agent
    result = agent.run("请帮我检查系统状态")
    print(f"用户: 请帮我检查系统状态")
    print(f"Agent: {result['response']}")
    print(f"适应水平: {result['adaptation_level']:.2f}")
    print(f"环境事件数量: {result['environment_events_count']}")
    print()

def demo_user_feedback_adaptation():
    """演示用户反馈适应"""
    print("=== 用户反馈适应演示 ===")
    
    agent = create_react_agent(
        tools=EXAMPLE_TOOLS,
        adaptive_rules=get_adaptive_rules_by_category("error_correction")
    )
    
    # 第一次对话
    result1 = agent.run("请解释什么是人工智能")
    print(f"用户: 请解释什么是人工智能")
    print(f"Agent: {result1['response']}")
    print()
    
    # 添加负面反馈
    agent.add_user_feedback(
        feedback_type=ReactionType.NEGATIVE,
        content="你的解释太复杂了，我不理解",
        confidence=0.9
    )
    
    # 第二次对话 - 应该适应
    result2 = agent.run("请重新解释人工智能")
    print(f"用户: 请重新解释人工智能")
    print(f"Agent: {result2['response']}")
    print(f"适应水平: {result2['adaptation_level']:.2f}")
    print(f"用户反馈数量: {result2['user_feedback_count']}")
    print()

def demo_adaptive_rules():
    """演示自适应规则"""
    print("=== 自适应规则演示 ===")
    
    # 创建自定义规则
    custom_rule = create_custom_adaptive_rule(
        name="编程问题规则",
        description="处理编程问题时提供代码示例",
        condition="编程 代码 函数 类 变量",
        action="提供代码示例和详细解释",
        priority=8,
        adaptation_factor=1.3
    )
    
    agent = create_react_agent(
        tools=EXAMPLE_TOOLS,
        adaptive_rules=[custom_rule] + get_adaptive_rules_by_category("technical")
    )
    
    result = agent.run("请帮我写一个Python函数来计算斐波那契数列")
    print(f"用户: 请帮我写一个Python函数来计算斐波那契数列")
    print(f"Agent: {result['response']}")
    print(f"自适应规则数量: {result['adaptive_rules_count']}")
    print()

def demo_behavior_patterns():
    """演示行为模式"""
    print("=== 行为模式演示 ===")
    
    agent = create_react_agent(
        behavior_patterns=get_behavior_patterns_by_category("learning_guidance")
    )
    
    result = agent.run("请帮我理解机器学习的基本概念")
    print(f"用户: 请帮我理解机器学习的基本概念")
    print(f"Agent: {result['response']}")
    print(f"行为模式数量: {result['behavior_patterns_count']}")
    print()

def demo_context_analysis():
    """演示上下文分析"""
    print("=== 上下文分析演示 ===")
    
    agent = create_react_agent(
        tools=EXAMPLE_TOOLS,
        adaptive_rules=get_adaptive_rules_by_category("all")
    )
    
    # 添加多个环境事件和用户反馈
    agent.add_environment_event("网络延迟", "网络连接不稳定", 0.6)
    agent.add_environment_event("内存不足", "系统内存使用率过高", 0.7)
    agent.add_user_feedback(ReactionType.POSITIVE, "回答很准确", 0.8)
    agent.add_user_feedback(ReactionType.CORRECTION, "这个信息过时了", 0.9)
    
    result = agent.run("请帮我优化系统性能")
    print(f"用户: 请帮我优化系统性能")
    print(f"Agent: {result['response']}")
    print(f"适应水平: {result['adaptation_level']:.2f}")
    print(f"环境事件数量: {result['environment_events_count']}")
    print(f"用户反馈数量: {result['user_feedback_count']}")
    
    # 显示上下文分析
    context = result.get('context_analysis', {})
    print(f"适用规则: {len(context.get('applicable_rules', []))}")
    print(f"匹配模式: {len(context.get('matching_patterns', []))}")
    print()

def demo_learning_adaptation():
    """演示学习适应"""
    print("=== 学习适应演示 ===")
    
    agent = create_react_agent(
        adaptive_rules=get_adaptive_rules_by_category("learning"),
        behavior_patterns=get_behavior_patterns_by_category("learning_guidance")
    )
    
    # 第一次学习请求
    result1 = agent.run("请解释什么是递归")
    print(f"用户: 请解释什么是递归")
    print(f"Agent: {result1['response']}")
    print()
    
    # 添加澄清反馈
    agent.add_user_feedback(
        feedback_type=ReactionType.CLARIFICATION,
        content="能举个具体的例子吗？",
        confidence=0.7
    )
    
    # 第二次学习请求
    result2 = agent.run("请用例子解释递归")
    print(f"用户: 请用例子解释递归")
    print(f"Agent: {result2['response']}")
    print(f"适应水平: {result2['adaptation_level']:.2f}")
    print()

def demo_creative_adaptation():
    """演示创意适应"""
    print("=== 创意适应演示 ===")
    
    agent = create_react_agent(
        adaptive_rules=get_adaptive_rules_by_category("creative"),
        behavior_patterns=get_behavior_patterns_by_category("creative_inspiration")
    )
    
    result = agent.run("请帮我写一个科幻故事的开头")
    print(f"用户: 请帮我写一个科幻故事的开头")
    print(f"Agent: {result['response']}")
    print(f"适应水平: {result['adaptation_level']:.2f}")
    print()

def demo_adaptation_stats():
    """演示适应统计"""
    print("=== 适应统计演示 ===")
    
    agent = create_react_agent()
    
    # 添加各种反馈
    agent.add_user_feedback(ReactionType.POSITIVE, "回答很好", 0.8)
    agent.add_user_feedback(ReactionType.NEGATIVE, "不够详细", 0.6)
    agent.add_user_feedback(ReactionType.CORRECTION, "这个错了", 0.9)
    agent.add_user_feedback(ReactionType.POSITIVE, "现在明白了", 0.7)
    
    # 添加环境事件
    agent.add_environment_event("用户切换", "用户从初学者切换到专家模式", 0.5)
    agent.add_environment_event("时间压力", "用户需要快速回答", 0.8)
    
    # 获取适应统计
    stats = agent.get_adaptation_stats()
    print(f"适应统计:")
    print(f"- 平均适应水平: {stats['average_adaptation']:.2f}")
    print(f"- 总反馈数量: {stats['total_feedback']}")
    print(f"- 总事件数量: {stats['total_events']}")
    print(f"- 反馈分布: {stats['feedback_distribution']}")
    print()

def demo_configuration():
    """演示配置管理"""
    print("=== 配置管理演示 ===")
    
    # 自定义配置
    config = ReactAgentConfig(
        temperature=0.3,  # 更确定性的回答
        adaptation_threshold=0.2,  # 更敏感的适应阈值
        learning_rate=0.15,  # 更快的学习率
        feedback_weight=0.8,  # 更重视用户反馈
        event_weight=0.2  # 较少重视环境事件
    )
    
    agent = create_react_agent(
        config=config,
        tools=get_tools_by_category("time"),
        adaptive_rules=get_adaptive_rules_by_category("basic")
    )
    
    # 查看配置
    agent_config = agent.get_config()
    print(f"Agent配置:")
    print(f"- 模型: {agent_config['model_config']['model_name']}")
    print(f"- 温度: {agent_config['model_config']['temperature']}")
    print(f"- 工具数量: {len(agent_config['tools'])}")
    print(f"- 自适应规则数量: {len(agent_config['adaptive_rules'])}")
    print(f"- 行为模式数量: {len(agent_config['behavior_patterns'])}")
    print(f"- 环境事件数量: {agent_config['environment_events_count']}")
    print(f"- 用户反馈数量: {agent_config['user_feedback_count']}")
    print()

def demo_continuous_adaptation():
    """演示持续适应"""
    print("=== 持续适应演示 ===")
    
    agent = create_react_agent(
        adaptive_rules=get_adaptive_rules_by_category("all"),
        behavior_patterns=get_behavior_patterns_by_category("all")
    )
    
    # 模拟连续对话和适应过程
    conversations = [
        ("请解释什么是API", "技术问题"),
        ("你的解释太复杂了", "负面反馈"),
        ("请简单解释API", "简化请求"),
        ("很好，现在明白了", "正面反馈"),
        ("请给我一个API的例子", "具体请求"),
        ("这个例子过时了", "纠正反馈"),
        ("请提供最新的API例子", "更新请求")
    ]
    
    for i, (message, context) in enumerate(conversations, 1):
        print(f"对话 {i}: {context}")
        print(f"用户: {message}")
        
        result = agent.run(message)
        print(f"Agent: {result['response'][:100]}...")
        print(f"适应水平: {result['adaptation_level']:.2f}")
        
        # 模拟添加反馈
        if "负面" in context:
            agent.add_user_feedback(ReactionType.NEGATIVE, "用户不满意", 0.8)
        elif "正面" in context:
            agent.add_user_feedback(ReactionType.POSITIVE, "用户满意", 0.8)
        elif "纠正" in context:
            agent.add_user_feedback(ReactionType.CORRECTION, "信息需要更新", 0.9)
        
        print()

def main():
    """主函数"""
    print("React Agent演示程序")
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
        demo_basic_react_agent()
        demo_environment_adaptation()
        demo_user_feedback_adaptation()
        demo_adaptive_rules()
        demo_behavior_patterns()
        demo_context_analysis()
        demo_learning_adaptation()
        demo_creative_adaptation()
        demo_adaptation_stats()
        demo_configuration()
        demo_continuous_adaptation()
        
        print("React Agent演示完成！")
        print("\n特点总结:")
        print("- ✅ 环境事件感知")
        print("- ✅ 用户反馈适应")
        print("- ✅ 自适应规则系统")
        print("- ✅ 行为模式匹配")
        print("- ✅ 上下文分析")
        print("- ✅ 动态参数调整")
        print("- ✅ 持续学习能力")
        print("- ✅ 适应统计监控")
        
    except Exception as e:
        print(f"演示过程中出现错误: {str(e)}")
        print("请检查您的配置和网络连接")

if __name__ == "__main__":
    main() 