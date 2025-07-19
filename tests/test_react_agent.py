#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
React Agent测试文件
测试React Agent的基本功能
"""

import unittest
from unittest.mock import patch, MagicMock
from lightce.agent.react_agent import ReactAgent, create_react_agent, ReactAgentConfig, EnvironmentEvent, UserFeedback, AdaptiveRule, BehaviorPattern, ReactionType
from lightce.tools.example_tools import get_current_time, calculate
from lightce.tools.example_adaptive_rules import get_adaptive_rules_by_category, get_behavior_patterns_by_category, create_custom_adaptive_rule

class TestReactAgent(unittest.TestCase):
    """测试ReactAgent类"""
    
    def setUp(self):
        """测试前的设置"""
        self.config = ReactAgentConfig(
            temperature=0.7,
            max_environment_events=10,
            max_user_feedback=10
        )
    
    def test_environment_event_creation(self):
        """测试环境事件创建"""
        event = EnvironmentEvent(
            event_type="系统错误",
            description="数据库连接失败",
            severity=0.8
        )
        
        self.assertEqual(event.event_type, "系统错误")
        self.assertEqual(event.description, "数据库连接失败")
        self.assertEqual(event.severity, 0.8)
    
    def test_user_feedback_creation(self):
        """测试用户反馈创建"""
        feedback = UserFeedback(
            feedback_type=ReactionType.NEGATIVE,
            content="回答不够详细",
            confidence=0.8
        )
        
        self.assertEqual(feedback.feedback_type, ReactionType.NEGATIVE)
        self.assertEqual(feedback.content, "回答不够详细")
        self.assertEqual(feedback.confidence, 0.8)
    
    def test_adaptive_rule_creation(self):
        """测试自适应规则创建"""
        rule = AdaptiveRule(
            name="测试规则",
            description="测试规则描述",
            condition="测试条件",
            action="测试动作",
            priority=8
        )
        
        self.assertEqual(rule.name, "测试规则")
        self.assertEqual(rule.priority, 8)
        self.assertTrue(rule.active)
    
    def test_behavior_pattern_creation(self):
        """测试行为模式创建"""
        pattern = BehaviorPattern(
            pattern_name="测试模式",
            description="测试模式描述",
            triggers=["触发1", "触发2"],
            responses=["响应1", "响应2"],
            success_rate=0.8
        )
        
        self.assertEqual(pattern.pattern_name, "测试模式")
        self.assertEqual(len(pattern.triggers), 2)
        self.assertEqual(len(pattern.responses), 2)
        self.assertEqual(pattern.success_rate, 0.8)
    
    def test_react_agent_creation(self):
        """测试React Agent创建"""
        with patch('lightce.agent.react_agent.ChatOpenAI'):
            agent = ReactAgent(self.config)
            
            self.assertIsNotNone(agent)
            self.assertEqual(len(agent.environment_events), 0)
            self.assertEqual(len(agent.user_feedback), 0)
            self.assertEqual(len(agent.adaptive_rules), 0)
            self.assertEqual(len(agent.behavior_patterns), 0)
    
    def test_add_environment_event(self):
        """测试添加环境事件"""
        with patch('lightce.agent.react_agent.ChatOpenAI'):
            agent = ReactAgent(self.config)
            
            agent.add_environment_event(
                event_type="网络延迟",
                description="网络连接不稳定",
                severity=0.6
            )
            
            self.assertEqual(len(agent.environment_events), 1)
            self.assertEqual(agent.environment_events[0].event_type, "网络延迟")
            self.assertEqual(agent.environment_events[0].severity, 0.6)
    
    def test_add_user_feedback(self):
        """测试添加用户反馈"""
        with patch('lightce.agent.react_agent.ChatOpenAI'):
            agent = ReactAgent(self.config)
            
            agent.add_user_feedback(
                feedback_type=ReactionType.POSITIVE,
                content="回答很好",
                confidence=0.9
            )
            
            self.assertEqual(len(agent.user_feedback), 1)
            self.assertEqual(agent.user_feedback[0].feedback_type, ReactionType.POSITIVE)
            self.assertEqual(agent.user_feedback[0].confidence, 0.9)
    
    def test_add_adaptive_rule(self):
        """测试添加自适应规则"""
        with patch('lightce.agent.react_agent.ChatOpenAI'):
            agent = ReactAgent(self.config)
            
            rule = AdaptiveRule(
                name="测试规则",
                description="测试描述",
                condition="测试条件",
                action="测试动作",
                priority=5
            )
            
            agent.add_adaptive_rule(rule)
            
            self.assertEqual(len(agent.adaptive_rules), 1)
            self.assertEqual(agent.adaptive_rules[0].name, "测试规则")
    
    def test_add_behavior_pattern(self):
        """测试添加行为模式"""
        with patch('lightce.agent.react_agent.ChatOpenAI'):
            agent = ReactAgent(self.config)
            
            pattern = BehaviorPattern(
                pattern_name="测试模式",
                description="测试描述",
                triggers=["触发"],
                responses=["响应"],
                success_rate=0.7
            )
            
            agent.add_behavior_pattern(pattern)
            
            self.assertEqual(len(agent.behavior_patterns), 1)
            self.assertEqual(agent.behavior_patterns[0].pattern_name, "测试模式")
    
    def test_analyze_context(self):
        """测试上下文分析"""
        with patch('lightce.agent.react_agent.ChatOpenAI'):
            agent = ReactAgent(self.config)
            
            # 添加一些事件和反馈
            agent.add_environment_event("系统错误", "数据库连接失败", 0.8)
            agent.add_user_feedback(ReactionType.NEGATIVE, "回答不够详细", 0.7)
            
            context = agent.analyze_context("请帮我解决这个问题")
            
            self.assertIn("recent_events", context)
            self.assertIn("recent_feedback", context)
            self.assertIn("adaptation_needed", context)
            self.assertIn("adaptation_score", context)
    
    def test_environment_events_overflow(self):
        """测试环境事件溢出处理"""
        with patch('lightce.agent.react_agent.ChatOpenAI'):
            agent = ReactAgent(self.config)
            
            # 添加超过限制的事件
            for i in range(15):
                agent.add_environment_event(f"事件{i}", f"描述{i}", 0.5)
            
            # 应该保持在限制内
            self.assertLessEqual(len(agent.environment_events), self.config.max_environment_events)
    
    def test_user_feedback_overflow(self):
        """测试用户反馈溢出处理"""
        with patch('lightce.agent.react_agent.ChatOpenAI'):
            agent = ReactAgent(self.config)
            
            # 添加超过限制的反馈
            for i in range(15):
                agent.add_user_feedback(ReactionType.NEUTRAL, f"反馈{i}", 0.5)
            
            # 应该保持在限制内
            self.assertLessEqual(len(agent.user_feedback), self.config.max_user_feedback)
    
    def test_get_adaptation_stats(self):
        """测试适应统计"""
        with patch('lightce.agent.react_agent.ChatOpenAI'):
            agent = ReactAgent(self.config)
            
            # 添加各种反馈
            agent.add_user_feedback(ReactionType.POSITIVE, "很好", 0.8)
            agent.add_user_feedback(ReactionType.NEGATIVE, "不好", 0.6)
            agent.add_user_feedback(ReactionType.CORRECTION, "错了", 0.9)
            
            # 添加环境事件
            agent.add_environment_event("系统错误", "数据库连接失败", 0.8)
            
            stats = agent.get_adaptation_stats()
            
            self.assertIn("average_adaptation", stats)
            self.assertIn("feedback_distribution", stats)
            self.assertEqual(stats["total_feedback"], 3)
            self.assertEqual(stats["total_events"], 1)
    
    def test_clear_history(self):
        """测试清除历史"""
        with patch('lightce.agent.react_agent.ChatOpenAI'):
            agent = ReactAgent(self.config)
            
            # 添加一些数据
            agent.add_environment_event("事件", "描述", 0.5)
            agent.add_user_feedback(ReactionType.POSITIVE, "反馈", 0.5)
            
            # 清除特定类型
            agent.clear_history("events")
            self.assertEqual(len(agent.environment_events), 0)
            self.assertEqual(len(agent.user_feedback), 1)
            
            # 清除所有
            agent.clear_history("all")
            self.assertEqual(len(agent.user_feedback), 0)

class TestCreateReactAgent(unittest.TestCase):
    """测试create_react_agent便捷函数"""
    
    @patch('lightce.agent.react_agent.ChatOpenAI')
    def test_create_react_agent_basic(self, mock_openai):
        """测试基本React Agent创建"""
        agent = create_react_agent()
        
        self.assertIsNotNone(agent)
        self.assertEqual(agent.config.model_name, "gpt-3.5-turbo")
        self.assertEqual(agent.config.temperature, 0.7)
    
    @patch('lightce.agent.react_agent.ChatOpenAI')
    def test_create_react_agent_with_rules_and_patterns(self, mock_openai):
        """测试带规则和模式的React Agent创建"""
        tools = [get_current_time, calculate]
        adaptive_rules = get_adaptive_rules_by_category("technical")
        behavior_patterns = get_behavior_patterns_by_category("technical_support")
        
        agent = create_react_agent(
            tools=tools,
            adaptive_rules=adaptive_rules,
            behavior_patterns=behavior_patterns
        )
        
        self.assertEqual(len(agent.tools), 2)
        self.assertEqual(len(agent.adaptive_rules), 1)
        self.assertEqual(len(agent.behavior_patterns), 1)

class TestAdaptiveRulesIntegration(unittest.TestCase):
    """测试自适应规则集成"""
    
    def test_adaptive_rule_categories(self):
        """测试自适应规则分类"""
        # 测试技术规则
        technical_rules = get_adaptive_rules_by_category("technical")
        self.assertEqual(len(technical_rules), 1)
        
        # 测试错误纠正规则
        error_rules = get_adaptive_rules_by_category("error_correction")
        self.assertEqual(len(error_rules), 1)
        
        # 测试所有规则
        all_rules = get_adaptive_rules_by_category("all")
        self.assertEqual(len(all_rules), 8)
    
    def test_behavior_pattern_categories(self):
        """测试行为模式分类"""
        # 测试技术支持模式
        tech_patterns = get_behavior_patterns_by_category("technical_support")
        self.assertEqual(len(tech_patterns), 1)
        
        # 测试学习指导模式
        learning_patterns = get_behavior_patterns_by_category("learning_guidance")
        self.assertEqual(len(learning_patterns), 1)
        
        # 测试所有模式
        all_patterns = get_behavior_patterns_by_category("all")
        self.assertEqual(len(all_patterns), 6)
    
    def test_create_custom_adaptive_rule(self):
        """测试创建自定义自适应规则"""
        rule = create_custom_adaptive_rule(
            name="自定义规则",
            description="自定义规则描述",
            condition="自定义条件",
            action="自定义动作",
            priority=7,
            adaptation_factor=1.2
        )
        
        self.assertEqual(rule.name, "自定义规则")
        self.assertEqual(rule.priority, 7)
        self.assertEqual(rule.adaptation_factor, 1.2)
        self.assertTrue(rule.active)

def run_basic_functionality_test():
    """运行基本功能测试（不需要API密钥）"""
    print("运行React Agent基本功能测试...")
    
    # 测试环境事件
    print("测试环境事件:")
    event = EnvironmentEvent(event_type="测试事件", description="测试描述", severity=0.7)
    print(f"事件: {event.event_type}, 严重程度: {event.severity}")
    
    # 测试用户反馈
    print("\n测试用户反馈:")
    feedback = UserFeedback(feedback_type=ReactionType.POSITIVE, content="测试反馈", confidence=0.8)
    print(f"反馈类型: {feedback.feedback_type.value}, 置信度: {feedback.confidence}")
    
    # 测试自适应规则
    print("\n测试自适应规则:")
    rule = AdaptiveRule(name="测试规则", description="测试描述", condition="测试条件", action="测试动作")
    print(f"规则: {rule.name}, 优先级: {rule.priority}")
    
    # 测试行为模式
    print("\n测试行为模式:")
    pattern = BehaviorPattern(pattern_name="测试模式", description="测试描述", triggers=["触发"], responses=["响应"])
    print(f"模式: {pattern.pattern_name}, 成功率: {pattern.success_rate}")
    
    # 测试配置
    print("\n测试配置:")
    config = ReactAgentConfig(temperature=0.5, adaptation_threshold=0.3)
    print(f"配置: 温度={config.temperature}, 适应阈值={config.adaptation_threshold}")
    
    # 测试规则分类
    print("\n测试规则分类:")
    technical_rules = get_adaptive_rules_by_category("technical")
    print(f"技术规则数量: {len(technical_rules)}")
    
    # 测试模式分类
    print("\n测试模式分类:")
    tech_patterns = get_behavior_patterns_by_category("technical_support")
    print(f"技术支持模式数量: {len(tech_patterns)}")
    
    print("\n基本功能测试完成！")

if __name__ == "__main__":
    print("React Agent系统测试")
    print("=" * 30)
    
    # 运行基本功能测试
    run_basic_functionality_test()
    
    print("\n" + "=" * 30)
    print("运行单元测试...")
    
    # 运行单元测试
    unittest.main(argv=[''], exit=False, verbosity=2) 