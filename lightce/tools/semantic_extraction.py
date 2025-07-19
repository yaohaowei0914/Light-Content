#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语义提取工具
使用UniversalAgent和语义提取提示词来完成语义提取功能
"""

from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from langchain_core.messages import HumanMessage
import json
import logging

from ..agent.system import UniversalAgent, ModelConfig
from ..prompt.semantic_extration import (
    ExtractionLevel, ExtractionType,
    get_extraction_prompt, get_all_extraction_prompts,
    get_extraction_workflow, get_level_description
)

# 配置日志
logger = logging.getLogger(__name__)

class SemanticExtractionConfig(BaseModel):
    """语义提取配置"""
    extraction_level: ExtractionLevel = Field(
        default=ExtractionLevel.BASIC,
        description="提取级别：BASIC, INTERMEDIATE, ADVANCED, EXPERT"
    )
    extraction_types: Optional[List[ExtractionType]] = Field(
        default=None,
        description="指定提取类型列表，如果为None则使用该级别的所有类型"
    )
    model_config: Optional[ModelConfig] = Field(
        default=None,
        description="模型配置参数"
    )
    enable_multi_stage: bool = Field(
        default=True,
        description="是否启用多阶段处理"
    )

class SemanticExtractionResult(BaseModel):
    """语义提取结果"""
    success: bool = Field(description="是否成功")
    extraction_level: str = Field(description="提取级别")
    extraction_types: List[str] = Field(description="提取类型列表")
    results: Dict[str, Any] = Field(description="提取结果")

class SemanticExtractionAgent:
    """语义提取代理类"""
    
    def __init__(self, config: Optional[SemanticExtractionConfig] = None):
        """
        初始化语义提取代理
        
        Args:
            config: 语义提取配置
        """
        self.config = config or SemanticExtractionConfig()
        self.agent = UniversalAgent(self.config.model_config)
        self.extraction_history: List[SemanticExtractionResult] = []
        
        logger.info(f"初始化语义提取代理，级别: {self.config.extraction_level.value}")
    
    def extract_semantic(self, text: str, extraction_types: Optional[List[ExtractionType]] = None) -> SemanticExtractionResult:
        """
        执行语义提取
        
        Args:
            text: 输入文本
            extraction_types: 指定提取类型，如果为None则使用配置中的类型
        
        Returns:
            语义提取结果
        """
        try:
            # 确定要使用的提取类型
            if extraction_types is None:
                if self.config.extraction_types is None:
                    # 使用该级别的所有类型
                    all_prompts = get_all_extraction_prompts(self.config.extraction_level, text=text)
                    extraction_types = [ExtractionType(t) for t in all_prompts.keys()]
                else:
                    extraction_types = self.config.extraction_types
            
            logger.info(f"开始语义提取，级别: {self.config.extraction_level.value}, 类型: {[t.value for t in extraction_types]}")
            
            results = {}
            
            # 执行每种类型的提取
            for extraction_type in extraction_types:
                try:
                    result = self._extract_single_type(text, extraction_type)
                    results[extraction_type.value] = result
                    
                    logger.info(f"完成 {extraction_type.value} 提取")
                    
                except Exception as e:
                    error_msg = f"{extraction_type.value} 提取失败: {str(e)}"
                    logger.error(error_msg)
                    results[extraction_type.value] = {"error": error_msg}
            
            # 创建结果
            extraction_result = SemanticExtractionResult(
                success=True,
                extraction_level=self.config.extraction_level.value,
                extraction_types=[t.value for t in extraction_types],
                results=results
            )
            
            # 保存到历史记录
            self.extraction_history.append(extraction_result)
            
            logger.info("语义提取完成")
            return extraction_result
            
        except Exception as e:
            error_msg = f"语义提取失败: {str(e)}"
            logger.error(error_msg)
            
            return SemanticExtractionResult(
                success=False,
                extraction_level=self.config.extraction_level.value,
                extraction_types=[],
                results={}
            )
    
    def _extract_single_type(self, text: str, extraction_type: ExtractionType) -> Dict[str, Any]:
        """
        执行单一类型的语义提取
        
        Args:
            text: 输入文本
            extraction_type: 提取类型
        
        Returns:
            提取结果
        """
        # 获取提示词
        prompt = get_extraction_prompt(
            self.config.extraction_level,
            extraction_type,
            text=text
        )
        
        # 构建完整的用户消息
        user_message = f"""
请根据以下提示词进行语义提取：

{prompt}

