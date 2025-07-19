# React Agent使用指南

## 概述

React Agent是一个能够根据环境变化和用户反馈动态调整行为的智能Agent系统。它通过实时分析上下文、应用自适应规则和匹配行为模式，提供个性化的智能响应。

## 主要特性

- 🌍 **环境事件感知**: 实时监控和响应环境变化
- 💬 **用户反馈适应**: 根据用户反馈动态调整行为
- 📋 **自适应规则系统**: 可配置的智能适应规则
- 🎯 **行为模式匹配**: 智能匹配和应用行为模式
- 🔍 **上下文分析**: 深度分析当前对话上下文
- ⚙️ **动态参数调整**: 实时调整模型参数
- 📊 **适应统计监控**: 全面的适应效果统计
- 🧠 **持续学习能力**: 不断优化和适应

## 核心组件

### 1. 环境事件 (EnvironmentEvent)

```python
from lightce.agent.react_agent import EnvironmentEvent

event = EnvironmentEvent(
    event_type="系统错误",
    description="数据库连接失败",
    severity=0.8,  # 严重程度 (0.0-1.0)
    metadata={"component": "database", "error_code": "DB001"}
)
```

### 2. 用户反馈 (UserFeedback)

```python
from lightce.agent.react_agent import UserFeedback, ReactionType

feedback = UserFeedback(
    feedback_type=ReactionType.NEGATIVE,  # 反馈类型
    content="回答不够详细",
    confidence=0.8,  # 置信度 (0.0-1.0)
    context={"topic": "技术问题"}
)
```

### 3. 自适应规则 (AdaptiveRule)

```python
from lightce.agent.react_agent import AdaptiveRule

rule = AdaptiveRule(
    name="错误纠正规则",
    description="当用户指出错误时，降低创造性并提高准确性",
    condition="错误 不对 错了 不正确",
    action="降低temperature参数，提高准确性",
    priority=9,  # 优先级 (1-10)
    adaptation_factor=1.5  # 适应因子 (0.0-2.0)
)
```

### 4. 行为模式 (BehaviorPattern)

```python
from lightce.agent.react_agent import BehaviorPattern

pattern = BehaviorPattern(
    pattern_name="技术支持模式",
    description="专门处理技术问题的行为模式",
    triggers=["代码", "编程", "技术", "bug", "错误", "系统"],
    responses=[
        "让我帮您分析这个技术问题...",
        "从技术角度来看，这个问题可以这样解决..."
    ],
    success_rate=0.85  # 成功率 (0.0-1.0)
)
```

### 5. React Agent配置 (ReactAgentConfig)

```python
from lightce.agent.react_agent import ReactAgentConfig

config = ReactAgentConfig(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
    max_environment_events=50,  # 最大环境事件数量
    max_user_feedback=100,  # 最大用户反馈数量
    adaptation_threshold=0.3,  # 适应阈值
    learning_rate=0.1,  # 学习率
    feedback_weight=0.7,  # 反馈权重
    event_weight=0.3  # 事件权重
)
```

## 快速开始

### 1. 基本使用

```python
from lightce.agent.react_agent import create_react_agent
from lightce.tools.example_tools import EXAMPLE_TOOLS
from lightce.tools.example_adaptive_rules import get_adaptive_rules_by_category, get_behavior_patterns_by_category

# 创建React Agent
agent = create_react_agent(
    tools=EXAMPLE_TOOLS,
    adaptive_rules=get_adaptive_rules_by_category("all"),
    behavior_patterns=get_behavior_patterns_by_category("all")
)

# 运行Agent
result = agent.run("请告诉我现在的时间")
print(f"回答: {result['response']}")
print(f"适应水平: {result['adaptation_level']:.2f}")
```

### 2. 添加环境事件

```python
# 添加系统事件
agent.add_environment_event(
    event_type="系统错误",
    description="检测到系统性能下降",
    severity=0.8,
    metadata={"component": "database", "error_code": "DB001"}
)

# 添加用户行为事件
agent.add_environment_event(
    event_type="用户切换",
    description="用户从初学者切换到专家模式",
    severity=0.5
)
```

### 3. 添加用户反馈

```python
from lightce.agent.react_agent import ReactionType

# 添加负面反馈
agent.add_user_feedback(
    feedback_type=ReactionType.NEGATIVE,
    content="你的解释太复杂了，我不理解",
    confidence=0.9
)

# 添加正面反馈
agent.add_user_feedback(
    feedback_type=ReactionType.POSITIVE,
    content="回答很准确，谢谢",
    confidence=0.8
)

# 添加纠正反馈
agent.add_user_feedback(
    feedback_type=ReactionType.CORRECTION,
    content="这个信息过时了，需要更新",
    confidence=0.9
)
```

### 4. 添加自适应规则

