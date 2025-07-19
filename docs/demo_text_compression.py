#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本压缩提示词演示程序
展示四个阶段的文本压缩提示词系统
"""

from lightce.prompt.mini_contents import (
    CompressionStage, CompressionType, get_compression_prompt, 
    get_all_compression_prompts, get_compression_type_from_text,
    create_compression_workflow, calculate_compression_ratio,
    calculate_information_retention
)

def demo_compression_types():
    """演示不同压缩类型"""
    print("=== 压缩类型演示 ===")
    
    # 示例文本
    sample_texts = {
        CompressionType.TECHNICAL: """
Python是一种高级编程语言，具有简洁的语法和强大的功能。它支持面向对象编程、函数式编程和过程式编程等多种编程范式。
Python的主要特点包括：动态类型、自动内存管理、丰富的标准库和第三方库生态系统。Python广泛应用于Web开发、数据科学、人工智能、机器学习、自动化测试等领域。
在Web开发中，Python可以使用Django、Flask等框架快速构建Web应用。在数据科学领域，Python的NumPy、Pandas、Matplotlib等库提供了强大的数据处理和可视化能力。
在人工智能和机器学习领域，Python的TensorFlow、PyTorch、Scikit-learn等库使得开发和部署机器学习模型变得简单高效。
        """,
        
        CompressionType.ACADEMIC: """
本研究旨在探讨人工智能技术在自然语言处理领域的应用及其对文本理解能力的影响。通过对比分析传统的基于规则的方法和现代的深度学习方法，我们发现深度学习模型在文本分类、情感分析、机器翻译等任务上表现出了显著的优势。
研究采用BERT、GPT等预训练语言模型进行实验，通过在大规模语料库上进行预训练，这些模型能够学习到丰富的语言表示。实验结果表明，预训练模型在多个基准数据集上的性能都超过了传统方法。
然而，我们也发现深度学习模型存在计算资源消耗大、可解释性差等问题。为了解决这些问题，我们提出了一种轻量级的模型压缩方法，在保持模型性能的同时显著减少了计算复杂度。
        """,
        
        CompressionType.NEWS: """
据新华社报道，2024年1月15日，在北京举行的全国科技创新大会上，科技部部长王志刚宣布了多项重要科技政策。会议指出，我国将继续加大科技投入，推动关键核心技术攻关，加快建设科技强国。
会议期间，来自全国各地的科技工作者代表就人工智能、量子计算、生物技术等前沿科技领域的发展进行了深入讨论。多位专家表示，我国在这些领域已经取得了重要突破，但仍需要进一步加强基础研究和应用转化。
科技部相关负责人透露，未来五年内，我国将投入超过2万亿元资金用于科技研发，重点支持新一代信息技术、生物技术、新能源、新材料等战略性新兴产业的发展。
        """,
        
        CompressionType.CREATIVE: """
春天的午后，阳光透过树叶的缝隙洒在青石板路上，形成斑驳的光影。微风轻拂，带来阵阵花香，让人心旷神怡。远处的山峦在薄雾中若隐若现，如同水墨画中的意境。
小溪潺潺流淌，清澈的水中倒映着蓝天白云，偶尔有几片花瓣飘落，在水面上激起小小的涟漪。鸟儿在枝头欢快地歌唱，为这美好的春日增添了几分生机。
漫步在这如诗如画的景色中，所有的烦恼都烟消云散。这里没有城市的喧嚣，没有工作的压力，只有大自然的宁静与和谐。让人不禁想起陶渊明笔下的桃花源，这里或许就是现代人心中的一片净土。
        """,
        
        CompressionType.CONVERSATION: """
小明：你好，我想了解一下Python编程，你能给我介绍一下吗？
老师：当然可以！Python是一种非常流行的编程语言，特别适合初学者。
小明：那它有什么特点呢？
老师：Python的语法很简洁，代码可读性强，而且有丰富的库支持。
小明：我想学习Python，应该从哪里开始呢？
老师：建议你先从基础语法开始，然后学习面向对象编程，最后可以做一些小项目。
小明：好的，谢谢你的建议！
老师：不客气！如果学习过程中遇到问题，随时可以问我。
        """
    }
    
    for compression_type, text in sample_texts.items():
        print(f"\n--- {compression_type.value.upper()} 类型 ---")
        print(f"文本长度: {len(text)} 字符")
        print(f"自动识别类型: {get_compression_type_from_text(text).value}")
        print(f"文本预览: {text[:100]}...")

def demo_compression_stages():
    """演示四个压缩阶段"""
    print("\n=== 压缩阶段演示 ===")
    
    # 示例技术文档
    technical_text = """
