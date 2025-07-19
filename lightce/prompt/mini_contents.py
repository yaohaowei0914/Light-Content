#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本压缩提示词系统
分为四个阶段：预处理、压缩、优化、后处理
"""

from typing import Dict, List, Any, Optional
from enum import Enum

class CompressionStage(Enum):
    """压缩阶段枚举"""
    PREPROCESS = "preprocess"    # 预处理阶段
    COMPRESS = "compress"        # 压缩阶段
    OPTIMIZE = "optimize"        # 优化阶段
    POSTPROCESS = "postprocess"  # 后处理阶段

class CompressionType(Enum):
    """压缩类型枚举"""
    TEXT = "text"                # 文本压缩
    CODE = "code"                # 代码压缩
    FORMULA = "formula"          # 公式压缩
    TABLE = "table"              # 表格压缩
    LINK = "link"                # 链接压缩

# 预处理阶段提示词
PREPROCESS_PROMPTS = {
    CompressionType.TEXT: """你是一个专业的文本预处理专家。请对以下文本进行预处理，为后续压缩做准备。

预处理任务：
1. 识别文本类型和主题
2. 分析文本结构和逻辑关系
3. 识别关键信息和冗余内容
4. 评估文本的复杂度和重要性
5. 确定压缩目标和保留重点

输入文本：
{text}

请按以下格式输出预处理结果：
- 文本类型：[类型]
- 主要主题：[主题]
- 核心信息：[列出3-5个核心信息点]
- 冗余内容：[列出可删除的冗余部分]
- 压缩建议：[建议的压缩策略]
- 保留重点：[必须保留的关键内容]""",

    CompressionType.CODE: """你是一个代码预处理专家。请对以下代码进行预处理分析。

预处理任务：
1. 识别编程语言和代码类型
2. 分析代码结构和功能模块
3. 识别核心逻辑和关键函数
4. 评估代码复杂度和重要性
5. 确定代码压缩策略

输入代码：
{text}

请按以下格式输出预处理结果：
- 编程语言：[语言类型]
- 代码类型：[功能类型]
- 核心功能：[主要功能点]
- 关键函数：[重要函数/方法]
- 冗余代码：[可删除的冗余部分]
- 压缩策略：[代码压缩建议]
- 保留重点：[必须保留的代码逻辑]""",

    CompressionType.FORMULA: """你是一个公式预处理专家。请对以下公式进行预处理分析。

预处理任务：
1. 识别公式类型和数学领域
2. 分析公式结构和变量关系
3. 识别核心变量和参数
4. 评估公式复杂度和重要性
5. 确定公式压缩策略

输入公式：
{text}

请按以下格式输出预处理结果：
- 公式类型：[数学类型]
- 数学领域：[应用领域]
- 核心变量：[主要变量]
- 关键参数：[重要参数]
- 冗余部分：[可简化的部分]
- 压缩策略：[公式压缩建议]
- 保留重点：[必须保留的数学关系]""",

    CompressionType.TABLE: """你是一个表格预处理专家。请对以下表格进行预处理分析。

预处理任务：
1. 识别表格类型和数据结构
2. 分析表格行列和数据类型
3. 识别关键数据和重要列
4. 评估表格复杂度和重要性
5. 确定表格压缩策略

输入表格：
{text}

请按以下格式输出预处理结果：
- 表格类型：[数据类型]
- 数据结构：[行列结构]
- 关键列：[重要列名]
- 核心数据：[重要数据]
- 冗余列：[可删除的列]
- 压缩策略：[表格压缩建议]
- 保留重点：[必须保留的数据]""",

    CompressionType.LINK: """你是一个链接预处理专家。请对以下链接进行预处理分析。

预处理任务：
1. 识别链接类型和用途
2. 分析链接结构和参数
3. 识别关键参数和路径
4. 评估链接复杂度和重要性
5. 确定链接压缩策略