```python
from lightce.tools.example_adaptive_rules import create_custom_adaptive_rule

# 创建自定义规则
custom_rule = create_custom_adaptive_rule(
    name="编程问题规则",
    description="处理编程问题时提供代码示例",
    condition="编程 代码 函数 类 变量",
    action="提供代码示例和详细解释",
    priority=8,
    adaptation_factor=1.3
)

agent.add_adaptive_rule(custom_rule)
```

## 高级功能

### 1. 上下文分析

```python
# 分析当前上下文
context = agent.analyze_context("请帮我解决这个问题")

print(f"环境事件: {len(context['recent_events'])}")
print(f"用户反馈: {len(context['recent_feedback'])}")
print(f"适用规则: {len(context['applicable_rules'])}")
print(f"匹配模式: {len(context['matching_patterns'])}")
print(f"适应水平: {context['adaptation_score']:.2f}")
print(f"需要适应: {context['adaptation_needed']}")
```

### 2. 适应统计

```python
# 获取适应统计信息
stats = agent.get_adaptation_stats()

print(f"平均适应水平: {stats['average_adaptation']:.2f}")
print(f"总反馈数量: {stats['total_feedback']}")
print(f"总事件数量: {stats['total_events']}")
print(f"反馈分布: {stats['feedback_distribution']}")
```

### 3. 配置管理

```python
from lightce.agent.react_agent import ReactAgentConfig

# 自定义配置
config = ReactAgentConfig(
    temperature=0.3,  # 更确定性的回答
    adaptation_threshold=0.2,  # 更敏感的适应阈值
    learning_rate=0.15,  # 更快的学习率
    feedback_weight=0.8,  # 更重视用户反馈
    event_weight=0.2  # 较少重视环境事件
)

agent = create_react_agent(config=config)

# 查看配置
agent_config = agent.get_config()
print(f"模型: {agent_config['model_config']['model_name']}")
print(f"工具数量: {len(agent_config['tools'])}")
print(f"自适应规则数量: {len(agent_config['adaptive_rules'])}")
print(f"行为模式数量: {len(agent_config['behavior_patterns'])}")
```

### 4. 历史管理

```python
# 清除特定类型的历史
agent.clear_history("events")  # 清除环境事件
agent.clear_history("feedback")  # 清除用户反馈
agent.clear_history("rules")  # 清除自适应规则
agent.clear_history("patterns")  # 清除行为模式

# 清除所有历史
agent.clear_history("all")
```

## 使用场景

### 1. 智能客服系统

```python
# 创建智能客服Agent
agent = create_react_agent(
    tools=EXAMPLE_TOOLS,
    adaptive_rules=get_adaptive_rules_by_category("user_satisfaction") + get_adaptive_rules_by_category("error_correction"),
    behavior_patterns=get_behavior_patterns_by_category("problem_solving")
)

# 模拟客服对话
result1 = agent.run("我的订单没有收到")
print(f"客服: {result1['response']}")

# 用户不满意
agent.add_user_feedback(ReactionType.NEGATIVE, "你的回答没有帮助", 0.8)

# 重新回答
result2 = agent.run("请重新帮我解决订单问题")
print(f"客服: {result2['response']}")
```

### 2. 学习助手系统

```python
# 创建学习助手
agent = create_react_agent(
    adaptive_rules=get_adaptive_rules_by_category("learning"),
    behavior_patterns=get_behavior_patterns_by_category("learning_guidance")
)

# 记录学习进度
agent.add_environment_event("学习阶段", "用户开始学习微积分", 0.6)

# 学习指导
result = agent.run("请解释什么是导数")
print(f"学习助手: {result['response']}")

# 用户需要澄清
agent.add_user_feedback(ReactionType.CLARIFICATION, "能举个具体的例子吗？", 0.7)

# 提供例子
result2 = agent.run("请用例子解释导数")
print(f"学习助手: {result2['response']}")
```

### 3. 技术支持系统

```python
# 创建技术支持Agent
agent = create_react_agent(
    tools=EXAMPLE_TOOLS,
    adaptive_rules=get_adaptive_rules_by_category("technical") + get_adaptive_rules_by_category("emergency"),
    behavior_patterns=get_behavior_patterns_by_category("technical_support")
)

# 记录技术背景
agent.add_environment_event("技术环境", "用户使用Python 3.9", 0.5)
agent.add_environment_event("用户水平", "用户是初学者", 0.7)

# 技术支持
result = agent.run("我的Python代码出现了错误，请帮我检查")
print(f"技术支持: {result['response']}")
```

### 4. 创意写作助手

```python
# 创建创意写作助手
agent = create_react_agent(
    adaptive_rules=get_adaptive_rules_by_category("creative"),
    behavior_patterns=get_behavior_patterns_by_category("creative_inspiration")
)

# 记录创作偏好
agent.add_environment_event("创作风格", "用户偏好科幻题材", 0.6)
agent.add_user_feedback(ReactionType.POSITIVE, "这个创意很好", 0.8)

# 创意写作
result = agent.run("请帮我写一个科幻故事的开头")
print(f"创意助手: {result['response']}")
```

