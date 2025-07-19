#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
静态信息提取工具
使用UniversalAgent和静态信息提取提示词来完成静态信息提取功能
"""

from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from langchain_core.messages import HumanMessage
import json
import logging
import re

from ..agent.system import UniversalAgent, ModelConfig
from ..prompt.static_information import (
    InformationLevel, InformationType,
    get_information_prompt, get_all_information_prompts,
    get_information_workflow, get_level_description
)

# 配置日志
logger = logging.getLogger(__name__)

class StaticInformationConfig(BaseModel):
    """静态信息提取配置"""
    information_level: InformationLevel = Field(
        default=InformationLevel.BASIC,
        description="提取级别：BASIC, INTERMEDIATE, ADVANCED, EXPERT"
    )
    model_config: Optional[ModelConfig] = Field(
        default=None,
        description="模型配置参数"
    )

class StaticInformationResult(BaseModel):
    """静态信息提取结果"""
    success: bool = Field(description="是否成功")
    information_level: str = Field(description="提取级别")
    information_types: List[str] = Field(description="提取类型列表")
    results: Dict[str, Any] = Field(description="提取结果")

class StaticInformationAgent:
    """静态信息提取代理类"""
    
    def __init__(self, config: Optional[StaticInformationConfig] = None):
        """
        初始化静态信息提取代理
        
        Args:
            config: 静态信息提取配置
        """
        self.config = config or StaticInformationConfig()
        self.agent = UniversalAgent(self.config.model_config)
        self.extraction_history: List[StaticInformationResult] = []
        
        logger.info(f"初始化静态信息提取代理，级别: {self.config.information_level.value}")
    
    def extract_information(self, text: str) -> StaticInformationResult:
        """
        执行静态信息提取
        
        Args:
            text: 输入文本
        
        Returns:
            静态信息提取结果
        """
        try:
            # 使用该级别的所有类型
            all_prompts = get_all_information_prompts(self.config.information_level, text=text)
            information_types = [InformationType(t) for t in all_prompts.keys()]
            
            logger.info(f"开始静态信息提取，级别: {self.config.information_level.value}, 类型: {[t.value for t in information_types]}")
            
            results = {}
            
            # 执行每种类型的提取
            for information_type in information_types:
                try:
                    result = self._extract_single_type(text, information_type)
                    results[information_type.value] = result
                    
                    logger.info(f"完成 {information_type.value} 提取")
                    
                except Exception as e:
                    error_msg = f"{information_type.value} 提取失败: {str(e)}"
                    logger.error(error_msg)
                    results[information_type.value] = {"error": error_msg}
            
            # 创建结果
            extraction_result = StaticInformationResult(
                success=True,
                information_level=self.config.information_level.value,
                information_types=[t.value for t in information_types],
                results=results
            )
            
            # 保存到历史记录
            self.extraction_history.append(extraction_result)
            
            logger.info("静态信息提取完成")
            return extraction_result
            
        except Exception as e:
            error_msg = f"静态信息提取失败: {str(e)}"
            logger.error(error_msg)
            
            return StaticInformationResult(
                success=False,
                information_level=self.config.information_level.value,
                information_types=[],
                results={}
            )
    
    def _extract_single_type(self, text: str, information_type: InformationType) -> Dict[str, Any]:
        """
        执行单一类型的静态信息提取
        
        Args:
            text: 输入文本
            information_type: 提取类型
        
        Returns:
            提取结果
        """
        # 获取提示词
        prompt = get_information_prompt(
            self.config.information_level,
            information_type,
            text=text
        )
        
        # 构建完整的用户消息
        user_message = f"""
请根据以下提示词进行静态信息提取：

{prompt}

