# LangGraph Agent 项目

这是一个使用LangGraph构建的智能助手项目，支持工具调用和对话功能。

## 功能特性

- 🤖 基于LangGraph的状态管理
- 🛠️ 内置多种工具（搜索、计算、天气查询）
- 💬 自然语言对话
- 🔄 多轮对话支持
- ⚙️ 可配置的模型参数

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

### 命令行运行

```bash
python main.py
```

### 作为模块使用

```python
from lightce import run_agent

# 运行agent
messages = run_agent("你好，请帮我计算 2 + 3 * 4")
print(messages)
```

## 项目结构

```
context-enigeneering-for-default-agent/
├── lightce/
│   ├── __init__.py          # 包初始化
│   ├── agent.py             # LangGraph agent核心
│   ├── config.py            # 配置文件
│   └── api/
│       └── ollama.py        # Ollama API集成
├── main.py                  # 主程序入口
├── requirements.txt         # 依赖列表
├── env_example.txt          # 环境变量示例
└── README.md               # 项目说明
```

## 支持的工具

1. **search_web**: 搜索网络信息
2. **calculate**: 计算数学表达式
3. **get_weather**: 获取天气信息

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
- **Pydantic**: 数据验证

## 开发说明

### 添加新工具

在 `lightce/agent.py` 中添加新的工具函数：

```python
@tool
def your_new_tool(param: str) -> str:
    """工具描述"""
    # 工具实现
    return "结果"
```

### 修改配置

在 `lightce/config.py` 中修改相关配置参数。

## 许可证

MIT License 