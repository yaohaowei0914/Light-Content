#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
压缩Agent测试文件
测试使用UniversalAgent和mini_contents提示词重构的智能文本压缩工具
"""

import unittest
from unittest.mock import Mock, patch
import json
from typing import Dict, Any

from lightce.tools.compression import (
    CompressionAgent, CompressionAgentConfig, CompressionResult,
    create_compression_agent, compress_text_with_agent, analyze_text_compression_potential
)
from lightce.prompt.mini_contents import CompressionType, CompressionStage

class TestCompressionAgentConfig(unittest.TestCase):
    """测试压缩Agent配置"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = CompressionAgentConfig()
        
        self.assertEqual(config.model_name, "gpt-3.5-turbo")
        self.assertEqual(config.temperature, 0.3)
        self.assertEqual(config.max_tokens, 2000)
        self.assertEqual(config.provider, "openai")
        self.assertEqual(config.default_compression_ratio, 50.0)
        self.assertTrue(config.enable_auto_type_detection)
        self.assertTrue(config.enable_quality_check)
        self.assertTrue(config.enable_stage_processing)
    
    def test_custom_config(self):
        """测试自定义配置"""
        config = CompressionAgentConfig(
            model_name="gpt-4",
            temperature=0.1,
            max_tokens=4000,
            provider="openai",
            default_compression_ratio=70.0,
            enable_auto_type_detection=False,
            enable_quality_check=False,
            enable_stage_processing=False
        )
        
        self.assertEqual(config.model_name, "gpt-4")
        self.assertEqual(config.temperature, 0.1)
        self.assertEqual(config.max_tokens, 4000)
        self.assertEqual(config.default_compression_ratio, 70.0)
        self.assertFalse(config.enable_auto_type_detection)
        self.assertFalse(config.enable_quality_check)
        self.assertFalse(config.enable_stage_processing)

class TestCompressionResult(unittest.TestCase):
    """测试压缩结果模型"""
    
    def test_compression_result_creation(self):
        """测试压缩结果创建"""
        result = CompressionResult(
            success=True,
            original_text="原始文本",
            compressed_text="压缩文本",
            compression_type="general",
            compression_ratio=50.0,
            information_retention=80.0,
            quality_report={"test": "value"},
            processing_stages={"stage1": {"result": "test"}}
        )
        
        self.assertTrue(result.success)
        self.assertEqual(result.original_text, "原始文本")
        self.assertEqual(result.compressed_text, "压缩文本")
        self.assertEqual(result.compression_type, "general")
        self.assertEqual(result.compression_ratio, 50.0)
        self.assertEqual(result.information_retention, 80.0)
        self.assertEqual(result.quality_report["test"], "value")
        self.assertEqual(result.processing_stages["stage1"]["result"], "test")

