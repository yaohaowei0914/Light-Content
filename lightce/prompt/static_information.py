#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
静态信息提取提示词系统
提供不同级别的静态信息提取功能，按照最终提取数量划分级别
"""

from typing import Dict, List, Any, Optional
from enum import Enum

class InformationLevel(Enum):
    """信息提取级别枚举 - 按最终提取数量划分"""
    MINIMAL = "minimal"       # 最小级别：1-5个实体/关系
    MODERATE = "moderate"     # 中等级别：5-15个实体/关系
    COMPREHENSIVE = "comprehensive"  # 全面级别：15-30个实体/关系
    EXTENSIVE = "extensive"   # 扩展级别：30+个实体/关系

class InformationType(Enum):
    """信息提取类型枚举"""
    ENTITY = "entity"         # 实体提取
    RELATION = "relation"     # 关系提取

# 最小级别提示词
MINIMAL_PROMPTS = {
    InformationType.ENTITY: """你是一个实体提取专家。请从以下文本中提取最重要的实体信息。

提取要求：
1. 识别核心实体（人名、地名、组织名）
2. 识别关键数字实体（金额、数量、时间）
3. 识别重要标识符（编号、代码）
4. 按实体类型分类
5. 提取1-5个最重要的实体

输入文本：
{text}

请按以下格式输出：
核心实体：
- 人名：[人名列表]
- 地名：[地名列表]
- 组织：[组织列表]
- 数字：[重要数字]
- 标识符：[编号代码]""",

    InformationType.RELATION: """你是一个关系提取专家。请从以下文本中提取最重要的关系信息。

提取要求：
1. 识别核心关系（所属、包含、对比）
2. 识别关键动作关系（执行、参与、负责）
3. 识别重要属性关系（拥有、具备、属于）
4. 按关系类型分类
5. 提取1-5个最重要的关系

输入文本：
{text}

请按以下格式输出：
核心关系：
- 所属关系：[实体A属于实体B]
- 包含关系：[实体A包含实体B]
- 动作关系：[实体A执行动作B]
- 属性关系：[实体A具备属性B]
- 其他关系：[其他重要关系]"""
}

# 中等级别提示词
MODERATE_PROMPTS = {
    InformationType.ENTITY: """你是一个实体提取专家。请从以下文本中提取详细的实体信息。

提取要求：
1. 识别所有实体（人名、地名、组织名、时间、数字）
2. 识别实体属性（职位、部门、联系方式）
3. 识别实体分类（个人、组织、地点、事件）
4. 识别实体状态（活跃、历史、计划）
5. 提取5-15个实体，按重要性排序

""",

    InformationType.RELATION: """你是一个关系提取专家。请从以下文本中提取详细的关系信息。

提取要求：
1. 识别所有关系类型（所属、包含、对比、因果、合作）
2. 识别关系强度（强、中、弱）
3. 识别关系方向（单向、双向、多向）
4. 识别关系时间（当前、历史、未来）
5. 提取5-15个关系，按重要性排序
"""
}

# 全面级别提示词
COMPREHENSIVE_PROMPTS = {
    InformationType.ENTITY: """你是一个实体提取专家。请从以下文本中进行全面的实体信息提取。

提取要求：
1. 识别所有实体及其详细属性
2. 识别实体间的层级关系
3. 识别实体的历史变化
4. 识别实体的上下文信息
5. 识别实体的关联实体
6. 提取15-30个实体，构建实体网络
""",

    InformationType.RELATION: """你是一个关系提取专家。请从以下文本中进行全面的关系信息提取。

提取要求：
1. 识别所有关系类型和详细属性
2. 识别关系的强度和可信度
3. 识别关系的时序变化
4. 识别关系的上下文信息
5. 识别关系的网络结构
6. 提取15-30个关系，构建关系网络

"""
}

# 扩展级别提示词
EXTENSIVE_PROMPTS = {
    InformationType.ENTITY: """你是一个实体提取专家。请从以下文本中进行深度和广泛的实体信息提取。

提取要求：
1. 识别所有可能的实体及其完整属性
2. 识别实体的深层特征和隐含信息
3. 识别实体的历史轨迹和未来趋势
4. 识别实体的多维关联和影响
5. 识别实体的价值评估和风险评估
6. 提取30+个实体，构建完整的实体知识图谱
""",

    InformationType.RELATION: """你是一个关系提取专家。请从以下文本中进行深度和广泛的关系信息提取。

