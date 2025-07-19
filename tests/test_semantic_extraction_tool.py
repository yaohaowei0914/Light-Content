#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语义提取工具测试
验证语义提取工具的各种功能
"""

import unittest
from unittest.mock import patch, MagicMock
import time

from lightce.tools.semantic_extraction import (
    SemanticExtractionAgent, SemanticExtractionConfig,
    SemanticExtractionResult, SemanticExtractionTool,
    create_semantic_extraction_agent, extract_semantic_with_agent
)
from lightce.prompt.semantic_extration import ExtractionLevel, ExtractionType
from lightce.agent.system import ModelConfig

class TestSemanticExtractionTool(unittest.TestCase):
    """语义提取工具测试类"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.test_text = """
        人工智能技术正在快速发展，为各行各业带来了革命性的变化。
        深度学习模型在自然语言处理任务中取得了显著的效果提升。
        通过对比分析，我们发现Transformer架构在处理长文本时具有明显优势。
        这些发现为后续的研究提供了重要的理论基础和实践指导。
        """
    
    def test_semantic_extraction_config(self):
        """测试语义提取配置"""
        config = SemanticExtractionConfig()
        
        self.assertEqual(config.extraction_level, ExtractionLevel.BASIC)
        self.assertIsNone(config.extraction_types)
        self.assertIsNone(config.model_config)
        self.assertTrue(config.enable_multi_stage)
        self.assertEqual(config.quality_threshold, 0.8)
    
    def test_semantic_extraction_result(self):
        """测试语义提取结果"""
        result = SemanticExtractionResult(
            success=True,
            extraction_level="basic",
            extraction_types=["keywords", "topics"],
            results={"keywords": {"content": "test"}},
            quality_score=0.9,
            processing_time=1.5,
            error_message=None
        )
        
        self.assertTrue(result.success)
        self.assertEqual(result.extraction_level, "basic")
        self.assertEqual(result.extraction_types, ["keywords", "topics"])
        self.assertEqual(result.quality_score, 0.9)
        self.assertEqual(result.processing_time, 1.5)
        self.assertIsNone(result.error_message)
    
    @patch('lightce.tools.semantic_extraction.UniversalAgent')
    def test_semantic_extraction_agent_initialization(self, mock_agent_class):
        """测试语义提取代理初始化"""
        # 模拟UniversalAgent
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        config = SemanticExtractionConfig()
        agent = SemanticExtractionAgent(config)
        
        self.assertEqual(agent.config, config)
        self.assertEqual(agent.extraction_history, [])
        mock_agent_class.assert_called_once()
    
    @patch('lightce.tools.semantic_extraction.UniversalAgent')
    def test_create_semantic_extraction_agent(self, mock_agent_class):
        """测试创建语义提取代理的便捷函数"""
        # 模拟UniversalAgent
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        agent = create_semantic_extraction_agent("basic", "gpt-3.5-turbo", 0.1)
        
        self.assertIsInstance(agent, SemanticExtractionAgent)
        self.assertEqual(agent.config.extraction_level, ExtractionLevel.BASIC)
        self.assertIsNotNone(agent.config.model_config)
        self.assertEqual(agent.config.model_config.model_name, "gpt-3.5-turbo")
        self.assertEqual(agent.config.model_config.temperature, 0.1)
    
    @patch('lightce.tools.semantic_extraction.UniversalAgent')
    def test_extract_semantic_with_agent(self, mock_agent_class):
        """测试使用代理进行语义提取的便捷函数"""
        # 模拟UniversalAgent和提取结果
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        mock_result = SemanticExtractionResult(
            success=True,
            extraction_level="basic",
            extraction_types=["keywords"],
            results={"keywords": {"content": "test"}},
            quality_score=0.8,
            processing_time=1.0,
            error_message=None
        )
        
        mock_agent.extract_semantic.return_value = mock_result
        
        result = extract_semantic_with_agent(self.test_text, "basic")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["extraction_level"], "basic")
        self.assertEqual(result["quality_score"], 0.8)
    
    def test_quality_evaluation_methods(self):
        """测试质量评估方法"""
        agent = SemanticExtractionAgent()
        
        # 测试关键词质量评估
        keywords_content = "关键词列表：\n1. 人工智能 - 名词 - 核心技术\n2. 深度学习 - 名词 - 重要方法"
        quality = agent._evaluate_keywords_quality(keywords_content)
        self.assertGreater(quality, 0.8)
        
        # 测试主题质量评估
        topics_content = "主题列表：\n1. 人工智能发展 - 技术发展趋势\n2. 深度学习应用 - 实际应用场景"
        quality = agent._evaluate_topics_quality(topics_content)
        self.assertGreater(quality, 0.8)
        
        # 测试实体质量评估
        entities_content = "实体分类：\n- 人名：张三、李四\n- 地名：北京、上海\n- 组织：OpenAI、微软"
        quality = agent._evaluate_entities_quality(entities_content)
        self.assertGreater(quality, 0.8)
        
        # 测试情感质量评估
        sentiment_content = "情感分析结果：\n- 整体倾向：正面\n- 情感强度：中等\n- 主要情感：积极"
        quality = agent._evaluate_sentiment_quality(sentiment_content)
        self.assertGreater(quality, 0.8)
        
        # 测试通用质量评估
        short_content = "简短内容"
        quality = agent._evaluate_general_quality(short_content)
        self.assertLess(quality, 0.5)
        
        long_content = "这是一个很长的内容，包含了大量的信息和细节。" * 10
        quality = agent._evaluate_general_quality(long_content)
        self.assertGreater(quality, 0.7)
    
    @patch('lightce.tools.semantic_extraction.UniversalAgent')
    def test_batch_extraction(self, mock_agent_class):
        """测试批量提取"""
        # 模拟UniversalAgent
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        mock_result = SemanticExtractionResult(
            success=True,
            extraction_level="basic",
            extraction_types=["keywords"],
            results={"keywords": {"content": "test"}},
            quality_score=0.8,
            processing_time=1.0,
            error_message=None
        )
        
        mock_agent.extract_semantic.return_value = mock_result
        
        agent = SemanticExtractionAgent()
        texts = ["文本1", "文本2", "文本3"]
        results = agent.batch_extract(texts)
        
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertTrue(result.success)
            self.assertEqual(result.quality_score, 0.8)
    
    @patch('lightce.tools.semantic_extraction.UniversalAgent')
    def test_statistics(self, mock_agent_class):
        """测试统计信息"""
        # 模拟UniversalAgent
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        mock_result = SemanticExtractionResult(
            success=True,
            extraction_level="basic",
            extraction_types=["keywords"],
            results={"keywords": {"content": "test"}},
            quality_score=0.8,
            processing_time=1.0,
            error_message=None
        )
        
        mock_agent.extract_semantic.return_value = mock_result
        
        agent = SemanticExtractionAgent()
        
        # 执行多次提取
        for _ in range(3):
            agent.extract_semantic(self.test_text)
        
        stats = agent.get_statistics()
        
        self.assertEqual(stats["total_extractions"], 3)
        self.assertEqual(stats["successful_extractions"], 3)
        self.assertEqual(stats["success_rate"], 1.0)
        self.assertEqual(stats["average_quality"], 0.8)
        self.assertIn("basic", stats["level_statistics"])
    
    def test_semantic_extraction_tool(self):
        """测试LangChain工具包装器"""
        # 创建模拟代理
        mock_agent = MagicMock()
        mock_result = SemanticExtractionResult(
            success=True,
            extraction_level="basic",
            extraction_types=["keywords"],
            results={"keywords": {"content": "test"}},
            quality_score=0.8,
            processing_time=1.0,
            error_message=None
        )
        mock_agent.extract_semantic.return_value = mock_result
        
        # 创建工具
        tool = SemanticExtractionTool(mock_agent)
        
        self.assertEqual(tool.name, "semantic_extraction")
        self.assertIn("语义提取", tool.description)
        
        # 测试工具执行
        result = tool._run(self.test_text, "basic", ["keywords"])
        
        self.assertTrue(result["success"])
        self.assertEqual(result["extraction_level"], "basic")
        self.assertEqual(result["quality_score"], 0.8)
    
    def test_error_handling(self):
        """测试错误处理"""
        agent = SemanticExtractionAgent()
        
        # 测试空文本
        result = agent.extract_semantic("")
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error_message)
        
        # 测试无效提取类型
        with self.assertRaises(ValueError):
            agent.extract_semantic(self.test_text, ["invalid_type"])
    
    def test_configuration_validation(self):
        """测试配置验证"""
        # 测试有效的质量阈值
        config = SemanticExtractionConfig(quality_threshold=0.5)
        self.assertEqual(config.quality_threshold, 0.5)
        
        # 测试无效的质量阈值
        with self.assertRaises(ValueError):
            SemanticExtractionConfig(quality_threshold=1.5)
        
        with self.assertRaises(ValueError):
            SemanticExtractionConfig(quality_threshold=-0.1)

def run_quick_test():
    """运行快速测试"""
    print("运行语义提取工具快速测试...")
    
    # 创建测试实例
    test = TestSemanticExtractionTool()
    test.setUp()
    
    # 运行关键测试
    test_cases = [
        test.test_semantic_extraction_config,
        test.test_semantic_extraction_result,
        test.test_create_semantic_extraction_agent,
        test.test_quality_evaluation_methods,
        test.test_semantic_extraction_tool,
        test.test_error_handling
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