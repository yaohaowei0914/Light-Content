#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语义提取系统测试
测试修改后的语义提取系统，验证两个参数和基于长度的级别划分
"""

from lightce.prompt.semantic_extration import (
    ExtractionLevel,
    ExtractionType,
    get_level_by_text_length,
    auto_extract,
    get_extraction_workflow
)

def test_extraction_levels():
    """测试提取级别"""
    print("=== 测试提取级别 ===\n")
    
    print("1. 提取级别枚举:")
    for level in ExtractionLevel:
        print(f"   - {level.value}: {level.name}")
    
    print("\n2. 提取类型枚举:")
    for extraction_type in ExtractionType:
        print(f"   - {extraction_type.value}: {extraction_type.name}")
    
    print("\n3. 级别描述:")
    from lightce.prompt.semantic_extration import get_level_description
    for level in ExtractionLevel:
        print(f"   - {level.value}: {get_level_description(level)}")

def test_length_based_levels():
    """测试基于长度的级别划分"""
    print("\n=== 测试基于长度的级别划分 ===\n")
    
    test_cases = [
        (50, "短文本"),
        (150, "短文本"),
        (250, "中等文本"),
        (400, "中等文本"),
        (600, "长文本"),
        (800, "长文本"),
        (1200, "扩展文本"),
        (2000, "扩展文本")
    ]
    
    for length, expected in test_cases:
        level = get_level_by_text_length(length)
        print(f"文本长度 {length} 字符 -> {level.value} ({expected})")

def test_auto_extraction():
    """测试自动提取功能"""
    print("\n=== 测试自动提取功能 ===\n")
    
    test_texts = [
        "人工智能技术正在快速发展。",  # 短文本
        "人工智能技术正在快速发展，为各行各业带来了革命性的变化。深度学习模型在自然语言处理任务中取得了显著的效果提升。",  # 中等文本
        "人工智能技术正在快速发展，为各行各业带来了革命性的变化。深度学习模型在自然语言处理任务中取得了显著的效果提升。通过对比分析，我们发现Transformer架构在处理长文本时具有明显优势。这些发现为后续的研究提供了重要的理论基础和实践指导。",  # 长文本
        "人工智能技术正在快速发展，为各行各业带来了革命性的变化。深度学习模型在自然语言处理任务中取得了显著的效果提升。通过对比分析，我们发现Transformer架构在处理长文本时具有明显优势。这些发现为后续的研究提供了重要的理论基础和实践指导。随着技术的不断进步，我们预计在未来几年内，人工智能将在更多领域发挥重要作用，包括医疗诊断、自动驾驶、智能客服等。同时，我们也需要关注人工智能发展过程中可能带来的伦理和安全问题，确保技术的健康发展。"  # 扩展文本
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"测试文本 {i} (长度: {len(text)} 字符):")
        print(f"内容: {text[:50]}...")
        
        for extraction_type in ExtractionType:
            result = auto_extract(text, extraction_type)
            print(f"\n  {extraction_type.value.upper()} 提取:")
            print(f"    级别: {result['level']}")
            print(f"    目标长度: {result['target_length_range']}")
            print(f"    提示词长度: {len(result['prompt'])} 字符")
            print(f"    提示词前100字符: {result['prompt'][:100]}...")
        
        print("-" * 60)

def test_workflow():
    """测试工作流功能"""
    print("\n=== 测试工作流功能 ===\n")
    
    test_text = "这是一个测试文本，用于验证工作流功能。"
    
    for level in ExtractionLevel:
        workflow = get_extraction_workflow(level, test_text)
        print(f"{level.value.upper()} 级别工作流:")
        print(f"  描述: {workflow['level_description']}")
        print(f"  目标长度: {workflow['target_length_range']}")
        print(f"  工作流步骤:")
        for step in workflow['workflow_steps']:
            print(f"    {step}")
        print(f"  提示词数量: {len(workflow['prompts'])}")
        print()

def test_prompt_compression():
    """测试提示词压缩效果"""
    print("\n=== 测试提示词压缩效果 ===\n")
    
    test_text = "测试文本"
    
    # 测试所有级别和类型的提示词长度
    total_length = 0
    prompt_count = 0
    
    for level in ExtractionLevel:
        level_length = 0
        for extraction_type in ExtractionType:
            from lightce.prompt.semantic_extration import get_extraction_prompt
            prompt = get_extraction_prompt(level, extraction_type, text=test_text)
            length = len(prompt)
            level_length += length
            total_length += length
            prompt_count += 1
            
            print(f"{level.value} + {extraction_type.value}: {length} 字符")
        
        print(f"{level.value} 级别总计: {level_length} 字符\n")
    
    print(f"所有提示词总计: {total_length} 字符")
    print(f"提示词数量: {prompt_count}")
    print(f"平均长度: {total_length // prompt_count} 字符")

if __name__ == "__main__":
    test_extraction_levels()
    test_length_based_levels()
    test_auto_extraction()
    test_workflow()
    test_prompt_compression()
    
    print("\n=== 测试完成 ===") 