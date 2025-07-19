#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语义提取系统演示
展示修改后的语义提取系统，包含两个参数和基于长度的级别划分
"""

from lightce.prompt.semantic_extration import (
    ExtractionLevel,
    ExtractionType,
    auto_extract,
    get_extraction_workflow,
    get_level_by_text_length
)

def demo_semantic_extraction():
    """演示语义提取系统"""
    print("=== 语义提取系统演示 ===\n")
    
    # 展示系统参数
    print("系统参数:")
    print("1. 提取级别 (按最终文本长度划分):")
    for level in ExtractionLevel:
        print(f"   - {level.value}: {level.name}")
    
    print("\n2. 提取类型:")
    for extraction_type in ExtractionType:
        print(f"   - {extraction_type.value}: {extraction_type.name}")
    
    print("\n" + "=" * 60)
    
    # 测试不同长度的文本
    test_texts = [
        {
            "name": "短文本示例",
            "text": "人工智能技术正在快速发展。",
            "description": "适合快速信息提取和简洁摘要"
        },
        {
            "name": "中等文本示例", 
            "text": "人工智能技术正在快速发展，为各行各业带来了革命性的变化。深度学习模型在自然语言处理任务中取得了显著的效果提升。",
            "description": "适合结构化信息提取和详细摘要"
        },
        {
            "name": "长文本示例",
            "text": "人工智能技术正在快速发展，为各行各业带来了革命性的变化。深度学习模型在自然语言处理任务中取得了显著的效果提升。通过对比分析，我们发现Transformer架构在处理长文本时具有明显优势。这些发现为后续的研究提供了重要的理论基础和实践指导。",
            "description": "适合深度信息提取和全面摘要"
        },
        {
            "name": "扩展文本示例",
            "text": "人工智能技术正在快速发展，为各行各业带来了革命性的变化。深度学习模型在自然语言处理任务中取得了显著的效果提升。通过对比分析，我们发现Transformer架构在处理长文本时具有明显优势。这些发现为后续的研究提供了重要的理论基础和实践指导。随着技术的不断进步，我们预计在未来几年内，人工智能将在更多领域发挥重要作用，包括医疗诊断、自动驾驶、智能客服等。同时，我们也需要关注人工智能发展过程中可能带来的伦理和安全问题，确保技术的健康发展。",
            "description": "适合复杂语义分析和深度摘要"
        }
    ]
    
    for test_case in test_texts:
        print(f"\n{test_case['name']}:")
        print(f"长度: {len(test_case['text'])} 字符")
        print(f"描述: {test_case['description']}")
        print(f"内容: {test_case['text'][:50]}...")
        
        # 自动确定级别
        level = get_level_by_text_length(len(test_case['text']))
        print(f"自动识别级别: {level.value}")
        
        # 展示工作流
        workflow = get_extraction_workflow(level, test_case['text'])
        print(f"目标长度范围: {workflow['target_length_range']}")
        print(f"工作流步骤:")
        for step in workflow['workflow_steps']:
            print(f"  {step}")
        
        # 展示提取结果
        print(f"\n提取结果:")
        for extraction_type in ExtractionType:
            result = auto_extract(test_case['text'], extraction_type)
            print(f"  {extraction_type.value.upper()}:")
            print(f"    级别: {result['level']}")
            print(f"    目标长度: {result['target_length_range']}")
            print(f"    提示词长度: {len(result['prompt'])} 字符")
        
        print("-" * 60)
    
    print("\n" + "=" * 60)
    
    # 展示系统特点
    print("\n系统特点:")
    print("1. 简化参数: 只保留提取级别和提取类型两个参数")
    print("2. 智能分级: 根据文本长度自动确定合适的提取级别")
    print("3. 长度导向: 提取级别按照最终提取文本的长度划分")
    print("4. 自动适配: 系统自动为不同长度的文本选择合适的处理策略")
    print("5. 压缩优化: 提示词经过压缩，减少冗余空行和换行")
    
    print("\n级别划分标准:")
    print("- SHORT (短文本): 50-200字符，快速提取，简洁摘要")
    print("- MEDIUM (中等文本): 200-500字符，结构化提取，详细摘要")
    print("- LONG (长文本): 500-1000字符，深度提取，全面摘要")
    print("- EXTENDED (扩展文本): 1000+字符，复杂分析，深度摘要")
    
    print("\n提取类型:")
    print("- KEYWORDS: 关键词提取，识别核心词汇和概念")
    print("- SUMMARY: 摘要生成，生成不同层次的文本摘要")

def demo_auto_extraction():
    """演示自动提取功能"""
    print("\n=== 自动提取功能演示 ===\n")
    
    # 测试一个中等长度的文本
    test_text = "机器学习技术在近年来取得了突破性进展，特别是在深度学习领域。神经网络模型在图像识别、自然语言处理、语音识别等任务中表现出了超越人类的能力。这些技术的应用正在改变我们的生活方式，从智能手机的语音助手到自动驾驶汽车，从医疗诊断到金融风控，机器学习无处不在。"
    
    print(f"测试文本 (长度: {len(test_text)} 字符):")
    print(f"内容: {test_text}")
    
    print(f"\n自动级别识别: {get_level_by_text_length(len(test_text)).value}")
    
    # 展示两种提取类型的结果
    for extraction_type in ExtractionType:
        print(f"\n{extraction_type.value.upper()} 自动提取:")
        result = auto_extract(test_text, extraction_type)
        
        print(f"  级别: {result['level']}")
        print(f"  描述: {result['level_description']}")
        print(f"  目标长度: {result['target_length_range']}")
        print(f"  提示词长度: {len(result['prompt'])} 字符")
        print(f"  提示词预览: {result['prompt'][:100]}...")

if __name__ == "__main__":
    demo_semantic_extraction()
    demo_auto_extraction()
    
    print("\n=== 演示完成 ===") 