class TestCompressionAgent(unittest.TestCase):
    """测试压缩Agent"""
    
    def setUp(self):
        """设置测试环境"""
        self.config = CompressionAgentConfig(
            enable_stage_processing=False,  # 简化测试
            enable_quality_check=False
        )
    
    @patch('lightce.tools.compression_agent.UniversalAgent')
    def test_agent_creation(self, mock_universal_agent):
        """测试Agent创建"""
        mock_agent_instance = Mock()
        mock_universal_agent.return_value = mock_agent_instance
        
        agent = CompressionAgent(self.config)
        
        self.assertIsNotNone(agent)
        self.assertEqual(agent.config, self.config)
        self.assertEqual(len(agent.compression_history), 0)
        mock_universal_agent.assert_called_once()
    
    @patch('lightce.tools.compression_agent.UniversalAgent')
    def test_empty_text_compression(self, mock_universal_agent):
        """测试空文本压缩"""
        mock_agent_instance = Mock()
        mock_universal_agent.return_value = mock_agent_instance
        
        agent = CompressionAgent(self.config)
        result = agent.compress_text("")
        
        self.assertFalse(result.success)
        self.assertEqual(result.original_text, "")
        self.assertEqual(result.compressed_text, "")
        self.assertEqual(result.quality_report["error"], "文本为空")
    
    @patch('lightce.tools.compression_agent.UniversalAgent')
    def test_simple_compression(self, mock_universal_agent):
        """测试简单压缩"""
        mock_agent_instance = Mock()
        mock_agent_instance.run.return_value = {
            'success': True,
            'response': '压缩后的文本'
        }
        mock_universal_agent.return_value = mock_agent_instance
        
        agent = CompressionAgent(self.config)
        result = agent.compress_text("测试文本", compression_ratio=50.0)
        
        self.assertTrue(result.success)
        self.assertEqual(result.original_text, "测试文本")
        self.assertEqual(result.compressed_text, "压缩后的文本")
        self.assertEqual(result.compression_type, "general")
        
        # 验证Agent被调用
        mock_agent_instance.run.assert_called_once()
    
    @patch('lightce.tools.compression_agent.UniversalAgent')
    def test_compression_with_error(self, mock_universal_agent):
        """测试压缩错误处理"""
        mock_agent_instance = Mock()
        mock_agent_instance.run.side_effect = Exception("测试错误")
        mock_universal_agent.return_value = mock_agent_instance
        
        agent = CompressionAgent(self.config)
        result = agent.compress_text("测试文本")
        
        self.assertFalse(result.success)
        self.assertEqual(result.original_text, "测试文本")
        self.assertEqual(result.compressed_text, "")
        self.assertEqual(result.quality_report["error"], "测试错误")
    
    @patch('lightce.tools.compression_agent.UniversalAgent')
    def test_batch_compression(self, mock_universal_agent):
        """测试批量压缩"""
        mock_agent_instance = Mock()
        mock_agent_instance.run.return_value = {
            'success': True,
            'response': '压缩后的文本'
        }
        mock_universal_agent.return_value = mock_agent_instance
        
        agent = CompressionAgent(self.config)
        texts = ["文本1", "文本2", "文本3"]
        results = agent.batch_compress(texts, compression_ratio=30.0)
        
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertTrue(result.success)
            self.assertEqual(result.compressed_text, "压缩后的文本")
        
        # 验证每个文本都被处理
        self.assertEqual(mock_agent_instance.run.call_count, 3)
    
    @patch('lightce.tools.compression_agent.UniversalAgent')
    def test_compression_stats(self, mock_universal_agent):
        """测试压缩统计"""
        mock_agent_instance = Mock()
        mock_agent_instance.run.return_value = {
            'success': True,
            'response': '压缩后的文本'
        }
        mock_universal_agent.return_value = mock_agent_instance
        
        agent = CompressionAgent(self.config)
        
        # 空历史记录
        stats = agent.get_compression_stats()
        self.assertIn("message", stats)
        
        # 添加一些压缩记录
        agent.compress_text("文本1")
        agent.compress_text("文本2")
        
        stats = agent.get_compression_stats()
        self.assertEqual(stats["total_compressions"], 2)
        self.assertEqual(stats["successful_compressions"], 2)
        self.assertEqual(stats["success_rate"], 100.0)
    
    @patch('lightce.tools.compression_agent.UniversalAgent')
    def test_clear_history(self, mock_universal_agent):
        """测试清空历史"""
        mock_agent_instance = Mock()
        mock_agent_instance.run.return_value = {
            'success': True,
            'response': '压缩后的文本'
        }
        mock_universal_agent.return_value = mock_agent_instance
        
        agent = CompressionAgent(self.config)
        agent.compress_text("测试文本")
        
        self.assertEqual(len(agent.compression_history), 1)
        
        agent.clear_history()
        self.assertEqual(len(agent.compression_history), 0)

