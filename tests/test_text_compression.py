#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本压缩提示词测试文件
测试四个阶段的文本压缩提示词系统
"""

import unittest
from lightce.prompt.mini_contents import (
    CompressionStage, CompressionType, get_compression_prompt, 
    get_all_compression_prompts, get_compression_type_from_text,
    create_compression_workflow, calculate_compression_ratio,
    calculate_information_retention
)

class TestTextCompression(unittest.TestCase):
    """测试文本压缩提示词系统"""
    
    def test_compression_stages(self):
        """测试压缩阶段枚举"""
        self.assertEqual(CompressionStage.PREPROCESS.value, "preprocess")
        self.assertEqual(CompressionStage.COMPRESS.value, "compress")
        self.assertEqual(CompressionStage.OPTIMIZE.value, "optimize")
        self.assertEqual(CompressionStage.POSTPROCESS.value, "postprocess")
    
    def test_compression_types(self):
        """测试压缩类型枚举"""
        self.assertEqual(CompressionType.GENERAL.value, "general")
        self.assertEqual(CompressionType.TECHNICAL.value, "technical")
        self.assertEqual(CompressionType.CREATIVE.value, "creative")
        self.assertEqual(CompressionType.ACADEMIC.value, "academic")
        self.assertEqual(CompressionType.NEWS.value, "news")
        self.assertEqual(CompressionType.CONVERSATION.value, "conversation")
    
    def test_get_compression_type_from_text(self):
        """测试文本类型自动识别"""
        # 技术文档
        technical_text = "Python是一种编程语言，具有简洁的语法"
        self.assertEqual(get_compression_type_from_text(technical_text), CompressionType.TECHNICAL)
        
        # 学术文本
        academic_text = "本研究探讨了人工智能的应用"
        self.assertEqual(get_compression_type_from_text(academic_text), CompressionType.ACADEMIC)
        
        # 新闻文本
        news_text = "据新华社报道，今日发生重要事件"
        self.assertEqual(get_compression_type_from_text(news_text), CompressionType.NEWS)
        
        # 创意文本
        creative_text = "春天的午后，阳光透过树叶洒在青石板上"
        self.assertEqual(get_compression_type_from_text(creative_text), CompressionType.CREATIVE)
        
        # 对话文本
        conversation_text = "你好，我想了解一下这个技术"
        self.assertEqual(get_compression_type_from_text(conversation_text), CompressionType.CONVERSATION)
        
        # 通用文本
        general_text = "这是一个普通的文本内容"
        self.assertEqual(get_compression_type_from_text(general_text), CompressionType.GENERAL)
    
    def test_get_compression_prompt(self):
        """测试获取压缩提示词"""
        text = "这是一个测试文本"
        
        # 测试预处理阶段
        preprocess_prompt = get_compression_prompt(
            CompressionStage.PREPROCESS,
            CompressionType.GENERAL,
            text=text
        )
        self.assertIsInstance(preprocess_prompt, str)
        self.assertIn("预处理", preprocess_prompt)
        self.assertIn(text, preprocess_prompt)
        
        # 测试压缩阶段
        compress_prompt = get_compression_prompt(
            CompressionStage.COMPRESS,
            CompressionType.TECHNICAL,
            text=text,
            preprocess_result="预处理结果",
            compression_ratio=50.0
        )
        self.assertIsInstance(compress_prompt, str)
        self.assertIn("压缩", compress_prompt)
        self.assertIn("50.0", compress_prompt)
    
    def test_get_all_compression_prompts(self):
        """测试获取所有阶段提示词"""
        text = "测试文本"
        all_prompts = get_all_compression_prompts(
            CompressionType.ACADEMIC,
            text=text,
            compression_ratio=60.0
        )
        
        self.assertIn("preprocess", all_prompts)
        self.assertIn("compress", all_prompts)
        self.assertIn("optimize", all_prompts)
        self.assertIn("postprocess", all_prompts)
        
        for stage, prompt in all_prompts.items():
            self.assertIsInstance(prompt, str)
            self.assertGreater(len(prompt), 0)
    
    def test_calculate_compression_ratio(self):
        """测试压缩比例计算"""
        # 正常情况
        ratio = calculate_compression_ratio(100, 50)
        self.assertEqual(ratio, 50.0)
        
        # 无压缩
        ratio = calculate_compression_ratio(100, 100)
        self.assertEqual(ratio, 0.0)
        
        # 边界情况
        ratio = calculate_compression_ratio(0, 0)
        self.assertEqual(ratio, 0.0)
        
        # 压缩比例超过100%
        ratio = calculate_compression_ratio(100, 0)
        self.assertEqual(ratio, 100.0)
    
    def test_calculate_information_retention(self):
        """测试信息保留率计算"""
        original = "这是一个测试文本，包含一些重要信息"
        compressed = "这是测试文本，包含重要信息"
        
        retention = calculate_information_retention(original, compressed)
        self.assertIsInstance(retention, float)
        self.assertGreaterEqual(retention, 0.0)
        self.assertLessEqual(retention, 100.0)
        
        # 完全相同的文本
        retention = calculate_information_retention(original, original)
        self.assertGreater(retention, 0.0)
        
        # 空文本
        retention = calculate_information_retention("", "")
        self.assertEqual(retention, 100.0)
    
    def test_create_compression_workflow(self):
        """测试创建压缩工作流"""
        text = "这是一个用于测试的文本内容，包含一些技术术语如Python和算法"
        workflow = create_compression_workflow(text, target_ratio=40.0)
        
        self.assertIn("compression_type", workflow)
        self.assertIn("target_ratio", workflow)
        self.assertIn("original_length", workflow)
        self.assertIn("prompts", workflow)
        self.assertIn("workflow", workflow)
        
        self.assertEqual(workflow["target_ratio"], 40.0)
        self.assertEqual(workflow["original_length"], len(text))
        self.assertEqual(workflow["compression_type"], "technical")  # 应该识别为技术类型
        
        # 检查工作流阶段
        workflow_stages = workflow["workflow"]
        self.assertIn("stage_1", workflow_stages)
        self.assertIn("stage_2", workflow_stages)
        self.assertIn("stage_3", workflow_stages)
        self.assertIn("stage_4", workflow_stages)
        
        # 检查提示词
        prompts = workflow["prompts"]
        self.assertIn("preprocess", prompts)
        self.assertIn("compress", prompts)
        self.assertIn("optimize", prompts)
        self.assertIn("postprocess", prompts)

def run_basic_functionality_test():
    """运行基本功能测试"""
    print("运行文本压缩提示词基本功能测试...")
    
    # 测试枚举
    print("测试压缩阶段:")
    for stage in CompressionStage:
        print(f"- {stage.name}: {stage.value}")
    
    print("\n测试压缩类型:")
    for comp_type in CompressionType:
        print(f"- {comp_type.name}: {comp_type.value}")
    
    # 测试文本类型识别
    print("\n测试文本类型识别:")
    test_texts = [
        ("Python是一种编程语言", "technical"),
        ("本研究探讨了人工智能", "academic"),
        ("据新华社报道", "news"),
        ("春天的午后，阳光透过树叶", "creative"),
        ("你好，我想了解一下", "conversation"),
        ("这是一个普通的文本", "general")
    ]
    
    for text, expected_type in test_texts:
        detected_type = get_compression_type_from_text(text)
        print(f"文本: {text[:20]}... -> 识别: {detected_type.value} (期望: {expected_type})")
    
    # 测试提示词生成
    print("\n测试提示词生成:")
    text = "这是一个测试文本"
    prompt = get_compression_prompt(
        CompressionStage.PREPROCESS,
        CompressionType.GENERAL,
        text=text
    )
    print(f"预处理提示词长度: {len(prompt)} 字符")
    
    # 测试压缩比例计算
    print("\n测试压缩比例计算:")
    original_length = 100
    compressed_length = 60
    ratio = calculate_compression_ratio(original_length, compressed_length)
    print(f"原始长度: {original_length}, 压缩后: {compressed_length}, 压缩比例: {ratio}%")
    
    # 测试工作流创建
    print("\n测试工作流创建:")
    workflow = create_compression_workflow(text, target_ratio=50.0)
    print(f"工作流类型: {workflow['compression_type']}")
    print(f"目标压缩比例: {workflow['target_ratio']}%")
    print(f"工作流阶段数量: {len(workflow['workflow'])}")
    print(f"提示词数量: {len(workflow['prompts'])}")
    
    print("\n基本功能测试完成！")

if __name__ == "__main__":
    print("文本压缩提示词系统测试")
    print("=" * 30)
    
    # 运行基本功能测试
    run_basic_functionality_test()
    
    print("\n" + "=" * 30)
    print("运行单元测试...")
    
    # 运行单元测试
    unittest.main(argv=[''], exit=False, verbosity=2) 