
衡量了以下两者之间的权衡：
- 压缩（您组织信息的效率）
- 含义保留（您保留了多少语义细节）


二、语义压缩的实现方法
（一）利用数据重复性

Bazaarvoice 发现许多产品评论存在内容重复的情况，这为解决问题提供了思路。通过识别表达相同意思的文本段，减少发送给 LLM 的文本量，既能避免超出上下文窗口限制，又能降低系统运营成本。

（二）多步骤处理流程

句子分割
首先将产品评论分割成单个句子，为后续处理奠定基础。
向量嵌入计算
使用在语义文本相似性（STS）基准测试中表现良好的网络，为每个句子计算嵌入向量。这一步骤的关键在于选择合适的嵌入模型，确保能够准确捕捉句子的语义信息。
层次聚类
对每个产品的所有嵌入向量进行凝聚式聚类。在聚类过程中，面临如何确保语义相似性的挑战。Bazaarvoice 通过对 STS 基准数据集的分析，计算训练数据集中所有句子对的距离，并拟合多项式来确定距离阈值，从而实现根据语义相似性目标选择合适的聚类阈值。例如，选择语义相似性分数为 3.5 的阈值，保证大多数聚类中的句子具有较高的语义等价性。
代表性句子选择
从每个聚类中保留最接近聚类质心的句子作为代表发送给 LLM，同时丢弃其他句子。对于小聚类，将其视为异常值，随机采样后纳入 LLM 处理。此外，还会在 LLM 提示中包含每个聚类所代表的句子数量，以确保考虑到每个情感的权重。
（三）多轮聚类策略

第一轮聚类（无损压缩）
首先使用语义相似性分数为 4 的阈值进行聚类，此轮可视为无损压缩，压缩比为 1.18（节省 15% 的空间），但对于大规模数据处理而言，无损压缩远远不够。
后续轮次聚类（有损压缩）
选择第一轮聚类中较小的异常聚类（向量数量少的聚类），使用更低的语义相似性分数阈值（如 3）再次进行聚类。随着轮次增加，不断降低阈值，虽然会牺牲更多信息，但能获得更高的压缩比。重复这一过程，直到达到理想的压缩效果。在实际操作中，经过多次降低阈值后，仍存在大量仅含单个向量的聚类，这些被视为异常值，随机采样以确保最终提示包含 25,000 个令牌。



From Tokens to Thoughts:How LLMs and Humans Trade Compression for Meaning

压缩效率 语义丰富性
LLMs与人类在概念表征策略上存在根本差异：LLMs偏向统计压缩的“最优性”，而人类概念系统优先考虑语义适应性和功能性效用。
这一发现揭示了当前AI与人类认知的差距，为开发更具人类对齐性的语言模型提供了理论方向。未来的研究需探索如何在压缩效率与语义丰富性之间实现更平衡的优化。



Context Engineering - What it is, and techniques to consider



Before writing this blog, we read “The New Skill in AI is Not Prompting, It’s Context Engineering”, by Philipp Schmid, where he does a great job of breaking down what makes up the context of an AI Agent or LLM. So, here’s what we narrow down as “context” based on both his list, and a few additions from our side:
在写这篇博客之前，我们读了Philipp Schmid写的《AI中的新技能不是提示，而是上下文工程》，他在文中很好地分解了构成AI Agent或LLM的上下文的内容。所以，以下是我们根据他的列表和我们的一些补充来缩小的“背景”：

The system prompt/instruction: sets the scene for the agent about what sort of tasks we want it to perform
系统提示/指令：为代理设置我们希望它执行哪种任务的场景
The user input: can be anything from a question to a request for a task to be completed.
用户输入可以是任何东西，从问题到完成任务的请求。
Short term memory or chat history: provides the LLM context about the ongoing chat.
短期记忆或聊天历史：提供有关正在进行的聊天的LLM上下文。
Long-term memory: can be used to store and retrieve both long-term chat history or other relevant information.
长期记忆：可用于存储和检索长期聊天记录或其他相关信息。
Information retrieved from a knowledge base: this could still be retrieval based on vector search over a database, but could also entail relevant information retrieved from any external knowledge base behind API calls, MCP tools or other sources.
从知识库检索的信息：这仍然可以是基于数据库上的向量搜索的检索，但也可能需要从API调用、MCP工具或其他来源背后的任何外部知识库检索相关信息。
Tools and their definitions: provide additional context to the LLM as to what tools it has access to.
工具及其定义：为LLM提供额外的上下文，说明它可以访问哪些工具。
Responses from tools: provide the responses from tool runs back to the LLM as additional context to work with.
来自工具的响应：将来自工具运行的响应作为额外的上下文提供给LLM。
Structured Outputs: provide context on what kind of information we are after from the LLM. But can also go the other way in providing condensed, structured information as context for specific tasks.
结构化输出：提供我们从LLM中获得什么样的信息的上下文。但也可以用另一种方式提供浓缩的、结构化的信息作为特定任务的上下文。
Global State/Context: especially relevant to agents built with LlamaIndex, allowing us to use workflow Context as a sort of scratchpad that we can store and retrieve global information across agent steps.
全局状态/上下文：特别与使用LlamaIndex构建的代理相关，允许我们使用workflow  Context 作为一种便签本，我们可以跨代理步骤存储和检索全局信息。


















