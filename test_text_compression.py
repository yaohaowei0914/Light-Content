#!/usr/bin/env python3
"""
文本压缩功能测试脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lightce.tools.mini_contents import get_text_length, compress_text, analyze_and_compress

def test_text_length():
    """测试文本长度统计功能"""
    print("=" * 60)
    print("测试文本长度统计功能")
    print("=" * 60)
    
    test_text = """人工智能（Artificial Intelligence，AI）是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。人工智能从诞生以来，理论和技术日益成熟，应用领域也不断扩大，可以设想，未来人工智能带来的科技产品，将会是人类智慧的"容器"。
    
    人工智能可以对人的意识、思维的信息过程的模拟。人工智能不是人的智能，但能像人那样思考、也可能超过人的智能。人工智能是一门极富挑战性的科学，从事人工智能研究的人员必须懂得计算机知识，心理学和哲学。人工智能是包括十分广泛的科学，它由不同的领域组成，如机器学习，计算机视觉等等，总的说来，人工智能研究的一个主要目标是使机器能够胜任一些通常需要人类智能才能完成的复杂工作。"""
    
    result = get_text_length.invoke({"text": test_text})
    print(result)

def test_text_compression():
    """测试文本压缩功能"""
    print("\n" + "=" * 60)
    print("测试文本压缩功能")
    print("=" * 60)
    
    test_text = """人工智能是计算机科学的一个重要分支，它致力于研究和开发能够模拟人类智能的计算机系统。人工智能的核心目标是让机器能够执行通常需要人类智能才能完成的任务，如学习、推理、感知、语言理解和问题解决等。

    人工智能的主要技术包括机器学习、深度学习、自然语言处理、计算机视觉、专家系统等。机器学习是人工智能的一个重要子领域，它使计算机能够在没有明确编程的情况下学习和改进。深度学习是机器学习的一个分支，使用多层神经网络来模拟人脑的工作方式。

    人工智能在各个领域都有广泛的应用，包括医疗诊断、自动驾驶、智能助手、金融分析、游戏开发等。随着技术的不断发展，人工智能正在改变我们的生活方式和工作方式，为人类社会带来巨大的潜力和机遇。

    然而，人工智能的发展也带来了一些挑战和担忧，如就业影响、隐私保护、算法偏见、安全风险等。因此，在推动人工智能发展的同时，我们也需要关注其伦理和社会影响，确保人工智能技术能够造福人类。"""
    
    print("原文本:")
    print(test_text)
    print("\n" + "-" * 40)
    
    # 测试不同压缩倍数
    compression_ratios = [2.0, 3.0, 4.0]
    
    for ratio in compression_ratios:
        print(f"\n压缩倍数: {ratio}")
        result = compress_text.invoke({"text": test_text, "compression_ratio": str(ratio)})
        print(result)
        print("-" * 40)

def test_analyze_and_compress():
    """测试综合分析功能"""
    print("\n" + "=" * 60)
    print("测试综合分析功能")
    print("=" * 60)
    
    test_text = """Python是一种高级编程语言，以其简洁的语法和强大的功能而闻名。它被广泛应用于数据分析、机器学习、网络开发、自动化脚本等领域。Python的设计哲学强调代码的可读性和简洁性，这使得它成为初学者和专业开发者的理想选择。

    Python拥有丰富的标准库和第三方包生态系统，如NumPy、Pandas、Matplotlib用于数据科学，Django、Flask用于Web开发，TensorFlow、PyTorch用于机器学习等。这些工具使得Python在各个领域都能发挥重要作用。

    Python的语法简单明了，使用缩进来表示代码块，这使得代码结构清晰易读。同时，Python支持多种编程范式，包括面向对象编程、函数式编程和过程式编程，为开发者提供了灵活的编程方式。"""
    
    result = analyze_and_compress.invoke({"text": test_text, "compression_ratio": str(2.5)})
    print(result)

def main():
    """主测试函数"""
    print("文本压缩工具功能测试")
    print("这个测试将验证文本长度统计、压缩和综合分析功能")
    
    # 测试文本长度统计
    test_text_length()
    
    # 测试文本压缩
    test_text_compression()
    
    # 测试综合分析
    test_analyze_and_compress()
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)
    print("\n现在您可以在agent中使用这些文本压缩工具了!")
    print("示例用法:")
    print("- 获取文本长度: '请分析这段文本的长度'")
    print("- 压缩文本: '请将这段文本压缩到原来的1/3'")
    print("- 综合分析: '请分析并压缩这段文本'")

if __name__ == "__main__":
    main() 