输入链接：
{text}

请按以下格式输出预处理结果：
- 链接类型：[URL类型]
- 链接用途：[使用目的]
- 关键参数：[重要参数]
- 核心路径：[主要路径]
- 冗余参数：[可删除的参数]
- 压缩策略：[链接压缩建议]
- 保留重点：[必须保留的链接信息]"""
}

# 压缩阶段提示词
COMPRESS_PROMPTS = {
    CompressionType.TEXT: """你是一个专业的文本压缩专家。请根据预处理结果对文本进行高效压缩。

压缩要求：
1. 保持核心信息和主要观点
2. 删除冗余和重复内容
3. 简化复杂表达
4. 保持逻辑连贯性
5. 确保压缩后的文本清晰易懂

预处理结果：
{preprocess_result}

原始文本：
{text}

目标压缩比例：{compression_ratio}%

请输出压缩后的文本：""",

    CompressionType.CODE: """你是一个代码压缩专家。请根据预处理结果对代码进行专业压缩。

压缩要求：
1. 保留核心逻辑和关键函数
2. 简化代码结构，保持功能
3. 删除冗余的代码注释
4. 保持代码的可读性
5. 确保压缩后的代码仍能正常运行

预处理结果：
{preprocess_result}

原始代码：
{text}

目标压缩比例：{compression_ratio}%

请输出压缩后的代码：""",

    CompressionType.FORMULA: """你是一个公式压缩专家。请根据预处理结果对公式进行数学压缩。

压缩要求：
1. 保留核心数学关系
2. 简化公式表达，保持准确性
3. 删除冗余的数学符号
4. 保持公式的数学意义
5. 确保压缩后的公式仍具有数学价值

预处理结果：
{preprocess_result}

原始公式：
{text}

目标压缩比例：{compression_ratio}%

请输出压缩后的公式：""",

    CompressionType.TABLE: """你是一个表格压缩专家。请根据预处理结果对表格进行数据压缩。

压缩要求：
1. 保留关键数据和重要列
2. 简化表格结构，保持数据完整性
3. 删除冗余的行列
4. 保持表格的可读性
5. 确保压缩后的表格仍具有数据价值

预处理结果：
{preprocess_result}

原始表格：
{text}

目标压缩比例：{compression_ratio}%

请输出压缩后的表格：""",

    CompressionType.LINK: """你是一个链接压缩专家。请根据预处理结果对链接进行URL压缩。

压缩要求：
1. 保留关键参数和路径
2. 简化链接结构，保持功能
3. 删除冗余的URL参数
4. 保持链接的有效性
5. 确保压缩后的链接仍能正常访问

预处理结果：
{preprocess_result}

原始链接：
{text}

目标压缩比例：{compression_ratio}%

请输出压缩后的链接："""
}

# 优化阶段提示词
OPTIMIZE_PROMPTS = {
    CompressionType.TEXT: """你是一个文本优化专家。请对压缩后的文本进行质量优化。

优化任务：
1. 检查信息完整性
2. 优化语言表达
3. 确保逻辑连贯性
4. 提高可读性
5. 验证压缩效果

压缩后文本：
{compressed_text}

原始文本长度：{original_length} 字符
压缩后长度：{compressed_length} 字符
压缩比例：{actual_ratio}%

请进行以下优化：
1. 信息完整性检查：[检查是否遗漏重要信息]
2. 语言表达优化：[优化语言表达]
3. 逻辑连贯性检查：[确保逻辑清晰]
4. 可读性提升：[提高可读性]
5. 最终优化建议：[给出优化建议]

优化后的文本：""",

    CompressionType.CODE: """你是一个代码优化专家。请对压缩后的代码进行专业优化。

优化任务：
1. 检查代码功能性
2. 优化代码结构
3. 确保代码逻辑完整
4. 提高代码可读性
5. 验证代码价值

压缩后代码：
{compressed_text}

