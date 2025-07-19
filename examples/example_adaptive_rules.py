from lightce.agent.react_agent import AdaptiveRule, BehaviorPattern, ReactionType
from typing import List

# 自适应规则示例
ADAPTIVE_RULES = [
    AdaptiveRule(
        name="错误纠正规则",
        description="当用户指出错误时，降低创造性并提高准确性",
        condition="错误 不对 错了 不正确",
        action="降低temperature参数，提高准确性",
        priority=9,
        adaptation_factor=1.5
    ),
    AdaptiveRule(
        name="用户满意度规则",
        description="当用户表达满意时，保持当前行为模式",
        condition="好 满意 不错 谢谢 感谢",
        action="保持当前参数设置",
        priority=7,
        adaptation_factor=0.8
    ),
    AdaptiveRule(
        name="技术问题规则",
        description="处理技术问题时使用更专业的语言",
        condition="技术 代码 编程 算法 系统",
        action="使用专业术语，提供详细解释",
        priority=8,
        adaptation_factor=1.2
    ),
    AdaptiveRule(
        name="紧急情况规则",
        description="处理紧急或重要问题时采用谨慎态度",
        condition="紧急 重要 关键 危险 问题",
        action="采用谨慎的响应风格，降低创造性",
        priority=10,
        adaptation_factor=1.8
    ),
    AdaptiveRule(
        name="学习模式规则",
        description="在学习场景下引导用户思考",
        condition="学习 理解 解释 为什么 如何",
        action="引导思考，提供步骤性解释",
        priority=6,
        adaptation_factor=1.1
    ),
    AdaptiveRule(
        name="创意模式规则",
        description="在创意场景下提高创造性",
        condition="创意 想象 故事 写作 设计",
        action="提高创造性，鼓励发散思维",
        priority=5,
        adaptation_factor=1.3
    ),
    AdaptiveRule(
        name="简化回答规则",
        description="当用户要求简化时，使用更简洁的语言",
        condition="简单 简洁 简短 简化 通俗",
        action="使用简洁明了的语言",
        priority=6,
        adaptation_factor=0.9
    ),
    AdaptiveRule(
        name="详细解释规则",
        description="当用户要求详细时，提供更全面的解释",
        condition="详细 全面 深入 具体 更多",
        action="提供详细全面的解释",
        priority=7,
        adaptation_factor=1.4
    )
]

# 行为模式示例
BEHAVIOR_PATTERNS = [
    BehaviorPattern(
        pattern_name="技术支持模式",
        description="专门处理技术问题的行为模式",
        triggers=["代码", "编程", "技术", "bug", "错误", "系统"],
        responses=[
            "让我帮您分析这个技术问题...",
            "从技术角度来看，这个问题可以这样解决...",
            "我建议采用以下技术方案...",
            "这个技术问题的根本原因是..."
        ],
        success_rate=0.85,
        usage_count=0
    ),
    BehaviorPattern(
        pattern_name="学习指导模式",
        description="专门用于学习指导的行为模式",
        triggers=["学习", "理解", "解释", "概念", "原理", "为什么"],
        responses=[
            "让我帮您理解这个概念...",
            "我们可以从基础开始，逐步深入...",
            "这个原理的关键点是...",
            "为了更好地理解，让我们一步步分析..."
        ],
        success_rate=0.80,
        usage_count=0
    ),
    BehaviorPattern(
        pattern_name="创意激发模式",
        description="专门用于创意激发的行为模式",
        triggers=["创意", "想象", "故事", "写作", "设计", "灵感"],
        responses=[
            "让我们一起来探索创意想法...",
            "从不同的角度来看这个问题...",
            "我们可以尝试一些创新的方法...",
            "这个创意可以这样发展..."
        ],
        success_rate=0.75,
        usage_count=0
    ),
    BehaviorPattern(
        pattern_name="问题解决模式",
        description="专门用于问题解决的行为模式",
        triggers=["问题", "解决", "方案", "方法", "如何", "怎么办"],
        responses=[
            "让我帮您分析这个问题...",
            "我们可以考虑以下几种解决方案...",
            "这个问题的解决思路是...",
            "建议采用以下步骤来解决..."
        ],
        success_rate=0.82,
        usage_count=0
    ),
    BehaviorPattern(
        pattern_name="情感支持模式",
        description="专门用于情感支持的行为模式",
        triggers=["心情", "情感", "压力", "困难", "帮助", "支持"],
        responses=[
            "我理解您的感受...",
            "让我们一起面对这个挑战...",
            "您并不孤单，我会一直支持您...",
            "让我们找到积极的方式来处理..."
        ],
        success_rate=0.78,
        usage_count=0
    ),
    BehaviorPattern(
        pattern_name="信息查询模式",
        description="专门用于信息查询的行为模式",
        triggers=["查询", "搜索", "信息", "数据", "统计", "事实"],
        responses=[
            "让我为您查找相关信息...",
            "根据最新的信息，我可以告诉您...",
            "让我为您提供准确的数据...",
            "这些信息可以帮助您了解..."
        ],
        success_rate=0.88,
        usage_count=0
    )
]

