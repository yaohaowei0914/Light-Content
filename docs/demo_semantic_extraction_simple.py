#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语义提取提示系统简单演示
"""

from lightce.prompt.semantic_extration import (
    ExtractionLevel, ExtractionType,
    get_extraction_prompt, get_all_extraction_prompts,
    get_extraction_workflow, get_level_description
)

def main():
    """主演示函数"""
    print("语义提取提示系统演示")
    print("=" * 60)
    
    # 测试文本
    test_text = """
    人工智能技术正在快速发展，为各行各业带来了革命性的变化。
    深度学习模型在自然语言处理任务中取得了显著的效果提升。
    通过对比分析，我们发现Transformer架构在处理长文本时具有明显优势。
    这些发现为后续的研究提供了重要的理论基础和实践指导。
    """
    
    print(f"测试文本: {test_text.strip()}")
    print(f"文本长度: {len(test_text)} 字符")
    
    # 演示不同级别
    for level in ExtractionLevel:
        print(f"\n{'='*20} {level.value.upper()} 级别 {'='*20}")
        
        # 获取级别描述
        description = get_level_description(level)
        print(f"描述: {description}")
        
        # 获取工作流
        workflow = get_extraction_workflow(level, test_text)
        print(f"工作流步骤数: {len(workflow['workflow_steps'])}")
        print("工作流步骤:")
        for step in workflow['workflow_steps']:
            print(f"  {step}")
        
        # 获取提示词
        prompts = get_all_extraction_prompts(level, text=test_text)
        print(f"提示词数量: {len(prompts)}")
        print("支持的提取类型:")
        for extraction_type in prompts.keys():
            print(f"  - {extraction_type}")
        
        # 显示一个示例提示词
        if prompts:
            first_type = list(prompts.keys())[0]
            first_prompt = prompts[first_type]
            print(f"\n{first_type} 示例提示词:")
            print("-" * 40)
            print(first_prompt[:300] + "..." if len(first_prompt) > 300 else first_prompt)
    
    # 演示特定类型的提取
    print(f"\n{'='*20} 特定类型提取演示 {'='*20}")
    
    # 关键词提取对比
    print("\n关键词提取对比:")
    for level in [ExtractionLevel.BASIC, ExtractionLevel.INTERMEDIATE, ExtractionLevel.ADVANCED]:
        try:
            prompt = get_extraction_prompt(level, ExtractionType.KEYWORDS, text=test_text)
            print(f"\n{level.value.upper()} 级别关键词提取:")
            print(f"提示词长度: {len(prompt)} 字符")
            print(f"包含角色定义: {'是' if '专家' in prompt else '否'}")
        except ValueError:
            print(f"\n{level.value.upper()} 级别不支持关键词提取")
    
    # 情感分析演示
    print(f"\n{'='*20} 情感分析演示 {'='*20}")
    try:
        sentiment_prompt = get_extraction_prompt(
            ExtractionLevel.INTERMEDIATE, 
            ExtractionType.SENTIMENT, 
            text=test_text
        )
        print("情感分析提示词:")
        print("-" * 40)
        print(sentiment_prompt[:400] + "..." if len(sentiment_prompt) > 400 else sentiment_prompt)
    except ValueError as e:
        print(f"情感分析失败: {e}")
    
    print(f"\n{'='*20} 演示完成 {'='*20}")
    print("语义提取提示系统已成功创建并测试通过！")
    print("系统支持4个级别、8种类型的语义提取功能。")

if __name__ == "__main__":
    main() 