# 原有功能
try:
    from .agent import run_agent, agent_graph, search_web, calculate, get_weather
    from .tools.mini_contents import get_text_length, compress_text, analyze_and_compress
    from .tools.get_llm import get_llm_parameters, list_available_models, compare_models
    from .config import AGENT_NAME, OPENAI_MODEL
except ImportError:
    # 如果某些模块不存在，忽略错误
    pass

# 新的压缩Agent系统
try:
    from .tools.compression import (
        CompressionAgent, CompressionAgentConfig, CompressionResult,
        create_compression_agent, compress_text_with_agent, analyze_text_compression_potential
    )
except ImportError:
    # 如果某些模块不存在，忽略错误
    pass

# 新的通用Agent系统
try:
    from .agent.system import UniversalAgent, create_agent, ModelConfig
    from .tools.example_tools import EXAMPLE_TOOLS, get_tools_by_category
except ImportError:
    # 如果某些模块不存在，忽略错误
    pass

# 记忆Agent系统
try:
    from .agent.memory_agent import MemoryAgent, create_memory_agent, MemoryAgentConfig, MemoryItem, Rule
    from .tools.example_rules import get_rules_by_category, create_custom_rule, EXAMPLE_RULES
except ImportError:
    # 如果某些模块不存在，忽略错误
    pass

# React Agent系统
try:
    from .agent.react_agent import ReactAgent, create_react_agent, ReactAgentConfig, EnvironmentEvent, UserFeedback, AdaptiveRule, BehaviorPattern, ReactionType
    from .tools.example_adaptive_rules import get_adaptive_rules_by_category, get_behavior_patterns_by_category, create_custom_adaptive_rule, create_custom_behavior_pattern, EXAMPLE_ADAPTIVE_RULES, EXAMPLE_BEHAVIOR_PATTERNS
except ImportError:
    # 如果某些模块不存在，忽略错误
    pass

__version__ = "1.0.0"
__all__ = [
    # 原有功能
    "run_agent", "agent_graph", 
    "search_web", "calculate", "get_weather",
    "get_text_length", "compress_text", "analyze_and_compress",
    "get_llm_parameters", "list_available_models", "compare_models",
    "AGENT_NAME", "OPENAI_MODEL",
    # 新的压缩Agent系统
    "CompressionAgent", "CompressionAgentConfig", "CompressionResult",
    "create_compression_agent", "compress_text_with_agent", "analyze_text_compression_potential",
    # 新的通用Agent系统
    "UniversalAgent", "create_agent", "ModelConfig",
    "EXAMPLE_TOOLS", "get_tools_by_category",
    # 记忆Agent系统
    "MemoryAgent", "create_memory_agent", "MemoryAgentConfig", "MemoryItem", "Rule",
    "get_rules_by_category", "create_custom_rule", "EXAMPLE_RULES",
    # React Agent系统
    "ReactAgent", "create_react_agent", "ReactAgentConfig", "EnvironmentEvent", "UserFeedback", "AdaptiveRule", "BehaviorPattern", "ReactionType",
    "get_adaptive_rules_by_category", "get_behavior_patterns_by_category", "create_custom_adaptive_rule", "create_custom_behavior_pattern", "EXAMPLE_ADAPTIVE_RULES", "EXAMPLE_BEHAVIOR_PATTERNS"
] 