## 自适应规则类别

### 1. 错误纠正规则 (error_correction)
- 当用户指出错误时，降低创造性并提高准确性

### 2. 用户满意度规则 (user_satisfaction)
- 当用户表达满意时，保持当前行为模式

### 3. 技术问题规则 (technical)
- 处理技术问题时使用更专业的语言

### 4. 紧急情况规则 (emergency)
- 处理紧急或重要问题时采用谨慎态度

### 5. 学习模式规则 (learning)
- 在学习场景下引导用户思考

### 6. 创意模式规则 (creative)
- 在创意场景下提高创造性

### 7. 简化回答规则 (simplification)
- 当用户要求简化时，使用更简洁的语言

### 8. 详细解释规则 (detailed)
- 当用户要求详细时，提供更全面的解释

## 行为模式类别

### 1. 技术支持模式 (technical_support)
- 专门处理技术问题的行为模式

### 2. 学习指导模式 (learning_guidance)
- 专门用于学习指导的行为模式

### 3. 创意激发模式 (creative_inspiration)
- 专门用于创意激发的行为模式

### 4. 问题解决模式 (problem_solving)
- 专门用于问题解决的行为模式

### 5. 情感支持模式 (emotional_support)
- 专门用于情感支持的行为模式

### 6. 信息查询模式 (information_query)
- 专门用于信息查询的行为模式

## 反应类型

### 1. POSITIVE
- 正面反应，表示用户满意

### 2. NEGATIVE
- 负面反应，表示用户不满意

### 3. NEUTRAL
- 中性反应，表示用户态度中立

### 4. CORRECTION
- 纠正反应，表示需要纠正信息

### 5. CLARIFICATION
- 澄清反应，表示需要进一步澄清

## 最佳实践

### 1. 环境事件管理
- 及时记录重要的环境变化
- 设置合理的严重程度评分
- 使用有意义的元数据
- 定期清理过期事件

### 2. 用户反馈处理
- 快速响应用户反馈
- 设置合理的置信度
- 记录反馈的上下文信息
- 分析反馈模式

### 3. 自适应规则配置
- 根据使用场景选择合适的规则
- 设置合理的优先级
- 调整适应因子
- 定期评估规则效果

### 4. 行为模式优化
- 设计有效的触发条件
- 提供多样化的响应模板
- 监控成功率
- 持续优化模式

### 5. 配置调优
- 根据应用场景调整适应阈值
- 平衡反馈权重和事件权重
- 优化学习率
- 监控适应效果

## 运行示例

```bash
# 运行演示程序
python demo_react_agent.py

# 运行测试
python test_react_agent.py
```

## 故障排除

### 1. 适应效果不佳
- 检查适应阈值设置
- 调整反馈权重和事件权重
- 增加更多相关规则和模式
- 优化学习率

### 2. 响应速度慢
- 减少环境事件和反馈数量
- 优化规则和模式数量
- 简化上下文分析逻辑
- 使用更高效的算法

### 3. 规则冲突
- 检查规则优先级设置
- 确保规则条件不冲突
- 使用规则类别隔离
- 定期清理无效规则

### 4. 内存占用过高
- 减少最大事件和反馈数量
- 定期清理历史记录
- 优化数据结构
- 使用更高效的存储方式

## 扩展开发

### 1. 添加新的反应类型
```python
from enum import Enum

class CustomReactionType(Enum):
    SUGGESTION = "suggestion"
    COMPLAINT = "complaint"
    PRAISE = "praise"
```

### 2. 自定义上下文分析
```python
class CustomReactAgent(ReactAgent):
    def analyze_context(self, current_message: str) -> Dict[str, Any]:
        # 自定义上下文分析逻辑
        context = super().analyze_context(current_message)
        # 添加自定义分析
        return context
```

### 3. 自定义适应算法
```python
class CustomReactAgent(ReactAgent):
    def adapt_behavior(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # 自定义适应算法
        adaptation = super().adapt_behavior(context)
        # 添加自定义适应逻辑
        return adaptation
```

## 总结

React Agent提供了一个完整的自适应智能助手解决方案，支持：

1. **智能环境感知**: 实时监控和响应环境变化
2. **用户反馈适应**: 根据用户反馈动态调整行为
3. **灵活规则系统**: 可配置的自适应规则
4. **行为模式匹配**: 智能匹配和应用行为模式
5. **深度上下文分析**: 全面的上下文理解
6. **动态参数调整**: 实时优化模型参数
7. **持续学习优化**: 不断改进和适应
8. **全面监控统计**: 详细的适应效果分析

通过合理配置和使用，React Agent能够提供智能、自适应和个性化的交互体验，满足各种复杂的应用场景需求。 