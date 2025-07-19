import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# OpenAI配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# 原有Agent配置
AGENT_NAME = "智能助手"
MAX_ITERATIONS = 10
TEMPERATURE = 0.7

# 通用Agent系统默认配置
DEFAULT_MODEL_NAME = "gpt-3.5-turbo"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 1.0
DEFAULT_TOP_K = 40
DEFAULT_MAX_TOKENS = 1000
DEFAULT_PROVIDER = "openai"

# 模型提供商配置
SUPPORTED_PROVIDERS = ["openai", "ollama"]

# 参数范围限制
TEMPERATURE_MIN = 0.0
TEMPERATURE_MAX = 2.0
TOP_P_MIN = 0.0
TOP_P_MAX = 1.0
TOP_K_MIN = 1
MAX_TOKENS_MIN = 1

# 工具配置
DEFAULT_TOOL_CATEGORIES = ["time", "math", "weather", "search", "translate", "file", "all"]

# 日志配置
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 错误处理配置
MAX_RETRIES = 3
RETRY_DELAY = 1.0  # 秒

# 工作流配置
DEFAULT_MAX_ITERATIONS = 10
DEFAULT_TIMEOUT = 30.0  # 秒

def validate_config():
    """验证配置参数的有效性"""
    errors = []
    
    # 验证参数范围
    if not TEMPERATURE_MIN <= DEFAULT_TEMPERATURE <= TEMPERATURE_MAX:
        errors.append(f"默认温度值 {DEFAULT_TEMPERATURE} 超出范围 [{TEMPERATURE_MIN}, {TEMPERATURE_MAX}]")
    
    if not TOP_P_MIN <= DEFAULT_TOP_P <= TOP_P_MAX:
        errors.append(f"默认Top-p值 {DEFAULT_TOP_P} 超出范围 [{TOP_P_MIN}, {TOP_P_MAX}]")
    
    if DEFAULT_TOP_K < TOP_K_MIN:
        errors.append(f"默认Top-k值 {DEFAULT_TOP_K} 小于最小值 {TOP_K_MIN}")
    
    if DEFAULT_MAX_TOKENS < MAX_TOKENS_MIN:
        errors.append(f"默认最大token数 {DEFAULT_MAX_TOKENS} 小于最小值 {MAX_TOKENS_MIN}")
    
    # 验证提供商
    if DEFAULT_PROVIDER not in SUPPORTED_PROVIDERS:
        errors.append(f"默认提供商 {DEFAULT_PROVIDER} 不在支持列表中: {SUPPORTED_PROVIDERS}")
    
    if errors:
        raise ValueError(f"配置验证失败:\n" + "\n".join(f"- {error}" for error in errors))
    
    return True

# 验证配置
try:
    validate_config()
except ValueError as e:
    print(f"配置错误: {e}")
    raise
