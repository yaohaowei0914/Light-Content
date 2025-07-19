#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON提取工具
使用UniversalAgent来完成JSON数据的提取功能
"""

from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from langchain_core.messages import HumanMessage
import json
import logging
import re

from ..agent.system import UniversalAgent, ModelConfig

# 配置日志
logger = logging.getLogger(__name__)

class JSONExtractConfig(BaseModel):
    """JSON提取配置"""
    model_config: Optional[ModelConfig] = Field(
        default=None,
        description="模型配置参数"
    )
    enable_extraction: bool = Field(
        default=True,
        description="是否启用内容提取"
    )

class JSONExtractResult(BaseModel):
    """JSON提取结果"""
    success: bool = Field(description="是否成功")
    extracted_content: Dict[str, Any] = Field(description="提取的内容")

class JSONExtractAgent:
    """JSON提取代理类"""
    
    def __init__(self, config: Optional[JSONExtractConfig] = None):
        """
        初始化JSON提取代理
        
        Args:
            config: JSON提取配置
        """
        self.config = config or JSONExtractConfig()
        self.agent = UniversalAgent(self.config.model_config)
        self.processing_history: List[JSONExtractResult] = []
        
        logger.info("初始化JSON提取代理")
    
    def extract_json(self, input_data: str) -> JSONExtractResult:
        """
        提取JSON数据
        
        Args:
            input_data: 输入的JSON数据
        
        Returns:
            JSON提取结果
        """
        import time
        start_time = time.time()
        
        try:
            logger.info("开始提取JSON数据")
            
            # 提取内容
            extracted_content = {}
            if self.config.enable_extraction:
                extracted_content = self._extract_content(input_data)
            
            # 创建结果
            result = JSONExtractResult(
                success=True,
                extracted_content=extracted_content
            )
            
            # 保存到历史记录
            self.processing_history.append(result)
            
            logger.info(f"JSON提取完成，处理时间: {time.time() - start_time:.2f}秒")
            return result
            
        except Exception as e:
            error_msg = f"JSON提取失败: {str(e)}"
            logger.error(error_msg)
            
            return JSONExtractResult(
                success=False,
                extracted_content={}
            )
    
    def _extract_content(self, input_data: str) -> Dict[str, Any]:
        """
        提取JSON内容
        
        Args:
            input_data: 输入数据
        
        Returns:
            提取的内容
        """
        # 构建提取提示词
        prompt = self._build_extraction_prompt(input_data)
        
        # 使用agent执行提取
        result = self.agent.run(prompt)
        
        if result["success"]:
            try:
                # 尝试解析JSON响应
                extracted = json.loads(result["response"])
                return extracted
            except json.JSONDecodeError:
                # 如果不是JSON，尝试结构化解析
                return self._parse_json_response(result["response"])
        else:
            raise Exception(f"Agent执行失败: {result.get('error', '未知错误')}")
    
    def _build_extraction_prompt(self, input_data: str) -> str:
        """构建JSON提取提示词"""
        return f"""
请从以下JSON数据中提取所有相关内容，并返回结构化的JSON格式：

{input_data}

要求：
1. 完整提取所有字段和值
2. 保持原有的数据结构
3. 处理嵌套对象和数组
4. 确保输出为有效的JSON格式
5. 如果数据不完整，请补充合理的默认值

请直接返回JSON格式的结果，不要包含其他说明文字。
"""
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """解析JSON响应"""
        try:
            # 尝试提取JSON部分
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            # 尝试解析为列表
            if response.strip().startswith('['):
                return {"items": json.loads(response)}
            
            # 尝试解析为对象
            if response.strip().startswith('{'):
                return json.loads(response)
            
            # 如果都不是，返回原始响应
            return {"raw_content": response, "parsed": False}
            
        except Exception as e:
            logger.warning(f"解析响应失败: {str(e)}")
            return {"raw_content": response, "parsed": False, "error": str(e)}
    
    def batch_extract(self, input_data_list: List[str]) -> List[JSONExtractResult]:
        """
        批量提取JSON数据
        
        Args:
            input_data_list: 输入数据列表
        
        Returns:
            提取结果列表
        """
        results = []
        
        for i, input_data in enumerate(input_data_list):
            logger.info(f"处理第 {i+1}/{len(input_data_list)} 个JSON数据")
            result = self.extract_json(input_data)
            results.append(result)
        
        return results
    
    def get_processing_history(self) -> List[JSONExtractResult]:
        """获取处理历史记录"""
        return self.processing_history
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        if not self.processing_history:
            return {"total_extractions": 0}
        
        total_extractions = len(self.processing_history)
        successful_extractions = sum(1 for r in self.processing_history if r.success)
        
        return {
            "total_extractions": total_extractions,
            "successful_extractions": successful_extractions,
            "success_rate": successful_extractions / total_extractions
        }

# LangChain工具包装器
class JSONExtractTool(BaseTool):
    """JSON提取LangChain工具"""
    
    name: str = "json_extract"
    description: str = "提取JSON数据中的内容"
    
    def __init__(self, agent: JSONExtractAgent):
        super().__init__()
        self.agent = agent
    
    def _run(self, input_data: str) -> Dict[str, Any]:
        """
        运行JSON提取
        
        Args:
            input_data: 输入的JSON数据
        
        Returns:
            提取结果
        """
        try:
            # 执行提取
            result = self.agent.extract_json(input_data)
            
            return {
                "success": result.success,
                "extracted_content": result.extracted_content,
                "error_message": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "error_message": f"JSON提取工具执行失败: {str(e)}"
            }

# 便捷函数
def create_json_extract_agent(
    model_name: Optional[str] = None,
    temperature: float = 0.1,
    provider: str = "openai"
) -> JSONExtractAgent:
    """
    创建JSON提取代理的便捷函数
    
    Args:
        model_name: 模型名称
        temperature: 温度参数
        provider: 模型提供商
    
    Returns:
        JSONExtractAgent实例
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
    config = JSONExtractConfig(
        model_config=model_config
    )
    
    return JSONExtractAgent(config)

def extract_json_with_agent(
    input_data: str,
    model_name: Optional[str] = None,
    temperature: float = 0.1
) -> Dict[str, Any]:
    """
    使用JSON提取代理进行提取的便捷函数
    
    Args:
        input_data: 输入的JSON数据
        model_name: 模型名称
        temperature: 温度参数
    
    Returns:
        提取结果
    """
    agent = create_json_extract_agent(model_name, temperature)
    result = agent.extract_json(input_data)
    return result.dict()

# 示例使用
if __name__ == "__main__":
    # 测试JSON数据
    test_json = """
    {
        "users": [
            {"id": 3, "name": "张三", "age": 28, "priority": "high"},
            {"id": 1, "name": "李四", "age": 32, "priority": "medium"},
            {"id": 2, "name": "王五", "age": 25, "priority": "low"}
        ]
    }
    """
    
    # 创建JSON提取代理
    agent = create_json_extract_agent()
    
    # 执行提取
    result = agent.extract_json(test_json)
    
    print("JSON提取结果:")
    print(f"成功: {result.success}")
    print(f"提取内容: {result.extracted_content}")
    
    if result.success:
        print(f"\n提取的内容类型: {type(result.extracted_content)}")
        print(f"内容长度: {len(str(result.extracted_content))} 字符")
