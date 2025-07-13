"""
文本压缩工具
提供文本长度获取和智能压缩功能
"""

from typing import Dict, Any
from langchain_core.tools import tool
import re

@tool
def get_text_length(text: str) -> str:
    """
    获取文本的长度信息
    
    Args:
        text: 要分析的文本内容
        
    Returns:
        包含字符数、词数、行数等统计信息的字符串
    """
    if not text:
        return "文本为空"
    
    # 计算各种长度指标
    char_count = len(text)
    word_count = len(text.split())
    line_count = len(text.splitlines())
    
    # 计算中文字符数（简单统计）
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    
    # 计算英文单词数
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    
    result = f"""文本长度统计:
- 总字符数: {char_count}
- 中文字符数: {chinese_chars}
- 英文单词数: {english_words}
- 总词数: {word_count}
- 行数: {line_count}"""
    
    return result

@tool
def compress_text(text: str, compression_ratio: float) -> str:
    """
    根据压缩倍数压缩文本内容
    
    Args:
        text: 要压缩的文本内容
        compression_ratio: 压缩倍数（如2.0表示压缩到原来的1/2，3.0表示压缩到原来的1/3）
        
    Returns:
        压缩后的文本内容
    """
    if not text:
        return "文本为空，无法压缩"
    try:
        compression_ratio = float(compression_ratio)
    except Exception:
        return f"压缩倍数参数无效: {compression_ratio}"
    if compression_ratio <= 0:
        return "压缩倍数必须大于0"
    
    # 计算目标长度
    original_length = len(text)
    target_length = int(original_length / compression_ratio)
    
    if target_length <= 0:
        return "压缩倍数过大，无法生成有效文本"
    
    # 如果目标长度大于等于原长度，返回原文本
    if target_length >= original_length:
        return f"压缩倍数 {compression_ratio} 过小，返回原文本:\n\n{text}"
    
    # 智能压缩策略
    compressed_text = _smart_compress(text, target_length)
    
    result = f"""压缩结果:
- 原文本长度: {original_length} 字符
- 目标长度: {target_length} 字符
- 压缩倍数: {compression_ratio}
- 实际压缩后长度: {len(compressed_text)} 字符

压缩后的文本:
{compressed_text}"""
    
    return result

def _smart_compress(text: str, target_length: int) -> str:
    """
    智能压缩文本的内部函数
    
    Args:
        text: 原文本
        target_length: 目标长度
        
    Returns:
        压缩后的文本
    """
    # 如果目标长度太短，直接截取
    if target_length < 50:
        return text[:target_length] + "..."
    
    # 按句子分割
    sentences = re.split(r'[。！？.!?]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return text[:target_length] + "..."
    
    # 计算每个句子的重要性（简单策略：按长度加权）
    sentence_scores = []
    for i, sentence in enumerate(sentences):
        # 基础分数：句子长度
        score = len(sentence)
        # 首句加分
        if i == 0:
            score += 10
        # 包含关键词加分
        keywords = ['重要', '关键', '主要', '核心', '总结', '结论']
        for keyword in keywords:
            if keyword in sentence:
                score += 5
        sentence_scores.append((score, sentence))
    
    # 按重要性排序
    sentence_scores.sort(reverse=True)
    
    # 选择最重要的句子，直到达到目标长度
    selected_sentences = []
    current_length = 0
    
    for score, sentence in sentence_scores:
        if current_length + len(sentence) <= target_length:
            selected_sentences.append(sentence)
            current_length += len(sentence)
        else:
            # 如果当前句子太长，尝试截取
            remaining_length = target_length - current_length
            if remaining_length > 10:  # 至少保留10个字符
                selected_sentences.append(sentence[:remaining_length] + "...")
            break
    
    # 如果还没有达到目标长度，从原文本中补充
    if current_length < target_length and selected_sentences:
        remaining_length = target_length - current_length
        # 从原文本末尾补充
        remaining_text = text[-(remaining_length-3):] if remaining_length > 3 else ""
        if remaining_text:
            selected_sentences.append("..." + remaining_text)
    
    # 如果还是没有内容，直接截取
    if not selected_sentences:
        return text[:target_length] + "..."
    
    return "。".join(selected_sentences) + "。"

@tool
def analyze_and_compress(text: str, compression_ratio: float = 2.0) -> str:
    """
    分析文本并压缩的综合工具
    
    Args:
        text: 要分析的文本内容
        compression_ratio: 压缩倍数（默认2.0，即压缩到原来的1/2）
        
    Returns:
        包含分析和压缩结果的完整报告
    """
    try:
        compression_ratio_f = float(compression_ratio)
    except Exception:
        return f"压缩倍数参数无效: {compression_ratio}"
    # 先获取文本长度信息
    length_info = get_text_length.invoke({"text": text})
    # 然后进行压缩（用tool的invoke方式，参数为字符串）
    compression_result = compress_text.invoke({"text": text, "compression_ratio": str(compression_ratio_f)})
    # 组合结果
    result = f"""=== 文本分析报告 ===\n\n{length_info}\n\n=== 压缩结果 ===\n\n{compression_result}"""
    return result