def get_adaptive_rules_by_category(category: str) -> list:
    """
    根据类别获取自适应规则
    
    Args:
        category: 规则类别 (error_correction, user_satisfaction, technical, emergency, learning, creative, simplification, detailed)
    
    Returns:
        规则列表
    """
    rule_categories = {
        "error_correction": [ADAPTIVE_RULES[0]],
        "user_satisfaction": [ADAPTIVE_RULES[1]],
        "technical": [ADAPTIVE_RULES[2]],
        "emergency": [ADAPTIVE_RULES[3]],
        "learning": [ADAPTIVE_RULES[4]],
        "creative": [ADAPTIVE_RULES[5]],
        "simplification": [ADAPTIVE_RULES[6]],
        "detailed": [ADAPTIVE_RULES[7]],
        "all": ADAPTIVE_RULES
    }
    
    return rule_categories.get(category, [])

def get_behavior_patterns_by_category(category: str) -> list:
    """
    根据类别获取行为模式
    
    Args:
        category: 模式类别 (technical_support, learning_guidance, creative_inspiration, problem_solving, emotional_support, information_query)
    
    Returns:
        行为模式列表
    """
    pattern_categories = {
        "technical_support": [BEHAVIOR_PATTERNS[0]],
        "learning_guidance": [BEHAVIOR_PATTERNS[1]],
        "creative_inspiration": [BEHAVIOR_PATTERNS[2]],
        "problem_solving": [BEHAVIOR_PATTERNS[3]],
        "emotional_support": [BEHAVIOR_PATTERNS[4]],
        "information_query": [BEHAVIOR_PATTERNS[5]],
        "all": BEHAVIOR_PATTERNS
    }
    
    return pattern_categories.get(category, [])

def create_custom_adaptive_rule(
    name: str, 
    description: str, 
    condition: str, 
    action: str, 
    priority: int = 5,
    adaptation_factor: float = 1.0
) -> AdaptiveRule:
    """
    创建自定义自适应规则
    
    Args:
        name: 规则名称
        description: 规则描述
        condition: 触发条件
        action: 执行动作
        priority: 优先级 (1-10)
        adaptation_factor: 适应因子 (0.0-2.0)
    
    Returns:
        AdaptiveRule实例
    """
    return AdaptiveRule(
        name=name,
        description=description,
        condition=condition,
        action=action,
        priority=priority,
        adaptation_factor=adaptation_factor,
        active=True
    )

def create_custom_behavior_pattern(
    pattern_name: str,
    description: str,
    triggers: List[str],
    responses: List[str],
    success_rate: float = 0.5
) -> BehaviorPattern:
    """
    创建自定义行为模式
    
    Args:
        pattern_name: 模式名称
        description: 模式描述
        triggers: 触发条件列表
        responses: 响应模板列表
        success_rate: 成功率 (0.0-1.0)
    
    Returns:
        BehaviorPattern实例
    """
    return BehaviorPattern(
        pattern_name=pattern_name,
        description=description,
        triggers=triggers,
        responses=responses,
        success_rate=success_rate,
        usage_count=0
    )

# 预定义的规则和模式集合
EXAMPLE_ADAPTIVE_RULES = {
    "error_correction": [ADAPTIVE_RULES[0]],
    "user_satisfaction": [ADAPTIVE_RULES[1]],
    "technical": [ADAPTIVE_RULES[2]],
    "emergency": [ADAPTIVE_RULES[3]],
    "learning": [ADAPTIVE_RULES[4]],
    "creative": [ADAPTIVE_RULES[5]],
    "simplification": [ADAPTIVE_RULES[6]],
    "detailed": [ADAPTIVE_RULES[7]],
    "all": ADAPTIVE_RULES
}

EXAMPLE_BEHAVIOR_PATTERNS = {
    "technical_support": [BEHAVIOR_PATTERNS[0]],
    "learning_guidance": [BEHAVIOR_PATTERNS[1]],
    "creative_inspiration": [BEHAVIOR_PATTERNS[2]],
    "problem_solving": [BEHAVIOR_PATTERNS[3]],
    "emotional_support": [BEHAVIOR_PATTERNS[4]],
    "information_query": [BEHAVIOR_PATTERNS[5]],
    "all": BEHAVIOR_PATTERNS
} 