# 压缩Agent使用指南

## 概述

压缩Agent是一个基于UniversalAgent系统和mini_contents提示词的智能文本压缩工具。它提供了分阶段的文本压缩处理，支持多种文本类型，并具有自动类型检测和质量评估功能。

## 主要特性

### 1. 分阶段处理
- **预处理阶段**: 分析文本类型、结构和关键信息
- **压缩阶段**: 根据预处理结果进行智能压缩
- **优化阶段**: 对压缩结果进行质量优化
- **后处理阶段**: 最终质量检查和报告生成

### 2. 多文本类型支持
- **通用压缩**: 适用于一般文本
- **技术文档**: 专门处理技术、编程相关内容
- **学术文本**: 处理研究论文、学术报告
- **新闻文本**: 处理新闻报道、时事内容
- **创意文本**: 处理文学、艺术创作
- **对话文本**: 处理对话、交流内容

### 3. 智能功能
- **自动类型检测**: 根据文本内容自动判断压缩类型
- **质量评估**: 提供压缩质量和信息保留率评估
- **批量处理**: 支持多个文本的批量压缩
- **历史记录**: 保存压缩历史，提供统计分析

## 快速开始

### 基本使用

```python
from lightce import create_compression_agent

# 创建压缩Agent
agent = create_compression_agent()

# 压缩文本
text = "这是一个需要压缩的长文本，包含了很多冗余信息..."
result = agent.compress_text(text, compression_ratio=50.0)

print(f"压缩比例: {result.compression_ratio:.2f}%")
print(f"信息保留率: {result.information_retention:.2f}%")
print(f"压缩后文本: {result.compressed_text}")
```

### 使用LangChain工具

```python
from lightce import compress_text_with_agent, analyze_text_compression_potential
import json

# 分析文本压缩潜力
analysis = analyze_text_compression_potential("要分析的文本")
analysis_dict = json.loads(analysis)
print(f"检测类型: {analysis_dict['detected_type']}")
print(f"推荐压缩比例: {analysis_dict['recommended_ratio']}%")

# 执行压缩
result = compress_text_with_agent("要压缩的文本", compression_ratio=50.0, compression_type="auto")
result_dict = json.loads(result)
print(f"压缩后文本: {result_dict['compressed_text']}")
```

## 高级配置

### 自定义配置

```python
from lightce import CompressionAgentConfig, create_compression_agent

# 创建自定义配置
config = CompressionAgentConfig(
    model_name="gpt-4",
    temperature=0.1,
    max_tokens=3000,
    default_compression_ratio=70.0,
    enable_auto_type_detection=True,
    enable_quality_check=True,
    enable_stage_processing=True
)

# 使用自定义配置创建Agent
agent = create_compression_agent()
agent.config = config
```

### 分阶段处理

```python
# 启用分阶段处理
agent = create_compression_agent(enable_stage_processing=True)

result = agent.compress_text("测试文本", compression_ratio=50.0)

# 查看各阶段结果
for stage_name, stage_data in result.processing_stages.items():
    print(f"{stage_name}: {len(stage_data['result'])} 字符")
```

### 指定压缩类型

```python
from lightce.prompt.mini_contents import CompressionType

# 指定技术文档压缩
result = agent.compress_text(
    "技术文档内容...", 
    compression_ratio=50.0,
    compression_type=CompressionType.TECHNICAL
)

# 指定学术文本压缩
result = agent.compress_text(
    "学术论文内容...", 
    compression_ratio=40.0,
    compression_type=CompressionType.ACADEMIC
)
```

## 批量处理

```python
# 批量压缩多个文本
texts = [
    "第一个文本内容...",
    "第二个文本内容...",
    "第三个文本内容..."
]

results = agent.batch_compress(texts, compression_ratio=50.0)

for i, result in enumerate(results):
    print(f"文本 {i+1}:")
    print(f"- 压缩比例: {result.compression_ratio:.2f}%")
    print(f"- 压缩后: {result.compressed_text}")
```

## 统计分析

```python
# 获取压缩统计信息
stats = agent.get_compression_stats()

print(f"总压缩次数: {stats['total_compressions']}")
print(f"成功率: {stats['success_rate']:.2f}%")
print(f"平均压缩比例: {stats['average_compression_ratio']:.2f}%")
print(f"平均信息保留率: {stats['average_information_retention']:.2f}%")
print(f"类型分布: {stats['compression_type_distribution']}")

# 清空历史记录
agent.clear_history()
```

## 质量报告

压缩结果包含详细的质量报告：

