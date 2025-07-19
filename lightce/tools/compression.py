#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本压缩Agent
使用UniversalAgent系统和mini_contents提示词重构的智能文本压缩工具
"""

from typing import Dict, List, Any, Optional, Union
from langchain_core.tools import BaseTool, tool
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel, Field
import json
import logging
from datetime import datetime

from ..agent.system import UniversalAgent, ModelConfig
from ..prompt.mini_contents import (
    CompressionStage, CompressionType, get_compression_prompt, 
    get_all_compression_prompts, get_compression_type_from_text,
    calculate_compression_ratio, calculate_information_retention
)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompressionResult(BaseModel):
    """压缩结果模型"""
    success: bool = Field(description="是否成功")
    original_text: str = Field(description="原始文本")
    compressed_text: str = Field(description="压缩后文本")


class CompressionAgentConfig(BaseModel):
    """压缩Agent配置"""
    model_name: str = Field(default="gpt-3.5-turbo", description="模型名称")
    temperature: float = Field(default=0.3, description="温度参数")
    max_tokens: int = Field(default=2000, description="最大token数")
    provider: str = Field(default="openai", description="模型提供商")
    


class CompressionAgent:
    """智能文本压缩Agent"""
    
    def __init__(self, config: Optional[CompressionAgentConfig] = None):
        """
        初始化压缩Agent
        
        Args:
            config: Agent配置参数
        """
        self.config = config or CompressionAgentConfig()
        self.agent = self._create_agent()
        self.compression_history: List[CompressionResult] = []
        
    def _create_agent(self) -> UniversalAgent:
        """创建底层Agent"""
        model_config = ModelConfig(
            model_name=self.config.model_name,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            provider=self.config.provider
        )
        return UniversalAgent(model_config)
    
    def compress_text(
        self, 
        text: str, 
        compression_ratio: Optional[float] = None,
        compression_type: Optional[CompressionType] = None,
        enable_stages: bool = None
    ) -> CompressionResult:
        """
        压缩文本
        
        Args:
            text: 要压缩的文本
            compression_ratio: 压缩比例（百分比）
            compression_type: 压缩类型
            enable_stages: 是否启用分阶段处理
            
        Returns:
            压缩结果
        """
        if not text:
            return CompressionResult(
                success=False,
                original_text="",
                compressed_text=""
            )
        
        # 设置默认值
        compression_ratio = compression_ratio or 50.0
        
        # 设置压缩类型
        if compression_type is None:
            compression_type = CompressionType.GENERAL
        
        try:
            return self._compress_simple(text, compression_ratio, compression_type)
                
        except Exception as e:
            logger.error(f"压缩失败: {str(e)}")
            return CompressionResult(
                success=False,
                original_text=text,
                compressed_text=""
            )
    
    
    def _compress_simple(
        self, 
        text: str, 
        compression_ratio: float, 
        compression_type: CompressionType
    ) -> CompressionResult:
        """简单压缩处理"""
        # 使用压缩阶段的提示词进行一次性压缩
        compress_prompt = get_compression_prompt(
            CompressionStage.COMPRESS,
            compression_type,
            text=text,
            compression_ratio=f"{compression_ratio}%",
            preprocess_result="文本已预处理，准备进行压缩"
        )
        
        compress_result = self.agent.run(compress_prompt)
        if not compress_result['success']:
            raise Exception(f"压缩失败: {compress_result.get('error', '未知错误')}")
        
        compressed_text = compress_result['response']
        
        # 创建结果
        result = CompressionResult(
            success=True,
            original_text=text,
            compressed_text=compressed_text
        )
        
        return result
    

    
    def batch_compress(
        self, 
        texts: List[str], 
        compression_ratio: Optional[float] = None,
        compression_type: Optional[CompressionType] = None
    ) -> List[CompressionResult]:
        """
        批量压缩文本
        
        Args:
            texts: 文本列表
            compression_ratio: 压缩比例
            compression_type: 压缩类型
            
        Returns:
            压缩结果列表
        """
        results = []
        for i, text in enumerate(texts):
            logger.info(f"处理第 {i+1}/{len(texts)} 个文本")
            result = self.compress_text(text, compression_ratio, compression_type)
            results.append(result)
        return results
    
    def get_compression_stats(self) -> Dict[str, Any]:
        """获取压缩统计信息"""
        if not self.compression_history:
            return {"message": "暂无压缩历史"}
        
        total_compressions = len(self.compression_history)
        successful_compressions = sum(1 for r in self.compression_history if r.success)
        
        if successful_compressions == 0:
            return {"message": "暂无成功压缩记录"}
        
        return {
            "total_compressions": total_compressions,
            "successful_compressions": successful_compressions,
            "success_rate": (successful_compressions / total_compressions) * 100
        }
    
    def clear_history(self):
        """清空压缩历史"""
        self.compression_history.clear()
        logger.info("压缩历史已清空")
    
    def update_config(self, **kwargs):
        """更新配置"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        
        # 重新创建Agent
        self.agent = self._create_agent()
        logger.info(f"配置已更新: {kwargs}")

# 便捷函数
def create_compression_agent(
    model_name: str = "gpt-3.5-turbo",
    temperature: float = 0.3,
    max_tokens: int = 2000,
    provider: str = "openai"
) -> CompressionAgent:
    """
    创建压缩Agent的便捷函数
    
    Args:
        model_name: 模型名称
        temperature: 温度参数
        max_tokens: 最大token数
        provider: 模型提供商
        
    Returns:
        压缩Agent实例
    """
    config = CompressionAgentConfig(
        model_name=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        provider=provider
    )
    return CompressionAgent(config)

# LangChain工具包装
@tool
def compress_text_with_agent(
    text: str, 
    compression_ratio: float = 50.0,
    compression_type: str = "auto"
) -> str:
    """
    使用智能Agent压缩文本
    
    Args:
        text: 要压缩的文本
        compression_ratio: 压缩比例（百分比）
        compression_type: 压缩类型（auto/general/technical/creative/academic/news/conversation）
        
    Returns:
        压缩结果JSON字符串
    """
    try:
        # 创建压缩Agent
        agent = create_compression_agent()
        
        # 解析压缩类型
        if compression_type == "auto":
            comp_type = None  # 自动检测
        else:
            try:
                comp_type = CompressionType(compression_type)
            except ValueError:
                comp_type = CompressionType.GENERAL
        
        # 执行压缩
        result = agent.compress_text(text, compression_ratio, comp_type)
        
        # 返回JSON格式的结果
        return json.dumps({
            "success": result.success,
            "original_length": len(result.original_text),
            "compressed_length": len(result.compressed_text),
            "compressed_text": result.compressed_text
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)