请确保输出格式规范，内容准确完整。
"""
        
        # 使用agent执行提取
        result = self.agent.run(user_message)
        
        if result["success"]:
            return {
                "extracted_content": result["response"],
                "prompt_used": prompt,
                "agent_response": result
            }
        else:
            raise Exception(f"Agent执行失败: {result.get('error', '未知错误')}")
    
    def batch_extract(self, texts: List[str], extraction_types: Optional[List[ExtractionType]] = None) -> List[SemanticExtractionResult]:
        """
        批量语义提取
        
        Args:
            texts: 文本列表
            extraction_types: 指定提取类型
        
        Returns:
            提取结果列表
        """
        results = []
        
        for i, text in enumerate(texts):
            logger.info(f"处理第 {i+1}/{len(texts)} 个文本")
            result = self.extract_semantic(text, extraction_types)
            results.append(result)
        
        return results
    
    def get_extraction_history(self) -> List[SemanticExtractionResult]:
        """获取提取历史记录"""
        return self.extraction_history
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        if not self.extraction_history:
            return {"total_extractions": 0}
        
        total_extractions = len(self.extraction_history)
        successful_extractions = sum(1 for r in self.extraction_history if r.success)
        
        return {
            "total_extractions": total_extractions,
            "successful_extractions": successful_extractions,
            "success_rate": successful_extractions / total_extractions
        }

# LangChain工具包装器
class SemanticExtractionTool(BaseTool):
    """语义提取LangChain工具"""
    
    name: str = "semantic_extraction"
    description: str = "执行语义提取，支持关键词、主题、实体、情感等多种类型的提取"
    
    def __init__(self, agent: SemanticExtractionAgent):
        super().__init__()
        self.agent = agent
    
    def _run(self, text: str, extraction_level: str = "basic", extraction_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        运行语义提取
        
        Args:
            text: 输入文本
            extraction_level: 提取级别 (basic, intermediate, advanced, expert)
            extraction_types: 提取类型列表
        
        Returns:
            提取结果
        """
        try:
            # 转换提取级别
            level_map = {
                "basic": ExtractionLevel.BASIC,
                "intermediate": ExtractionLevel.INTERMEDIATE,
                "advanced": ExtractionLevel.ADVANCED,
                "expert": ExtractionLevel.EXPERT
            }
            
            extraction_level_enum = level_map.get(extraction_level.lower(), ExtractionLevel.BASIC)
            
            # 转换提取类型
            extraction_types_enum = None
            if extraction_types:
                type_map = {
                    "keywords": ExtractionType.KEYWORDS,
                    "topics": ExtractionType.TOPICS,
                    "concepts": ExtractionType.CONCEPTS,
                    "entities": ExtractionType.ENTITIES,
                    "relations": ExtractionType.RELATIONS,
                    "sentiment": ExtractionType.SENTIMENT,
                    "intent": ExtractionType.INTENT,
                    "summary": ExtractionType.SUMMARY
                }
                extraction_types_enum = [type_map.get(t.lower()) for t in extraction_types if t.lower() in type_map]
            
            # 执行提取
            result = self.agent.extract_semantic(text, extraction_types_enum)
            
            return {
                "success": result.success,
                "extraction_level": result.extraction_level,
                "extraction_types": result.extraction_types,
                "results": result.results
            }
            
        except Exception as e:
            return {
                "success": False,
                "error_message": f"语义提取工具执行失败: {str(e)}"
            }

# 便捷函数
def create_semantic_extraction_agent(
    extraction_level: str = "basic",
    model_name: Optional[str] = None,
    temperature: float = 0.1,
    provider: str = "openai"
) -> SemanticExtractionAgent:
    """
    创建语义提取代理的便捷函数
    
    Args:
        extraction_level: 提取级别
        model_name: 模型名称
        temperature: 温度参数
        provider: 模型提供商
    
    Returns:
        SemanticExtractionAgent实例
    """
    # 转换提取级别
    level_map = {
        "basic": ExtractionLevel.BASIC,
        "intermediate": ExtractionLevel.INTERMEDIATE,
        "advanced": ExtractionLevel.ADVANCED,
        "expert": ExtractionLevel.EXPERT
    }
    
    extraction_level_enum = level_map.get(extraction_level.lower(), ExtractionLevel.BASIC)
    
    # 创建模型配置
    model_config = None
    if model_name:
        model_config = ModelConfig(
            model_name=model_name,
            temperature=temperature,
            provider=provider
        )
    
    # 创建配置
    config = SemanticExtractionConfig(
        extraction_level=extraction_level_enum,
        model_config=model_config
    )
    
    return SemanticExtractionAgent(config)

def extract_semantic_with_agent(
    text: str,
    extraction_level: str = "basic",
    extraction_types: Optional[List[str]] = None,
    model_name: Optional[str] = None,
    temperature: float = 0.1
) -> Dict[str, Any]:
    """
    使用语义提取代理进行提取的便捷函数
    
    Args:
        text: 输入文本
        extraction_level: 提取级别
        extraction_types: 提取类型列表
        model_name: 模型名称
        temperature: 温度参数
    
    Returns:
        提取结果
    """
    agent = create_semantic_extraction_agent(extraction_level, model_name, temperature)
    result = agent.extract_semantic(text, extraction_types)
    return result.dict()

# 示例使用
if __name__ == "__main__":
    # 测试文本
    test_text = """
    人工智能技术正在快速发展，为各行各业带来了革命性的变化。
    深度学习模型在自然语言处理任务中取得了显著的效果提升。
    通过对比分析，我们发现Transformer架构在处理长文本时具有明显优势。
    这些发现为后续的研究提供了重要的理论基础和实践指导。
    """
    
    # 创建语义提取代理
    agent = create_semantic_extraction_agent("basic")
    
    # 执行提取
    result = agent.extract_semantic(test_text)
    
    print("语义提取结果:")
    print(f"成功: {result.success}")
    print(f"级别: {result.extraction_level}")
    
    if result.success:
        for extraction_type, extraction_result in result.results.items():
            print(f"\n{extraction_type}:")
            if "error" in extraction_result:
                print(f"  错误: {extraction_result['error']}")
            else:
                print(f"  内容: {extraction_result['extracted_content'][:200]}...")