提取要求：
1. 识别所有可能的关系类型和完整属性
2. 识别关系的深层特征和隐含信息
3. 识别关系的历史变化和未来趋势
4. 识别关系的多维影响和连锁反应
5. 识别关系的价值评估和风险评估
6. 提取30+个关系，构建完整的关系知识图谱

"""
}

def get_information_prompt(level: InformationLevel, information_type: InformationType, **kwargs) -> str:
    """
    获取指定级别和类型的信息提取提示词
    
    Args:
        level: 信息提取级别
        information_type: 信息提取类型
        **kwargs: 其他参数
    
    Returns:
        格式化后的提示词
    """
    if level == InformationLevel.MINIMAL:
        prompt_template = MINIMAL_PROMPTS.get(information_type)
    elif level == InformationLevel.MODERATE:
        prompt_template = MODERATE_PROMPTS.get(information_type)
    elif level == InformationLevel.COMPREHENSIVE:
        prompt_template = COMPREHENSIVE_PROMPTS.get(information_type)
    elif level == InformationLevel.EXTENSIVE:
        prompt_template = EXTENSIVE_PROMPTS.get(information_type)
    else:
        raise ValueError(f"不支持的信息提取级别: {level}")
    
    if not prompt_template:
        raise ValueError(f"不支持的信息提取类型: {information_type}")
    
    return prompt_template.format(**kwargs)

def get_all_information_prompts(level: InformationLevel, **kwargs) -> Dict[str, str]:
    """
    获取指定级别的所有信息提取提示词
    
    Args:
        level: 信息提取级别
        **kwargs: 其他参数
    
    Returns:
        包含所有信息提取类型提示词的字典
    """
    if level == InformationLevel.MINIMAL:
        prompts = MINIMAL_PROMPTS
    elif level == InformationLevel.MODERATE:
        prompts = MODERATE_PROMPTS
    elif level == InformationLevel.COMPREHENSIVE:
        prompts = COMPREHENSIVE_PROMPTS
    elif level == InformationLevel.EXTENSIVE:
        prompts = EXTENSIVE_PROMPTS
    else:
        raise ValueError(f"不支持的信息提取级别: {level}")
    
    return {
        information_type.value: get_information_prompt(level, information_type, **kwargs)
        for information_type in prompts.keys()
    }

def get_level_description(level: InformationLevel) -> str:
    """
    获取级别的描述信息
    
    Args:
        level: 信息提取级别
    
    Returns:
        级别描述
    """
    descriptions = {
        InformationLevel.MINIMAL: "最小级别：1-5个实体/关系，适合快速信息提取和核心信息识别",
        InformationLevel.MODERATE: "中等级别：5-15个实体/关系，适合结构化信息提取和详细分析",
        InformationLevel.COMPREHENSIVE: "全面级别：15-30个实体/关系，适合深度信息提取和网络构建",
        InformationLevel.EXTENSIVE: "扩展级别：30+个实体/关系，适合复杂信息提取和知识图谱构建"
    }
    return descriptions.get(level, "未知级别")

def get_level_by_quantity(estimated_quantity: int) -> InformationLevel:
    """
    根据预估提取数量自动确定提取级别
    
    Args:
        estimated_quantity: 预估提取数量
    
    Returns:
        提取级别
    """
    if estimated_quantity <= 5:
        return InformationLevel.MINIMAL
    elif estimated_quantity <= 15:
        return InformationLevel.MODERATE
    elif estimated_quantity <= 30:
        return InformationLevel.COMPREHENSIVE
    else:
        return InformationLevel.EXTENSIVE

def get_information_workflow(level: InformationLevel, text: str) -> Dict[str, Any]:
    """
    创建完整的信息提取工作流
    
    Args:
        level: 信息提取级别
        text: 输入文本
    
    Returns:
        包含工作流信息的字典
    """
    workflow_info = {
        "level": level.value,
        "level_description": get_level_description(level),
        "input_text_length": len(text),
        "target_quantity_range": "",
        "workflow_steps": []
    }
    
    if level == InformationLevel.MINIMAL:
        workflow_info["target_quantity_range"] = "1-5个实体/关系"
        workflow_info["workflow_steps"] = [
            "步骤1: 核心实体提取 - 识别最重要的实体",
            "步骤2: 核心关系提取 - 识别最重要的关系"
        ]
    elif level == InformationLevel.MODERATE:
        workflow_info["target_quantity_range"] = "5-15个实体/关系"
        workflow_info["workflow_steps"] = [
            "步骤1: 详细实体提取 - 分类提取实体信息",
            "步骤2: 详细关系提取 - 分类提取关系信息"
        ]
    elif level == InformationLevel.COMPREHENSIVE:
        workflow_info["target_quantity_range"] = "15-30个实体/关系"
        workflow_info["workflow_steps"] = [
            "步骤1: 全面实体提取 - 构建实体网络",
            "步骤2: 全面关系提取 - 构建关系网络"
        ]
    elif level == InformationLevel.EXTENSIVE:
        workflow_info["target_quantity_range"] = "30+个实体/关系"
        workflow_info["workflow_steps"] = [
            "步骤1: 深度实体提取 - 构建知识图谱",
            "步骤2: 深度关系提取 - 构建关系知识图谱"
        ]
    
    # 获取该级别的所有提示词
    workflow_info["prompts"] = get_all_information_prompts(level, text=text)
    
    return workflow_info

# 便捷函数
def create_minimal_information(text: str) -> Dict[str, str]:
    """创建最小级别的信息提取提示词"""
    return get_all_information_prompts(InformationLevel.MINIMAL, text=text)

def create_moderate_information(text: str) -> Dict[str, str]:
    """创建中等级别的信息提取提示词"""
    return get_all_information_prompts(InformationLevel.MODERATE, text=text)

def create_comprehensive_information(text: str) -> Dict[str, str]:
    """创建全面级别的信息提取提示词"""
    return get_all_information_prompts(InformationLevel.COMPREHENSIVE, text=text)

def create_extensive_information(text: str) -> Dict[str, str]:
    """创建扩展级别的信息提取提示词"""
    return get_all_information_prompts(InformationLevel.EXTENSIVE, text=text)

def auto_extract(text: str, information_type: InformationType, estimated_quantity: int = None) -> Dict[str, Any]:
    """
    自动根据预估数量进行信息提取
    
    Args:
        text: 输入文本
        information_type: 信息提取类型
        estimated_quantity: 预估提取数量，如果不提供则根据文本长度估算
    
    Returns:
        提取结果信息
    """
    if estimated_quantity is None:
        # 根据文本长度估算提取数量
        text_length = len(text)
        if text_length < 100:
            estimated_quantity = 3
        elif text_length < 500:
            estimated_quantity = 8
        elif text_length < 1000:
            estimated_quantity = 20
        else:
            estimated_quantity = 35
    
    level = get_level_by_quantity(estimated_quantity)
    prompt = get_information_prompt(level, information_type, text=text)
    
    return {
        "level": level.value,
        "level_description": get_level_description(level),
        "information_type": information_type.value,
        "input_length": len(text),
        "estimated_quantity": estimated_quantity,
        "target_quantity_range": get_information_workflow(level, text)["target_quantity_range"],
        "prompt": prompt
    }

# 示例使用
if __name__ == "__main__":
    # 测试文本
    test_texts = [
        "张三在北京工作。",  # 短文本，预估2个实体，1个关系
        "张三在北京ABC公司技术部工作，月薪15000元，联系电话13812345678。",  # 中等文本，预估5个实体，3个关系
        "张三在北京ABC公司技术部担任经理职位，月薪15000元，联系电话13812345678，邮箱zhangsan@abc.com，负责管理10名员工，与市场部李四合作开发新产品。",  # 长文本，预估15个实体，8个关系
        "张三在北京ABC公司技术部担任经理职位，月薪15000元，联系电话13812345678，邮箱zhangsan@abc.com，负责管理10名员工，与市场部李四合作开发新产品，该产品预计明年3月上市，投资预算500万元，目标客户包括个人用户和企业用户，竞争对手包括XYZ公司和DEF公司，技术合作伙伴包括清华大学和微软公司。"  # 扩展文本，预估25个实体，15个关系
    ]
    
    print("=== 静态信息提取提示词系统演示 ===")
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n测试文本 {i} (长度: {len(text)} 字符):")
        print(f"内容: {text[:50]}...")
        
        # 自动提取
        for information_type in InformationType:
            result = auto_extract(text, information_type)
            print(f"\n{information_type.value.upper()} 提取:")
            print(f"  级别: {result['level']}")
            print(f"  描述: {result['level_description']}")
            print(f"  预估数量: {result['estimated_quantity']}")
            print(f"  目标范围: {result['target_quantity_range']}")
            print(f"  提示词长度: {len(result['prompt'])} 字符")
