#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试压缩类型更新
验证压缩类型是否已正确更新为文本、代码、公式、表格、链接5种类型
"""

from lightce.prompt.mini_contents import CompressionType, get_compression_type_from_text
from lightce.tools.policy_select import CompressionStrategy

def test_compression_types():
    """测试压缩类型枚举"""
    print("=== 测试压缩类型枚举 ===")
    
    # 测试mini_contents.py中的压缩类型
    print("\n1. mini_contents.py中的压缩类型:")
    for compression_type in CompressionType:
        print(f"   - {compression_type.name}: {compression_type.value}")
    
    # 测试policy_select.py中的压缩策略
    print("\n2. policy_select.py中的压缩策略:")
    for strategy in CompressionStrategy:
        print(f"   - {strategy.name}: {strategy.value}")
    
    # 测试自动类型识别
    print("\n3. 测试自动类型识别:")
    test_texts = [
        "这是一段普通的文本内容，包含一些基本的信息。",
        "def calculate_sum(a, b):\n    return a + b",
        "E = mc² + ∫f(x)dx",
        "|姓名|年龄|职业|\n|张三|25|工程师|",
        "https://www.example.com/api/v1/users?page=1&limit=10"
    ]
    
    for i, text in enumerate(test_texts, 1):
        detected_type = get_compression_type_from_text(text)
        print(f"   测试{i}: {detected_type.value}")
        print(f"   内容: {text[:50]}...")
        print()

def test_compression_prompts():
    """测试压缩提示词"""
    print("=== 测试压缩提示词 ===")
    
    from lightce.prompt.mini_contents import get_compression_prompt, CompressionStage
    
    # 测试每种类型的预处理提示词
    for compression_type in CompressionType:
        print(f"\n{compression_type.value}类型的预处理提示词:")
        prompt = get_compression_prompt(
            CompressionStage.PREPROCESS, 
            compression_type, 
            text="测试内容"
        )
        print(f"长度: {len(prompt)} 字符")
        print(f"前100字符: {prompt[:100]}...")

if __name__ == "__main__":
    test_compression_types()
    test_compression_prompts()
    print("\n=== 测试完成 ===") 