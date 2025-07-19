#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
策略选择工具
通过分析LLM输入的prompt，为短期记忆、长期记忆、参数输入、遵循的规则选择相应的处理策略
"""

from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
import logging
import re
from enum import Enum

from ..agent.system import UniversalAgent, ModelConfig

# 配置日志
logger = logging.getLogger(__name__)

class MemoryType(str, Enum):
    """记忆类型枚举"""
    SHORT_TERM = "short_term"      # 短期记忆
    LONG_TERM = "long_term"        # 长期记忆
    PARAMETER = "parameter"        # 参数输入
    RULE = "rule"                  # 遵循的规则

class PolicySelectConfig(BaseModel):
    """策略选择配置"""
    
    agent_model_config: Optional[ModelConfig] = None
    enable_analysis: bool = True
    enable_strategy_selection: bool = True
    memory_priority: Dict[MemoryType, int] = Field(
        default_factory=lambda: {
            MemoryType.SHORT_TERM: 1,
            MemoryType.LONG_TERM: 2,
            MemoryType.PARAMETER: 3,
            MemoryType.RULE: 4
        }
    )

class PolicySelectResult(BaseModel):
    """策略选择结果"""
    success: bool
    prompt_analysis: Dict[str, Any]
    compression_levels: Dict[MemoryType, int]  # 压缩级别1-4，越往上越激进

class PolicySelectAgent:
    """策略选择代理类"""
    
    def __init__(self, config: Optional[PolicySelectConfig] = None):
        """
        初始化策略选择代理
        
        Args:
            config: 策略选择配置
        """
        self.config = config or PolicySelectConfig()
        self.agent = UniversalAgent(self.config.agent_model_config)
        
        logger.info("初始化策略选择代理")
    
    def select_policy(self, prompt: str) -> PolicySelectResult:
        """
        为给定的prompt选择处理策略
        
        Args:
            prompt: LLM输入的prompt
        
        Returns:
            策略选择结果
        """
        try:
            logger.info("开始分析prompt并选择策略")
            
            # 分析prompt
            prompt_analysis = {}
            if self.config.enable_analysis:
                prompt_analysis = self._analyze_prompt(prompt)
            
            # 选择策略
            compression_levels = {}
            if self.config.enable_strategy_selection:
                compression_levels = self._select_compression_levels(prompt, prompt_analysis)
            
            # 创建结果
            result = PolicySelectResult(
                success=True,
                prompt_analysis=prompt_analysis,
                compression_levels=compression_levels
            )
            
            logger.info("策略选择完成")
            return result
            
        except Exception as e:
            error_msg = f"策略选择失败: {str(e)}"
            logger.error(error_msg)
            
            return PolicySelectResult(
                success=False,
                prompt_analysis={},
                compression_levels={}
            )
    
    def _analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        分析prompt的特征
        
        Args:
            prompt: 输入的prompt
        
        Returns:
            prompt分析结果
        """
        analysis_prompt = f"""
请分析以下LLM输入的prompt，识别其特征和需求：

{prompt}

请从以下维度进行分析：

1. **内容类型分析**：
   - 文本类型（文本、代码、公式、表格、链接等）
   - 主题领域（技术、商业、学术、娱乐、新闻等）
   - 复杂度级别（简单、中等、复杂）

2. **功能需求分析**：
   - 主要功能（信息提取、内容生成、问题解答、分析判断等）
   - 输出要求（结构化、非结构化、特定格式等）
   - 精度要求（高精度、中等精度、快速响应等）

3. **记忆需求分析**：
   - 短期记忆需求（临时信息、上下文保持等）
   - 长期记忆需求（知识积累、经验存储等）
   - 参数输入需求（配置信息、约束条件等）
   - 规则遵循需求（操作规范、约束规则等）

4. **处理需求分析**：
   - 处理目标（信息密度、存储效率、传输效率等）
   - 保留重点（关键信息、核心观点、重要细节等）
   - 处理比例（高处理、中等处理、低处理等）

请以JSON格式输出分析结果，包含上述所有维度。
"""
        
        # 使用agent执行分析
        result = self.agent.run(analysis_prompt)
        
        if result["success"]:
            # 直接返回agent的响应
            return {"analysis_response": result["response"]}
        else:
            raise Exception(f"Agent执行失败: {result.get('error', '未知错误')}")
    
    def _select_compression_levels(self, prompt: str, analysis: Dict[str, Any]) -> Dict[MemoryType, int]:
        """
        根据分析结果选择压缩级别
        
        Args:
            prompt: 输入的prompt
            analysis: prompt分析结果
        
        Returns:
            选择的压缩级别
        """
        compression_levels = {}
        
        # 为每种记忆类型选择压缩级别
        for memory_type in MemoryType:
            level, reason = self._select_compression_level_for_memory(memory_type, prompt, analysis)
            compression_levels[memory_type] = level
        
        return compression_levels
    
    def _select_compression_level_for_memory(self, memory_type: MemoryType, prompt: str, analysis: Dict[str, Any]) -> tuple[int, str]:
        """
        为特定记忆类型选择压缩级别
        
        Args:
            memory_type: 记忆类型
            prompt: 输入的prompt
            analysis: prompt分析结果
        
        Returns:
            压缩级别(1-4)和选择理由
        """
        # 构建选择提示词
        selection_prompt = f"""
请根据以下信息为{memory_type.value}记忆类型选择处理策略：

**输入内容信息：**
- 内容长度：{len(prompt)}字符
- 内容分析：{analysis.get('analysis_response', '无分析结果')}

**处理策略级别说明：**
- 级别1：轻度处理，保留大部分原始信息，适合重要且需要详细保留的内容
- 级别2：中度处理，平衡信息保留和处理效率，适合一般重要内容
- 级别3：高度处理，大幅减少内容但保留核心信息，适合次要内容
- 级别4：极度处理，只保留最关键信息，适合临时或参考性内容

**记忆类型特点：**
- 短期记忆：临时存储，可接受较高处理强度
- 长期记忆：永久存储，需要保留重要信息
- 参数输入：配置信息，需要精确保留
- 遵循规则：操作规范，需要清晰保留

请综合考虑内容长度、复杂度、重要性和记忆类型特点，选择最合适的处理策略级别（1-4），并说明选择理由。

请以JSON格式输出：
{{
    "compression_level": 数字,
    "reason": "选择理由"
}}
"""
        
        # 使用agent执行选择
        result = self.agent.run(selection_prompt)
        
        if result["success"]:
            # 直接返回agent的响应
            return 2, result["response"]
        else:
            logger.warning(f"处理策略级别选择失败: {result.get('error', '未知错误')}")
            # 使用默认策略
            return 2, "选择失败，使用默认级别"
    
    def batch_select_policy(self, prompts: List[str]) -> List[PolicySelectResult]:
        """
        批量选择策略
        
        Args:
            prompts: prompt列表
        
        Returns:
            策略选择结果列表
        """
        results = []
        
        for i, prompt in enumerate(prompts):
            logger.info(f"处理第 {i+1}/{len(prompts)} 个prompt")
            result = self.select_policy(prompt)
            results.append(result)
        
        return results
    
    def get_policy_history(self) -> List[PolicySelectResult]:
        """获取策略选择历史记录"""
        return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_selections": 0,
            "successful_selections": 0,
            "success_rate": 0.0,
            "strategy_level_usage": {}
        }