Python是一种高级编程语言，具有简洁的语法和强大的功能。它支持面向对象编程、函数式编程和过程式编程等多种编程范式。
Python的主要特点包括：动态类型、自动内存管理、丰富的标准库和第三方库生态系统。Python广泛应用于Web开发、数据科学、人工智能、机器学习、自动化测试等领域。
在Web开发中，Python可以使用Django、Flask等框架快速构建Web应用。在数据科学领域，Python的NumPy、Pandas、Matplotlib等库提供了强大的数据处理和可视化能力。
在人工智能和机器学习领域，Python的TensorFlow、PyTorch、Scikit-learn等库使得开发和部署机器学习模型变得简单高效。
    """
    
    compression_type = CompressionType.TECHNICAL
    target_ratio = 60.0
    
    print(f"原始文本长度: {len(technical_text)} 字符")
    print(f"目标压缩比例: {target_ratio}%")
    
    # 演示四个阶段的提示词
    stages = [
        (CompressionStage.PREPROCESS, "预处理阶段"),
        (CompressionStage.COMPRESS, "压缩阶段"),
        (CompressionStage.OPTIMIZE, "优化阶段"),
        (CompressionStage.POSTPROCESS, "后处理阶段")
    ]
    
    for stage, stage_name in stages:
        print(f"\n--- {stage_name} ---")
        prompt = get_compression_prompt(
            stage, 
            compression_type,
            text=technical_text,
            compression_ratio=target_ratio,
            original_length=len(technical_text),
            compressed_length=int(len(technical_text) * (1 - target_ratio / 100)),
            actual_ratio=target_ratio,
            final_length=int(len(technical_text) * (1 - target_ratio / 100)),
            final_ratio=target_ratio,
            information_retention=85.0,
            original_text=technical_text,
            optimized_text=technical_text[:int(len(technical_text) * (1 - target_ratio / 100))],
            final_text=technical_text[:int(len(technical_text) * (1 - target_ratio / 100))]
        )
        print(f"提示词长度: {len(prompt)} 字符")
        print(f"提示词预览: {prompt[:200]}...")

def demo_compression_workflow():
    """演示完整压缩工作流"""
    print("\n=== 完整压缩工作流演示 ===")
    
    # 示例学术文本
    academic_text = """
本研究旨在探讨人工智能技术在自然语言处理领域的应用及其对文本理解能力的影响。通过对比分析传统的基于规则的方法和现代的深度学习方法，我们发现深度学习模型在文本分类、情感分析、机器翻译等任务上表现出了显著的优势。
研究采用BERT、GPT等预训练语言模型进行实验，通过在大规模语料库上进行预训练，这些模型能够学习到丰富的语言表示。实验结果表明，预训练模型在多个基准数据集上的性能都超过了传统方法。
然而，我们也发现深度学习模型存在计算资源消耗大、可解释性差等问题。为了解决这些问题，我们提出了一种轻量级的模型压缩方法，在保持模型性能的同时显著减少了计算复杂度。
    """
    
    # 创建压缩工作流
    workflow = create_compression_workflow(academic_text, target_ratio=50.0)
    
    print(f"压缩类型: {workflow['compression_type']}")
    print(f"目标压缩比例: {workflow['target_ratio']}%")
    print(f"原始文本长度: {workflow['original_length']} 字符")
    
    print("\n工作流阶段:")
    for stage_key, stage_desc in workflow['workflow'].items():
        print(f"- {stage_desc}")
    
    print("\n各阶段提示词:")
    for stage_name, prompt in workflow['prompts'].items():
        print(f"\n{stage_name.upper()} 阶段:")
        print(f"提示词长度: {len(prompt)} 字符")
        print(f"提示词预览: {prompt[:150]}...")

def demo_compression_analysis():
    """演示压缩分析功能"""
    print("\n=== 压缩分析演示 ===")
    
    # 示例文本
    original_text = """
人工智能是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。
人工智能从诞生以来，理论和技术日益成熟，应用领域也不断扩大，可以设想，未来人工智能带来的科技产品，将会是人类智慧的"容器"。人工智能可以对人的意识、思维的信息过程的模拟。人工智能不是人的智能，但能像人那样思考、也可能超过人的智能。
    """
    
    # 模拟压缩后的文本
    compressed_text = """