假设我们的目标是**对一篇关于“可持续时尚”的文章进行摘要**。文章内容可能包含了该运动的定义、重要性、面临的挑战以及给消费者的建议等。

---

### 场景：从“最大压缩”到“语义均衡”

我们将通过三个不同层次的提示（Prompt）来展示如何逐步调整，以实现从追求极致压缩到兼顾语义丰富的转变。

**原始文章（假设片段）：**

> 可持续时尚是一项旨在改变时尚产业运作方式的综合性运动，其核心是减少对环境的负面影响和改善供应链中的社会条件。它涵盖了从原材料的采购、生产过程中的水资源与能源消耗，到最终产品的运输、销售和废弃处理等所有环节。该运动之所以重要，是因为传统“快时尚”模式造成了巨大的资源浪费、环境污染和劳工权益问题。例如，每年有数百万吨的纺织废料被填埋，生产一件棉质T恤需要消耗近3000升水。可持续时尚面临的挑战包括生产成本较高、消费者意识有待提高以及缺乏统一的行业标准。为了推动变革，消费者可以采取多种行动，比如选择由有机棉、亚麻或再生聚酯等环保材料制成的服装，支持那些公开其供应链信息、并获得如“公平贸易”或“全球有机纺织品标准”（GOTS）等认证的品牌，同时通过减少购买、修补旧衣和二手交易来延长服装的使用寿命。

---

#### 例子1：追求最大压缩效率（忽略语义丰富性）

这种提示的目标是得到最简短的文本，压缩率最高，但可能会丢失大量重要细节和情感色彩。

**一个不佳的提示 (Prompt 1):**

> **“总结一下关于可持续时尚的文章。”**

**模型可能的输出 (高压缩，低丰富度):**

> 可持续时尚旨在减少时尚业对环境和社会的负面影响。消费者可以通过选择环保材料和支持透明品牌来参与其中。

**分析：**
*   **压缩效率**：非常高。寥寥数语就概括了核心概念。
*   **语义丰富性**：非常低。这个摘要虽然没错，但极其笼统。它丢失了“快时尚”带来的具体问题（如水资源消耗、纺织废料）、面临的挑战（成本、意识）以及给消费者的具体行动建议（修补、二手交易）等关键信息。它更像一个词条解释，而不是一篇有深度的文章摘要。

---

#### 例子2：通过提示工程进行优化，寻求平衡

现在，我们通过更精细的提示来引导模型，要求它在压缩文本的同时，保留更多的关键语义信息。

**一个优化的提示 (Prompt 2):**

> **请为一篇关于“可持续时尚”的文章撰写一段约100字的摘要。**
>
> **请在摘要中包含以下几个要点：**
> **1. 可持续时尚的核心定义。**
> **2. 传统“快时尚”模式带来的至少一个具体问题（例如，资源浪费或环境污染）。**
> **3. 消费者可以采取的两种不同类型的行动建议。**
>
> **摘要应面向对该话题不熟悉的普通读者，风格要简洁易懂。**

**模型可能的输出 (均衡压缩与丰富度):**

> 可持续时尚是一项旨在减少时尚产业对环境和社会造成伤害的运动，它关注从生产到废弃的整个流程。 传统“快时尚”模式导致了惊人的资源浪费，例如生产一件棉T恤就要消耗数千升水。 普通消费者可以通过多种方式参与进来，一方面是明智消费，选择由有机棉等环保材料制成、并获得“公平贸易”等认证的品牌；另一方面是改变消费习惯，通过修补旧衣和进行二手交易来延长衣物寿命，从而减少浪费。

**分析：**
*   **压缩效率**：依然很高，将原文压缩到了约100字。
*   **语义丰富性**：显著提升。我们通过提示工程实现了以下目标：
    *   **明确了核心要素**: 提示中的“要点1, 2, 3”强制模型保留了定义、问题和解决方案这三个关键的语义块。
    *   **保留了具体细节**: “至少一个具体问题”的指令，引导模型保留了“消耗数千升水”这个强有力的例证，使摘要更具说服力。
    *   **增加了行动指导性**: “两种不同类型的行动建议”的指令，使得摘要不仅停留在解释概念，还给出了“购买选择”和“改变习惯”两个维度的实用建议，语义更加完整。
    *   **控制了风格和受众**: “面向普通读者，风格简洁易懂”的指令，确保了文本在压缩后依然保持了良好的可读性。

### 结论：提示工程如何实现权衡

这个例子清晰地表明，提示工程是通过**提供明确的约束和指引**来实现压缩效率和语义丰富性之间的权衡的。

*   **追求压缩效率**，可以通过**限制输出长度**（如“约100字”）来实现。
*   **追求语义丰富性**，可以通过以下方式实现：
    *   **指定关键信息点**：要求必须包含某些定义、原因、例子或结论。
    *   **要求保留细节**：明确指出需要包含具体的数据、名称或案例。
    *   **定义输出结构**：要求按特定逻辑（如“问题-分析-解决方案”）组织内容。
    *   **设定角色和目标受众**：让模型模拟特定专家或为特定人群写作，从而保留相应的语境和深度。

通过将这些指令组合在同一个提示中，我们就能像操作精密的仪器一样，精确地调整输出文本的天平，让它在简洁紧凑与信息饱满之间达到理想的平衡点。