```python
result = agent.compress_text("测试文本")

# 查看质量报告
quality_report = result.quality_report
print(f"压缩比例: {quality_report['compression_ratio']:.2f}%")
print(f"信息保留率: {quality_report['information_retention']:.2f}%")
print(f"原始长度: {quality_report['original_length']} 字符")
print(f"压缩后长度: {quality_report['compressed_length']} 字符")
print(f"长度减少: {quality_report['length_reduction']} 字符")
```

## 配置参数说明

### CompressionAgentConfig

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| model_name | str | "gpt-3.5-turbo" | 使用的模型名称 |
| temperature | float | 0.3 | 模型温度参数 |
| max_tokens | int | 2000 | 最大输出token数 |
| provider | str | "openai" | 模型提供商 |
| default_compression_ratio | float | 50.0 | 默认压缩比例 |
| enable_auto_type_detection | bool | True | 启用自动类型检测 |
| enable_quality_check | bool | True | 启用质量检查 |
| enable_stage_processing | bool | True | 启用分阶段处理 |

### 压缩类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| general | 通用压缩 | 一般文本内容 |
| technical | 技术文档 | 编程、技术相关内容 |
| academic | 学术文本 | 研究论文、学术报告 |
| news | 新闻文本 | 新闻报道、时事内容 |
| creative | 创意文本 | 文学、艺术创作 |
| conversation | 对话文本 | 对话、交流内容 |

## 最佳实践

### 1. 选择合适的压缩比例
- **高压缩比例（60-80%）**: 适用于摘要、要点提取
- **中等压缩比例（40-60%）**: 适用于一般压缩需求
- **低压缩比例（20-40%）**: 适用于精细压缩，保留更多细节

### 2. 启用自动类型检测
```python
# 推荐：启用自动类型检测
agent = create_compression_agent(enable_auto_type_detection=True)
```

### 3. 使用分阶段处理
```python
# 推荐：启用分阶段处理以获得更好的质量
agent = create_compression_agent(enable_stage_processing=True)
```

### 4. 批量处理优化
```python
# 对于大量文本，使用批量处理
results = agent.batch_compress(texts, compression_ratio=50.0)
```

## 错误处理

### 常见错误及解决方案

1. **API密钥错误**
   ```python
   # 确保设置了正确的API密钥
   import os
   os.environ["OPENAI_API_KEY"] = "your_api_key_here"
   ```

2. **网络连接问题**
   ```python
   # 添加重试机制
   try:
       result = agent.compress_text(text)
   except Exception as e:
       print(f"压缩失败: {e}")
   ```

3. **文本过长**
   ```python
   # 对于超长文本，考虑分段处理
   if len(text) > 4000:
       # 分段处理
       segments = [text[i:i+4000] for i in range(0, len(text), 4000)]
       results = agent.batch_compress(segments)
   ```

## 性能优化

### 1. 模型选择
```python
# 对于快速处理，使用较小的模型
agent = create_compression_agent(model_name="gpt-3.5-turbo")

# 对于高质量处理，使用较大的模型
agent = create_compression_agent(model_name="gpt-4")
```

### 2. 批量处理
```python
# 批量处理比单个处理更高效
results = agent.batch_compress(texts)
```

### 3. 缓存结果
```python
# 保存压缩结果以避免重复处理
import pickle

# 保存结果
with open('compression_results.pkl', 'wb') as f:
    pickle.dump(results, f)

# 加载结果
with open('compression_results.pkl', 'rb') as f:
    results = pickle.load(f)
```

## 示例应用

### 1. 文档摘要生成
```python
def generate_summary(document_text, summary_ratio=70.0):
    agent = create_compression_agent()
    result = agent.compress_text(document_text, compression_ratio=summary_ratio)
    return result.compressed_text
```

### 2. 技术文档简化
```python
def simplify_tech_doc(tech_text):
    agent = create_compression_agent()
    result = agent.compress_text(
        tech_text, 
        compression_ratio=50.0,
        compression_type=CompressionType.TECHNICAL
    )
    return result.compressed_text
```

### 3. 新闻摘要
```python
def create_news_summary(news_text):
    agent = create_compression_agent()
    result = agent.compress_text(
        news_text,
        compression_ratio=60.0,
        compression_type=CompressionType.NEWS
    )
    return result.compressed_text
```

## 总结

压缩Agent提供了一个强大而灵活的文本压缩解决方案，结合了UniversalAgent的智能处理能力和mini_contents的专门化提示词系统。通过合理配置和使用，可以实现高质量的文本压缩效果。 