class TestCompressionAgentFunctions(unittest.TestCase):
    """测试压缩Agent便捷函数"""
    
    def test_create_compression_agent(self):
        """测试创建压缩Agent函数"""
        agent = create_compression_agent(
            model_name="gpt-4",
            temperature=0.1,
            max_tokens=3000,
            provider="openai",
            default_compression_ratio=60.0,
            enable_auto_type_detection=False,
            enable_quality_check=False,
            enable_stage_processing=False
        )
        
        self.assertIsInstance(agent, CompressionAgent)
        self.assertEqual(agent.config.model_name, "gpt-4")
        self.assertEqual(agent.config.temperature, 0.1)
        self.assertEqual(agent.config.default_compression_ratio, 60.0)
        self.assertFalse(agent.config.enable_auto_type_detection)
    
    @patch('lightce.tools.compression_agent.create_compression_agent')
    def test_compress_text_with_agent_tool(self, mock_create_agent):
        """测试compress_text_with_agent工具"""
        mock_agent = Mock()
        mock_agent.compress_text.return_value = CompressionResult(
            success=True,
            original_text="原始文本",
            compressed_text="压缩文本",
            compression_type="general",
            compression_ratio=50.0,
            information_retention=80.0,
            quality_report={},
            processing_stages={}
        )
        mock_create_agent.return_value = mock_agent
        
        result = compress_text_with_agent.invoke({
            "text": "测试文本",
            "compression_ratio": 50.0,
            "compression_type": "auto"
        })
        result_dict = json.loads(result)
        
        self.assertTrue(result_dict["success"])
        self.assertEqual(result_dict["compressed_text"], "压缩文本")
        self.assertEqual(result_dict["compression_ratio"], 50.0)
    
    def test_analyze_text_compression_potential_tool(self):
        """测试analyze_text_compression_potential工具"""
        test_text = "这是一个包含技术词汇的测试文本，包含编程、算法、系统等技术术语。"
        
        result = analyze_text_compression_potential(test_text)
        result_dict = json.loads(result)
        
        self.assertIn("text_length", result_dict)
        self.assertIn("detected_type", result_dict)
        self.assertIn("compression_potential", result_dict)
        self.assertIn("recommended_ratio", result_dict)
        
        self.assertEqual(result_dict["detected_type"], "technical")
        self.assertGreater(result_dict["text_length"], 0)

class TestCompressionAgentIntegration(unittest.TestCase):
    """测试压缩Agent集成功能"""
    
    @patch('lightce.tools.compression_agent.UniversalAgent')
    def test_stage_processing(self, mock_universal_agent):
        """测试分阶段处理"""
        mock_agent_instance = Mock()
        mock_agent_instance.run.side_effect = [
            {'success': True, 'response': '预处理结果'},
            {'success': True, 'response': '压缩结果'},
            {'success': True, 'response': '优化结果'},
            {'success': True, 'response': '后处理结果'}
        ]
        mock_universal_agent.return_value = mock_agent_instance
        
        config = CompressionAgentConfig(
            enable_stage_processing=True,
            enable_quality_check=True
        )
        agent = CompressionAgent(config)
        
        result = agent.compress_text("测试文本", compression_ratio=50.0)
        
        self.assertTrue(result.success)
        self.assertIn("preprocess", result.processing_stages)
        self.assertIn("compress", result.processing_stages)
        self.assertIn("optimize", result.processing_stages)
        self.assertIn("postprocess", result.processing_stages)
        
        # 验证每个阶段都被调用
        self.assertEqual(mock_agent_instance.run.call_count, 4)
    
    @patch('lightce.tools.compression_agent.UniversalAgent')
    def test_auto_type_detection(self, mock_universal_agent):
        """测试自动类型检测"""
        mock_agent_instance = Mock()
        mock_agent_instance.run.return_value = {
            'success': True,
            'response': '压缩后的文本'
        }
        mock_universal_agent.return_value = mock_agent_instance
        
        config = CompressionAgentConfig(enable_auto_type_detection=True)
        agent = CompressionAgent(config)
        
        # 技术文本
        tech_result = agent.compress_text("这是一个包含编程、算法、系统的技术文档。")
        self.assertEqual(tech_result.compression_type, "technical")
        
        # 学术文本
        academic_result = agent.compress_text("本研究探讨了机器学习在自然语言处理中的应用。")
        self.assertEqual(academic_result.compression_type, "academic")
        
        # 新闻文本
        news_result = agent.compress_text("据最新报道，某公司今日宣布重要消息。")
        self.assertEqual(news_result.compression_type, "news")

def run_tests():
    """运行所有测试"""
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试类
    test_classes = [
        TestCompressionAgentConfig,
        TestCompressionResult,
        TestCompressionAgent,
        TestCompressionAgentFunctions,
        TestCompressionAgentIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    if success:
        print("\n所有测试通过！")
    else:
        print("\n部分测试失败！") 