原始代码长度：{original_length} 字符
压缩后长度：{compressed_length} 字符
压缩比例：{actual_ratio}%

请进行以下优化：
1. 代码功能性检查：[检查代码功能是否完整]
2. 代码结构优化：[优化代码结构]
3. 代码逻辑检查：[确保代码逻辑完整]
4. 代码可读性提升：[提高代码可读性]
5. 代码价值验证：[验证代码价值]

优化后的代码：""",

    CompressionType.FORMULA: """你是一个公式优化专家。请对压缩后的公式进行数学优化。

优化任务：
1. 检查数学准确性
2. 优化公式表达
3. 确保数学逻辑完整
4. 提高公式可读性
5. 验证数学价值

压缩后公式：
{compressed_text}

原始公式长度：{original_length} 字符
压缩后长度：{compressed_length} 字符
压缩比例：{actual_ratio}%

请进行以下优化：
1. 数学准确性检查：[检查数学内容是否准确]
2. 公式表达优化：[优化公式表达]
3. 数学逻辑检查：[确保数学逻辑完整]
4. 公式可读性提升：[提高公式可读性]
5. 数学价值验证：[验证数学价值]

优化后的公式：""",

    CompressionType.TABLE: """你是一个表格优化专家。请对压缩后的表格进行数据优化。

优化任务：
1. 检查数据完整性
2. 优化表格结构
3. 确保数据逻辑完整
4. 提高表格可读性
5. 验证数据价值

压缩后表格：
{compressed_text}

原始表格长度：{original_length} 字符
压缩后长度：{compressed_length} 字符
压缩比例：{actual_ratio}%

请进行以下优化：
1. 数据完整性检查：[检查数据是否完整]
2. 表格结构优化：[优化表格结构]
3. 数据逻辑检查：[确保数据逻辑完整]
4. 表格可读性提升：[提高表格可读性]
5. 数据价值验证：[验证数据价值]

优化后的表格：""",

    CompressionType.LINK: """你是一个链接优化专家。请对压缩后的链接进行URL优化。

优化任务：
1. 检查链接有效性
2. 优化链接结构
3. 确保链接功能完整
4. 提高链接可读性
5. 验证链接价值

压缩后链接：
{compressed_text}

原始链接长度：{original_length} 字符
压缩后长度：{compressed_length} 字符
压缩比例：{actual_ratio}%

请进行以下优化：
1. 链接有效性检查：[检查链接是否有效]
2. 链接结构优化：[优化链接结构]
3. 链接功能检查：[确保链接功能完整]
4. 链接可读性提升：[提高链接可读性]
5. 链接价值验证：[验证链接价值]

优化后的链接："""
}

# 后处理阶段提示词
POSTPROCESS_PROMPTS = {
    CompressionType.TEXT: """你是一个文本后处理专家。请对优化后的文本进行最终处理和质量检查。

后处理任务：
1. 最终质量检查
2. 格式标准化
3. 压缩效果评估
4. 使用建议提供
5. 质量报告生成

优化后文本：
{optimized_text}

原始文本：
{original_text}

压缩统计：
- 原始长度：{original_length} 字符
- 压缩后长度：{final_length} 字符
- 压缩比例：{final_ratio}%
- 信息保留率：{information_retention}%

请进行以下后处理：
1. 最终质量检查：[全面质量检查结果]
2. 格式标准化：[标准化处理]
3. 压缩效果评估：[压缩效果评价]
4. 使用建议：[使用建议]
5. 质量报告：[质量报告摘要]

最终压缩文本：
{final_text}

质量报告：
- 信息完整性：[完整性评分]
- 语言质量：[语言质量评分]
- 逻辑连贯性：[逻辑性评分]
- 可读性：[可读性评分]
- 压缩效果：[压缩效果评分]
- 总体评价：[总体评价]""",

    CompressionType.CODE: """你是一个代码后处理专家。请对优化后的代码进行最终处理和质量检查。

