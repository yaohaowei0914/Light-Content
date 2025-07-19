#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语义提取提示词系统
提供不同级别的语义提取功能，按照最终提取文本长度划分级别
"""

from typing import Dict, List, Any, Optional
from enum import Enum

class ExtractionLevel(Enum):
    """提取级别枚举 - 按最终文本长度划分"""
    SHORT = "short"           # 短文本：50-200字符
    MEDIUM = "medium"         # 中等文本：200-500字符
    LONG = "long"             # 长文本：500-1000字符
    EXTENDED = "extended"     # 扩展文本：1000+字符

class ExtractionType(Enum):
    """提取类型枚举"""
    KEYWORDS = "keywords"         # 关键词提取
    SUMMARY = "summary"           # 摘要生成

# 短文本级别提示词
SHORT_PROMPTS = {
    ExtractionType.KEYWORDS: """你是一个关键词提取专家。请从以下文本中提取最重要的关键词。

提取要求：
1. 识别文本中的核心词汇
2. 包含名词、动词、形容词等关键词性
3. 按重要性排序
4. 去除重复和无关词汇
5. 提供3-5个关键词

输入文本：
{text}

请按以下格式输出：
关键词列表：
1. [关键词1] - [词性] - [重要性说明]
2. [关键词2] - [词性] - [重要性说明]
...""",

    ExtractionType.SUMMARY: """你是一个摘要生成专家。请为以下文本生成简洁的摘要。

摘要要求：
1. 保留核心信息
2. 突出主要观点
3. 保持逻辑清晰
4. 控制在50-200字符
5. 确保信息准确

输入文本：
{text}

请输出摘要："""
}

# 中等文本级别提示词
MEDIUM_PROMPTS = {
    ExtractionType.KEYWORDS: """你是一个关键词提取专家。请从以下文本中提取最重要的关键词。

提取要求：
1. 识别文本中的核心词汇
2. 包含名词、动词、形容词等关键词性
3. 按重要性排序
4. 去除重复和无关词汇
5. 提供5-8个关键词

输入文本：
{text}

请按以下格式输出：
关键词列表：
1. [关键词1] - [词性] - [重要性说明]
2. [关键词2] - [词性] - [重要性说明]
...

主题分类：
- 主要主题：[主题列表]
- 次要主题：[主题列表]""",

    ExtractionType.SUMMARY: """你是一个摘要生成专家。请为以下文本生成详细的摘要。

摘要要求：
1. 保留核心信息和重要观点
2. 突出关键结论和发现
3. 维持逻辑结构
4. 控制在200-500字符
5. 包含关键证据支撑

输入文本：
{text}

请按以下格式输出：
核心观点：
[主要观点]

关键信息：
[重要信息点]

结论：
[主要结论]"""
}

# 长文本级别提示词
LONG_PROMPTS = {
    ExtractionType.KEYWORDS: """你是一个关键词提取专家。请从以下文本中提取最重要的关键词。

提取要求：
1. 识别文本中的核心词汇
2. 包含名词、动词、形容词等关键词性
3. 按重要性排序
4. 去除重复和无关词汇
5. 提供8-12个关键词

输入文本：
{text}

请按以下格式输出：
关键词列表：
1. [关键词1] - [词性] - [重要性说明]
2. [关键词2] - [词性] - [重要性说明]
...

主题分类：
- 主要主题：[主题列表]
- 次要主题：[主题列表]
- 相关概念：[概念列表]

实体识别：
- 人名：[实体列表]
- 地名：[实体列表]
- 组织：[实体列表]
- 技术术语：[术语列表]""",

    ExtractionType.SUMMARY: """你是一个摘要生成专家。请为以下文本生成全面的摘要。

摘要要求：
1. 保留核心信息和重要观点
2. 突出关键结论和发现
3. 维持逻辑结构和关系
4. 控制在500-1000字符
5. 包含关键证据和支撑
6. 提供多层次的摘要

输入文本：
{text}

请按以下格式输出：
核心观点：
[主要观点列表]

关键信息：
[重要信息点]

逻辑结构：
[文本的逻辑组织]

证据支撑：
[关键证据和例子]

结论：
[主要结论]"""
}

# 扩展文本级别提示词
EXTENDED_PROMPTS = {
    ExtractionType.KEYWORDS: """你是一个关键词提取专家。请从以下文本中提取最重要的关键词。

提取要求：
1. 识别文本中的核心词汇
2. 包含名词、动词、形容词等关键词性
3. 按重要性排序
4. 去除重复和无关词汇
5. 提供12-20个关键词

输入文本：
{text}

请按以下格式输出：
关键词列表：
1. [关键词1] - [词性] - [重要性说明]
2. [关键词2] - [词性] - [重要性说明]
...

