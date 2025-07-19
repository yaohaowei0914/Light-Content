#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent系统测试文件
测试通用agent的基本功能
"""

import unittest
from unittest.mock import patch, MagicMock
from lightce.agent.system import UniversalAgent, create_agent, ModelConfig
from lightce.tools.example_tools import get_current_time, calculate

class TestUniversalAgent(unittest.TestCase):
    """测试UniversalAgent类"""
    
    def setUp(self):
        """测试前的设置"""
        self.config = ModelConfig(
            temperature=0.7
        )
    
    def test_model_config_creation(self):
        """测试ModelConfig创建"""
        config = ModelConfig()
        self.assertEqual(config.model_name, "gpt-3.5-turbo")  # 默认值
        self.assertEqual(config.temperature, 0.7)  # 默认值
        self.assertEqual(config.provider, "openai")  # 默认值
    
    def test_model_config_validation(self):
        """测试ModelConfig参数验证"""
        # 测试温度范围
        with self.assertRaises(ValueError):
            ModelConfig(temperature=3.0)  # 超出范围
        
        with self.assertRaises(ValueError):
            ModelConfig(temperature=-1.0)  # 超出范围
        
        # 测试top_p范围
        with self.assertRaises(ValueError):
            ModelConfig(top_p=1.5)  # 超出范围
        
        # 测试top_k范围
        with self.assertRaises(ValueError):
            ModelConfig(top_k=0)  # 超出范围
    
    @patch('lightce.agent.system.ChatOpenAI')
    def test_agent_creation(self, mock_openai):
        """测试Agent创建"""
        mock_llm = MagicMock()
        mock_openai.return_value = mock_llm
        
        agent = UniversalAgent(self.config)
        
        self.assertIsNotNone(agent)
        self.assertEqual(agent.model_config.model_name, "gpt-3.5-turbo")  # 默认值
        self.assertEqual(len(agent.tools), 0)
    
    def test_add_tools(self):
        """测试添加工具"""
        with patch('lightce.agent.system.ChatOpenAI'):
            agent = UniversalAgent(self.config)
            
            # 添加单个工具
            agent.add_tool(get_current_time)
            self.assertEqual(len(agent.tools), 1)
            self.assertEqual(agent.tools[0].name, "get_current_time")
            
            # 添加多个工具
            agent.add_tools([calculate])
            self.assertEqual(len(agent.tools), 2)
    
    def test_update_model_config(self):
        """测试更新模型配置"""
        with patch('lightce.agent.system.ChatOpenAI') as mock_openai:
            agent = UniversalAgent(self.config)
            
            # 更新配置
            agent.update_model_config(temperature=0.5, max_tokens=2000)
            
            self.assertEqual(agent.model_config.temperature, 0.5)
            self.assertEqual(agent.model_config.max_tokens, 2000)
            
            # 应该重新创建LLM
            self.assertEqual(mock_openai.call_count, 2)
    
    def test_get_config(self):
        """测试获取配置"""
        with patch('lightce.agent.system.ChatOpenAI'):
            agent = UniversalAgent(self.config)
            agent.add_tool(get_current_time)
            
            config = agent.get_config()
            
            self.assertIn('model_config', config)
            self.assertIn('tools', config)
            self.assertIn('graph_nodes', config)
            self.assertEqual(config['tools'], ['get_current_time'])

class TestCreateAgent(unittest.TestCase):
    """测试create_agent便捷函数"""
    
    @patch('lightce.agent.system.ChatOpenAI')
    def test_create_agent_basic(self, mock_openai):
        """测试基本agent创建"""
        agent = create_agent(
            model_name="gpt-3.5-turbo",
            temperature=0.5
        )
        
        self.assertIsNotNone(agent)
        self.assertEqual(agent.model_config.model_name, "gpt-3.5-turbo")
        self.assertEqual(agent.model_config.temperature, 0.5)
    
    @patch('lightce.agent.system.ChatOpenAI')
    def test_create_agent_with_tools(self, mock_openai):
        """测试带工具的agent创建"""
        tools = [get_current_time, calculate]
        agent = create_agent(tools=tools)
        
        self.assertEqual(len(agent.tools), 2)
        tool_names = [tool.name for tool in agent.tools]
        self.assertIn('get_current_time', tool_names)
        self.assertIn('calculate', tool_names)

class TestToolIntegration(unittest.TestCase):
    """测试工具集成"""
    
    def test_tool_categories(self):
        """测试工具分类"""
        from lightce.tools.example_tools import get_tools_by_category
        
        # 测试数学工具
        math_tools = get_tools_by_category("math")
        self.assertEqual(len(math_tools), 1)
        self.assertEqual(math_tools[0].name, "calculate")
        
        # 测试时间工具
        time_tools = get_tools_by_category("time")
        self.assertEqual(len(time_tools), 1)
        self.assertEqual(time_tools[0].name, "get_current_time")
        
        # 测试所有工具
        all_tools = get_tools_by_category("all")
        self.assertGreater(len(all_tools), 5)  # 应该有多个工具
    
    def test_tool_execution(self):
        """测试工具执行"""
        # 测试时间工具
        result = get_current_time()
        self.assertIn("当前时间", result)
        
        # 测试计算工具
        result = calculate("2 + 3")
        self.assertIn("计算结果", result)
        self.assertIn("5", result)

def run_basic_functionality_test():
    """运行基本功能测试（不需要API密钥）"""
    print("运行基本功能测试...")
    
    # 测试工具
    print("测试工具执行:")
    time_result = get_current_time()
    print(f"时间工具: {time_result}")
    
    calc_result = calculate("10 + 20")
    print(f"计算工具: {calc_result}")
    
    # 测试配置
    print("\n测试配置:")
    config = ModelConfig(temperature=0.5, max_tokens=500)
    print(f"配置: {config.dict()}")
    
    print("\n基本功能测试完成！")

if __name__ == "__main__":
    print("Agent系统测试")
    print("=" * 30)
    
    # 运行基本功能测试
    run_basic_functionality_test()
    
    print("\n" + "=" * 30)
    print("运行单元测试...")
    
    # 运行单元测试
    unittest.main(argv=[''], exit=False, verbosity=2) 