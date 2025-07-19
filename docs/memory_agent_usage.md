# 记忆Agent使用指南

## 概述

记忆Agent是一个支持长期记忆、短期对话、工具输出、规则和输出文本的智能Agent系统。它能够记住用户偏好、对话历史，并根据规则提供个性化的回答。

## 主要特性

- 🧠 **长期记忆管理**: 持久化存储重要信息
- 💬 **短期对话记忆**: 保持对话连贯性
- 🛠️ **工具调用集成**: 支持多种工具调用
- 📋 **规则系统**: 可配置的行为规则
- 📝 **输出文本生成**: 智能生成最终回答
- 🔍 **记忆检索**: 智能检索相关记忆
- ⚙️ **配置管理**: 灵活的配置选项

## 核心组件

### 1. 记忆项 (MemoryItem)

```python
from lightce.agent.memory_agent import MemoryItem

memory = MemoryItem(
    content="用户喜欢简洁明了的回答",
    importance=0.8,  # 重要性评分 (0.0-1.0)
    category="preference",  # 记忆类别
    metadata={"source": "conversation"}  # 元数据
)
```

### 2. 规则 (Rule)

```python
from lightce.agent.memory_agent import Rule

rule = Rule(
    name="礼貌回应",
    description="始终保持礼貌和友好的态度",
    content="在回答用户问题时，始终保持礼貌、友好和专业的语气。",
    priority=10,  # 优先级 (1-10)
    active=True
)
```

### 3. 记忆Agent配置 (MemoryAgentConfig)

```python
from lightce.agent.memory_agent import MemoryAgentConfig

config = MemoryAgentConfig(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
    max_short_term_memory=10,  # 短期记忆最大条数
    max_long_term_memory=1000,  # 长期记忆最大条数
    memory_importance_threshold=0.3,  # 记忆重要性阈值
    max_rules=50,  # 最大规则数量
    max_tool_outputs=20  # 最大工具输出数量
)
```

## 快速开始

### 1. 基本使用

```python
from lightce.agent.memory_agent import create_memory_agent
from lightce.tools.example_tools import EXAMPLE_TOOLS
from lightce.tools.example_rules import get_rules_by_category

# 创建记忆Agent
agent = create_memory_agent(
    tools=EXAMPLE_TOOLS,
    rules=get_rules_by_category("basic")
)

# 运行Agent
result = agent.run("请告诉我现在的时间")
print(result['response'])
```

### 2. 添加记忆

```python
# 添加用户偏好记忆
agent.add_memory(
    content="用户喜欢简洁明了的回答",
    importance=0.8,
    category="preference"
)

# 添加行为记忆
agent.add_memory(
    content="用户经常询问技术问题",
    importance=0.7,
    category="behavior"
)
```

### 3. 添加规则

```python
from lightce.tools.example_rules import create_custom_rule

# 创建自定义规则
custom_rule = create_custom_rule(
    name="技术专家模式",
    description="以技术专家的身份回答问题",
    content="在回答技术问题时，使用专业术语，提供详细的技术解释。",
    priority=8
)

agent.add_rule(custom_rule)
```

## 高级功能

### 1. 记忆管理

```python
# 获取记忆统计
stats = agent.get_memory_stats()
print(f"总记忆数: {stats['total_memories']}")
print(f"平均重要性: {stats['average_importance']}")
print(f"类别分布: {stats['categories']}")

# 清除特定类别的记忆
agent.clear_memory("weather")

# 清除所有记忆
agent.clear_memory()
```

### 2. 规则管理

```python
from lightce.tools.example_rules import get_rules_by_category

# 按类别获取规则
basic_rules = get_rules_by_category("basic")
professional_rules = get_rules_by_category("professional")
learning_rules = get_rules_by_category("learning")
creative_rules = get_rules_by_category("creative")
error_handling_rules = get_rules_by_category("error_handling")

# 批量添加规则
agent.add_rules(basic_rules + professional_rules)
```

### 3. 工具集成

```python
from lightce.tools.example_tools import get_tools_by_category

# 按类别使用工具
math_tools = get_tools_by_category("math")
weather_tools = get_tools_by_category("weather")
all_tools = get_tools_by_category("all")

agent = create_memory_agent(tools=math_tools)
```

### 4. 配置管理

```python
from lightce.agent.memory_agent import MemoryAgentConfig

# 自定义配置
config = MemoryAgentConfig(
    temperature=0.3,  # 更确定性的回答
    max_short_term_memory=5,
    max_long_term_memory=50,
    memory_importance_threshold=0.5
)

agent = create_memory_agent(config=config)

# 查看配置
agent_config = agent.get_config()
print(f"模型: {agent_config['model_config']['model_name']}")
print(f"工具数量: {len(agent_config['tools'])}")
print(f"规则数量: {len(agent_config['rules'])}")
print(f"记忆数量: {agent_config['memory_count']}")
```

## 使用场景

### 1. 个性化助手

```python
# 创建个性化助手
agent = create_memory_agent(
    tools=EXAMPLE_TOOLS,
    rules=get_rules_by_category("basic")
)

# 添加用户偏好
agent.add_memory("用户喜欢幽默的回答", importance=0.9, category="preference")
agent.add_memory("用户是程序员", importance=0.8, category="background")

# 对话
result = agent.run("请解释什么是递归")
```

