#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆Agent测试文件
测试记忆Agent的基本功能
"""

import unittest
from unittest.mock import patch, MagicMock
from lightce.agent.memory_agent import MemoryAgent, create_memory_agent, MemoryAgentConfig, MemoryItem, Rule
from lightce.tools.example_tools import get_current_time, calculate
from lightce.tools.example_rules import get_rules_by_category, create_custom_rule

class TestMemoryAgent(unittest.TestCase):
    """测试MemoryAgent类"""
    
    def setUp(self):
        """测试前的设置"""
        self.config = MemoryAgentConfig(
            temperature=0.7,
            max_long_term_memory=10,
            max_short_term_memory=5
        )
    
    def test_memory_item_creation(self):
        """测试记忆项创建"""
        memory = MemoryItem(
            content="测试记忆",
            importance=0.8,
            category="test"
        )
        
        self.assertEqual(memory.content, "测试记忆")
        self.assertEqual(memory.importance, 0.8)
        self.assertEqual(memory.category, "test")
    
    def test_rule_creation(self):
        """测试规则创建"""
        rule = Rule(
            name="测试规则",
            description="测试规则描述",
            content="测试规则内容",
            priority=5
        )
        
        self.assertEqual(rule.name, "测试规则")
        self.assertEqual(rule.priority, 5)
        self.assertTrue(rule.active)
    
    def test_memory_agent_creation(self):
        """测试记忆Agent创建"""
        with patch('lightce.agent.memory_agent.ChatOpenAI'):
            agent = MemoryAgent(self.config)
            
            self.assertIsNotNone(agent)
            self.assertEqual(len(agent.long_term_memory), 0)
            self.assertEqual(len(agent.rules), 0)
            self.assertEqual(len(agent.tools), 0)
    
    def test_add_memory(self):
        """测试添加记忆"""
        with patch('lightce.agent.memory_agent.ChatOpenAI'):
            agent = MemoryAgent(self.config)
            
            # 添加记忆
            agent.add_memory("测试记忆内容", importance=0.8, category="test")
            
            self.assertEqual(len(agent.long_term_memory), 1)
            self.assertEqual(agent.long_term_memory[0].content, "测试记忆内容")
            self.assertEqual(agent.long_term_memory[0].importance, 0.8)
    
    def test_add_rule(self):
        """测试添加规则"""
        with patch('lightce.agent.memory_agent.ChatOpenAI'):
            agent = MemoryAgent(self.config)
            
            rule = Rule(
                name="测试规则",
                description="测试描述",
                content="测试内容",
                priority=5
            )
            
            agent.add_rule(rule)
            
            self.assertEqual(len(agent.rules), 1)
            self.assertEqual(agent.rules[0].name, "测试规则")
    
    def test_add_tool(self):
        """测试添加工具"""
        with patch('lightce.agent.memory_agent.ChatOpenAI'):
            agent = MemoryAgent(self.config)
            
            agent.add_tool(get_current_time)
            
            self.assertEqual(len(agent.tools), 1)
            self.assertEqual(agent.tools[0].name, "get_current_time")
    
    def test_get_relevant_memories(self):
        """测试获取相关记忆"""
        with patch('lightce.agent.memory_agent.ChatOpenAI'):
            agent = MemoryAgent(self.config)
            
            # 添加一些记忆
            agent.add_memory("用户喜欢编程", importance=0.8, category="preference")
            agent.add_memory("今天是晴天", importance=0.3, category="weather")
            agent.add_memory("用户住在北京", importance=0.7, category="location")
            
            # 测试相关记忆检索
            relevant = agent.get_relevant_memories("编程", limit=2)
            
            self.assertGreater(len(relevant), 0)
            # 应该找到包含"编程"的记忆
            found_programming = any("编程" in memory.content for memory in relevant)
            self.assertTrue(found_programming)
    
    def test_memory_overflow(self):
        """测试记忆溢出处理"""
        with patch('lightce.agent.memory_agent.ChatOpenAI'):
            agent = MemoryAgent(self.config)
            
            # 添加超过限制的记忆
            for i in range(15):
                agent.add_memory(f"记忆{i}", importance=0.1 + i * 0.05, category="test")
            
            # 应该保持在限制内
            self.assertLessEqual(len(agent.long_term_memory), self.config.max_long_term_memory)
    
    def test_rule_overflow(self):
        """测试规则溢出处理"""
        with patch('lightce.agent.memory_agent.ChatOpenAI'):
            agent = MemoryAgent(self.config)
            
            # 添加超过限制的规则
            for i in range(60):
                rule = Rule(
                    name=f"规则{i}",
                    description=f"描述{i}",
                    content=f"内容{i}",
                    priority=i % 10 + 1
                )
                agent.add_rule(rule)
            
            # 应该保持在限制内
            self.assertLessEqual(len(agent.rules), self.config.max_rules)
    
    def test_get_memory_stats(self):
        """测试记忆统计"""
        with patch('lightce.agent.memory_agent.ChatOpenAI'):
            agent = MemoryAgent(self.config)
            
            # 添加不同类型的记忆
            agent.add_memory("记忆1", importance=0.8, category="personal")
            agent.add_memory("记忆2", importance=0.6, category="work")
            agent.add_memory("记忆3", importance=0.4, category="personal")
            
            stats = agent.get_memory_stats()
            
            self.assertEqual(stats["total_memories"], 3)
            self.assertIn("personal", stats["categories"])
            self.assertIn("work", stats["categories"])
            self.assertEqual(stats["categories"]["personal"], 2)
            self.assertEqual(stats["categories"]["work"], 1)
    
    def test_clear_memory(self):
        """测试清除记忆"""
        with patch('lightce.agent.memory_agent.ChatOpenAI'):
            agent = MemoryAgent(self.config)
            
            # 添加记忆
            agent.add_memory("记忆1", category="personal")
            agent.add_memory("记忆2", category="work")
            agent.add_memory("记忆3", category="personal")
            
            # 清除特定类别的记忆
            agent.clear_memory("personal")
            
            self.assertEqual(len(agent.long_term_memory), 1)
            self.assertEqual(agent.long_term_memory[0].category, "work")
            
            # 清除所有记忆
            agent.clear_memory()
            self.assertEqual(len(agent.long_term_memory), 0)

class TestCreateMemoryAgent(unittest.TestCase):
    """测试create_memory_agent便捷函数"""
    
    @patch('lightce.agent.memory_agent.ChatOpenAI')
    def test_create_memory_agent_basic(self, mock_openai):
        """测试基本记忆Agent创建"""
        agent = create_memory_agent()
        
        self.assertIsNotNone(agent)
        self.assertEqual(agent.config.model_name, "gpt-3.5-turbo")
        self.assertEqual(agent.config.temperature, 0.7)
    
    @patch('lightce.agent.memory_agent.ChatOpenAI')
    def test_create_memory_agent_with_tools_and_rules(self, mock_openai):
        """测试带工具和规则的记忆Agent创建"""
        tools = [get_current_time, calculate]
        rules = get_rules_by_category("basic")
        
        agent = create_memory_agent(tools=tools, rules=rules)
        
        self.assertEqual(len(agent.tools), 2)
        self.assertEqual(len(agent.rules), 5)  # basic规则有5个

class TestRuleIntegration(unittest.TestCase):
    """测试规则集成"""
    
    def test_rule_categories(self):
        """测试规则分类"""
        # 测试基础规则
        basic_rules = get_rules_by_category("basic")
        self.assertEqual(len(basic_rules), 5)
        
        # 测试专业规则
        professional_rules = get_rules_by_category("professional")
        self.assertEqual(len(professional_rules), 3)
        
        # 测试所有规则
        all_rules = get_rules_by_category("all")
        self.assertGreater(len(all_rules), 10)
    
    def test_create_custom_rule(self):
        """测试创建自定义规则"""
        rule = create_custom_rule(
            name="自定义规则",
            description="自定义规则描述",
            content="自定义规则内容",
            priority=8
        )
        
        self.assertEqual(rule.name, "自定义规则")
        self.assertEqual(rule.priority, 8)
        self.assertTrue(rule.active)

def run_basic_functionality_test():
    """运行基本功能测试（不需要API密钥）"""
    print("运行记忆Agent基本功能测试...")
    
    # 测试记忆项
    print("测试记忆项:")
    memory = MemoryItem(content="测试记忆", importance=0.8, category="test")
    print(f"记忆项: {memory.content}, 重要性: {memory.importance}")
    
    # 测试规则
    print("\n测试规则:")
    rule = Rule(name="测试规则", description="测试描述", content="测试内容")
    print(f"规则: {rule.name}, 优先级: {rule.priority}")
    
    # 测试配置
    print("\n测试配置:")
    config = MemoryAgentConfig(temperature=0.5, max_long_term_memory=50)
    print(f"配置: 温度={config.temperature}, 最大记忆={config.max_long_term_memory}")
    
    # 测试规则分类
    print("\n测试规则分类:")
    basic_rules = get_rules_by_category("basic")
    print(f"基础规则数量: {len(basic_rules)}")
    
    print("\n基本功能测试完成！")

if __name__ == "__main__":
    print("记忆Agent系统测试")
    print("=" * 30)
    
    # 运行基本功能测试
    run_basic_functionality_test()
    
    print("\n" + "=" * 30)
    print("运行单元测试...")
    
    # 运行单元测试
    unittest.main(argv=[''], exit=False, verbosity=2) 