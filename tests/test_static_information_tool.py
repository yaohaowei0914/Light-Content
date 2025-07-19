#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
静态信息提取工具测试
验证静态信息提取工具的各种功能
"""

import unittest
from unittest.mock import patch, MagicMock
import time
import re

from lightce.tools.static_information import (
    StaticInformationAgent, StaticInformationConfig,
    StaticInformationResult, StaticInformationTool,
    create_static_information_agent, extract_static_information_with_agent
)
from lightce.prompt.static_information import InformationLevel, InformationType
from lightce.agent.system import ModelConfig

class TestStaticInformationTool(unittest.TestCase):
    """静态信息提取工具测试类"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.test_text = """
        张三，男，28岁，软件工程师，毕业于清华大学计算机系。
        联系方式：zhangsan@example.com，电话：138-1234-5678。
        工作地址：北京市海淀区中关村软件园，月薪15000元。
        入职时间：2020年3月15日，技术栈：Python、Java、React。
        """
    
    def test_static_information_config(self):
        """测试静态信息提取配置"""
        config = StaticInformationConfig()
        
        self.assertEqual(config.information_level, InformationLevel.BASIC)
        self.assertIsNone(config.information_types)
        self.assertIsNone(config.model_config)
        self.assertTrue(config.enable_validation)
        self.assertEqual(config.quality_threshold, 0.8)
        self.assertTrue(config.enable_format_check)
    
    def test_static_information_result(self):
        """测试静态信息提取结果"""
        result = StaticInformationResult(
            success=True,
            information_level="basic",
            information_types=["contact", "personal"],
            results={"contact": {"content": "test"}},
            quality_score=0.9,
            processing_time=1.5,
            error_message=None,
            validation_passed=True
        )
        
        self.assertTrue(result.success)
        self.assertEqual(result.information_level, "basic")
        self.assertEqual(result.information_types, ["contact", "personal"])
        self.assertEqual(result.quality_score, 0.9)
        self.assertEqual(result.processing_time, 1.5)
        self.assertIsNone(result.error_message)
        self.assertTrue(result.validation_passed)
    
    @patch('lightce.tools.static_information.UniversalAgent')
    def test_static_information_agent_initialization(self, mock_agent_class):
        """测试静态信息提取代理初始化"""
        # 模拟UniversalAgent
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        config = StaticInformationConfig()
        agent = StaticInformationAgent(config)
        
        self.assertEqual(agent.config, config)
        self.assertEqual(agent.extraction_history, [])
        mock_agent_class.assert_called_once()
    
    @patch('lightce.tools.static_information.UniversalAgent')
    def test_create_static_information_agent(self, mock_agent_class):
        """测试创建静态信息提取代理的便捷函数"""
        # 模拟UniversalAgent
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        agent = create_static_information_agent("basic", "gpt-3.5-turbo", 0.1)
        
        self.assertIsInstance(agent, StaticInformationAgent)
        self.assertEqual(agent.config.information_level, InformationLevel.BASIC)
        self.assertIsNotNone(agent.config.model_config)
        self.assertEqual(agent.config.model_config.model_name, "gpt-3.5-turbo")
        self.assertEqual(agent.config.model_config.temperature, 0.1)
    
    @patch('lightce.tools.static_information.UniversalAgent')
    def test_extract_static_information_with_agent(self, mock_agent_class):
        """测试使用代理进行静态信息提取的便捷函数"""
        # 模拟UniversalAgent和提取结果
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        mock_result = StaticInformationResult(
            success=True,
            information_level="basic",
            information_types=["contact"],
            results={"contact": {"content": "test"}},
            quality_score=0.8,
            processing_time=1.0,
            error_message=None,
            validation_passed=True
        )
        
        mock_agent.extract_information.return_value = mock_result
        
        result = extract_static_information_with_agent(self.test_text, "basic")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["information_level"], "basic")
        self.assertEqual(result["quality_score"], 0.8)
        self.assertTrue(result["validation_passed"])
    
    def test_format_methods(self):
        """测试格式化方法"""
        agent = StaticInformationAgent()
        
        # 测试联系人信息格式化
        contact_content = "邮箱：test@example.com，电话：138-1234-5678"
        formatted = agent._format_contact_info(contact_content)
        self.assertIn("邮箱地址：", formatted)
        self.assertIn("电话号码：", formatted)
        
        # 测试个人信息格式化
        personal_content = "姓名：张三，年龄：28岁"
        formatted = agent._format_personal_info(personal_content)
        self.assertIn("姓名", formatted)
        self.assertIn("年龄", formatted)
        
        # 测试数字信息格式化
        numeric_content = "数量：100，价格：50.5，数量：200"
        formatted = agent._format_numeric_info(numeric_content)
        self.assertIn("提取的数字：", formatted)
        
        # 测试时间信息格式化
        temporal_content = "日期：2020年3月15日，时间：2021年6月1日"
        formatted = agent._format_temporal_info(temporal_content)
        self.assertIn("提取的日期：", formatted)
        
        # 测试位置信息格式化
        location_content = "地址：北京市海淀区"
        formatted = agent._format_location_info(location_content)
        self.assertIn("地址信息：", formatted)
        
        # 测试组织信息格式化
        org_content = "组织名称：某公司"
        formatted = agent._format_organization_info(org_content)
        self.assertIn("组织名称", formatted)
        
        # 测试技术信息格式化
        tech_content = "技术名称：Python"
        formatted = agent._format_technical_info(tech_content)
        self.assertIn("技术名称", formatted)
        
        # 测试财务信息格式化
        financial_content = "金额：$1000，价格：¥500"
        formatted = agent._format_financial_info(financial_content)
        self.assertIn("提取的金额：", formatted)
    
    def test_quality_evaluation_methods(self):
        """测试质量评估方法"""
        agent = StaticInformationAgent()
        
        # 测试联系人质量评估
        contact_content = "邮箱：test@example.com，电话：138-1234-5678"
        quality = agent._evaluate_contact_quality(contact_content)
        self.assertGreater(quality, 0.8)
        
        # 测试个人信息质量评估
        personal_content = "姓名：张三，年龄：28岁，性别：男，职业：工程师，学历：本科"
        quality = agent._evaluate_personal_quality(personal_content)
        self.assertGreater(quality, 0.9)
        
        # 测试数字信息质量评估
        numeric_content = "数字：100，数值：200，数量：300"
        quality = agent._evaluate_numeric_quality(numeric_content)
        self.assertGreater(quality, 0.8)
        
        # 测试时间信息质量评估
        temporal_content = "日期：2020年3月15日，时间：2021年6月1日"
        quality = agent._evaluate_temporal_quality(temporal_content)
        self.assertGreater(quality, 0.8)
        
        # 测试位置信息质量评估
        location_content = "地址：北京市，位置：海淀区，城市：北京"
        quality = agent._evaluate_location_quality(location_content)
        self.assertGreater(quality, 0.5)
        
        # 测试组织信息质量评估
        org_content = "组织名称：某公司，成立时间：2020年，组织类型：科技公司，规模：100人"
        quality = agent._evaluate_organization_quality(org_content)
        self.assertGreater(quality, 0.9)
        
        # 测试技术信息质量评估
        tech_content = "技术名称：Python，版本：3.8，平台：Linux，功能：Web开发"
        quality = agent._evaluate_technical_quality(tech_content)
        self.assertGreater(quality, 0.9)
        
        # 测试财务信息质量评估
        financial_content = "金额：$1000，价格：¥500，成本：€300"
        quality = agent._evaluate_financial_quality(financial_content)
        self.assertGreater(quality, 0.8)
        
        # 测试通用质量评估
        short_content = "简短内容"
        quality = agent._evaluate_general_quality(short_content)
        self.assertLess(quality, 0.5)
        
        long_content = "这是一个很长的内容，包含了大量的信息和细节。" * 10
        quality = agent._evaluate_general_quality(long_content)
        self.assertGreater(quality, 0.7)
    
    def test_validation_methods(self):
        """测试验证方法"""
        agent = StaticInformationAgent()
        
        # 测试联系人信息验证
        contact_content = "邮箱：test@example.com，电话：138-1234-5678"
        self.assertTrue(agent._validate_contact_info(contact_content))
        
        # 测试个人信息验证
        personal_content = "姓名：张三，年龄：28岁"
        self.assertTrue(agent._validate_personal_info(personal_content))
        
        # 测试数字信息验证
        numeric_content = "数量：100，价格：50.5"
        self.assertTrue(agent._validate_numeric_info(numeric_content))
        
        # 测试时间信息验证
        temporal_content = "日期：2020年3月15日"
        self.assertTrue(agent._validate_temporal_info(temporal_content))
        
        # 测试无效内容验证
        invalid_content = ""
        self.assertFalse(agent._validate_contact_info(invalid_content))
        self.assertFalse(agent._validate_personal_info(invalid_content))
        self.assertFalse(agent._validate_numeric_info(invalid_content))
        self.assertFalse(agent._validate_temporal_info(invalid_content))
    
    @patch('lightce.tools.static_information.UniversalAgent')
    def test_batch_extraction(self, mock_agent_class):
        """测试批量提取"""
        # 模拟UniversalAgent
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        mock_result = StaticInformationResult(
            success=True,
            information_level="basic",
            information_types=["contact"],
            results={"contact": {"content": "test"}},
            quality_score=0.8,
            processing_time=1.0,
            error_message=None,
            validation_passed=True
        )
        
        mock_agent.extract_information.return_value = mock_result
        
        agent = StaticInformationAgent()
        texts = ["文本1", "文本2", "文本3"]
        results = agent.batch_extract(texts)
        
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertTrue(result.success)
            self.assertEqual(result.quality_score, 0.8)
            self.assertTrue(result.validation_passed)
    
    @patch('lightce.tools.static_information.UniversalAgent')
    def test_statistics(self, mock_agent_class):
        """测试统计信息"""
        # 模拟UniversalAgent
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        mock_result = StaticInformationResult(
            success=True,
            information_level="basic",
            information_types=["contact"],
            results={"contact": {"content": "test"}},
            quality_score=0.8,
            processing_time=1.0,
            error_message=None,
            validation_passed=True
        )
        
        mock_agent.extract_information.return_value = mock_result
        
        agent = StaticInformationAgent()
        
        # 执行多次提取
        for _ in range(3):
            agent.extract_information(self.test_text)
        
        stats = agent.get_statistics()
        
        self.assertEqual(stats["total_extractions"], 3)
        self.assertEqual(stats["successful_extractions"], 3)
        self.assertEqual(stats["success_rate"], 1.0)
        self.assertEqual(stats["average_quality"], 0.8)
        self.assertEqual(stats["validation_passed"], 3)
        self.assertEqual(stats["validation_rate"], 1.0)
        self.assertIn("basic", stats["level_statistics"])
    
    def test_static_information_tool(self):
        """测试LangChain工具包装器"""
        # 创建模拟代理
        mock_agent = MagicMock()
        mock_result = StaticInformationResult(
            success=True,
            information_level="basic",
            information_types=["contact"],
            results={"contact": {"content": "test"}},
            quality_score=0.8,
            processing_time=1.0,
            error_message=None,
            validation_passed=True
        )
        mock_agent.extract_information.return_value = mock_result
        
        # 创建工具
        tool = StaticInformationTool(mock_agent)
        
        self.assertEqual(tool.name, "static_information_extraction")
        self.assertIn("静态信息提取", tool.description)
        
        # 测试工具执行
        result = tool._run(self.test_text, "basic", ["contact"])
        
        self.assertTrue(result["success"])
        self.assertEqual(result["information_level"], "basic")
        self.assertEqual(result["quality_score"], 0.8)
        self.assertTrue(result["validation_passed"])
    
    def test_error_handling(self):
        """测试错误处理"""
        agent = StaticInformationAgent()
        
        # 测试空文本
        result = agent.extract_information("")
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error_message)
        self.assertFalse(result.validation_passed)
        
        # 测试无效提取类型
        with self.assertRaises(ValueError):
            agent.extract_information(self.test_text, ["invalid_type"])
    
    def test_configuration_validation(self):
        """测试配置验证"""
        # 测试有效的质量阈值
        config = StaticInformationConfig(quality_threshold=0.5)
        self.assertEqual(config.quality_threshold, 0.5)
        
        # 测试无效的质量阈值
        with self.assertRaises(ValueError):
            StaticInformationConfig(quality_threshold=1.5)
        
        with self.assertRaises(ValueError):
            StaticInformationConfig(quality_threshold=-0.1)
    
    def test_content_cleaning(self):
        """测试内容清理功能"""
        agent = StaticInformationAgent()
        
        # 测试内容清理和格式化
        content = "  原始内容  \n\n  包含多余空白  \n\n  需要清理  "
        cleaned = agent._clean_and_format_content(content, InformationType.CONTACT)
        
        # 检查是否移除了多余的空白
        self.assertNotIn("  ", cleaned)
        self.assertNotIn("\n\n\n", cleaned)
    
    def test_regex_patterns(self):
        """测试正则表达式模式"""
        # 测试邮箱模式
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.assertTrue(re.search(email_pattern, "test@example.com"))
        self.assertFalse(re.search(email_pattern, "invalid-email"))
        
        # 测试电话模式
        phone_pattern = r'(\+?[\d\s\-\(\)]{7,})'
        self.assertTrue(re.search(phone_pattern, "138-1234-5678"))
        self.assertTrue(re.search(phone_pattern, "+86 138 1234 5678"))
        
        # 测试数字模式
        number_pattern = r'\d+(?:\.\d+)?'
        numbers = re.findall(number_pattern, "数量：100，价格：50.5")
        self.assertEqual(len(numbers), 2)
        self.assertIn("100", numbers)
        self.assertIn("50.5", numbers)
        
        # 测试日期模式
        date_pattern = r'\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?'
        self.assertTrue(re.search(date_pattern, "2020年3月15日"))
        self.assertTrue(re.search(date_pattern, "2020-03-15"))
        
        # 测试货币模式
        currency_pattern = r'[\$¥€£]?\s*\d+(?:,\d{3})*(?:\.\d{2})?'
        self.assertTrue(re.search(currency_pattern, "$1000"))
        self.assertTrue(re.search(currency_pattern, "¥500"))
        self.assertTrue(re.search(currency_pattern, "€300.50"))

def run_quick_test():
    """运行快速测试"""
    print("运行静态信息提取工具快速测试...")
    
    # 创建测试实例
    test = TestStaticInformationTool()
    test.setUp()
    
    # 运行关键测试
    test_cases = [
        test.test_static_information_config,
        test.test_static_information_result,
        test.test_create_static_information_agent,
        test.test_format_methods,
        test.test_quality_evaluation_methods,
        test.test_validation_methods,
        test.test_static_information_tool,
        test.test_error_handling,
        test.test_content_cleaning,
        test.test_regex_patterns
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