# LangChain工具包装器
class PolicySelectTool(BaseTool):
    """策略选择LangChain工具"""
    
    name: str = "policy_select"
    description: str = "通过分析LLM输入的prompt，为短期记忆、长期记忆、参数输入、遵循的规则选择相应的处理策略"
    
    def __init__(self, agent: PolicySelectAgent):
        super().__init__()
        self.agent = agent
    
    def _run(self, prompt: str) -> Dict[str, Any]:
        """
        运行策略选择
        
        Args:
            prompt: LLM输入的prompt
        
        Returns:
            策略选择结果
        """
        try:
            result = self.agent.select_policy(prompt)
            
            return {
                "success": result.success,
                "prompt_analysis": result.prompt_analysis,
                "compression_levels": {k.value: v for k, v in result.compression_levels.items()}
            }
            
        except Exception as e:
            return {
                "success": False,
                "error_message": f"策略选择工具执行失败: {str(e)}"
            }

# 便捷函数
def create_policy_select_agent(
    model_name: Optional[str] = None,
    temperature: float = 0.1,
    provider: str = "openai"
) -> PolicySelectAgent:
    """
    创建策略选择代理的便捷函数
    
    Args:
        model_name: 模型名称
        temperature: 温度参数
        provider: 模型提供商
    
    Returns:
        PolicySelectAgent实例
    """
    # 创建模型配置
    model_config = None
    if model_name:
        model_config = ModelConfig(
            model_name=model_name,
            temperature=temperature,
            provider=provider
        )
    
    # 创建配置
    config = PolicySelectConfig(
        agent_model_config=model_config
    )
    
    return PolicySelectAgent(config)

def select_policy_with_agent(
    prompt: str,
    model_name: Optional[str] = None,
    temperature: float = 0.1
) -> Dict[str, Any]:
    """
    使用策略选择代理进行策略选择的便捷函数
    
    Args:
        prompt: LLM输入的prompt
        model_name: 模型名称
        temperature: 温度参数
    
    Returns:
        策略选择结果
    """
    agent = create_policy_select_agent(model_name, temperature)
    result = agent.select_policy(prompt)
    return result.dict()

# 示例使用
if __name__ == "__main__":
    # 测试prompt
    test_prompt = """
    请分析以下技术文档，提取其中的关键技术要点和实现细节，并生成一个结构化的技术摘要。
    文档内容涉及机器学习算法、深度学习框架和人工智能应用。
    需要保持技术准确性，同时确保信息密度高，便于后续的技术决策和知识管理。
    """
    
    # 创建策略选择代理
    agent = create_policy_select_agent()
    
    # 执行策略选择
    result = agent.select_policy(test_prompt)
    
    print("策略选择结果:")
    print(f"成功: {result.success}")
    
    if result.success:
        print(f"\nPrompt分析: {result.prompt_analysis}")
        print(f"\n选择的处理策略级别:")
        for memory_type, level in result.compression_levels.items():
            print(f"  {memory_type.value}: 级别{level}")
