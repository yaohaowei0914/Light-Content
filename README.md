# LangGraph Agent 项目

这是一个使用LangGraph构建的智能助手项目，支持工具调用和对话功能。

## 功能特性

- 🤖 基于LangGraph的状态管理
- 🛠️ 内置多种工具（搜索、计算、天气查询）
- 💬 自然语言对话
- 🔄 多轮对话支持
- ⚙️ 可配置的模型参数
- 🚀 **新增：通用Agent系统** - 支持多种模型提供商和灵活参数配置

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

1. 复制环境变量示例文件：
```bash
cp env_example.txt .env
```

2. 编辑 `.env` 文件，设置您的OpenAI API密钥：
```
OPENAI_API_KEY=your_openai_api_key_here
```

## 使用方法

### 1. 原有Agent系统

#### 命令行运行

```bash
python main.py
```

#### 作为模块使用

```python
from lightce import run_agent

# 运行agent
messages = run_agent("你好，请帮我计算 2 + 3 * 4")
print(messages)
```

### 2. 新的通用Agent系统

#### 基本使用

```python
from lightce.agent.system import create_agent
from lightce.tools.example_tools import EXAMPLE_TOOLS

# 创建agent
agent = create_agent(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
    tools=EXAMPLE_TOOLS
)

# 运行agent
result = agent.run("请告诉我现在的时间")
print(result['response'])
```

### 3. 记忆Agent系统

#### 基本使用

```python
from lightce.agent.memory_agent import create_memory_agent
from lightce.tools.example_tools import EXAMPLE_TOOLS
from lightce.tools.example_rules import get_rules_by_category

# 创建记忆Agent
agent = create_memory_agent(
    tools=EXAMPLE_TOOLS,
    rules=get_rules_by_category("basic")
)

# 添加记忆
agent.add_memory("用户喜欢简洁明了的回答", importance=0.8, category="preference")

# 运行Agent
result = agent.run("请告诉我现在的时间")
print(result['response'])
print(f"使用的记忆: {result['memories_used']}")
print(f"应用的规则: {result['rules_applied']}")
```

### 4. React Agent系统

#### 基本使用

```python
from lightce.agent.react_agent import create_react_agent, ReactionType
from lightce.tools.example_tools import EXAMPLE_TOOLS
from lightce.tools.example_adaptive_rules import get_adaptive_rules_by_category, get_behavior_patterns_by_category

# 创建React Agent
agent = create_react_agent(
    tools=EXAMPLE_TOOLS,
    adaptive_rules=get_adaptive_rules_by_category("all"),
    behavior_patterns=get_behavior_patterns_by_category("all")
)

# 添加环境事件
agent.add_environment_event("系统错误", "数据库连接失败", severity=0.8)

# 添加用户反馈
agent.add_user_feedback(ReactionType.NEGATIVE, "回答不够详细", confidence=0.9)

# 运行Agent
result = agent.run("请帮我解决这个问题")
print(result['response'])
print(f"适应水平: {result['adaptation_level']:.2f}")
print(f"应用的反应: {result['reaction_applied']}")
```

#### 参数配置

```python
from lightce.agent.system import UniversalAgent, ModelConfig

# 详细配置
config = ModelConfig(
    model_name="gpt-3.5-turbo",
    temperature=0.1,      # 控制创造性
    top_p=0.9,           # 核采样参数
    top_k=20,            # Top-k采样
    max_tokens=1000,     # 最大输出token数
    provider="openai"    # 模型提供商
)

agent = UniversalAgent(config)
```

#### 动态配置更新

```python
# 运行时更新配置
agent.update_model_config(temperature=1.2, max_tokens=2000)
```

#### 工具管理

```python
from lightce.tools.example_tools import get_tools_by_category

# 按类别使用工具
math_tools = get_tools_by_category("math")
weather_tools = get_tools_by_category("weather")
all_tools = get_tools_by_category("all")
```

#### 运行示例

```bash
# 运行演示程序
python demo_agent.py

# 运行记忆Agent演示
python demo_memory_agent.py

# 运行React Agent演示
python demo_react_agent.py

# 运行使用示例
python example_usage.py

# 运行配置示例
python config_example.py

# 运行测试
python simple_test.py
python test_memory_agent.py
python test_react_agent.py
```

## 项目结构

```
context-enigeneering-for-default-agent/
├── lightce/
│   ├── __init__.py          # 包初始化
│   ├── agent.py             # 原有LangGraph agent核心
│   ├── agent/
│   │   ├── __init__.py      # Agent包初始化
│   │   ├── system.py        # 新的通用Agent系统
│   │   └── output.py        # 输出处理
│   ├── config.py            # 配置文件
│   ├── api/
│   │   └── ollama.py        # Ollama API集成
│   └── tools/
│       ├── __init__.py      # 工具包初始化
│       ├── example_tools.py # 示例工具集合
│       └── ...              # 其他工具
├── main.py                  # 主程序入口
├── demo_agent.py            # 通用Agent演示程序
├── demo_memory_agent.py     # 记忆Agent演示程序
├── demo_react_agent.py      # React Agent演示程序
├── example_usage.py         # 使用示例
├── config_example.py        # 配置管理示例
├── simple_test.py           # 简单测试
├── test_agent_system.py     # 完整测试
├── test_memory_agent.py     # 记忆Agent测试
├── test_react_agent.py      # React Agent测试
├── requirements.txt         # 依赖列表
├── env_example.txt          # 环境变量示例
├── docs/
│   ├── agent_usage.md       # 通用Agent使用指南
│   ├── memory_agent_usage.md # 记忆Agent使用指南
│   ├── react_agent_usage.md # React Agent使用指南
│   ├── config_migration.md  # 配置迁移说明
│   └── summary.md           # 项目总结
└── README.md               # 项目说明
```