请确保输出格式规范，内容准确完整。严格按照要求的格式输出结果。
"""
        
        # 使用agent执行提取
        result = self.agent.run(user_message)
        
        if result["success"]:
            extracted_content = result["response"]
            
            return {
                "extracted_content": extracted_content,
                "prompt_used": prompt,
                "agent_response": result,
                "raw_content": result["response"]
            }
        else:
            raise Exception(f"Agent执行失败: {result.get('error', '未知错误')}")
    
    def batch_extract(self, texts: List[str]) -> List[StaticInformationResult]:
        """
        批量静态信息提取
        
        Args:
            texts: 文本列表
        
        Returns:
            提取结果列表
        """
        results = []
        
        for i, text in enumerate(texts):
            logger.info(f"处理第 {i+1}/{len(texts)} 个文本")
            result = self.extract_information(text)
            results.append(result)
        
        return results
    
    def get_extraction_history(self) -> List[StaticInformationResult]:
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
class StaticInformationTool(BaseTool):
    """静态信息提取LangChain工具"""
    
    name: str = "static_information_extraction"
    description: str = "执行静态信息提取，支持联系人、个人信息、数字、时间、位置、组织、技术、财务等多种类型的信息提取"
    
    def __init__(self, agent: StaticInformationAgent):
        super().__init__()
        self.agent = agent
    
    def _run(self, text: str, information_level: str = "basic") -> Dict[str, Any]:
        """
        运行静态信息提取
        
        Args:
            text: 输入文本
            information_level: 提取级别 (basic, intermediate, advanced, expert)
        
        Returns:
            提取结果
        """
        try:
            # 转换提取级别
            level_map = {
                "basic": InformationLevel.BASIC,
                "intermediate": InformationLevel.INTERMEDIATE,
                "advanced": InformationLevel.ADVANCED,
                "expert": InformationLevel.EXPERT
            }
            
            information_level_enum = level_map.get(information_level.lower(), InformationLevel.BASIC)
            
            # 执行提取
            result = self.agent.extract_information(text)
            
            return {
                "success": result.success,
                "information_level": result.information_level,
                "information_types": result.information_types,
                "results": result.results
            }
            
        except Exception as e:
            return {
                "success": False,
                "error_message": f"静态信息提取工具执行失败: {str(e)}"
            }

# 便捷函数
def create_static_information_agent(
    information_level: str = "basic",
    model_name: Optional[str] = None,
    temperature: float = 0.1,
    provider: str = "openai"
) -> StaticInformationAgent:
    """
    创建静态信息提取代理的便捷函数
    
    Args:
        information_level: 提取级别
        model_name: 模型名称
        temperature: 温度参数
        provider: 模型提供商
    
    Returns:
        StaticInformationAgent实例
    """
    # 转换提取级别
    level_map = {
        "basic": InformationLevel.BASIC,
        "intermediate": InformationLevel.INTERMEDIATE,
        "advanced": InformationLevel.ADVANCED,
        "expert": InformationLevel.EXPERT
    }
    
    information_level_enum = level_map.get(information_level.lower(), InformationLevel.BASIC)
    
    # 创建模型配置
    model_config = None
    if model_name:
        model_config = ModelConfig(
            model_name=model_name,
            temperature=temperature,
            provider=provider
        )
    
    # 创建配置
    config = StaticInformationConfig(
        information_level=information_level_enum,
        model_config=model_config
    )
    
    return StaticInformationAgent(config)

def extract_static_information_with_agent(
    text: str,
    information_level: str = "basic",
    model_name: Optional[str] = None,
    temperature: float = 0.1
) -> Dict[str, Any]:
    """
    使用静态信息提取代理进行提取的便捷函数
    
    Args:
        text: 输入文本
        information_level: 提取级别
        model_name: 模型名称
        temperature: 温度参数
    
    Returns:
        提取结果
    """
    agent = create_static_information_agent(information_level, model_name, temperature)
    result = agent.extract_information(text)
    return result.dict()

# 示例使用
if __name__ == "__main__":
    # 测试文本
    test_text = """
    张三，男，28岁，软件工程师，毕业于清华大学计算机系。
    联系方式：zhangsan@example.com，电话：138-1234-5678。
    工作地址：北京市海淀区中关村软件园，月薪15000元。
    入职时间：2020年3月15日，技术栈：Python、Java、React。
    """
    
    # 创建静态信息提取代理
    agent = create_static_information_agent("basic")
    
    # 执行提取
    result = agent.extract_information(test_text)
    
    print("静态信息提取结果:")
    print(f"成功: {result.success}")
    print(f"级别: {result.information_level}")
    
    if result.success:
        for information_type, information_result in result.results.items():
            print(f"\n{information_type}:")
            if "error" in information_result:
                print(f"  错误: {information_result['error']}")
            else:
                print(f"  内容: {information_result['extracted_content'][:200]}...")