后处理任务：
1. 代码功能性最终检查
2. 代码格式标准化
3. 代码压缩效果评估
4. 代码使用建议提供
5. 代码质量报告生成

优化后代码：
{optimized_text}

原始代码：
{original_text}

压缩统计：
- 原始长度：{original_length} 字符
- 压缩后长度：{final_length} 字符
- 压缩比例：{final_ratio}%
- 代码信息保留率：{information_retention}%

请进行以下后处理：
1. 代码功能性检查：[代码功能性检查结果]
2. 代码格式标准化：[代码格式标准化]
3. 代码压缩效果评估：[代码压缩效果评价]
4. 代码使用建议：[代码使用建议]
5. 代码质量报告：[代码质量报告摘要]

最终压缩代码：
{final_text}

代码质量报告：
- 代码功能性：[功能性评分]
- 代码完整性：[完整性评分]
- 代码逻辑性：[逻辑性评分]
- 代码可读性：[可读性评分]
- 代码压缩效果：[压缩效果评分]
- 代码价值：[代码价值评分]
- 总体评价：[总体评价]""",

    CompressionType.FORMULA: """你是一个公式后处理专家。请对优化后的公式进行最终处理和质量检查。

后处理任务：
1. 数学准确性最终检查
2. 公式格式标准化
3. 公式压缩效果评估
4. 公式使用建议提供
5. 公式质量报告生成

优化后公式：
{optimized_text}

原始公式：
{original_text}

压缩统计：
- 原始长度：{original_length} 字符
- 压缩后长度：{final_length} 字符
- 压缩比例：{final_ratio}%
- 公式信息保留率：{information_retention}%

请进行以下后处理：
1. 数学准确性检查：[数学准确性检查结果]
2. 公式格式标准化：[公式格式标准化]
3. 公式压缩效果评估：[公式压缩效果评价]
4. 公式使用建议：[公式使用建议]
5. 公式质量报告：[公式质量报告摘要]

最终压缩公式：
{final_text}

公式质量报告：
- 数学准确性：[数学准确性评分]
- 公式完整性：[完整性评分]
- 数学逻辑性：[逻辑性评分]
- 公式可读性：[可读性评分]
- 公式压缩效果：[压缩效果评分]
- 数学价值：[数学价值评分]
- 总体评价：[总体评价]""",

    CompressionType.TABLE: """你是一个表格后处理专家。请对优化后的表格进行最终处理和质量检查。

后处理任务：
1. 数据完整性最终检查
2. 表格格式标准化
3. 表格压缩效果评估
4. 表格使用建议提供
5. 表格质量报告生成

优化后表格：
{optimized_text}

原始表格：
{original_text}

压缩统计：
- 原始长度：{original_length} 字符
- 压缩后长度：{final_length} 字符
- 压缩比例：{final_ratio}%
- 表格信息保留率：{information_retention}%

请进行以下后处理：
1. 数据完整性检查：[数据完整性检查结果]
2. 表格格式标准化：[表格格式标准化]
3. 表格压缩效果评估：[表格压缩效果评价]
4. 表格使用建议：[表格使用建议]
5. 表格质量报告：[表格质量报告摘要]

最终压缩表格：
{final_text}

表格质量报告：
- 数据完整性：[数据完整性评分]
- 表格完整性：[完整性评分]
- 数据逻辑性：[逻辑性评分]
- 表格可读性：[可读性评分]
- 表格压缩效果：[压缩效果评分]
- 数据价值：[数据价值评分]
- 总体评价：[总体评价]""",

    CompressionType.LINK: """你是一个链接后处理专家。请对优化后的链接进行最终处理和质量检查。

后处理任务：
1. 链接有效性最终检查
2. 链接格式标准化
3. 链接压缩效果评估
4. 链接使用建议提供
5. 链接质量报告生成

