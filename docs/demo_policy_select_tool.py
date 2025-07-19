#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
策略选择工具演示
展示如何通过分析LLM输入的prompt来选择相应的压缩策略
"""

import json
from lightce.tools.policy_select import (
    PolicySelectAgent, PolicySelectConfig,
    create_policy_select_agent, select_policy_with_agent,
    PolicySelectTool, MemoryType, CompressionStrategy
)

def demo_technical_prompt():
    """演示技术文档prompt的策略选择"""
    print("=" * 60)
    print("技术文档Prompt策略选择演示")
    print("=" * 60)
    
    test_prompt = """
    请分析以下技术文档，提取其中的关键技术要点和实现细节，并生成一个结构化的技术摘要。
    文档内容涉及机器学习算法、深度学习框架和人工智能应用。
    需要保持技术准确性，同时确保信息密度高，便于后续的技术决策和知识管理。
    请重点关注算法原理、性能指标、实现方法和应用场景。
    """
    
    # 创建策略选择代理
    agent = create_policy_select_agent()
    
    # 执行策略选择
    result = agent.select_policy(test_prompt)
    
    print(f"输入Prompt: {test_prompt.strip()}")
    print(f"成功状态: {result.success}")
    print(f"处理时间: {result.processing_time:.2f}秒")
    
    if result.success:
        print(f"\nPrompt分析:")
        print(json.dumps(result.prompt_analysis, ensure_ascii=False, indent=2))
        
        print(f"\n选择的策略:")
        for memory_type, strategy in result.selected_strategies.items():
            print(f"  {memory_type.value}: {strategy.value}")
            print(f"    理由: {result.strategy_reasons[memory_type]}")
        
        print(f"\n压缩配置:")
        print(json.dumps(result.compression_config, ensure_ascii=False, indent=2))

def demo_creative_prompt():
    """演示创意文本prompt的策略选择"""
    print("\n" + "=" * 60)
    print("创意文本Prompt策略选择演示")
    print("=" * 60)
    
    test_prompt = """
    请创作一个富有想象力的科幻故事，故事背景设定在2150年的火星殖民地。
    要求故事具有独特的世界观、引人入胜的情节和深刻的人物刻画。
    请注重情感表达和氛围营造，让读者能够沉浸在这个未来世界中。
    故事长度控制在2000字左右，需要有完整的起承转合结构。
    """
    
    # 创建策略选择代理
    agent = create_policy_select_agent()
    
    # 执行策略选择
    result = agent.select_policy(test_prompt)
    
    print(f"输入Prompt: {test_prompt.strip()}")
    print(f"成功状态: {result.success}")
    print(f"处理时间: {result.processing_time:.2f}秒")
    
    if result.success:
        print(f"\nPrompt分析:")
        print(json.dumps(result.prompt_analysis, ensure_ascii=False, indent=2))
        
        print(f"\n选择的策略:")
        for memory_type, strategy in result.selected_strategies.items():
            print(f"  {memory_type.value}: {strategy.value}")
            print(f"    理由: {result.strategy_reasons[memory_type]}")
        
        print(f"\n压缩配置:")
        print(json.dumps(result.compression_config, ensure_ascii=False, indent=2))

def demo_academic_prompt():
    """演示学术文本prompt的策略选择"""
    print("\n" + "=" * 60)
    print("学术文本Prompt策略选择演示")
    print("=" * 60)
    
    test_prompt = """
    请对以下学术论文进行深度分析和评价，重点关注研究方法、理论贡献和实证结果。
    论文主题是关于人工智能在医疗诊断中的应用研究。
    请从学术严谨性、创新性、实用性和局限性等维度进行全面评价。
    需要提供具体的改进建议和未来研究方向。
    """
    
    # 创建策略选择代理
    agent = create_policy_select_agent()
    
    # 执行策略选择
    result = agent.select_policy(test_prompt)
    
    print(f"输入Prompt: {test_prompt.strip()}")
    print(f"成功状态: {result.success}")
    print(f"处理时间: {result.processing_time:.2f}秒")
    
    if result.success:
        print(f"\nPrompt分析:")
        print(json.dumps(result.prompt_analysis, ensure_ascii=False, indent=2))
        
        print(f"\n选择的策略:")
        for memory_type, strategy in result.selected_strategies.items():
            print(f"  {memory_type.value}: {strategy.value}")
            print(f"    理由: {result.strategy_reasons[memory_type]}")
        
        print(f"\n压缩配置:")
        print(json.dumps(result.compression_config, ensure_ascii=False, indent=2))

def demo_news_prompt():
    """演示新闻文本prompt的策略选择"""
    print("\n" + "=" * 60)
    print("新闻文本Prompt策略选择演示")
    print("=" * 60)
    
    test_prompt = """
    请根据以下新闻事件撰写一篇客观、准确的新闻报道。
    事件涉及最新的科技发展动态，需要突出新闻的时效性和重要性。
    请遵循新闻写作的5W1H原则，确保信息完整、准确。
    报道要客观中立，避免主观评价，重点突出事实和影响。
    """
    
    # 创建策略选择代理
    agent = create_policy_select_agent()
    
    # 执行策略选择
    result = agent.select_policy(test_prompt)
    
    print(f"输入Prompt: {test_prompt.strip()}")
    print(f"成功状态: {result.success}")
    print(f"处理时间: {result.processing_time:.2f}秒")
    
    if result.success:
        print(f"\nPrompt分析:")
        print(json.dumps(result.prompt_analysis, ensure_ascii=False, indent=2))
        
        print(f"\n选择的策略:")
        for memory_type, strategy in result.selected_strategies.items():
            print(f"  {memory_type.value}: {strategy.value}")
            print(f"    理由: {result.strategy_reasons[memory_type]}")
        
        print(f"\n压缩配置:")
        print(json.dumps(result.compression_config, ensure_ascii=False, indent=2))

def demo_conversation_prompt():
    """演示对话文本prompt的策略选择"""
    print("\n" + "=" * 60)
    print("对话文本Prompt策略选择演示")
    print("=" * 60)
    
    test_prompt = """
    请模拟一个客户服务对话场景，帮助用户解决技术问题。
    用户遇到了软件使用方面的困难，需要耐心、专业的指导。
    请保持友好、专业的语调，提供清晰、易懂的解决方案。
    需要记录对话过程，便于后续的问题跟踪和知识积累。
    """
    
    # 创建策略选择代理
    agent = create_policy_select_agent()
    
    # 执行策略选择
    result = agent.select_policy(test_prompt)
    
    print(f"输入Prompt: {test_prompt.strip()}")
    print(f"成功状态: {result.success}")
    print(f"处理时间: {result.processing_time:.2f}秒")
    
    if result.success:
        print(f"\nPrompt分析:")
        print(json.dumps(result.prompt_analysis, ensure_ascii=False, indent=2))
        
        print(f"\n选择的策略:")
        for memory_type, strategy in result.selected_strategies.items():
            print(f"  {memory_type.value}: {strategy.value}")
            print(f"    理由: {result.strategy_reasons[memory_type]}")
        
        print(f"\n压缩配置:")
        print(json.dumps(result.compression_config, ensure_ascii=False, indent=2))

def demo_extraction_prompt():
    """演示信息提取prompt的策略选择"""
    print("\n" + "=" * 60)
    print("信息提取Prompt策略选择演示")
    print("=" * 60)
    
    test_prompt = """
    请从以下文本中提取关键信息，包括人名、地名、时间、数量等实体信息。
    同时识别文本中的主要主题和核心概念，分析实体间的关系。
    需要保持信息的准确性和完整性，为后续的数据分析和知识图谱构建提供基础。
    请以结构化的格式输出提取结果。
    """
    
    # 创建策略选择代理
    agent = create_policy_select_agent()
    
    # 执行策略选择
    result = agent.select_policy(test_prompt)
    
    print(f"输入Prompt: {test_prompt.strip()}")
    print(f"成功状态: {result.success}")
    print(f"处理时间: {result.processing_time:.2f}秒")
    
    if result.success:
        print(f"\nPrompt分析:")
        print(json.dumps(result.prompt_analysis, ensure_ascii=False, indent=2))
        
        print(f"\n选择的策略:")
        for memory_type, strategy in result.selected_strategies.items():
            print(f"  {memory_type.value}: {strategy.value}")
            print(f"    理由: {result.strategy_reasons[memory_type]}")
        
        print(f"\n压缩配置:")
        print(json.dumps(result.compression_config, ensure_ascii=False, indent=2))

def demo_analysis_prompt():
    """演示分析判断prompt的策略选择"""
    print("\n" + "=" * 60)
    print("分析判断Prompt策略选择演示")
    print("=" * 60)
    
    test_prompt = """
    请对以下两段文本进行语义等价性分析，判断它们是否表达相同的意思。
    需要从核心含义、关键信息、逻辑关系和表达方式等维度进行详细对比。
    请提供分析依据和判断结果，评估文本间的相似度。
    分析结果将用于文本去重和质量评估。
    """
    
    # 创建策略选择代理
    agent = create_policy_select_agent()
    
    # 执行策略选择
    result = agent.select_policy(test_prompt)
    
    print(f"输入Prompt: {test_prompt.strip()}")
    print(f"成功状态: {result.success}")
    print(f"处理时间: {result.processing_time:.2f}秒")
    
    if result.success:
        print(f"\nPrompt分析:")
        print(json.dumps(result.prompt_analysis, ensure_ascii=False, indent=2))
        
        print(f"\n选择的策略:")
        for memory_type, strategy in result.selected_strategies.items():
            print(f"  {memory_type.value}: {strategy.value}")
            print(f"    理由: {result.strategy_reasons[memory_type]}")
        
        print(f"\n压缩配置:")
        print(json.dumps(result.compression_config, ensure_ascii=False, indent=2))

def demo_batch_processing():
    """演示批量处理"""
    print("\n" + "=" * 60)
    print("批量处理演示")
    print("=" * 60)
    
    prompts = [
        "请分析这个技术文档的技术要点",
        "创作一个科幻故事",
        "评价这篇学术论文",
        "撰写新闻稿",
        "进行客户服务对话",
        "提取文本中的关键信息",
        "分析两段文本的语义等价性"
    ]
    
    # 创建代理
    agent = create_policy_select_agent()
    
    # 批量处理
    results = agent.batch_select_policy(prompts)
    
    print(f"批量处理 {len(prompts)} 个prompt")
    
    for i, result in enumerate(results):
        print(f"\n--- Prompt {i+1} ---")
        print(f"成功: {result.success}")
        print(f"处理时间: {result.processing_time:.2f}秒")
        
        if result.success:
            print("选择的策略:")
            for memory_type, strategy in result.selected_strategies.items():
                print(f"  {memory_type.value}: {strategy.value}")

def demo_langchain_tool():
    """演示LangChain工具包装器"""
    print("\n" + "=" * 60)
    print("LangChain工具包装器演示")
    print("=" * 60)
    
    test_prompt = """
    请分析这个复杂的商业报告，提取关键数据和洞察，生成结构化的分析结果。
    需要保持数据的准确性和分析的深度，为决策提供支持。
    """
    
    # 创建策略选择代理
    agent = create_policy_select_agent()
    
    # 创建LangChain工具
    tool = PolicySelectTool(agent)
    
    # 使用工具进行处理
    result = tool._run(test_prompt)
    
    print(f"输入Prompt: {test_prompt.strip()}")
    print(f"工具名称: {tool.name}")
    print(f"工具描述: {tool.description}")
    print(f"执行结果: {result['success']}")
    
    if result['success']:
        print(f"处理时间: {result['processing_time']:.2f}秒")
        print(f"选择的策略: {result['selected_strategies']}")
        print(f"策略理由: {result['strategy_reasons']}")

def demo_statistics():
    """演示统计信息"""
    print("\n" + "=" * 60)
    print("统计信息演示")
    print("=" * 60)
    
    # 创建代理
    agent = create_policy_select_agent()
    
    # 执行多次策略选择
    test_prompts = [
        "分析技术文档",
        "创作创意故事",
        "评价学术论文",
        "撰写新闻报道",
        "进行客户对话"
    ]
    
    for prompt in test_prompts:
        agent.select_policy(prompt)
    
    # 获取统计信息
    stats = agent.get_statistics()
    
    print("策略选择统计信息:")
    print(f"总选择次数: {stats['total_selections']}")
    print(f"成功选择次数: {stats['successful_selections']}")
    print(f"成功率: {stats['success_rate']:.2%}")
    print(f"平均处理时间: {stats['average_processing_time']:.2f}秒")
    
    print("\n策略使用情况:")
    for strategy_name, usage in stats['strategy_usage'].items():
        print(f"  {strategy_name}: {usage['count']}次")
        print(f"    记忆类型: {usage['memory_types']}")

def demo_advanced_configuration():
    """演示高级配置"""
    print("\n" + "=" * 60)
    print("高级配置演示")
    print("=" * 60)
    
    test_prompt = """
    请对以下复杂的多领域文档进行深度分析，涉及技术、商业、法律等多个方面。
    需要提取关键信息、识别风险点、分析影响，并生成综合报告。
    """
    
    # 创建自定义配置
    from lightce.agent.system import ModelConfig
    
    model_config = ModelConfig(
        model_name="gpt-4",
        temperature=0.1,
        max_tokens=2000,
        provider="openai"
    )
    
    config = PolicySelectConfig(
        model_config=model_config,
        enable_analysis=True,
        enable_strategy_selection=True,
        enable_compression_optimization=True,
        default_strategy=CompressionStrategy.GENERAL,
        memory_priority={
            MemoryType.SHORT_TERM: 1,
            MemoryType.LONG_TERM: 2,
            MemoryType.PARAMETER: 3,
            MemoryType.RULE: 4
        }
    )
    
    # 创建代理
    agent = PolicySelectAgent(config)
    
    # 执行策略选择
    result = agent.select_policy(test_prompt)
    
    print(f"配置信息:")
    print(f"  模型配置: {config.model_config.dict()}")
    print(f"  启用分析: {config.enable_analysis}")
    print(f"  启用策略选择: {config.enable_strategy_selection}")
    print(f"  启用压缩优化: {config.enable_compression_optimization}")
    print(f"  默认策略: {config.default_strategy.value}")
    print(f"  记忆优先级: {config.memory_priority}")
    
    print(f"\n处理结果:")
    print(f"成功: {result.success}")
    print(f"处理时间: {result.processing_time:.2f}秒")
    
    if result.success:
        print(f"选择的策略: {result.selected_strategies}")
        print(f"压缩配置: {result.compression_config}")

def demo_memory_type_comparison():
    """演示不同记忆类型的策略选择"""
    print("\n" + "=" * 60)
    print("不同记忆类型策略选择演示")
    print("=" * 60)
    
    test_prompt = """
    请分析这个复杂的项目文档，提取关键信息并生成分析报告。
    需要保持信息的准确性和完整性，为项目决策提供支持。
    """
    
    # 创建代理
    agent = create_policy_select_agent()
    
    # 执行策略选择
    result = agent.select_policy(test_prompt)
    
    print(f"输入Prompt: {test_prompt.strip()}")
    print(f"成功: {result.success}")
    
    if result.success:
        print("\n各记忆类型的策略选择:")
        for memory_type, strategy in result.selected_strategies.items():
            print(f"\n{memory_type.value}记忆:")
            print(f"  策略: {strategy.value}")
            print(f"  理由: {result.strategy_reasons[memory_type]}")
            
            # 显示对应的压缩配置
            if memory_type.value in result.compression_config.get("compression_parameters", {}):
                params = result.compression_config["compression_parameters"][memory_type.value]
                print(f"  压缩比例: {params.get('compression_ratio', 'N/A')}%")
                print(f"  保留优先级: {params.get('retention_priority', 'N/A')}")
                print(f"  格式: {params.get('format', 'N/A')}")

def main():
    """主演示函数"""
    print("策略选择工具演示")
    print("=" * 60)
    
    while True:
        print("\n请选择演示功能:")
        print("1. 技术文档Prompt策略选择")
        print("2. 创意文本Prompt策略选择")
        print("3. 学术文本Prompt策略选择")
        print("4. 新闻文本Prompt策略选择")
        print("5. 对话文本Prompt策略选择")
        print("6. 信息提取Prompt策略选择")
        print("7. 分析判断Prompt策略选择")
        print("8. 批量处理")
        print("9. LangChain工具包装器")
        print("10. 统计信息")
        print("11. 高级配置")
        print("12. 不同记忆类型策略选择")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-12): ").strip()
        
        if choice == "0":
            print("感谢使用策略选择工具演示！")
            break
        elif choice == "1":
            demo_technical_prompt()
        elif choice == "2":
            demo_creative_prompt()
        elif choice == "3":
            demo_academic_prompt()
        elif choice == "4":
            demo_news_prompt()
        elif choice == "5":
            demo_conversation_prompt()
        elif choice == "6":
            demo_extraction_prompt()
        elif choice == "7":
            demo_analysis_prompt()
        elif choice == "8":
            demo_batch_processing()
        elif choice == "9":
            demo_langchain_tool()
        elif choice == "10":
            demo_statistics()
        elif choice == "11":
            demo_advanced_configuration()
        elif choice == "12":
            demo_memory_type_comparison()
        else:
            print("无效的选择，请重新输入")

if __name__ == "__main__":
    main() 