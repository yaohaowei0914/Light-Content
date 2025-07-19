#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语义提取工具演示
展示如何使用UniversalAgent和语义提取提示词进行语义提取
"""

import json
from lightce.tools.semantic_extraction import (
    SemanticExtractionAgent, SemanticExtractionConfig,
    create_semantic_extraction_agent, extract_semantic_with_agent,
    SemanticExtractionTool
)
from lightce.prompt.semantic_extration import ExtractionLevel, ExtractionType

def demo_basic_extraction():
    """演示基础级别语义提取"""
    print("=" * 60)
    print("基础级别语义提取演示")
    print("=" * 60)
    
    test_text = """
    人工智能技术正在快速发展，为各行各业带来了革命性的变化。
    深度学习模型在自然语言处理任务中取得了显著的效果提升。
    通过对比分析，我们发现Transformer架构在处理长文本时具有明显优势。
    这些发现为后续的研究提供了重要的理论基础和实践指导。
    """
    
    # 创建基础级别的语义提取代理
    agent = create_semantic_extraction_agent("basic")
    
    # 执行提取
    result = agent.extract_semantic(test_text)
    
    print(f"输入文本: {test_text.strip()}")
    print(f"提取级别: {result.extraction_level}")
    print(f"提取类型: {result.extraction_types}")
    print(f"成功状态: {result.success}")
    print(f"质量评分: {result.quality_score:.2f}")
    print(f"处理时间: {result.processing_time:.2f}秒")
    
    if result.success:
        print("\n提取结果:")
        for extraction_type, extraction_result in result.results.items():
            print(f"\n--- {extraction_type.upper()} ---")
            if "error" in extraction_result:
                print(f"错误: {extraction_result['error']}")
            else:
                content = extraction_result['extracted_content']
                print(f"内容: {content[:300]}{'...' if len(content) > 300 else ''}")

def demo_intermediate_extraction():
    """演示中级级别语义提取"""
    print("\n" + "=" * 60)
    print("中级级别语义提取演示")
    print("=" * 60)
    
    test_text = """
    在2023年的技术大会上，OpenAI公司发布了GPT-4模型，该模型在多个基准测试中超越了之前的版本。
    微软公司作为OpenAI的主要合作伙伴，在其Azure云平台上提供了GPT-4的API服务。
    研究人员发现，GPT-4在代码生成、数学推理和创意写作方面表现出色，但在某些特定领域的准确性仍有待提高。
    用户反馈显示，虽然模型性能优秀，但响应速度较慢，这影响了用户体验。
    """
    
    # 创建中级级别的语义提取代理
    agent = create_semantic_extraction_agent("intermediate")
    
    # 执行提取
    result = agent.extract_semantic(test_text)
    
    print(f"输入文本: {test_text.strip()}")
    print(f"提取级别: {result.extraction_level}")
    print(f"提取类型: {result.extraction_types}")
    print(f"成功状态: {result.success}")
    print(f"质量评分: {result.quality_score:.2f}")
    print(f"处理时间: {result.processing_time:.2f}秒")
    
    if result.success:
        print("\n提取结果:")
        for extraction_type, extraction_result in result.results.items():
            print(f"\n--- {extraction_type.upper()} ---")
            if "error" in extraction_result:
                print(f"错误: {extraction_result['error']}")
            else:
                content = extraction_result['extracted_content']
                print(f"内容: {content[:300]}{'...' if len(content) > 300 else ''}")

def demo_specific_extraction_types():
    """演示特定类型的语义提取"""
    print("\n" + "=" * 60)
    print("特定类型语义提取演示")
    print("=" * 60)
    
    test_text = """
    机器学习算法在医疗诊断中的应用越来越广泛。
    通过分析患者的医疗数据，AI系统能够辅助医生进行疾病诊断。
    研究表明，在某些疾病的早期检测方面，AI系统的准确率已经接近或超过了人类专家。
    然而，医疗AI的应用也面临着数据隐私、算法透明度和责任归属等伦理问题。
    """
    
    # 创建代理
    agent = create_semantic_extraction_agent("basic")
    
    # 指定特定类型进行提取
    specific_types = [ExtractionType.KEYWORDS, ExtractionType.TOPICS]
    
    result = agent.extract_semantic(test_text, specific_types)
    
    print(f"输入文本: {test_text.strip()}")
    print(f"指定提取类型: {[t.value for t in specific_types]}")
    print(f"成功状态: {result.success}")
    print(f"质量评分: {result.quality_score:.2f}")
    
    if result.success:
        print("\n提取结果:")
        for extraction_type, extraction_result in result.results.items():
            print(f"\n--- {extraction_type.upper()} ---")
            if "error" in extraction_result:
                print(f"错误: {extraction_result['error']}")
            else:
                content = extraction_result['extracted_content']
                print(f"内容: {content}")

def demo_batch_extraction():
    """演示批量语义提取"""
    print("\n" + "=" * 60)
    print("批量语义提取演示")
    print("=" * 60)
    
    texts = [
        "人工智能技术正在改变世界，为各行各业带来创新。",
        "深度学习在图像识别领域取得了突破性进展。",
        "自然语言处理技术让机器能够更好地理解人类语言。"
    ]
    
    # 创建代理
    agent = create_semantic_extraction_agent("basic")
    
    # 批量提取
    results = agent.batch_extract(texts)
    
    print(f"批量处理 {len(texts)} 个文本")
    
    for i, result in enumerate(results):
        print(f"\n--- 文本 {i+1} ---")
        print(f"成功: {result.success}")
        print(f"质量评分: {result.quality_score:.2f}")
        print(f"处理时间: {result.processing_time:.2f}秒")
        
        if result.success:
            for extraction_type, extraction_result in result.results.items():
                if "error" not in extraction_result:
                    content = extraction_result['extracted_content']
                    print(f"  {extraction_type}: {content[:100]}{'...' if len(content) > 100 else ''}")

def demo_langchain_tool():
    """演示LangChain工具包装器"""
    print("\n" + "=" * 60)
    print("LangChain工具包装器演示")
    print("=" * 60)
    
    test_text = """
    区块链技术作为一种分布式账本技术，正在改变传统的金融和商业模式。
    比特币作为第一个成功的区块链应用，展示了去中心化货币的潜力。
    以太坊平台通过智能合约功能，为去中心化应用开发提供了基础设施。
    """
    
    # 创建语义提取代理
    agent = create_semantic_extraction_agent("basic")
    
    # 创建LangChain工具
    tool = SemanticExtractionTool(agent)
    
    # 使用工具进行提取
    result = tool._run(
        text=test_text,
        extraction_level="basic",
        extraction_types=["keywords", "topics"]
    )
    
    print(f"输入文本: {test_text.strip()}")
    print(f"工具名称: {tool.name}")
    print(f"工具描述: {tool.description}")
    print(f"执行结果: {result['success']}")
    
    if result['success']:
        print(f"提取级别: {result['extraction_level']}")
        print(f"提取类型: {result['extraction_types']}")
        print(f"质量评分: {result['quality_score']:.2f}")
        print(f"处理时间: {result['processing_time']:.2f}秒")
        
        print("\n提取结果:")
        for extraction_type, extraction_result in result['results'].items():
            print(f"\n--- {extraction_type.upper()} ---")
            if "error" in extraction_result:
                print(f"错误: {extraction_result['error']}")
            else:
                content = extraction_result['extracted_content']
                print(f"内容: {content[:200]}{'...' if len(content) > 200 else ''}")

def demo_statistics():
    """演示统计信息"""
    print("\n" + "=" * 60)
    print("统计信息演示")
    print("=" * 60)
    
    # 创建代理
    agent = create_semantic_extraction_agent("basic")
    
    # 执行多次提取
    texts = [
        "人工智能技术正在快速发展。",
        "深度学习模型在自然语言处理中表现出色。",
        "机器学习算法在医疗诊断中应用广泛。"
    ]
    
    for text in texts:
        agent.extract_semantic(text)
    
    # 获取统计信息
    stats = agent.get_statistics()
    
    print("提取统计信息:")
    print(f"总提取次数: {stats['total_extractions']}")
    print(f"成功提取次数: {stats['successful_extractions']}")
    print(f"成功率: {stats['success_rate']:.2%}")
    print(f"平均质量评分: {stats['average_quality']:.2f}")
    print(f"平均处理时间: {stats['average_processing_time']:.2f}秒")
    
    print("\n级别统计:")
    for level, level_stats in stats['level_statistics'].items():
        print(f"  {level}: {level_stats['count']}次, 平均质量: {level_stats['avg_quality']:.2f}")

def demo_advanced_configuration():
    """演示高级配置"""
    print("\n" + "=" * 60)
    print("高级配置演示")
    print("=" * 60)
    
    test_text = """
    尽管当前的人工智能技术取得了显著进展，但我们仍然面临诸多挑战。
    从技术角度来看，模型的解释性和可解释性仍然是一个重要问题。
    从社会角度来看，AI技术的广泛应用可能带来就业结构的变化。
    从伦理角度来看，我们需要确保AI系统的公平性和透明度。
    """
    
    # 创建自定义配置
    from lightce.agent.system import ModelConfig
    
    model_config = ModelConfig(
        model_name="gpt-3.5-turbo",
        temperature=0.1,
        max_tokens=2000,
        provider="openai"
    )
    
    config = SemanticExtractionConfig(
        extraction_level=ExtractionLevel.ADVANCED,
        extraction_types=[ExtractionType.INTENT, ExtractionType.SUMMARY],
        model_config=model_config,
        enable_multi_stage=True,
        quality_threshold=0.8
    )
    
    # 创建代理
    agent = SemanticExtractionAgent(config)
    
    # 执行提取
    result = agent.extract_semantic(test_text)
    
    print(f"配置信息:")
    print(f"  提取级别: {config.extraction_level.value}")
    print(f"  提取类型: {[t.value for t in config.extraction_types]}")
    print(f"  模型配置: {config.model_config.dict()}")
    print(f"  质量阈值: {config.quality_threshold}")
    
    print(f"\n提取结果:")
    print(f"成功: {result.success}")
    print(f"质量评分: {result.quality_score:.2f}")
    print(f"处理时间: {result.processing_time:.2f}秒")
    
    if result.success:
        for extraction_type, extraction_result in result.results.items():
            print(f"\n--- {extraction_type.upper()} ---")
            if "error" not in extraction_result:
                content = extraction_result['extracted_content']
                print(f"内容: {content[:300]}{'...' if len(content) > 300 else ''}")

def main():
    """主演示函数"""
    print("语义提取工具演示")
    print("=" * 60)
    
    while True:
        print("\n请选择演示功能:")
        print("1. 基础级别语义提取")
        print("2. 中级级别语义提取")
        print("3. 特定类型提取")
        print("4. 批量提取")
        print("5. LangChain工具包装器")
        print("6. 统计信息")
        print("7. 高级配置")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-7): ").strip()
        
        if choice == "0":
            print("感谢使用语义提取工具演示！")
            break
        elif choice == "1":
            demo_basic_extraction()
        elif choice == "2":
            demo_intermediate_extraction()
        elif choice == "3":
            demo_specific_extraction_types()
        elif choice == "4":
            demo_batch_extraction()
        elif choice == "5":
            demo_langchain_tool()
        elif choice == "6":
            demo_statistics()
        elif choice == "7":
            demo_advanced_configuration()
        else:
            print("无效的选择，请重新输入")

if __name__ == "__main__":
    main() 