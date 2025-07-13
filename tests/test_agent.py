"""
LangGraph Agent 测试文件
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lightce.agent import run_agent, search_web, calculate, get_weather
from lightce.config import AGENT_NAME, OPENAI_MODEL

class TestAgentTools(unittest.TestCase):
    """测试agent工具函数"""
    
    def test_search_web(self):
        """测试搜索工具"""
        result = search_web("Python编程")
        self.assertIn("搜索结果", result)
        self.assertIn("Python编程", result)
    
    def test_calculate(self):
        """测试计算工具"""
        result = calculate("2 + 3 * 4")
        self.assertIn("计算结果", result)
        self.assertIn("14", result)  # 2 + 3 * 4 = 14
    
    def test_calculate_error(self):
        """测试计算错误处理"""
        result = calculate("invalid expression")
        self.assertIn("计算错误", result)
    
    def test_get_weather(self):
        """测试天气工具"""
        result = get_weather("北京")
        self.assertIn("北京", result)
        self.assertIn("天气", result)

class TestAgentConfig(unittest.TestCase):
    """测试agent配置"""
    
    def test_agent_name(self):
        """测试agent名称"""
        self.assertEqual(AGENT_NAME, "智能助手")
    
    def test_model_config(self):
        """测试模型配置"""
        self.assertIsInstance(OPENAI_MODEL, str)

class TestAgentIntegration(unittest.TestCase):
    """测试agent集成功能"""
    
    @patch('lightce.agent.ChatOpenAI')
    def test_agent_initialization(self, mock_llm):
        """测试agent初始化"""
        # 模拟LLM响应
        mock_response = MagicMock()
        mock_response.content = "你好！我是智能助手。"
        mock_response.type = "ai"
        mock_llm.return_value.invoke.return_value = mock_response
        
        # 测试agent运行
        try:
            messages = run_agent("你好")
            self.assertIsInstance(messages, list)
        except Exception as e:
            # 如果没有设置API密钥，这是预期的
            self.assertIn("api_key", str(e).lower())

if __name__ == "__main__":
    unittest.main() 