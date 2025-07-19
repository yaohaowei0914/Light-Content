import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lightce.prompt.context_judge import SEMANTIC_EQUIVALENCE_PROMPT
from lightce.api.ollama import OllamaAPI
from lightce.config import Config


class ContextJudgeAgent:
    """
    上下文判断代理，用于判断两段文本内容是否相同
    """
    
    def __init__(self, config: Config = None):
        """
        初始化ContextJudgeAgent
        
        Args:
            config: 配置对象，如果为None则使用默认配置
        """
        self.config = config or Config()
        self.llm_api = OllamaAPI(self.config)
    
    def judge_semantic_equivalence(self, text1: str, text2: str) -> bool:
        """
        判断两段文本在语义上是否表达相同的内容
        
        Args:
            text1: 第一段文本
            text2: 第二段文本
            
        Returns:
            bool: True表示内容相同，False表示内容不同
        """
        # 构建prompt
        prompt = SEMANTIC_EQUIVALENCE_PROMPT.format(text1=text1, text2=text2)
        
        try:
            # 调用LLM API
            response = self.llm_api.chat(prompt)
            
            # 解析响应
            result = self._parse_response(response)
            
            return result
            
        except Exception as e:
            print(f"判断过程中出现错误: {e}")
            return False
    
    def _parse_response(self, response: str) -> bool:
        """
        解析LLM的响应，判断结果
        
        Args:
            response: LLM的响应文本
            
        Returns:
            bool: True表示相同，False表示不同
        """
        # 清理响应文本
        response = response.strip().lower()
        
        # 判断响应内容
        if "相同" in response:
            return True
        elif "不同" in response or "部分相同" in response:
            return False
        else:
            # 如果无法明确判断，默认返回False
            print(f"无法解析响应: {response}")
            return False
    
    def judge_with_confidence(self, text1: str, text2: str) -> dict:
        """
        判断两段文本是否相同，并返回置信度信息
        
        Args:
            text1: 第一段文本
            text2: 第二段文本
            
        Returns:
            dict: 包含判断结果和置信度的字典
        """
        # 构建prompt
        prompt = SEMANTIC_EQUIVALENCE_PROMPT.format(text1=text1, text2=text2)
        
        try:
            # 调用LLM API
            response = self.llm_api.chat(prompt)
            
            # 解析响应
            is_same = self._parse_response(response)
            
            return {
                "is_same": is_same,
                "response": response,
                "confidence": "high" if "相同" in response or "不同" in response else "low"
            }
            
        except Exception as e:
            return {
                "is_same": False,
                "response": f"错误: {e}",
                "confidence": "error"
            }


def create_context_judge_agent(config: Config = None) -> ContextJudgeAgent:
    """
    创建ContextJudgeAgent实例的工厂函数
    
    Args:
        config: 配置对象
        
    Returns:
        ContextJudgeAgent: 上下文判断代理实例
    """
    return ContextJudgeAgent(config)


# 使用示例
if __name__ == "__main__":
    # 创建agent
    agent = create_context_judge_agent()
    
    # 测试用例
    text1 = "今天天气很好，阳光明媚。"
    text2 = "今天是个好天气，太阳很亮。"
    
    # 判断是否相同
    result = agent.judge_semantic_equivalence(text1, text2)
    print(f"文本1: {text1}")
    print(f"文本2: {text2}")
    print(f"判断结果: {'相同' if result else '不同'}")
    
    # 带置信度的判断
    detailed_result = agent.judge_with_confidence(text1, text2)
    print(f"详细结果: {detailed_result}")
