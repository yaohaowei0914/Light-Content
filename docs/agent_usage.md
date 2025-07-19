# 通用Agent使用指南

## 概述

这是一个基于LangGraph构建的通用Agent系统，支持工具调用和灵活的模型参数配置。

## 主要特性

- ✅ 基于LangGraph的工作流管理
- ✅ 支持多种模型提供商（OpenAI、Ollama）
- ✅ 灵活的参数配置（temperature、top_p、top_k、max_tokens）
- ✅ 工具调用支持
- ✅ 动态配置更新
- ✅ 错误处理和日志记录

## 快速开始

### 1. 环境设置

```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
cp env_example.txt .env
# 编辑.env文件，添加您的API密钥
```

### 2. 基本用法

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

### 3. 参数配置

```python
from lightce.agent.system import UniversalAgent, ModelConfig

# 使用ModelConfig进行详细配置
config = ModelConfig(
    model_name="gpt-3.5-turbo",
    temperature=0.1,      # 控制创造性（0.0-2.0）
    top_p=0.9,           # 核采样参数（0.0-1.0）
    top_k=20,            # Top-k采样（整数）
    max_tokens=1000,     # 最大输出token数
    provider="openai"    # 模型提供商
)

agent = UniversalAgent(config)
```

### 4. 动态配置更新

```python
# 运行时更新配置
agent.update_model_config(
    temperature=1.2,
    max_tokens=2000
)
```

## 工具使用

### 预定义工具

系统提供了以下示例工具：

- **时间工具**: `get_current_time()` - 获取当前时间
- **数学工具**: `calculate(expression)` - 计算数学表达式
- **天气工具**: `get_weather(city)` - 获取城市天气
- **搜索工具**: `search_web(query)` - 搜索网络信息
- **翻译工具**: `translate_text(text, target_language)` - 翻译文本
- **文件工具**: `file_operation(operation, filename, content)` - 文件操作

### 按类别使用工具

```python
from lightce.tools.example_tools import get_tools_by_category

# 只使用数学工具
math_tools = get_tools_by_category("math")
agent = create_agent(tools=math_tools)

# 使用所有工具
all_tools = get_tools_by_category("all")
agent = create_agent(tools=all_tools)
```

### 自定义工具

```python
from langchain_core.tools import tool

@tool
def my_custom_tool(param: str) -> str:
    """自定义工具描述"""
    return f"处理结果: {param}"

# 添加到agent
agent.add_tool(my_custom_tool)
```

## 模型提供商

### OpenAI

```python
agent = create_agent(
    model_name="gpt-3.5-turbo",
    provider="openai",
    temperature=0.7
)
```

### Ollama

```python
agent = create_agent(
    model_name="llama2",
    provider="ollama",
    temperature=0.7
)
```

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model_name` | str | "gpt-3.5-turbo" | 模型名称 |
| `temperature` | float | 0.7 | 温度参数，控制随机性 |
| `top_p` | float | 1.0 | Top-p采样参数 |
| `top_k` | int | 40 | Top-k采样参数 |
| `max_tokens` | int | 1000 | 最大输出token数 |
| `provider` | str | "openai" | 模型提供商 |

## 运行演示

```bash
python demo_agent.py
```

演示程序包含以下功能：
- 基本用法演示
- 参数配置演示
- 动态配置更新
- 工具类别演示
- 复杂交互演示
- 错误处理演示
- Ollama集成演示

## 错误处理

系统提供了完善的错误处理机制：

```python
result = agent.run("用户输入")

if result['success']:
    print(f"成功: {result['response']}")
else:
    print(f"错误: {result['error']}")
```

## 高级用法

### 状态管理

```python
# 获取当前配置
config = agent.get_config()
print(f"模型配置: {config['model_config']}")
print(f"可用工具: {config['tools']}")
```

### 批量工具添加

```python
from lightce.tools.example_tools import EXAMPLE_TOOLS

agent = UniversalAgent()
agent.add_tools(EXAMPLE_TOOLS)
```

### 自定义工作流

```python
# 可以继承UniversalAgent类来自定义工作流
class CustomAgent(UniversalAgent):
    def _build_graph(self):
        # 自定义图结构
        pass
```

## 注意事项

1. **API密钥**: 确保正确设置环境变量中的API密钥
2. **网络连接**: 使用OpenAI时需要稳定的网络连接
3. **Ollama**: 使用Ollama时需要本地安装并运行Ollama服务
4. **工具安全**: 自定义工具时注意安全性，避免执行危险操作
5. **Token限制**: 注意模型的token限制，避免超出限制

## 故障排除

### 常见问题

1. **API密钥错误**
   - 检查.env文件中的API密钥是否正确
   - 确认API密钥有足够的配额

2. **网络连接问题**
   - 检查网络连接
   - 确认防火墙设置

3. **工具调用失败**
   - 检查工具参数是否正确
   - 确认工具函数没有异常

4. **模型不可用**
   - 检查模型名称是否正确
   - 确认模型提供商服务正常

### 日志调试

系统提供了详细的日志记录：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 扩展开发

### 添加新工具

1. 使用`@tool`装饰器定义工具函数
2. 添加工具到agent：`agent.add_tool(your_tool)`

### 添加新模型提供商

1. 在`_create_llm`方法中添加新的提供商支持
2. 更新`ModelConfig`中的provider选项

### 自定义状态管理

1. 继承`AgentState`类
2. 重写相关方法以支持自定义状态 