优化后链接：
{optimized_text}

原始链接：
{original_text}

压缩统计：
- 原始长度：{original_length} 字符
- 压缩后长度：{final_length} 字符
- 压缩比例：{final_ratio}%
- 链接信息保留率：{information_retention}%

请进行以下后处理：
1. 链接有效性检查：[链接有效性检查结果]
2. 链接格式标准化：[链接格式标准化]
3. 链接压缩效果评估：[链接压缩效果评价]
4. 链接使用建议：[链接使用建议]
5. 链接质量报告：[链接质量报告摘要]

最终压缩链接：
{final_text}

链接质量报告：
- 链接有效性：[有效性评分]
- 链接完整性：[完整性评分]
- 链接功能性：[功能性评分]
- 链接可读性：[可读性评分]
- 链接压缩效果：[压缩效果评分]
- 链接价值：[链接价值评分]
- 总体评价：[总体评价]"""
}

def get_compression_prompt(stage: CompressionStage, compression_type: CompressionType, **kwargs) -> str:
    """
    获取指定阶段和类型的压缩提示词
    
    Args:
        stage: 压缩阶段
        compression_type: 压缩类型
        **kwargs: 其他参数
    
    Returns:
        格式化后的提示词
    """
    if stage == CompressionStage.PREPROCESS:
        prompt_template = PREPROCESS_PROMPTS.get(compression_type, PREPROCESS_PROMPTS[CompressionType.TEXT])
    elif stage == CompressionStage.COMPRESS:
        prompt_template = COMPRESS_PROMPTS.get(compression_type, COMPRESS_PROMPTS[CompressionType.TEXT])
    elif stage == CompressionStage.OPTIMIZE:
        prompt_template = OPTIMIZE_PROMPTS.get(compression_type, OPTIMIZE_PROMPTS[CompressionType.TEXT])
    elif stage == CompressionStage.POSTPROCESS:
        prompt_template = POSTPROCESS_PROMPTS.get(compression_type, POSTPROCESS_PROMPTS[CompressionType.TEXT])
    else:
        raise ValueError(f"不支持的压缩阶段: {stage}")
    
    return prompt_template.format(**kwargs)

def get_all_compression_prompts(compression_type: CompressionType, **kwargs) -> Dict[str, str]:
    """
    获取指定类型的所有阶段提示词
    
    Args:
        compression_type: 压缩类型
        **kwargs: 其他参数
    
    Returns:
        包含所有阶段提示词的字典
    """
    return {
        "preprocess": get_compression_prompt(CompressionStage.PREPROCESS, compression_type, **kwargs),
        "compress": get_compression_prompt(CompressionStage.COMPRESS, compression_type, **kwargs),
        "optimize": get_compression_prompt(CompressionStage.OPTIMIZE, compression_type, **kwargs),
        "postprocess": get_compression_prompt(CompressionStage.POSTPROCESS, compression_type, **kwargs)
    }

def get_compression_type_from_text(text: str) -> CompressionType:
    """
    根据文本内容自动判断压缩类型
    
    Args:
        text: 输入文本
    
    Returns:
        推断的压缩类型
    """
    text_lower = text.lower()
    
    # 链接特征（优先检查）
    link_keywords = ['http://', 'https://', 'www.', '.com', '.org', '.net', '.edu', '.gov', 'url', 'link', 'href', 'src', 'api/', 'endpoint', 'query', 'parameter']
    if any(keyword in text_lower for keyword in link_keywords):
        return CompressionType.LINK
    
    # 代码特征
    code_keywords = ['function', 'def ', 'class ', 'var ', 'const ', 'import ', 'from ', 'return', 'if ', 'for ', 'while ', 'try:', 'except:', 'public', 'private', 'void', 'int', 'string', 'array', 'list', 'dict', 'print', 'console.log', '<?php', '<script', 'html', 'css', 'javascript', 'python', 'java', 'c++', 'sql']
    if any(keyword in text_lower for keyword in code_keywords):
        return CompressionType.CODE
    
    # 表格特征
    table_keywords = ['|', '\t', 'table', 'row', 'column', 'header', 'data', 'cell', 'excel', 'csv', 'tsv', 'spreadsheet']
    if any(keyword in text_lower for keyword in table_keywords):
        return CompressionType.TABLE
    
    # 公式特征
    formula_keywords = ['=', '+', '-', '*', '/', '^', '√', '∫', '∑', '∏', '∞', 'π', 'θ', 'α', 'β', 'γ', 'δ', 'sin', 'cos', 'tan', 'log', 'ln', 'exp', 'sqrt', 'frac', 'frac{', '\\', '(', ')', '[', ']', '{', '}']
    if any(keyword in text_lower for keyword in formula_keywords):
        return CompressionType.FORMULA
    
    # 默认为文本类型
    return CompressionType.TEXT

def calculate_compression_ratio(original_length: int, compressed_length: int) -> float:
    """
    计算压缩比例
    
    Args:
        original_length: 原始文本长度
        compressed_length: 压缩后文本长度
    
    Returns:
        压缩比例（百分比）
    """
    if original_length == 0:
        return 0.0
    return ((original_length - compressed_length) / original_length) * 100

def calculate_information_retention(original_text: str, compressed_text: str) -> float:
    """
    估算信息保留率（简化版本）
    
    Args:
        original_text: 原始文本
        compressed_text: 压缩后文本
    
    Returns:
        信息保留率（百分比）
    """
    # 这是一个简化的估算方法，实际应用中可能需要更复杂的算法
    original_words = set(original_text.split())
    compressed_words = set(compressed_text.split())
    
    if len(original_words) == 0:
        return 100.0
    
    common_words = original_words.intersection(compressed_words)
    retention = (len(common_words) / len(original_words)) * 100
    
    # 考虑压缩比例的影响
    compression_ratio = calculate_compression_ratio(len(original_text), len(compressed_text))
    adjusted_retention = retention * (1 - compression_ratio / 200)  # 简单调整
    
    return max(0.0, min(100.0, adjusted_retention))

# 示例使用函数
def create_compression_workflow(text: str, target_ratio: float = 50.0) -> Dict[str, Any]:
    """
    创建完整的文本压缩工作流
    
    Args:
        text: 输入文本
        target_ratio: 目标压缩比例
    
    Returns:
        包含所有阶段结果的字典
    """
    # 自动判断压缩类型
    compression_type = get_compression_type_from_text(text)
    
    # 计算压缩后的长度
    compressed_length = int(len(text) * (1 - target_ratio / 100))
    
    # 准备所有参数
    kwargs = {
        "text": text,
        "compression_ratio": target_ratio,
        "original_length": len(text),
        "compressed_length": compressed_length,
        "actual_ratio": target_ratio,
        "final_length": compressed_length,
        "final_ratio": target_ratio,
        "information_retention": calculate_information_retention(text, text[:compressed_length]),
        "original_text": text,
        "optimized_text": text[:compressed_length],
        "final_text": text[:compressed_length],
        "preprocess_result": "预处理结果示例",  # 添加缺失的参数
        "compressed_text": text[:compressed_length]  # 添加缺失的参数
    }
    
    # 获取所有阶段的提示词
    prompts = get_all_compression_prompts(compression_type, **kwargs)
    
    return {
        "compression_type": compression_type.value,
        "target_ratio": target_ratio,
        "original_length": len(text),
        "prompts": prompts,
        "workflow": {
            "stage_1": "预处理 - 分析文本类型、结构和关键信息",
            "stage_2": "压缩 - 根据预处理结果进行文本压缩",
            "stage_3": "优化 - 对压缩结果进行质量优化",
            "stage_4": "后处理 - 最终质量检查和报告生成"
        }
    }
