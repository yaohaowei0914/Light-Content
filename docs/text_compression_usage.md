# 文本压缩提示词使用指南

## 概述

文本压缩提示词系统是一个分为四个阶段的智能文本压缩解决方案，支持六种不同类型的文本压缩，能够根据文本内容自动识别压缩类型，并提供专业的压缩提示词。

## 四个压缩阶段

### 1. 预处理阶段 (PREPROCESS)
- **功能**: 分析文本类型、结构和关键信息
- **任务**: 
  - 识别文本类型和主题
  - 分析文本结构和逻辑关系
  - 识别关键信息和冗余内容
  - 评估文本的复杂度和重要性
  - 确定压缩目标和保留重点

### 2. 压缩阶段 (COMPRESS)
- **功能**: 根据预处理结果进行文本压缩
- **任务**:
  - 保持核心信息和主要观点
  - 删除冗余和重复内容
  - 简化复杂表达
  - 保持逻辑连贯性
  - 确保压缩后的文本清晰易懂

### 3. 优化阶段 (OPTIMIZE)
- **功能**: 对压缩结果进行质量优化
- **任务**:
  - 检查信息完整性
  - 优化语言表达
  - 确保逻辑连贯性
  - 提高可读性
  - 验证压缩效果

### 4. 后处理阶段 (POSTPROCESS)
- **功能**: 最终质量检查和报告生成
- **任务**:
  - 最终质量检查
  - 格式标准化
  - 压缩效果评估
  - 使用建议提供
  - 质量报告生成

## 六种压缩类型

### 1. 通用压缩 (GENERAL)
- **适用场景**: 各种类型的文本
- **特点**: 通用性强，适合各种文本类型
- **关键词**: 通用文本、一般文档

### 2. 技术文档压缩 (TECHNICAL)
- **适用场景**: 技术文档、代码文档、技术说明
- **特点**: 注重技术准确性和专业性
- **关键词**: 技术、代码、编程、算法、系统、架构、API、函数、类、变量、数据库、服务器

### 3. 学术文本压缩 (ACADEMIC)
- **适用场景**: 学术论文、研究报告、学术文档
- **特点**: 强调学术严谨性和逻辑性
- **关键词**: 研究、论文、学术、理论、分析、数据、实验、方法、结论、参考文献

### 4. 新闻文本压缩 (NEWS)
- **适用场景**: 新闻报道、新闻稿、时事新闻
- **特点**: 关注新闻要素和时效性
- **关键词**: 新闻、报道、消息、事件、发生、时间、地点、人物、采访、记者

### 5. 创意文本压缩 (CREATIVE)
- **适用场景**: 文学作品、创意写作、艺术文本
- **特点**: 重视创意元素和艺术性
- **关键词**: 故事、小说、诗歌、散文、创意、想象、艺术、美、情感、意境

### 6. 对话文本压缩 (CONVERSATION)
- **适用场景**: 对话记录、聊天记录、访谈记录
- **特点**: 注重对话自然性和连贯性
- **关键词**: 说、问、答、对话、交流、聊天、讨论、请问、回答、你好

## 快速开始

### 1. 基本使用

```python
from lightce.prompt.mini_contents import (
    CompressionStage, CompressionType, get_compression_prompt,
    get_compression_type_from_text
)

# 示例文本
text = "Python是一种高级编程语言，具有简洁的语法和强大的功能。"

# 自动识别压缩类型
compression_type = get_compression_type_from_text(text)
print(f"识别类型: {compression_type.value}")

# 获取预处理提示词
preprocess_prompt = get_compression_prompt(
    CompressionStage.PREPROCESS,
    compression_type,
    text=text
)
print(f"预处理提示词: {preprocess_prompt}")
```

### 2. 获取所有阶段提示词

```python
from lightce.prompt.mini_contents import get_all_compression_prompts

# 获取所有阶段的提示词
all_prompts = get_all_compression_prompts(
    CompressionType.TECHNICAL,
    text=text,
    compression_ratio=50.0,
    preprocess_result="预处理结果",
    compressed_text="压缩后文本"
)

for stage, prompt in all_prompts.items():
    print(f"{stage} 阶段提示词长度: {len(prompt)} 字符")
```

### 3. 创建完整工作流

```python
from lightce.prompt.mini_contents import create_compression_workflow

# 创建完整压缩工作流
workflow = create_compression_workflow(text, target_ratio=50.0)

print(f"压缩类型: {workflow['compression_type']}")
print(f"目标压缩比例: {workflow['target_ratio']}%")
print(f"原始文本长度: {workflow['original_length']} 字符")

# 查看工作流阶段
for stage_key, stage_desc in workflow['workflow'].items():
    print(f"- {stage_desc}")

# 查看各阶段提示词
for stage_name, prompt in workflow['prompts'].items():
    print(f"\n{stage_name.upper()} 阶段提示词:")
    print(f"长度: {len(prompt)} 字符")
    print(f"预览: {prompt[:100]}...")
```

## 高级功能

### 1. 压缩比例计算