## 支持的工具

### 原有工具
1. **search_web**: 搜索网络信息
2. **calculate**: 计算数学表达式
3. **get_weather**: 获取天气信息

### 新的示例工具
1. **get_current_time**: 获取当前时间
2. **calculate**: 计算数学表达式
3. **get_weather**: 获取城市天气信息
4. **search_web**: 搜索网络信息
5. **translate_text**: 翻译文本
6. **file_operation**: 文件操作（模拟）

### 工具分类
- **time**: 时间相关工具
- **math**: 数学计算工具
- **weather**: 天气查询工具
- **search**: 搜索工具
- **translate**: 翻译工具
- **file**: 文件操作工具
- **all**: 所有工具

### 规则系统
- **basic**: 基础行为规则（礼貌、准确性、简洁等）
- **professional**: 专业领域规则（技术准确性、安全提醒等）
- **learning**: 学习辅助规则（引导思考、循序渐进等）
- **creative**: 创意写作规则（创意激发、风格适应等）
- **error_handling**: 错误处理规则（错误承认、不确定性表达等）

### 自适应规则系统
- **error_correction**: 错误纠正规则（降低创造性，提高准确性）
- **user_satisfaction**: 用户满意度规则（保持当前行为模式）
- **technical**: 技术问题规则（使用专业术语）
- **emergency**: 紧急情况规则（采用谨慎态度）
- **learning**: 学习模式规则（引导思考）
- **creative**: 创意模式规则（提高创造性）
- **simplification**: 简化回答规则（使用简洁语言）
- **detailed**: 详细解释规则（提供全面解释）

### 行为模式系统
- **technical_support**: 技术支持模式（处理技术问题）
- **learning_guidance**: 学习指导模式（学习指导）
- **creative_inspiration**: 创意激发模式（创意激发）
- **problem_solving**: 问题解决模式（问题解决）
- **emotional_support**: 情感支持模式（情感支持）
- **information_query**: 信息查询模式（信息查询）

## 示例对话

```
您: 请帮我计算 15 * 8 + 20
智能助手: 让我为您计算这个表达式。
[工具调用]:
  - 工具: calculate
    参数: {'expression': '15 * 8 + 20'}

计算结果: 15 * 8 + 20 = 140
```

## 技术栈

- **LangGraph**: 图状态管理
- **LangChain**: LLM集成和工具管理
- **OpenAI**: 语言模型
- **Ollama**: 本地语言模型
- **Pydantic**: 数据验证
- **Python-dotenv**: 环境变量管理

## 开发说明

### 添加新工具

#### 原有系统
在 `lightce/agent.py` 中添加新的工具函数：

```python
@tool
def your_new_tool(param: str) -> str:
    """工具描述"""
    # 工具实现
    return "结果"
```

#### 新系统
在 `lightce/tools/example_tools.py` 中添加新的工具函数：

```python
@tool
def your_new_tool(param: str) -> str:
    """工具描述"""
    # 工具实现
    return "结果"
```

然后添加到相应的工具类别中。

### 修改配置

#### 集中配置管理
所有默认参数都在 `lightce/config.py` 中集中管理：

```python
# 默认模型参数
DEFAULT_MODEL_NAME = "gpt-3.5-turbo"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 1.0
DEFAULT_TOP_K = 40
DEFAULT_MAX_TOKENS = 1000
DEFAULT_PROVIDER = "openai"

# 参数范围限制
TEMPERATURE_MIN = 0.0
TEMPERATURE_MAX = 2.0
TOP_P_MIN = 0.0
TOP_P_MAX = 1.0
TOP_K_MIN = 1
MAX_TOKENS_MIN = 1

# 支持的提供商
SUPPORTED_PROVIDERS = ["openai", "ollama"]

# 工具类别
DEFAULT_TOOL_CATEGORIES = ["time", "math", "weather", "search", "translate", "file", "all"]
```

#### 配置验证
系统会自动验证配置参数的有效性，确保参数在合理范围内。

#### 环境变量覆盖
可以通过环境变量覆盖某些配置：

```bash
export OPENAI_API_KEY="your_api_key"
export OPENAI_MODEL="gpt-4"
```

### 自定义Agent

```python
from lightce.agent.system import UniversalAgent

class CustomAgent(UniversalAgent):
    def _build_graph(self):
        # 自定义图结构
        pass
```

## 许可证

MIT License 