主题分类：
- 主要主题：[主题列表]
- 次要主题：[主题列表]
- 相关概念：[概念列表]

实体识别：
- 人名：[实体列表]
- 地名：[实体列表]
- 组织：[实体列表]
- 技术术语：[术语列表]
- 时间：[时间列表]

关系网络：
- 核心关系：[关系列表]
- 次要关系：[关系列表]""",

    ExtractionType.SUMMARY: """你是一个摘要生成专家。请为以下文本生成深度语义摘要。

摘要要求：
1. 保留核心语义信息
2. 突出重要观点和结论
3. 维持逻辑结构和关系
4. 控制在1000+字符
5. 包含关键证据和支撑
6. 提供多层次的摘要
7. 包含语义分析和推理

输入文本：
{text}

请按以下格式输出：
语义摘要：

核心观点：
[主要观点列表]

关键信息：
[重要信息点]

逻辑结构：
[文本的逻辑组织]

证据支撑：
[关键证据和例子]

语义分析：
[深层语义理解]

推理过程：
[逻辑推理过程]

结论：
[主要结论]

影响评估：
[影响和意义分析]"""
}

def get_extraction_prompt(level: ExtractionLevel, extraction_type: ExtractionType, **kwargs) -> str:
    """
    获取指定级别和类型的提取提示词
    
    Args:
        level: 提取级别
        extraction_type: 提取类型
        **kwargs: 其他参数
    
    Returns:
        格式化后的提示词
    """
    if level == ExtractionLevel.SHORT:
        prompt_template = SHORT_PROMPTS.get(extraction_type)
    elif level == ExtractionLevel.MEDIUM:
        prompt_template = MEDIUM_PROMPTS.get(extraction_type)
    elif level == ExtractionLevel.LONG:
        prompt_template = LONG_PROMPTS.get(extraction_type)
    elif level == ExtractionLevel.EXTENDED:
        prompt_template = EXTENDED_PROMPTS.get(extraction_type)
    else:
        raise ValueError(f"不支持的提取级别: {level}")
    
    if not prompt_template:
        raise ValueError(f"不支持的提取类型: {extraction_type}")
    
    return prompt_template.format(**kwargs)

def get_all_extraction_prompts(level: ExtractionLevel, **kwargs) -> Dict[str, str]:
    """
    获取指定级别的所有提取提示词
    
    Args:
        level: 提取级别
        **kwargs: 其他参数
    
    Returns:
        包含所有提取类型提示词的字典
    """
    if level == ExtractionLevel.SHORT:
        prompts = SHORT_PROMPTS
    elif level == ExtractionLevel.MEDIUM:
        prompts = MEDIUM_PROMPTS
    elif level == ExtractionLevel.LONG:
        prompts = LONG_PROMPTS
    elif level == ExtractionLevel.EXTENDED:
        prompts = EXTENDED_PROMPTS
    else:
        raise ValueError(f"不支持的提取级别: {level}")
    
    return {
        extraction_type.value: get_extraction_prompt(level, extraction_type, **kwargs)
        for extraction_type in prompts.keys()
    }

def get_level_description(level: ExtractionLevel) -> str:
    """
    获取级别的描述信息
    
    Args:
        level: 提取级别
    
    Returns:
        级别描述
    """
    descriptions = {
        ExtractionLevel.SHORT: "短文本级别：50-200字符，适合快速信息提取和简洁摘要",
        ExtractionLevel.MEDIUM: "中等文本级别：200-500字符，适合结构化信息提取和详细摘要",
        ExtractionLevel.LONG: "长文本级别：500-1000字符，适合深度信息提取和全面摘要",
        ExtractionLevel.EXTENDED: "扩展文本级别：1000+字符，适合复杂语义分析和深度摘要"
    }
    return descriptions.get(level, "未知级别")

def get_level_by_text_length(text_length: int) -> ExtractionLevel:
    """
    根据文本长度自动确定提取级别
    
    Args:
        text_length: 文本长度（字符数）
    
    Returns:
        提取级别
    """
    if text_length < 200:
        return ExtractionLevel.SHORT
    elif text_length < 500:
        return ExtractionLevel.MEDIUM
    elif text_length < 1000:
        return ExtractionLevel.LONG
    else:
        return ExtractionLevel.EXTENDED

def get_extraction_workflow(level: ExtractionLevel, text: str) -> Dict[str, Any]:
    """
    创建完整的语义提取工作流
    
    Args:
        level: 提取级别
        text: 输入文本
    
    Returns:
        包含工作流信息的字典
    """
    workflow_info = {
        "level": level.value,
        "level_description": get_level_description(level),
        "input_text_length": len(text),
        "target_length_range": "",
        "workflow_steps": []
    }
    
    if level == ExtractionLevel.SHORT:
        workflow_info["target_length_range"] = "50-200字符"
        workflow_info["workflow_steps"] = [
            "步骤1: 快速关键词提取 - 识别核心词汇",
            "步骤2: 简洁摘要生成 - 生成简短摘要"
        ]
    elif level == ExtractionLevel.MEDIUM:
        workflow_info["target_length_range"] = "200-500字符"
        workflow_info["workflow_steps"] = [
            "步骤1: 结构化关键词提取 - 分类提取关键词",
            "步骤2: 详细摘要生成 - 包含主要观点和结论"
        ]
    elif level == ExtractionLevel.LONG:
        workflow_info["target_length_range"] = "500-1000字符"
        workflow_info["workflow_steps"] = [
            "步骤1: 深度关键词提取 - 包含实体识别和关系分析",
            "步骤2: 全面摘要生成 - 多层次信息提取"
        ]
    elif level == ExtractionLevel.EXTENDED:
        workflow_info["target_length_range"] = "1000+字符"
        workflow_info["workflow_steps"] = [
            "步骤1: 综合关键词提取 - 构建语义网络",
            "步骤2: 深度语义摘要 - 包含推理和分析"
        ]
    
    # 获取该级别的所有提示词
    workflow_info["prompts"] = get_all_extraction_prompts(level, text=text)
    
    return workflow_info

# 便捷函数
def create_short_extraction(text: str) -> Dict[str, str]:
    """创建短文本级别的提取提示词"""
    return get_all_extraction_prompts(ExtractionLevel.SHORT, text=text)

def create_medium_extraction(text: str) -> Dict[str, str]:
    """创建中等文本级别的提取提示词"""
    return get_all_extraction_prompts(ExtractionLevel.MEDIUM, text=text)

def create_long_extraction(text: str) -> Dict[str, str]:
    """创建长文本级别的提取提示词"""
    return get_all_extraction_prompts(ExtractionLevel.LONG, text=text)

def create_extended_extraction(text: str) -> Dict[str, str]:
    """创建扩展文本级别的提取提示词"""
    return get_all_extraction_prompts(ExtractionLevel.EXTENDED, text=text)

def auto_extract(text: str, extraction_type: ExtractionType) -> Dict[str, Any]:
    """
    自动根据文本长度进行提取
    
    Args:
        text: 输入文本
        extraction_type: 提取类型
    
    Returns:
        提取结果信息
    """
    level = get_level_by_text_length(len(text))
    prompt = get_extraction_prompt(level, extraction_type, text=text)
    
    return {
        "level": level.value,
        "level_description": get_level_description(level),
        "extraction_type": extraction_type.value,
        "input_length": len(text),
        "target_length_range": get_extraction_workflow(level, text)["target_length_range"],
        "prompt": prompt
    }

# 示例使用
if __name__ == "__main__":
    # 测试文本
    test_texts = [
        "人工智能技术正在快速发展。",  # 短文本
        "人工智能技术正在快速发展，为各行各业带来了革命性的变化。深度学习模型在自然语言处理任务中取得了显著的效果提升。",  # 中等文本
        "人工智能技术正在快速发展，为各行各业带来了革命性的变化。深度学习模型在自然语言处理任务中取得了显著的效果提升。通过对比分析，我们发现Transformer架构在处理长文本时具有明显优势。这些发现为后续的研究提供了重要的理论基础和实践指导。",  # 长文本
        "人工智能技术正在快速发展，为各行各业带来了革命性的变化。深度学习模型在自然语言处理任务中取得了显著的效果提升。通过对比分析，我们发现Transformer架构在处理长文本时具有明显优势。这些发现为后续的研究提供了重要的理论基础和实践指导。随着技术的不断进步，我们预计在未来几年内，人工智能将在更多领域发挥重要作用，包括医疗诊断、自动驾驶、智能客服等。同时，我们也需要关注人工智能发展过程中可能带来的伦理和安全问题，确保技术的健康发展。"  # 扩展文本
    ]
    
    print("=== 语义提取提示词系统演示 ===")
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n测试文本 {i} (长度: {len(text)} 字符):")
        print(f"内容: {text[:50]}...")
        
        # 自动提取
        for extraction_type in ExtractionType:
            result = auto_extract(text, extraction_type)
            print(f"\n{extraction_type.value.upper()} 提取:")
            print(f"  级别: {result['level']}")
            print(f"  描述: {result['level_description']}")
            print(f"  目标长度: {result['target_length_range']}")
            print(f"  提示词长度: {len(result['prompt'])} 字符")