```python
from lightce.prompt.mini_contents import calculate_compression_ratio

original_length = 1000
compressed_length = 600
ratio = calculate_compression_ratio(original_length, compressed_length)
print(f"压缩比例: {ratio:.1f}%")
```

### 2. 信息保留率估算

```python
from lightce.prompt.mini_contents import calculate_information_retention

original_text = "这是一个完整的文本内容"
compressed_text = "这是文本内容"
retention = calculate_information_retention(original_text, compressed_text)
print(f"信息保留率: {retention:.1f}%")
```

### 3. 自定义压缩类型

```python
# 手动指定压缩类型
compression_type = CompressionType.ACADEMIC

# 获取学术文本的压缩提示词
prompt = get_compression_prompt(
    CompressionStage.COMPRESS,
    compression_type,
    text=text,
    preprocess_result="学术文本预处理结果",
    compression_ratio=40.0
)
```

## 使用场景示例

### 1. 技术文档压缩

```python
technical_text = """
Python是一种高级编程语言，具有简洁的语法和强大的功能。它支持面向对象编程、函数式编程和过程式编程等多种编程范式。
Python的主要特点包括：动态类型、自动内存管理、丰富的标准库和第三方库生态系统。Python广泛应用于Web开发、数据科学、人工智能、机器学习、自动化测试等领域。
"""

# 创建技术文档压缩工作流
workflow = create_compression_workflow(technical_text, target_ratio=60.0)
print(f"技术文档压缩类型: {workflow['compression_type']}")
```

### 2. 学术论文压缩

```python
academic_text = """
本研究旨在探讨人工智能技术在自然语言处理领域的应用及其对文本理解能力的影响。通过对比分析传统的基于规则的方法和现代的深度学习方法，我们发现深度学习模型在文本分类、情感分析、机器翻译等任务上表现出了显著的优势。
"""

# 获取学术文本的预处理提示词
preprocess_prompt = get_compression_prompt(
    CompressionStage.PREPROCESS,
    CompressionType.ACADEMIC,
    text=academic_text
)
```

### 3. 新闻文本压缩

```python
news_text = """
据新华社报道，2024年1月15日，在北京举行的全国科技创新大会上，科技部部长王志刚宣布了多项重要科技政策。会议指出，我国将继续加大科技投入，推动关键核心技术攻关，加快建设科技强国。
"""

# 自动识别为新闻类型
detected_type = get_compression_type_from_text(news_text)
print(f"自动识别类型: {detected_type.value}")
```

### 4. 创意文本压缩

```python
creative_text = """
春天的午后，阳光透过树叶的缝隙洒在青石板路上，形成斑驳的光影。微风轻拂，带来阵阵花香，让人心旷神怡。远处的山峦在薄雾中若隐若现，如同水墨画中的意境。
"""

# 获取创意文本的优化提示词
optimize_prompt = get_compression_prompt(
    CompressionStage.OPTIMIZE,
    CompressionType.CREATIVE,
    compressed_text=creative_text[:100],
    original_length=len(creative_text),
    compressed_length=100,
    actual_ratio=50.0
)
```

## 最佳实践

### 1. 选择合适的压缩类型
- 根据文本内容自动识别压缩类型
- 对于特殊需求，可以手动指定压缩类型
- 考虑文本的专业领域和用途

### 2. 设置合理的压缩比例
- 一般文本：30-50%
- 技术文档：40-60%
- 学术文本：50-70%
- 新闻文本：30-50%
- 创意文本：20-40%
- 对话文本：40-60%

### 3. 按阶段顺序处理
1. 先进行预处理分析
2. 根据分析结果进行压缩
3. 对压缩结果进行优化
4. 最后进行后处理和质量检查

### 4. 注意信息保留
- 保持核心信息和主要观点
- 确保逻辑连贯性
- 维持文本的可读性
- 根据文本类型保持相应的专业性

### 5. 质量评估
- 计算压缩比例
- 估算信息保留率
- 检查文本质量
- 获取使用建议

## 运行示例

```bash
# 运行演示程序
python demo_text_compression.py

# 运行测试
python test_text_compression.py
```

## 故障排除

### 1. 参数缺失错误
- 确保提供所有必需的参数
- 检查参数名称是否正确
- 使用 `create_compression_workflow` 函数自动处理参数

### 2. 文本类型识别不准确
- 检查文本内容是否包含相关关键词
- 可以手动指定压缩类型
- 调整关键词匹配规则

### 3. 压缩效果不理想
- 调整压缩比例
- 检查文本类型是否合适
- 优化提示词参数

### 4. 性能问题
- 减少文本长度
- 简化提示词内容
- 使用缓存机制

## 总结

文本压缩提示词系统提供了：

1. **四个阶段**: 预处理、压缩、优化、后处理
2. **六种类型**: 通用、技术、学术、新闻、创意、对话
3. **自动识别**: 根据文本内容自动判断压缩类型
4. **灵活定制**: 支持不同阶段和类型的提示词定制
5. **完整工作流**: 提供端到端的压缩解决方案
6. **质量评估**: 包含压缩比例和信息保留率计算

通过合理使用这个系统，可以实现高质量的文本压缩，满足各种应用场景的需求。 