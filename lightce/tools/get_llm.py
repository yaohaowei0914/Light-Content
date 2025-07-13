import requests
import json
from bs4 import BeautifulSoup
import re
from typing import Dict, Optional, List, Any
from dataclasses import dataclass


@dataclass
class ModelInfo:
    """模型信息数据类"""
    model_name: str
    parameters: Optional[str] = None
    context_length: Optional[int] = None
    input_price_per_million_tokens: Optional[float] = None
    output_price_per_million_tokens: Optional[float] = None
    is_reasoning_model: bool = False
    notes: List[str] = None

    def __post_init__(self):
        if self.notes is None:
            self.notes = []

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "model_name": self.model_name,
            "parameters": self.parameters,
            "context_length": self.context_length,
            "input_price_per_million_tokens": self.input_price_per_million_tokens,
            "output_price_per_million_tokens": self.output_price_per_million_tokens,
            "is_reasoning_model": self.is_reasoning_model,
            "notes": self.notes
        }


class ModelInfoCollector:
    """模型信息收集器"""
    
    def __init__(self, api_base_url: str, model_name: str):
        self.api_base_url = api_base_url
        self.model_name = model_name
        self.model_info = ModelInfo(model_name=model_name)
    
    def collect_from_api(self) -> None:
        """从API收集模型信息"""
        try:
            response = requests.get(f"{self.api_base_url}/models/{self.model_name}")
            response.raise_for_status()
            api_data = response.json()
            
            # 提取上下文长度
            self._extract_context_length(api_data)
            
        except requests.exceptions.RequestException as e:
            self.model_info.notes.append(f"API请求失败: {e}。无法获取API提供的模型信息。")
        except json.JSONDecodeError:
            self.model_info.notes.append("无法解析API的响应，它可能不是有效的JSON格式。")
    
    def _extract_context_length(self, api_data: Dict[str, Any]) -> None:
        """从API响应中提取上下文长度"""
        context_keys = ['context_window', 'context_length', 'max_tokens']
        
        for key in context_keys:
            if key in api_data:
                self.model_info.context_length = api_data[key]
                return
        
        self.model_info.notes.append("无法通过API直接获取上下文长度，请查阅官方文档。")
    
    def analyze_model_characteristics(self) -> None:
        """分析模型特征"""
        # 设置默认参数信息
        self.model_info.parameters = (
            "通常在API文档中定义，例如：'temperature', 'top_p', 'max_tokens'等。"
            "请查阅官方文档获取详细列表。"
        )
        
        # 判断是否为推理模型
        if self._is_reasoning_model():
            self.model_info.is_reasoning_model = True
            self.model_info.notes.append("模型名称暗示这是一个推理模型。")
    
    def _is_reasoning_model(self) -> bool:
        """判断是否为推理模型"""
        reasoning_keywords = ["reason", "reasoner", "thinking", "logic"]
        model_name_lower = self.model_name.lower()
        return any(keyword in model_name_lower for keyword in reasoning_keywords)
    
    def collect_pricing_info(self, pricing_page_url: str) -> None:
        """从定价页面收集价格信息"""
        if not pricing_page_url:
            self.model_info.notes.append("未提供定价页面的URL，无法获取价格信息。")
            return
        
        try:
            page_response = requests.get(pricing_page_url)
            page_response.raise_for_status()
            soup = BeautifulSoup(page_response.content, 'html.parser')
            
            self._extract_pricing_from_soup(soup)
            
        except requests.exceptions.RequestException as e:
            self.model_info.notes.append(f"抓取定价页面失败: {e}")
        except (IndexError, ValueError) as e:
            self.model_info.notes.append(f"解析价格信息时出错: {e}。网页结构可能已更改。")
    
    def _extract_pricing_from_soup(self, soup: BeautifulSoup) -> None:
        """从BeautifulSoup对象中提取价格信息"""
        model_element = soup.find(string=re.compile(self.model_name, re.IGNORECASE))
        
        if not model_element:
            self.model_info.notes.append(
                f"在提供的定价页面URL上未找到模型'{self.model_name}'的信息。"
            )
            return
        
        parent_row = model_element.find_parent('tr')
        if not parent_row:
            self.model_info.notes.append(
                "在定价页面上找到了模型名称，但无法定位到价格信息所在的行。"
            )
            return
        
        columns = parent_row.find_all('td')
        if len(columns) <= 2:
            self.model_info.notes.append("价格表格列数不足，无法提取价格信息。")
            return
        
        try:
            input_price_text = columns[1].get_text(strip=True)
            output_price_text = columns[2].get_text(strip=True)
            
            # 提取数字
            input_price_match = re.findall(r"[\d\.]+", input_price_text)
            output_price_match = re.findall(r"[\d\.]+", output_price_text)
            
            if input_price_match:
                self.model_info.input_price_per_million_tokens = float(input_price_match[0])
            if output_price_match:
                self.model_info.output_price_per_million_tokens = float(output_price_match[0])
                
        except (IndexError, ValueError) as e:
            self.model_info.notes.append(f"解析价格数字时出错: {e}")
    
    def collect_all_info(self, pricing_page_url: Optional[str] = None) -> ModelInfo:
        """收集所有模型信息"""
        self.collect_from_api()
        self.analyze_model_characteristics()
        
        if pricing_page_url:
            self.collect_pricing_info(pricing_page_url)
        
        return self.model_info


def get_model_info(api_base_url: str, model_name: str, pricing_page_url: Optional[str] = None) -> Dict[str, Any]:
    """
    获取指定模型的相关信息。

    :param api_base_url: 模型API的基础URL (例如: https://api.openai.com/v1)
    :param model_name: 模型的名称 (例如: gpt-4)
    :param pricing_page_url: 包含价格信息的网页URL (可选)
    :return: 一个包含模型信息的字典
    """
    collector = ModelInfoCollector(api_base_url, model_name)
    model_info = collector.collect_all_info(pricing_page_url)
    return model_info.to_dict()


# 示例用法
if __name__ == "__main__":
    # 假设我们有一个模型提供商 "ExampleAI"
    API_URL = "https://api.example-ai.com/v1"  # 这是一个虚构的URL
    MODEL = "example-reasoner-v2"
    PRICING_URL = "https://example-ai.com/pricing"  # 这是一个虚构的URL

    # 调用工具函数
    collected_info = get_model_info(API_URL, MODEL, PRICING_URL)

    # 打印收集到的信息
    print(json.dumps(collected_info, indent=2, ensure_ascii=False))