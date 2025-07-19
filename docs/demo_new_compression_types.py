#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新的压缩类型演示
展示文本、代码、公式、表格、链接5种压缩类型的功能
"""

from lightce.prompt.mini_contents import (
    CompressionType, 
    get_compression_type_from_text,
    get_compression_prompt,
    CompressionStage
)
from lightce.tools.policy_select import CompressionStrategy

def demo_compression_types():
    """演示压缩类型功能"""
    print("=== 新的压缩类型演示 ===\n")
    
    # 1. 展示压缩类型枚举
    print("1. 支持的压缩类型:")
    for compression_type in CompressionType:
        print(f"   - {compression_type.name}: {compression_type.value}")
    print()
    
    # 2. 测试不同类型的内容识别
    print("2. 内容类型自动识别:")
    test_cases = [
        {
            "name": "普通文本",
            "content": "这是一段关于人工智能技术的介绍文本，包含了机器学习、深度学习等相关概念。",
            "expected": "text"
        },
        {
            "name": "Python代码",
            "content": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
            "expected": "code"
        },
        {
            "name": "数学公式",
            "content": "E = mc² + ∫₀^∞ f(x)dx = ∑ᵢ₌₁ⁿ aᵢxᵢ",
            "expected": "formula"
        },
        {
            "name": "数据表格",
            "content": "|产品|价格|库存|\n|手机|2999|100|\n|电脑|5999|50|",
            "expected": "table"
        },
        {
            "name": "API链接",
            "content": "https://api.example.com/v1/users?page=1&limit=10&sort=name",
            "expected": "link"
        }
    ]
    
    for case in test_cases:
        detected_type = get_compression_type_from_text(case["content"])
        status = "✓" if detected_type.value == case["expected"] else "✗"
        print(f"   {status} {case['name']}: 识别为 {detected_type.value}")
    print()
    
    # 3. 展示压缩策略
    print("3. 可用的压缩策略:")
    print("   基于mini_contents.py的策略:")
    for strategy in [CompressionStrategy.TEXT, CompressionStrategy.CODE, 
                    CompressionStrategy.FORMULA, CompressionStrategy.TABLE, 
                    CompressionStrategy.LINK]:
        print(f"   - {strategy.value}")
    
    print("\n   基于semantic_extration.py的策略:")
    semantic_strategies = [CompressionStrategy.KEYWORDS, CompressionStrategy.TOPICS,
                          CompressionStrategy.CONCEPTS, CompressionStrategy.ENTITIES,
                          CompressionStrategy.RELATIONS, CompressionStrategy.SENTIMENT,
                          CompressionStrategy.INTENT, CompressionStrategy.SUMMARY]
    for strategy in semantic_strategies:
        print(f"   - {strategy.value}")
    
    print("\n   基于context_judge.py的策略:")
    context_strategies = [CompressionStrategy.SEMANTIC_EQUIVALENCE,
                         CompressionStrategy.DETAILED_ANALYSIS,
                         CompressionStrategy.SIMPLE_EQUIVALENCE]
    for strategy in context_strategies:
        print(f"   - {strategy.value}")
    
    print("\n   基于compression.py的策略:")
    compression_strategies = [CompressionStrategy.COMPRESSION_LEVEL_1,
                             CompressionStrategy.COMPRESSION_LEVEL_2,
                             CompressionStrategy.COMPRESSION_LEVEL_3,
                             CompressionStrategy.COMPRESSION_LEVEL_4,
                             CompressionStrategy.COMPRESSION_LEVEL_5]
    for strategy in compression_strategies:
        print(f"   - {strategy.value}")
    print()

def demo_compression_prompts():
    """演示压缩提示词"""
    print("=== 压缩提示词演示 ===\n")
    
    # 测试每种类型的预处理提示词
    test_content = "这是一个测试内容"
    
    for compression_type in CompressionType:
        print(f"{compression_type.value}类型的预处理提示词:")
        prompt = get_compression_prompt(
            CompressionStage.PREPROCESS,
            compression_type,
            text=test_content
        )
        print(f"长度: {len(prompt)} 字符")
        print(f"前150字符: {prompt[:150]}...")
        print()

def demo_compression_workflow():
    """演示压缩工作流"""
    print("=== 压缩工作流演示 ===\n")
    
    # 模拟一个完整的压缩工作流
    sample_text = "这是一个包含代码和公式的混合内容：\n\ndef calculate_area(r):\n    return π * r²\n\n其中 π ≈ 3.14159"
    
    print("原始内容:")
    print(sample_text)
    print()
    
    # 自动识别类型
    detected_type = get_compression_type_from_text(sample_text)
    print(f"自动识别的类型: {detected_type.value}")
    print()
    
    # 展示工作流阶段
    stages = [
        CompressionStage.PREPROCESS,
        CompressionStage.COMPRESS,
        CompressionStage.OPTIMIZE,
        CompressionStage.POSTPROCESS
    ]
    
    print("压缩工作流阶段:")
    for i, stage in enumerate(stages, 1):
        print(f"   {i}. {stage.value} - {get_stage_description(stage)}")
    print()

def get_stage_description(stage: CompressionStage) -> str:
    """获取阶段描述"""
    descriptions = {
        CompressionStage.PREPROCESS: "预处理阶段：分析内容类型和结构",
        CompressionStage.COMPRESS: "压缩阶段：执行实际压缩操作",
        CompressionStage.OPTIMIZE: "优化阶段：优化压缩结果质量",
        CompressionStage.POSTPROCESS: "后处理阶段：最终质量检查和报告"
    }
    return descriptions.get(stage, "未知阶段")

if __name__ == "__main__":
    demo_compression_types()
    demo_compression_prompts()
    demo_compression_workflow()
    print("=== 演示完成 ===") 