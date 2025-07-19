#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化压缩Agent演示程序
展示使用UniversalAgent和mini_contents提示词重构的智能文本压缩工具
"""

import os
import json
from dotenv import load_dotenv
from lightce.tools.compression import (
    create_compression_agent, CompressionAgentConfig, 
    compress_text_with_agent, analyze_text_compression_potential
)
from lightce.prompt.mini_contents import CompressionType

# 加载环境变量
load_dotenv()

def demo_basic_compression():
    """演示基本压缩功能"""
    print("=== 基本压缩功能演示 ===")
    
    # 创建压缩Agent（禁用分阶段处理）
    agent = create_compression_agent(
        model_name="gpt-3.5-turbo",
        temperature=0.3,
        default_compression_ratio=50.0,
        enable_stage_processing=False,  # 禁用分阶段处理
        enable_quality_check=False      # 禁用质量检查
    )
    
    # 测试文本
    test_text = """
    人工智能（Artificial Intelligence，AI）是计算机科学的一个分支，它企图了解智能的实质，
    并生产出一种新的能以人类智能相似的方式做出反应的智能机器。该领域的研究包括机器人、
    语言识别、图像识别、自然语言处理和专家系统等。人工智能从诞生以来，理论和技术日益成熟，
    应用领域也不断扩大，可以设想，未来人工智能带来的科技产品，将会是人类智慧的"容器"。
    """
    
    print(f"原始文本长度: {len(test_text)} 字符")
    print(f"原始文本: {test_text.strip()}")
    print()
    
    # 执行压缩
    result = agent.compress_text(test_text, compression_ratio=60.0)
    
    print(f"压缩结果:")
    print(f"- 成功: {result.success}")
    print(f"- 压缩类型: {result.compression_type}")
    print(f"- 压缩比例: {result.compression_ratio:.2f}%")
    print(f"- 信息保留率: {result.information_retention:.2f}%")
    print(f"- 压缩后长度: {len(result.compressed_text)} 字符")
    print(f"- 压缩后文本: {result.compressed_text}")
    print()

def demo_auto_type_detection():
    """演示自动类型检测"""
    print("=== 自动类型检测演示 ===")
    
    agent = create_compression_agent(
        enable_auto_type_detection=True,
        enable_stage_processing=False,
        enable_quality_check=False
    )
    
    # 不同类型的测试文本
    test_cases = [
        ("学术文本", """
        本研究通过实验方法探讨了机器学习算法在自然语言处理任务中的表现。
        研究结果表明，深度学习模型在文本分类任务中取得了显著的效果提升。
        通过对比分析，我们发现Transformer架构在处理长文本时具有明显优势。
        这些发现为后续的研究提供了重要的理论基础和实践指导。
        """),
        
        ("新闻文本", """
        据最新报道，某科技公司今日宣布推出新一代人工智能产品。
        该产品采用了最新的深度学习技术，在多个领域都取得了突破性进展。
        公司CEO表示，这款产品将彻底改变人们的生活方式。
        专家认为，这标志着人工智能技术发展的重要里程碑。
        """),
        
        ("创意文本", """
        月光如水，洒在古老的石板路上，映照出斑驳的光影。
        远处的山峦在夜色中若隐若现，仿佛一幅水墨画般朦胧。
        微风轻拂，带来阵阵花香，让人心旷神怡。
        这是一个宁静而美好的夜晚，充满了诗意和想象。
        """)
    ]
    
    for text_type, text in test_cases:
        print(f"\n{text_type}:")
        print(f"原始长度: {len(text)} 字符")
        
        result = agent.compress_text(text, compression_ratio=40.0)
        
        print(f"- 检测类型: {result.compression_type}")
        print(f"- 压缩比例: {result.compression_ratio:.2f}%")
        print(f"- 压缩后: {result.compressed_text}")
    
    print()

def demo_batch_compression():
    """演示批量压缩"""
    print("=== 批量压缩演示 ===")
    
    agent = create_compression_agent(
        enable_stage_processing=False,
        enable_quality_check=False
    )
    
    # 多个文本
    texts = [
        "这是一个简单的测试文本，用于演示批量压缩功能。",
        "人工智能技术正在快速发展，为各行各业带来了革命性的变化。",
        "在编程中，代码的可读性和维护性是非常重要的考虑因素。"
    ]
    
    print(f"批量处理 {len(texts)} 个文本:")
    
    results = agent.batch_compress(texts, compression_ratio=30.0)
    
    for i, result in enumerate(results):
        print(f"\n文本 {i+1}:")
        print(f"- 原始: {result.original_text}")
        print(f"- 压缩后: {result.compressed_text}")
        print(f"- 压缩比例: {result.compression_ratio:.2f}%")
    
    print()

def demo_compression_stats():
    """演示压缩统计"""
    print("=== 压缩统计演示 ===")
    
    agent = create_compression_agent(
        enable_stage_processing=False,
        enable_quality_check=False
    )
    
    # 执行多次压缩
    test_texts = [
        "第一个测试文本，用于统计演示。",
        "第二个测试文本，包含更多内容用于压缩分析。",
        "第三个测试文本，这是一个较长的文本，包含更多的词汇和句子结构。"
    ]
    
    for text in test_texts:
        agent.compress_text(text, compression_ratio=40.0)
    
    # 获取统计信息
    stats = agent.get_compression_stats()
    
    print("压缩统计信息:")
    for key, value in stats.items():
        print(f"- {key}: {value}")
    
    print()

def demo_tool_integration():
    """演示工具集成"""
    print("=== 工具集成演示 ===")
    
    # 使用LangChain工具
    test_text = """
    这是一个用于演示工具集成的测试文本。我们将使用compress_text_with_agent工具
    来压缩这个文本，并分析其压缩潜力。这个文本包含了足够的内容来测试压缩功能。
    """
    
    print(f"原始文本: {test_text.strip()}")
    print()
    
    # 分析压缩潜力
    analysis_result = analyze_text_compression_potential.invoke({"text": test_text})
    analysis = json.loads(analysis_result)
    
    print("压缩潜力分析:")
    for key, value in analysis.items():
        print(f"- {key}: {value}")
    print()
    
    # 执行压缩
    compression_result = compress_text_with_agent.invoke({
        "text": test_text, 
        "compression_ratio": 50.0, 
        "compression_type": "auto"
    })
    result = json.loads(compression_result)
    
    print("压缩结果:")
    for key, value in result.items():
        if key != "compressed_text":
            print(f"- {key}: {value}")
    print(f"- 压缩后文本: {result.get('compressed_text', '')}")
    print()

def demo_configuration():
    """演示配置管理"""
    print("=== 配置管理演示 ===")
    
    # 创建自定义配置
    config = CompressionAgentConfig(
        model_name="gpt-3.5-turbo",
        temperature=0.1,  # 更保守的温度
        max_tokens=3000,
        default_compression_ratio=70.0,  # 更高的压缩比例
        enable_auto_type_detection=True,
        enable_quality_check=False,
        enable_stage_processing=False  # 禁用分阶段处理
    )
    
    agent = create_compression_agent()
    agent.config = config
    
    test_text = "这是一个用于演示配置管理的测试文本。我们将使用自定义配置来压缩这个文本。"
    
    print(f"使用自定义配置:")
    print(f"- 温度: {agent.config.temperature}")
    print(f"- 默认压缩比例: {agent.config.default_compression_ratio}%")
    print(f"- 分阶段处理: {agent.config.enable_stage_processing}")
    print()
    
    result = agent.compress_text(test_text)
    
    print(f"压缩结果:")
    print(f"- 压缩比例: {result.compression_ratio:.2f}%")
    print(f"- 压缩后文本: {result.compressed_text}")
    print()

def main():
    """主函数"""
    print("简化压缩Agent演示程序")
    print("=" * 50)
    
    # 检查API密钥
    if not os.getenv("OPENAI_API_KEY"):
        print("警告: 未设置OPENAI_API_KEY环境变量")
        print("某些功能可能无法正常工作")
        print()
    
    try:
        # 运行演示
        demo_basic_compression()
        demo_auto_type_detection()
        demo_batch_compression()
        demo_compression_stats()
        demo_tool_integration()
        demo_configuration()
        
        print("所有演示完成！")
        
    except Exception as e:
        print(f"演示过程中发生错误: {str(e)}")
        print("请检查API密钥设置和网络连接")

if __name__ == "__main__":
    main() 