# 标准语义等价性判断prompt
SEMANTIC_EQUIVALENCE_PROMPT = """
你是一个专业的语义分析专家。请仔细分析以下两段文本，判断它们在语义上是否表达相同的内容。

文本A：
{text1}

文本B：
{text2}

请按照以下标准进行判断：

1. **核心含义**：两段文本是否表达相同的核心观点、事实或信息
2. **关键信息**：是否包含相同的关键信息点
3. **逻辑关系**：是否具有相同的逻辑结构和因果关系
4. **表达方式**：即使用词不同，但语义是否相同

判断标准：
- 如果两段文本在语义上表达相同的内容，返回 "相同"
- 如果两段文本在语义上表达不同的内容，返回 "不同"
- 如果部分内容相同但存在重要差异，返回 "部分相同"

请只返回判断结果（"相同"、"不同"或"部分相同"），不要添加其他解释。
"""

# 详细语义分析prompt
DETAILED_SEMANTIC_ANALYSIS_PROMPT = """
你是一个专业的语义分析专家。请对以下两段文本进行详细的语义对比分析。

文本A：
{text1}

文本B：
{text2}

请从以下维度进行分析：

1. **核心主题对比**：
   - 两段文本的核心主题是否一致
   - 主要讨论的问题是否相同

2. **关键信息对比**：
   - 重要事实、数据、观点是否一致
   - 是否有遗漏或额外的关键信息

3. **逻辑结构对比**：
   - 论证逻辑是否相同
   - 因果关系是否一致

4. **表达方式对比**：
   - 用词选择的差异
   - 句式结构的差异
   - 但语义表达是否相同

5. **细节差异分析**：
   - 具体细节的差异
   - 这些差异是否影响核心语义

请提供：
1. 总体判断：相同/不同/部分相同
2. 详细分析理由
3. 主要差异点（如果有）
4. 相似度评分（0-100分）

请用中文回答，格式清晰易读。
"""

# 简化语义等价性判断prompt
SIMPLE_EQUIVALENCE_PROMPT = """
请判断以下两段文本是否表达相同的意思：

文本1：{text1}

文本2：{text2}

回答格式：
- 如果意思相同，回答：相同
- 如果意思不同，回答：不同
- 如果部分相同，回答：部分相同

只回答判断结果，不要解释。
"""
