#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
策略选择工具测试
验证策略选择工具的各种功能
"""

import unittest
from unittest.mock import patch, MagicMock
import time
import json
import re

from lightce.tools.policy_select import (
    PolicySelectAgent, PolicySelectConfig,
    PolicySelectResult, PolicySelectTool,
    create_policy_select_agent, select_policy_with_agent,
    MemoryType, CompressionStrategy
)
from lightce.agent.system import ModelConfig

class TestPolicySelectTool(unittest.TestCase):
    """策略选择工具测试类"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.test_prompt = """
        请分析以下技术文档，提取其中的关键技术要点和实现细节，并生成一个结构化的技术摘要。
        文档内容涉及机器学习算法、深度学习框架和人工智能应用。
        需要保持技术准确性，同时确保信息密度高，便于后续的技术决策和知识管理。
        """
        
        self.test_creative_prompt = """
        请创作一个富有想象力的科幻故事，故事背景设定在2150年的火星殖民地。
        要求故事具有独特的世界观、引人入胜的情节和深刻的人物刻画。
        """
        
        self.test_academic_prompt = """
        请对以下学术论文进行深度分析和评价，重点关注研究方法、理论贡献和实证结果。
        论文主题是关于人工智能在医疗诊断中的应用研究。
        """
    
    def test_policy_select_config(self):
        """测试策略选择配置"""
        config = PolicySelectConfig()
        
        self.assertIsNone(config.model_config)
        self.assertTrue(config.enable_analysis)
        self.assertTrue(config.enable_strategy_selection)
        self.assertTrue(config.enable_compression_optimization)
        self.assertEqual(config.default_strategy, CompressionStrategy.GENERAL)
        self.assertEqual(config.memory_priority[MemoryType.SHORT_TERM], 1)
        self.assertEqual(config.memory_priority[MemoryType.LONG_TERM], 2)
        self.assertEqual(config.memory_priority[MemoryType.PARAMETER], 3)
        self.assertEqual(config.memory_priority[MemoryType.RULE], 4)
    
    def test_policy_select_result(self):
        """测试策略选择结果"""
        result = PolicySelectResult(
            success=True,
            prompt_analysis={"test": "analysis"},
            selected_strategies={MemoryType.SHORT_TERM: CompressionStrategy.TECHNICAL},
            strategy_reasons={MemoryType.SHORT_TERM: "技术文档适合技术策略"},
            compression_config={"test": "config"},
            processing_time=1.5,
            error_message=None
        )
        
        self.assertTrue(result.success)
        self.assertEqual(result.prompt_analysis, {"test": "analysis"})
        self.assertEqual(result.selected_strategies[MemoryType.SHORT_TERM], CompressionStrategy.TECHNICAL)
        self.assertEqual(result.strategy_reasons[MemoryType.SHORT_TERM], "技术文档适合技术策略")
        self.assertEqual(result.compression_config, {"test": "config"})
        self.assertEqual(result.processing_time, 1.5)
        self.assertIsNone(result.error_message)
    
    @patch('lightce.tools.policy_select.UniversalAgent')
    def test_policy_select_agent_initialization(self, mock_agent_class):
        """测试策略选择代理初始化"""
        # 模拟UniversalAgent
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        config = PolicySelectConfig()
        agent = PolicySelectAgent(config)
        
        self.assertEqual(agent.config, config)
        self.assertEqual(agent.policy_history, [])
        mock_agent_class.assert_called_once()
    
    @patch('lightce.tools.policy_select.UniversalAgent')
    def test_create_policy_select_agent(self, mock_agent_class):
        """测试创建策略选择代理的便捷函数"""
        # 模拟UniversalAgent
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        agent = create_policy_select_agent("gpt-3.5-turbo", 0.1)
        
        self.assertIsInstance(agent, PolicySelectAgent)
        self.assertIsNotNone(agent.config.model_config)
        self.assertEqual(agent.config.model_config.model_name, "gpt-3.5-turbo")
        self.assertEqual(agent.config.model_config.temperature, 0.1)
    
    @patch('lightce.tools.policy_select.UniversalAgent')
    def test_select_policy_with_agent(self, mock_agent_class):
        """测试使用代理进行策略选择的便捷函数"""
        # 模拟UniversalAgent和处理结果
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        mock_result = PolicySelectResult(
            success=True,
            prompt_analysis={"test": "analysis"},
            selected_strategies={MemoryType.SHORT_TERM: CompressionStrategy.TECHNICAL},
            strategy_reasons={MemoryType.SHORT_TERM: "技术文档适合技术策略"},
            compression_config={"test": "config"},
            processing_time=1.0,
            error_message=None
        )
        
        mock_agent.select_policy.return_value = mock_result
        
        result = select_policy_with_agent(self.test_prompt, "gpt-3.5-turbo", 0.1)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["prompt_analysis"], {"test": "analysis"})
        self.assertEqual(result["selected_strategies"][MemoryType.SHORT_TERM.value], CompressionStrategy.TECHNICAL.value)
    
    def test_parse_analysis_response(self):
        """测试解析分析响应"""
        agent = PolicySelectAgent()
        
        # 测试技术文档响应
        response = "这是一个技术文档，内容复杂，涉及技术领域"
        analysis = agent._parse_analysis_response(response)
        self.assertEqual(analysis["content_type"]["type"], "technical")
        self.assertEqual(analysis["content_type"]["complexity"], "complex")
        self.assertEqual(analysis["functional_requirements"]["main_function"], "general")
        
        # 测试创意文本响应
        response = "这是一个创意文本，内容简单，涉及创意领域"
        analysis = agent._parse_analysis_response(response)
        self.assertEqual(analysis["content_type"]["type"], "creative")
        self.assertEqual(analysis["content_type"]["complexity"], "simple")
        
        # 测试学术文本响应
        response = "这是一个学术文本，内容复杂，涉及学术领域"
        analysis = agent._parse_analysis_response(response)
        self.assertEqual(analysis["content_type"]["type"], "academic")
        self.assertEqual(analysis["content_type"]["complexity"], "complex")
        
        # 测试新闻文本响应
        response = "这是一个新闻文本，内容中等，涉及新闻领域"
        analysis = agent._parse_analysis_response(response)
        self.assertEqual(analysis["content_type"]["type"], "news")
        self.assertEqual(analysis["content_type"]["complexity"], "medium")
        
        # 测试对话文本响应
        response = "这是一个对话文本，内容简单，涉及对话领域"
        analysis = agent._parse_analysis_response(response)
        self.assertEqual(analysis["content_type"]["type"], "conversation")
        self.assertEqual(analysis["content_type"]["complexity"], "simple")
        
        # 测试通用文本响应
        response = "这是一个通用文本，内容中等"
        analysis = agent._parse_analysis_response(response)
        self.assertEqual(analysis["content_type"]["type"], "general")
        self.assertEqual(analysis["content_type"]["complexity"], "medium")
        
        # 测试功能需求解析
        response = "需要提取信息"
        analysis = agent._parse_analysis_response(response)
        self.assertEqual(analysis["functional_requirements"]["main_function"], "extraction")
        
        response = "需要生成内容"
        analysis = agent._parse_analysis_response(response)
        self.assertEqual(analysis["functional_requirements"]["main_function"], "generation")
        
        response = "需要分析数据"
        analysis = agent._parse_analysis_response(response)
        self.assertEqual(analysis["functional_requirements"]["main_function"], "analysis")
    
    @patch('lightce.tools.policy_select.UniversalAgent')
    def test_select_strategies(self, mock_agent_class):
        """测试策略选择"""
        # 模拟UniversalAgent
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        # 模拟策略选择响应
        selection_response = {
            "strategy": "technical",
            "reason": "技术文档适合技术策略"
        }
        
        mock_agent.run.return_value = {
            "success": True,
            "response": json.dumps(selection_response)
        }
        
        agent = PolicySelectAgent()
        analysis = {
            "content_type": {"type": "technical", "complexity": "complex"},
            "functional_requirements": {"main_function": "extraction"}
        }
        
        selected_strategies, strategy_reasons = agent._select_strategies(self.test_prompt, analysis)
        
        # 验证所有记忆类型都有策略
        self.assertEqual(len(selected_strategies), 4)
        self.assertEqual(len(strategy_reasons), 4)
        
        for memory_type in MemoryType:
            self.assertIn(memory_type, selected_strategies)
            self.assertIn(memory_type, strategy_reasons)
            self.assertIsInstance(selected_strategies[memory_type], CompressionStrategy)
            self.assertIsInstance(strategy_reasons[memory_type], str)
    
    @patch('lightce.tools.policy_select.UniversalAgent')
    def test_select_strategy_for_memory(self, mock_agent_class):
        """测试为特定记忆类型选择策略"""
        # 模拟UniversalAgent
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        # 模拟策略选择响应
        selection_response = {
            "strategy": "technical",
            "reason": "技术文档适合技术策略"
        }
        
        mock_agent.run.return_value = {
            "success": True,
            "response": json.dumps(selection_response)
        }
        
        agent = PolicySelectAgent()
        analysis = {
            "content_type": {"type": "technical", "complexity": "complex"},
            "functional_requirements": {"main_function": "extraction"}
        }
        
        strategy, reason = agent._select_strategy_for_memory(MemoryType.SHORT_TERM, self.test_prompt, analysis)
        
        self.assertEqual(strategy, CompressionStrategy.TECHNICAL)
        self.assertEqual(reason, "技术文档适合技术策略")
    
    @patch('lightce.tools.policy_select.UniversalAgent')
    def test_select_strategy_for_memory_invalid_strategy(self, mock_agent_class):
        """测试无效策略的处理"""
        # 模拟UniversalAgent
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        # 模拟无效策略响应
        selection_response = {
            "strategy": "invalid_strategy",
            "reason": "无效策略"
        }
        
        mock_agent.run.return_value = {
            "success": True,
            "response": json.dumps(selection_response)
        }
        
        agent = PolicySelectAgent()
        analysis = {
            "content_type": {"type": "technical", "complexity": "complex"},
            "functional_requirements": {"main_function": "extraction"}
        }
        
        strategy, reason = agent._select_strategy_for_memory(MemoryType.SHORT_TERM, self.test_prompt, analysis)
        
        # 应该使用默认策略
        self.assertEqual(strategy, agent.config.default_strategy)
        self.assertIn("无效", reason)
    
    @patch('lightce.tools.policy_select.UniversalAgent')
    def test_select_strategy_for_memory_json_error(self, mock_agent_class):
        """测试JSON解析错误的处理"""
        # 模拟UniversalAgent
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        # 模拟无效JSON响应
        mock_agent.run.return_value = {
            "success": True,
            "response": "invalid json"
        }
        
        agent = PolicySelectAgent()
        analysis = {
            "content_type": {"type": "technical", "complexity": "complex"},
            "functional_requirements": {"main_function": "extraction"}
        }
        
        strategy, reason = agent._select_strategy_for_memory(MemoryType.SHORT_TERM, self.test_prompt, analysis)
        
        # 应该使用默认策略
        self.assertEqual(strategy, agent.config.default_strategy)
        self.assertIn("JSON解析失败", reason)
    
    @patch('lightce.tools.policy_select.UniversalAgent')
    def test_select_strategy_for_memory_agent_error(self, mock_agent_class):
        """测试Agent执行错误的处理"""
        # 模拟UniversalAgent
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        # 模拟Agent执行失败
        mock_agent.run.return_value = {
            "success": False,
            "error": "Agent执行失败"
        }
        
        agent = PolicySelectAgent()
        analysis = {
            "content_type": {"type": "technical", "complexity": "complex"},
            "functional_requirements": {"main_function": "extraction"}
        }
        
        strategy, reason = agent._select_strategy_for_memory(MemoryType.SHORT_TERM, self.test_prompt, analysis)
        
        # 应该使用默认策略
        self.assertEqual(strategy, agent.config.default_strategy)
        self.assertIn("Agent执行失败", reason)
    
    def test_generate_default_config(self):
        """测试生成默认配置"""
        agent = PolicySelectAgent()
        strategies = {
            MemoryType.SHORT_TERM: CompressionStrategy.TECHNICAL,
            MemoryType.LONG_TERM: CompressionStrategy.ACADEMIC,
            MemoryType.PARAMETER: CompressionStrategy.KEYWORDS,
            MemoryType.RULE: CompressionStrategy.SEMANTIC_EQUIVALENCE
        }
        
        config = agent._generate_default_config(strategies)
        
        # 验证配置结构
        self.assertIn("compression_parameters", config)
        self.assertIn("compression_levels", config)
        self.assertIn("information_priority", config)
        self.assertIn("optimization_suggestions", config)
        
        # 验证每种记忆类型都有配置
        for memory_type in MemoryType:
            self.assertIn(memory_type.value, config["compression_parameters"])
            self.assertIn(memory_type.value, config["compression_levels"])
        
        # 验证短期记忆配置
        short_term_params = config["compression_parameters"][MemoryType.SHORT_TERM.value]
        self.assertEqual(short_term_params["compression_ratio"], 30)
        self.assertEqual(short_term_params["retention_priority"], "speed")
        self.assertEqual(short_term_params["format"], "structured")
        
        # 验证长期记忆配置
        long_term_params = config["compression_parameters"][MemoryType.LONG_TERM.value]
        self.assertEqual(long_term_params["compression_ratio"], 70)
        self.assertEqual(long_term_params["retention_priority"], "accuracy")
        self.assertEqual(long_term_params["format"], "semantic")
        
        # 验证参数输入配置
        parameter_params = config["compression_parameters"][MemoryType.PARAMETER.value]
        self.assertEqual(parameter_params["compression_ratio"], 50)
        self.assertEqual(parameter_params["retention_priority"], "clarity")
        self.assertEqual(parameter_params["format"], "key_value")
        
        # 验证规则配置
        rule_params = config["compression_parameters"][MemoryType.RULE.value]
        self.assertEqual(rule_params["compression_ratio"], 40)
        self.assertEqual(rule_params["retention_priority"], "completeness")
        self.assertEqual(rule_params["format"], "rule_based")
    
    @patch('lightce.tools.policy_select.UniversalAgent')
    def test_batch_select_policy(self, mock_agent_class):
        """测试批量策略选择"""
        # 模拟UniversalAgent
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        # 模拟策略选择响应
        selection_response = {
            "strategy": "technical",
            "reason": "技术文档适合技术策略"
        }
        
        mock_agent.run.return_value = {
            "success": True,
            "response": json.dumps(selection_response)
        }
        
        agent = PolicySelectAgent()
        prompts = ["prompt1", "prompt2", "prompt3"]
        
        results = agent.batch_select_policy(prompts)
        
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertTrue(result.success)
            self.assertEqual(len(result.selected_strategies), 4)
            self.assertEqual(len(result.strategy_reasons), 4)
    
    @patch('lightce.tools.policy_select.UniversalAgent')
    def test_statistics(self, mock_agent_class):
        """测试统计信息"""
        # 模拟UniversalAgent
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        # 模拟策略选择响应
        selection_response = {
            "strategy": "technical",
            "reason": "技术文档适合技术策略"
        }
        
        mock_agent.run.return_value = {
            "success": True,
            "response": json.dumps(selection_response)
        }
        
        agent = PolicySelectAgent()
        
        # 执行多次策略选择
        for _ in range(3):
            agent.select_policy(self.test_prompt)
        
        stats = agent.get_statistics()
        
        self.assertEqual(stats["total_selections"], 3)
        self.assertEqual(stats["successful_selections"], 3)
        self.assertEqual(stats["success_rate"], 1.0)
        self.assertGreater(stats["average_processing_time"], 0)
        self.assertIn("strategy_usage", stats)
    
    def test_policy_select_tool(self):
        """测试LangChain工具包装器"""
        # 创建模拟代理
        mock_agent = MagicMock()
        mock_result = PolicySelectResult(
            success=True,
            prompt_analysis={"test": "analysis"},
            selected_strategies={MemoryType.SHORT_TERM: CompressionStrategy.TECHNICAL},
            strategy_reasons={MemoryType.SHORT_TERM: "技术文档适合技术策略"},
            compression_config={"test": "config"},
            processing_time=1.0,
            error_message=None
        )
        mock_agent.select_policy.return_value = mock_result
        
        # 创建工具
        tool = PolicySelectTool(mock_agent)
        
        self.assertEqual(tool.name, "policy_select")
        self.assertIn("LLM输入", tool.description)
        
        # 测试工具执行
        result = tool._run(self.test_prompt)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["prompt_analysis"], {"test": "analysis"})
        self.assertEqual(result["selected_strategies"][MemoryType.SHORT_TERM.value], CompressionStrategy.TECHNICAL.value)
        self.assertEqual(result["processing_time"], 1.0)
    
    def test_error_handling(self):
        """测试错误处理"""
        agent = PolicySelectAgent()
        
        # 测试空prompt
        result = agent.select_policy("")
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error_message)
        
        # 测试无效记忆类型
        with self.assertRaises(ValueError):
            MemoryType("invalid_type")
    
    def test_configuration_validation(self):
        """测试配置验证"""
        # 测试有效的配置
        config = PolicySelectConfig(
            enable_analysis=True,
            enable_strategy_selection=True,
            enable_compression_optimization=True,
            default_strategy=CompressionStrategy.GENERAL
        )
        
        self.assertTrue(config.enable_analysis)
        self.assertTrue(config.enable_strategy_selection)
        self.assertTrue(config.enable_compression_optimization)
        self.assertEqual(config.default_strategy, CompressionStrategy.GENERAL)
    
    def test_enum_values(self):
        """测试枚举值"""
        # 测试记忆类型枚举
        self.assertEqual(MemoryType.SHORT_TERM.value, "short_term")
        self.assertEqual(MemoryType.LONG_TERM.value, "long_term")
        self.assertEqual(MemoryType.PARAMETER.value, "parameter")
        self.assertEqual(MemoryType.RULE.value, "rule")
        
        # 测试压缩策略枚举
        self.assertEqual(CompressionStrategy.GENERAL.value, "general")
        self.assertEqual(CompressionStrategy.TECHNICAL.value, "technical")
        self.assertEqual(CompressionStrategy.CREATIVE.value, "creative")
        self.assertEqual(CompressionStrategy.ACADEMIC.value, "academic")
        self.assertEqual(CompressionStrategy.NEWS.value, "news")
        self.assertEqual(CompressionStrategy.CONVERSATION.value, "conversation")
        self.assertEqual(CompressionStrategy.KEYWORDS.value, "keywords")
        self.assertEqual(CompressionStrategy.TOPICS.value, "topics")
        self.assertEqual(CompressionStrategy.CONCEPTS.value, "concepts")
        self.assertEqual(CompressionStrategy.ENTITIES.value, "entities")
        self.assertEqual(CompressionStrategy.RELATIONS.value, "relations")
        self.assertEqual(CompressionStrategy.SENTIMENT.value, "sentiment")
        self.assertEqual(CompressionStrategy.INTENT.value, "intent")
        self.assertEqual(CompressionStrategy.SUMMARY.value, "summary")
        self.assertEqual(CompressionStrategy.SEMANTIC_EQUIVALENCE.value, "semantic_equivalence")
        self.assertEqual(CompressionStrategy.DETAILED_ANALYSIS.value, "detailed_analysis")
        self.assertEqual(CompressionStrategy.SIMPLE_EQUIVALENCE.value, "simple_equivalence")
        self.assertEqual(CompressionStrategy.COMPRESSION_LEVEL_1.value, "compression_level_1")
        self.assertEqual(CompressionStrategy.COMPRESSION_LEVEL_2.value, "compression_level_2")
        self.assertEqual(CompressionStrategy.COMPRESSION_LEVEL_3.value, "compression_level_3")
        self.assertEqual(CompressionStrategy.COMPRESSION_LEVEL_4.value, "compression_level_4")
        self.assertEqual(CompressionStrategy.COMPRESSION_LEVEL_5.value, "compression_level_5")

def run_quick_test():
    """运行快速测试"""
    print("运行策略选择工具快速测试...")
    
    # 创建测试实例
    test = TestPolicySelectTool()
    test.setUp()
    
    # 运行关键测试
    test_cases = [
        test.test_policy_select_config,
        test.test_policy_select_result,
        test.test_create_policy_select_agent,
        test.test_parse_analysis_response,
        test.test_generate_default_config,
        test.test_policy_select_tool,
        test.test_error_handling,
        test.test_configuration_validation,
        test.test_enum_values
    ]
    
    passed = 0
    total = len(test_cases)
    
    for test_case in test_cases:
        try:
            test_case()
            passed += 1
            print(f"✓ {test_case.__name__} 通过")
        except Exception as e:
            print(f"✗ {test_case.__name__} 失败: {e}")
    
    print(f"\n测试结果: {passed}/{total} 通过")
    return passed == total

if __name__ == "__main__":
    # 运行快速测试
    if run_quick_test():
        print("\n所有快速测试通过！")
        
        # 运行完整测试套件
        print("\n运行完整测试套件...")
        unittest.main(verbosity=2)
    else:
        print("\n快速测试失败，请检查代码！") 