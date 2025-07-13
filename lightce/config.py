import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# OpenAI配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# Agent配置
AGENT_NAME = "智能助手"
MAX_ITERATIONS = 10
TEMPERATURE = 0.7