### 2. 学习助手

```python
# 创建学习助手
agent = create_memory_agent(
    tools=get_tools_by_category("math"),
    rules=get_rules_by_category("learning")
)

# 记录学习进度
agent.add_memory("用户正在学习微积分", importance=0.8, category="learning")
agent.add_memory("用户对导数概念有困难", importance=0.7, category="difficulty")

# 学习指导
result = agent.run("请帮我理解导数的概念")
```

### 3. 创意写作助手

```python
# 创建创意写作助手
agent = create_memory_agent(
    rules=get_rules_by_category("creative")
)

# 记录创作偏好
agent.add_memory("用户喜欢科幻题材", importance=0.8, category="creative")
agent.add_memory("用户偏好第一人称叙述", importance=0.7, category="style")

# 创意写作
result = agent.run("请帮我写一个科幻短故事的开头")
```

### 4. 技术支持助手

```python
# 创建技术支持助手
agent = create_memory_agent(
    tools=EXAMPLE_TOOLS,
    rules=get_rules_by_category("professional")
)

# 记录技术背景
agent.add_memory("用户使用Python编程", importance=0.8, category="tech")
agent.add_memory("用户是初学者", importance=0.7, category="level")

# 技术支持
result = agent.run("我的Python代码出现了错误，请帮我检查")
```

## 规则类别

### 1. 基础规则 (basic)
- 礼貌回应
- 准确性优先
- 简洁明了
- 工具使用
- 记忆利用

### 2. 专业规则 (professional)
- 技术准确性
- 安全提醒
- 隐私保护

### 3. 学习规则 (learning)
- 引导思考
- 循序渐进
- 鼓励探索

### 4. 创意规则 (creative)
- 创意激发
- 风格适应
- 结构清晰

### 5. 错误处理规则 (error_handling)
- 错误承认
- 不确定性表达
- 建议替代方案

## 工具类别

### 1. 时间工具 (time)
- `get_current_time`: 获取当前时间

### 2. 数学工具 (math)
- `calculate`: 计算数学表达式

### 3. 天气工具 (weather)
- `get_weather`: 获取城市天气

### 4. 搜索工具 (search)
- `search_web`: 搜索网络信息

### 5. 翻译工具 (translate)
- `translate_text`: 翻译文本

### 6. 文件工具 (file)
- `file_operation`: 文件操作

### 7. 所有工具 (all)
- 包含所有可用工具

## 最佳实践

### 1. 记忆管理
- 为重要信息设置高重要性评分
- 使用有意义的类别标签
- 定期清理不重要的记忆
- 利用元数据存储额外信息

### 2. 规则配置
- 根据使用场景选择合适的规则类别
- 设置合理的规则优先级
- 定期检查和更新规则
- 避免规则冲突

### 3. 工具使用
- 按需加载工具，避免不必要的开销
- 组合使用多个工具完成复杂任务
- 监控工具调用的成功率

### 4. 配置优化
- 根据使用场景调整记忆容量
- 优化重要性阈值
- 平衡短期和长期记忆的比例

## 运行示例

```bash
# 运行演示程序
python demo_memory_agent.py

# 运行测试
python test_memory_agent.py
```

## 故障排除

### 1. 记忆溢出
- 增加 `max_long_term_memory` 配置
- 降低 `memory_importance_threshold`
- 定期清理不重要记忆

### 2. 规则冲突
- 检查规则优先级设置
- 确保规则内容不冲突
- 使用规则类别隔离不同场景

### 3. 工具调用失败
- 检查工具参数是否正确
- 确认工具依赖是否满足
- 查看错误日志获取详细信息

### 4. 性能问题
- 减少记忆和规则数量
- 优化重要性阈值
- 使用更高效的记忆检索算法

## 扩展开发

### 1. 添加新工具
```python
from langchain_core.tools import tool

@tool
def custom_tool(param: str) -> str:
    """自定义工具"""
    return f"处理结果: {param}"

agent.add_tool(custom_tool)
```

### 2. 添加新规则
```python
from lightce.tools.example_rules import create_custom_rule

rule = create_custom_rule(
    name="自定义规则",
    description="规则描述",
    content="规则内容",
    priority=5
)

agent.add_rule(rule)
```

### 3. 自定义记忆检索
```python
# 继承MemoryAgent类并重写get_relevant_memories方法
class CustomMemoryAgent(MemoryAgent):
    def get_relevant_memories(self, query: str, limit: int = 5):
        # 自定义检索逻辑
        pass
```

## 总结

记忆Agent提供了一个完整的智能助手解决方案，支持：

1. **智能记忆管理**: 长期和短期记忆的有机结合
2. **灵活规则系统**: 可配置的行为控制
3. **强大工具集成**: 丰富的功能扩展
4. **个性化体验**: 基于记忆的个性化回答
5. **易于扩展**: 模块化设计便于定制

通过合理配置和使用，记忆Agent能够提供智能、个性化和高效的交互体验。 