人工智能是计算机科学分支，旨在了解智能实质并生产类似人类智能的机器。研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。
人工智能理论技术日益成熟，应用领域不断扩大，未来将成为人类智慧的"容器"。它能模拟人的意识思维过程，可能超过人的智能。
    """
    
    # 计算压缩比例
    compression_ratio = calculate_compression_ratio(len(original_text), len(compressed_text))
    
    # 估算信息保留率
    information_retention = calculate_information_retention(original_text, compressed_text)
    
    print(f"原始文本长度: {len(original_text)} 字符")
    print(f"压缩后长度: {len(compressed_text)} 字符")
    print(f"压缩比例: {compression_ratio:.1f}%")
    print(f"信息保留率: {information_retention:.1f}%")
    
    print(f"\n原始文本: {original_text}")
    print(f"\n压缩后文本: {compressed_text}")

def demo_prompt_customization():
    """演示提示词定制"""
    print("\n=== 提示词定制演示 ===")
    
    # 示例文本
    text = "这是一个示例文本，用于演示提示词定制功能。"
    
    # 获取所有压缩类型的提示词
    compression_types = [
        CompressionType.GENERAL,
        CompressionType.TECHNICAL,
        CompressionType.ACADEMIC,
        CompressionType.NEWS,
        CompressionType.CREATIVE,
        CompressionType.CONVERSATION
    ]
    
    print("不同压缩类型的预处理提示词对比:")
    for comp_type in compression_types:
        prompt = get_compression_prompt(
            CompressionStage.PREPROCESS,
            comp_type,
            text=text
        )
        print(f"\n{comp_type.value.upper()}:")
        print(f"提示词长度: {len(prompt)} 字符")
        print(f"特点: {get_prompt_characteristics(comp_type)}")

def get_prompt_characteristics(compression_type: CompressionType) -> str:
    """获取提示词特点描述"""
    characteristics = {
        CompressionType.GENERAL: "通用性强，适合各种文本类型",
        CompressionType.TECHNICAL: "注重技术准确性和专业性",
        CompressionType.ACADEMIC: "强调学术严谨性和逻辑性",
        CompressionType.NEWS: "关注新闻要素和时效性",
        CompressionType.CREATIVE: "重视创意元素和艺术性",
        CompressionType.CONVERSATION: "注重对话自然性和连贯性"
    }
    return characteristics.get(compression_type, "未知类型")

def demo_usage_examples():
    """演示使用示例"""
    print("\n=== 使用示例演示 ===")
    
    # 示例1: 获取特定阶段的提示词
    print("示例1: 获取技术文档的预处理提示词")
    technical_text = "Python是一种编程语言..."
    prompt = get_compression_prompt(
        CompressionStage.PREPROCESS,
        CompressionType.TECHNICAL,
        text=technical_text
    )
    print(f"提示词长度: {len(prompt)} 字符")
    
    # 示例2: 获取所有阶段的提示词
    print("\n示例2: 获取学术文本的所有阶段提示词")
    academic_text = "本研究旨在探讨..."
    all_prompts = get_all_compression_prompts(
        CompressionType.ACADEMIC,
        text=academic_text,
        compression_ratio=50.0
    )
    for stage, prompt in all_prompts.items():
        print(f"{stage}: {len(prompt)} 字符")
    
    # 示例3: 自动识别文本类型
    print("\n示例3: 自动识别文本类型")
    texts = [
        "Python编程语言具有简洁的语法",
        "本研究探讨了人工智能的应用",
        "据新华社报道，今日发生重要事件",
        "春天的午后，阳光透过树叶洒在青石板上",
        "你好，我想了解一下这个技术"
    ]
    
    for text in texts:
        detected_type = get_compression_type_from_text(text)
        print(f"文本: {text[:30]}... -> 类型: {detected_type.value}")

def main():
    """主函数"""
    print("文本压缩提示词系统演示")
    print("=" * 50)
    
    try:
        # 运行各种演示
        demo_compression_types()
        demo_compression_stages()
        demo_compression_workflow()
        demo_compression_analysis()
        demo_prompt_customization()
        demo_usage_examples()
        
        print("\n" + "=" * 50)
        print("文本压缩提示词系统演示完成！")
        print("\n系统特点总结:")
        print("- ✅ 四个阶段：预处理、压缩、优化、后处理")
        print("- ✅ 六种类型：通用、技术、学术、新闻、创意、对话")
        print("- ✅ 自动识别：根据文本内容自动判断压缩类型")
        print("- ✅ 灵活定制：支持不同阶段和类型的提示词定制")
        print("- ✅ 完整工作流：提供端到端的压缩解决方案")
        print("- ✅ 质量评估：包含压缩比例和信息保留率计算")
        
        print("\n使用建议:")
        print("1. 根据文本类型选择合适的压缩类型")
        print("2. 按照四个阶段顺序进行文本压缩")
        print("3. 根据实际需求调整压缩比例")
        print("4. 注意保持文本的核心信息和质量")
        print("5. 定期评估压缩效果和用户反馈")
        
    except Exception as e:
        print(f"演示过程中出现错误: {str(e)}")
        print("请检查系统配置和依赖")

if __name__ == "__main__":
    main() 