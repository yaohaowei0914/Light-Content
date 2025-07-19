from typing import Dict, List, Any, Optional, TypedDict, Annotated, Union, Callable
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from pydantic import BaseModel, Field
import json
import logging
from datetime import datetime, timedelta
from enum import Enum
from ..config import (
    DEFAULT_MODEL_NAME, DEFAULT_TEMPERATURE, DEFAULT_TOP_P, DEFAULT_TOP_K, 
    DEFAULT_MAX_TOKENS, DEFAULT_PROVIDER, SUPPORTED_PROVIDERS,
    TEMPERATURE_MIN, TEMPERATURE_MAX, TOP_P_MIN, TOP_P_MAX, 
    TOP_K_MIN, MAX_TOKENS_MIN, LOG_LEVEL, LOG_FORMAT
)

# 配置日志
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)

class ReactionType(Enum):
    """反应类型"""
    POSITIVE = "positive"      # 正面反应
    NEGATIVE = "negative"      # 负面反应
    NEUTRAL = "neutral"        # 中性反应
    CORRECTION = "correction"  # 纠正反应
    CLARIFICATION = "clarification"  # 澄清反应

class EnvironmentEvent(BaseModel):
    """环境事件"""
    event_type: str = Field(description="事件类型")
    description: str = Field(description="事件描述")
    timestamp: datetime = Field(default_factory=datetime.now, description="事件时间")
    severity: float = Field(default=0.5, ge=0.0, le=1.0, description="严重程度")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")

class UserFeedback(BaseModel):
    """用户反馈"""
    feedback_type: ReactionType = Field(description="反馈类型")
    content: str = Field(description="反馈内容")
    timestamp: datetime = Field(default_factory=datetime.now, description="反馈时间")
    confidence: float = Field(default=0.5, ge=0.0, le=1.0, description="置信度")
    context: Dict[str, Any] = Field(default_factory=dict, description="上下文信息")

class AdaptiveRule(BaseModel):
    """自适应规则"""
    name: str = Field(description="规则名称")
    description: str = Field(description="规则描述")
    condition: str = Field(description="触发条件")
    action: str = Field(description="执行动作")
    priority: int = Field(default=5, ge=1, le=10, description="优先级")
    active: bool = Field(default=True, description="是否激活")
    adaptation_factor: float = Field(default=1.0, ge=0.0, le=2.0, description="适应因子")

class BehaviorPattern(BaseModel):
    """行为模式"""
    pattern_name: str = Field(description="模式名称")
    description: str = Field(description="模式描述")
    triggers: List[str] = Field(description="触发条件列表")
    responses: List[str] = Field(description="响应模板列表")
    success_rate: float = Field(default=0.5, ge=0.0, le=1.0, description="成功率")
    usage_count: int = Field(default=0, description="使用次数")
    last_used: Optional[datetime] = Field(default=None, description="最后使用时间")

class ReactAgentState(TypedDict):
    """React Agent状态定义"""
    # 基础组件
    messages: Annotated[List[BaseMessage], "对话消息列表"]
    tools: Annotated[List[BaseTool], "可用工具列表"]
    
    # 反应组件
    environment_events: Annotated[List[EnvironmentEvent], "环境事件列表"]
    user_feedback: Annotated[List[UserFeedback], "用户反馈列表"]
    adaptive_rules: Annotated[List[AdaptiveRule], "自适应规则列表"]
    behavior_patterns: Annotated[List[BehaviorPattern], "行为模式列表"]
    
    # 状态组件
    current_context: Annotated[Dict[str, Any], "当前上下文"]
    reaction_history: Annotated[List[Dict[str, Any]], "反应历史"]
    adaptation_level: Annotated[float, "适应水平"]
    
    # 配置组件
    model_config: Annotated[Dict[str, Any], "模型配置参数"]
    current_step: Annotated[str, "当前执行步骤"]
    error: Annotated[Optional[str], "错误信息"]
    
    # 输出组件
    output_text: Annotated[Optional[str], "最终输出文本"]
    reaction_applied: Annotated[Optional[str], "应用的反应"]

class ReactAgentConfig(BaseModel):
    """React Agent配置参数"""
    model_name: str = Field(default=DEFAULT_MODEL_NAME, description="模型名称")
    temperature: float = Field(default=DEFAULT_TEMPERATURE, description="温度参数", ge=TEMPERATURE_MIN, le=TEMPERATURE_MAX)
    top_p: float = Field(default=DEFAULT_TOP_P, description="Top-p参数", ge=TOP_P_MIN, le=TOP_P_MAX)
    top_k: int = Field(default=DEFAULT_TOP_K, description="Top-k参数", ge=TOP_K_MIN)
    max_tokens: int = Field(default=DEFAULT_MAX_TOKENS, description="最大token数", ge=MAX_TOKENS_MIN)
    provider: str = Field(default=DEFAULT_PROVIDER, description=f"模型提供商: {', '.join(SUPPORTED_PROVIDERS)}")
    
    # 反应相关配置
    max_environment_events: int = Field(default=50, description="最大环境事件数量")
    max_user_feedback: int = Field(default=100, description="最大用户反馈数量")
    max_adaptive_rules: int = Field(default=30, description="最大自适应规则数量")
    max_behavior_patterns: int = Field(default=20, description="最大行为模式数量")
    
    # 适应相关配置
    adaptation_threshold: float = Field(default=0.3, description="适应阈值")
    learning_rate: float = Field(default=0.1, description="学习率")
    feedback_weight: float = Field(default=0.7, description="反馈权重")
    event_weight: float = Field(default=0.3, description="事件权重")

class ReactAgent:
    """能够根据环境变化和用户反馈动态调整行为的智能Agent"""
    
    def __init__(self, config: Optional[ReactAgentConfig] = None):
        """
        初始化React Agent
        
        Args:
            config: Agent配置参数
        """
        self.config = config or ReactAgentConfig()
        self.llm = self._create_llm()
        self.tools: List[BaseTool] = []
        self.environment_events: List[EnvironmentEvent] = []
        self.user_feedback: List[UserFeedback] = []
        self.adaptive_rules: List[AdaptiveRule] = []
        self.behavior_patterns: List[BehaviorPattern] = []
        self.graph = self._build_graph()
        
    def _create_llm(self):
        """根据配置创建LLM实例"""
        if self.config.provider == "openai":
            return ChatOpenAI(
                model=self.config.model_name,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                top_p=self.config.top_p,
                top_k=self.config.top_k
            )
        elif self.config.provider == "ollama":
            return Ollama(
                model=self.config.model_name,
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                top_k=self.config.top_k
            )
        else:
            raise ValueError(f"不支持的模型提供商: {self.config.provider}。支持的提供商: {', '.join(SUPPORTED_PROVIDERS)}")
    
    def add_tool(self, tool: BaseTool):
        """添加工具到agent"""
        self.tools.append(tool)
        logger.info(f"添加工具: {tool.name}")
    
    def add_tools(self, tools: List[BaseTool]):
        """批量添加工具"""
        for tool in tools:
            self.add_tool(tool)
    
    def add_environment_event(self, event_type: str, description: str, severity: float = 0.5, metadata: Dict[str, Any] = None):
        """添加环境事件"""
        if len(self.environment_events) >= self.config.max_environment_events:
            # 移除最旧的事件
            self.environment_events.pop(0)
        
        event = EnvironmentEvent(
            event_type=event_type,
            description=description,
            severity=severity,
            metadata=metadata or {}
        )
        self.environment_events.append(event)
        logger.info(f"添加环境事件: {event_type} - {description}")
    
    def add_user_feedback(self, feedback_type: ReactionType, content: str, confidence: float = 0.5, context: Dict[str, Any] = None):
        """添加用户反馈"""
        if len(self.user_feedback) >= self.config.max_user_feedback:
            # 移除最旧的反馈
            self.user_feedback.pop(0)
        
        feedback = UserFeedback(
            feedback_type=feedback_type,
            content=content,
            confidence=confidence,
            context=context or {}
        )
        self.user_feedback.append(feedback)
        logger.info(f"添加用户反馈: {feedback_type.value} - {content}")
    
    def add_adaptive_rule(self, rule: AdaptiveRule):
        """添加自适应规则"""
        if len(self.adaptive_rules) >= self.config.max_adaptive_rules:
            # 移除优先级最低的规则
            self.adaptive_rules.sort(key=lambda x: x.priority)
            self.adaptive_rules.pop(0)
        
        self.adaptive_rules.append(rule)
        logger.info(f"添加自适应规则: {rule.name}")
    
    def add_behavior_pattern(self, pattern: BehaviorPattern):
        """添加行为模式"""
        if len(self.behavior_patterns) >= self.config.max_behavior_patterns:
            # 移除成功率最低的模式
            self.behavior_patterns.sort(key=lambda x: x.success_rate)
            self.behavior_patterns.pop(0)
        
        self.behavior_patterns.append(pattern)
        logger.info(f"添加行为模式: {pattern.pattern_name}")
    
    def analyze_context(self, current_message: str) -> Dict[str, Any]:
        """分析当前上下文"""
        context = {
            "recent_events": [],
            "recent_feedback": [],
            "applicable_rules": [],
            "matching_patterns": [],
            "adaptation_needed": False
        }
        
        # 分析最近的环境事件
        recent_events = self.environment_events[-5:] if self.environment_events else []
        context["recent_events"] = [
            {
                "type": event.event_type,
                "description": event.description,
                "severity": event.severity,
                "time": event.timestamp.isoformat()
            }
            for event in recent_events
        ]
        
        # 分析最近的用户反馈
        recent_feedback = self.user_feedback[-5:] if self.user_feedback else []
        context["recent_feedback"] = [
            {
                "type": feedback.feedback_type.value,
                "content": feedback.content,
                "confidence": feedback.confidence,
                "time": feedback.timestamp.isoformat()
            }
            for feedback in recent_feedback
        ]
        
        # 查找适用的自适应规则
        applicable_rules = []
        for rule in self.adaptive_rules:
            if rule.active and self._evaluate_rule_condition(rule, current_message, context):
                applicable_rules.append({
                    "name": rule.name,
                    "action": rule.action,
                    "priority": rule.priority,
                    "adaptation_factor": rule.adaptation_factor
                })
        
        context["applicable_rules"] = sorted(applicable_rules, key=lambda x: x["priority"], reverse=True)
        
        # 查找匹配的行为模式
        matching_patterns = []
        for pattern in self.behavior_patterns:
            if self._evaluate_pattern_triggers(pattern, current_message, context):
                matching_patterns.append({
                    "name": pattern.pattern_name,
                    "responses": pattern.responses,
                    "success_rate": pattern.success_rate,
                    "usage_count": pattern.usage_count
                })
        
        context["matching_patterns"] = sorted(matching_patterns, key=lambda x: x["success_rate"], reverse=True)
        
        # 判断是否需要适应
        adaptation_score = self._calculate_adaptation_score(context)
        context["adaptation_needed"] = adaptation_score > self.config.adaptation_threshold
        context["adaptation_score"] = adaptation_score
        
        return context
    
    def _evaluate_rule_condition(self, rule: AdaptiveRule, message: str, context: Dict[str, Any]) -> bool:
        """评估规则条件"""
        # 简单的关键词匹配，实际应用中可以使用更复杂的逻辑
        condition_lower = rule.condition.lower()
        message_lower = message.lower()
        
        # 检查消息中是否包含条件关键词
        if any(keyword in message_lower for keyword in condition_lower.split()):
            return True
        
        # 检查上下文中的事件和反馈
        for event in context["recent_events"]:
            if any(keyword in event["description"].lower() for keyword in condition_lower.split()):
                return True
        
        for feedback in context["recent_feedback"]:
            if any(keyword in feedback["content"].lower() for keyword in condition_lower.split()):
                return True
        
        return False
    
    def _evaluate_pattern_triggers(self, pattern: BehaviorPattern, message: str, context: Dict[str, Any]) -> bool:
        """评估模式触发条件"""
        message_lower = message.lower()
        
        for trigger in pattern.triggers:
            if trigger.lower() in message_lower:
                return True
        
        return False
    
    def _calculate_adaptation_score(self, context: Dict[str, Any]) -> float:
        """计算适应分数"""
        score = 0.0
        
        # 基于环境事件的分数
        for event in context["recent_events"]:
            score += event["severity"] * self.config.event_weight
        
        # 基于用户反馈的分数
        for feedback in context["recent_feedback"]:
            if feedback["type"] in ["negative", "correction"]:
                score += feedback["confidence"] * self.config.feedback_weight
            elif feedback["type"] == "positive":
                score -= feedback["confidence"] * self.config.feedback_weight * 0.5
        
        # 基于适用规则的分数
        score += len(context["applicable_rules"]) * 0.1
        
        return min(score, 1.0)
    
    def adapt_behavior(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """适应行为"""
        adaptation = {
            "temperature_adjustment": 0.0,
            "response_style": "normal",
            "tool_preference": [],
            "confidence_level": 0.5,
            "adaptation_reason": []
        }
        
        # 根据用户反馈调整温度
        negative_feedback_count = sum(1 for f in context["recent_feedback"] if f["type"] == "negative")
        positive_feedback_count = sum(1 for f in context["recent_feedback"] if f["type"] == "positive")
        
        if negative_feedback_count > positive_feedback_count:
            adaptation["temperature_adjustment"] = -0.2
            adaptation["adaptation_reason"].append("用户反馈偏向负面，降低创造性")
        elif positive_feedback_count > negative_feedback_count:
            adaptation["temperature_adjustment"] = 0.1
            adaptation["adaptation_reason"].append("用户反馈偏向正面，适度提高创造性")
        
        # 根据环境事件调整响应风格
        high_severity_events = [e for e in context["recent_events"] if e["severity"] > 0.7]
        if high_severity_events:
            adaptation["response_style"] = "cautious"
            adaptation["adaptation_reason"].append("检测到高严重性环境事件，采用谨慎响应风格")
        
        # 根据适用规则调整行为
        for rule in context["applicable_rules"]:
            adaptation["adaptation_reason"].append(f"应用规则: {rule['name']}")
        
        # 根据匹配模式调整工具偏好
        if context["matching_patterns"]:
            top_pattern = context["matching_patterns"][0]
            adaptation["confidence_level"] = min(top_pattern["success_rate"] + 0.2, 1.0)
            adaptation["adaptation_reason"].append(f"匹配行为模式: {top_pattern['name']}")
        
        return adaptation
    
    def update_model_config(self, **kwargs):
        """更新模型配置"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        
        # 重新创建LLM实例
        self.llm = self._create_llm()
        logger.info(f"更新模型配置: {kwargs}")
    
    def _should_continue(self, state: ReactAgentState) -> str:
        """判断是否继续执行"""
        last_message = state["messages"][-1]
        
        # 如果最后一条消息是工具调用，继续执行
        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            return "tools"
        
        # 如果最后一条消息是工具结果，继续执行
        if isinstance(last_message, ToolMessage):
            return "agent"
        
        # 否则结束
        return END
    
    def _analyze_and_adapt(self, state: ReactAgentState) -> ReactAgentState:
        """分析和适应"""
        try:
            # 获取当前用户消息
            user_messages = [msg for msg in state["messages"] if isinstance(msg, HumanMessage)]
            if not user_messages:
                return state
            
            current_message = user_messages[-1].content
            
            # 分析上下文
            context = self.analyze_context(current_message)
            state["current_context"] = context
            
            # 适应行为
            adaptation = self.adapt_behavior(context)
            
            # 更新适应水平
            state["adaptation_level"] = context["adaptation_score"]
            
            # 记录反应历史
            reaction_record = {
                "timestamp": datetime.now().isoformat(),
                "message": current_message,
                "context": context,
                "adaptation": adaptation,
                "adaptation_level": state["adaptation_level"]
            }
            state["reaction_history"].append(reaction_record)
            
            # 限制反应历史数量
            if len(state["reaction_history"]) > 50:
                state["reaction_history"] = state["reaction_history"][-50:]
            
            state["current_step"] = "analyzed_and_adapted"
            logger.info(f"分析和适应完成，适应水平: {state['adaptation_level']:.2f}")
            
            return state
            
        except Exception as e:
            error_msg = f"分析和适应失败: {str(e)}"
            logger.error(error_msg)
            state["error"] = error_msg
            return state
    
    def _call_model(self, state: ReactAgentState) -> ReactAgentState:
        """调用模型生成响应"""
        try:
            # 获取当前上下文和适应信息
            context = state.get("current_context", {})
            adaptation = context.get("adaptation", {})
            
            # 准备系统消息
            system_content = f"""你是一个能够根据环境变化和用户反馈动态调整行为的智能助手。

当前上下文:
- 环境事件: {len(context.get('recent_events', []))} 个
- 用户反馈: {len(context.get('recent_feedback', []))} 个
- 适用规则: {len(context.get('applicable_rules', []))} 个
- 匹配模式: {len(context.get('matching_patterns', []))} 个
- 适应水平: {state.get('adaptation_level', 0):.2f}

行为适应:
- 温度调整: {adaptation.get('temperature_adjustment', 0):+.2f}
- 响应风格: {adaptation.get('response_style', 'normal')}
- 置信水平: {adaptation.get('confidence_level', 0.5):.2f}
- 适应原因: {', '.join(adaptation.get('adaptation_reason', []))}

请根据以上信息提供智能、适应性的回答。"""
            
            system_message = SystemMessage(content=system_content)
            
            # 调整模型参数
            adjusted_temperature = max(0.0, min(2.0, self.config.temperature + adaptation.get("temperature_adjustment", 0)))
            adjusted_llm = ChatOpenAI(
                model=self.config.model_name,
                temperature=adjusted_temperature,
                max_tokens=self.config.max_tokens,
                top_p=self.config.top_p,
                top_k=self.config.top_k
            )
            
            # 绑定工具到LLM
            llm_with_tools = adjusted_llm.bind_tools(self.tools)
            
            # 准备消息列表
            messages = [system_message] + state["messages"]
            
            # 调用模型
            response = llm_with_tools.invoke(messages)
            
            # 添加AI响应到消息列表
            state["messages"].append(response)
            state["current_step"] = "model_response"
            
            logger.info("模型响应生成成功")
            return state
            
        except Exception as e:
            error_msg = f"模型调用失败: {str(e)}"
            logger.error(error_msg)
            state["error"] = error_msg
            return state
    
    def _call_tools(self, state: ReactAgentState) -> ReactAgentState:
        """调用工具"""
        try:
            # 使用ToolNode处理工具调用
            tool_node = ToolNode(self.tools)
            result = tool_node.invoke(state)
            
            # 更新状态
            state["messages"] = result["messages"]
            state["current_step"] = "tool_execution"
            
            logger.info("工具执行完成")
            return state
            
        except Exception as e:
            error_msg = f"工具调用失败: {str(e)}"
            logger.error(error_msg)
            state["error"] = error_msg
            return state
    
    def _generate_output(self, state: ReactAgentState) -> ReactAgentState:
        """生成最终输出文本"""
        try:
            # 从最后一条AI消息中提取内容
            ai_messages = [msg for msg in state["messages"] if isinstance(msg, AIMessage)]
            if ai_messages:
                last_ai_message = ai_messages[-1]
                state["output_text"] = last_ai_message.content
            else:
                state["output_text"] = "无法生成响应"
            
            # 记录应用的反应
            context = state.get("current_context", {})
            adaptation = context.get("adaptation", {})
            state["reaction_applied"] = f"适应水平: {state.get('adaptation_level', 0):.2f}, 响应风格: {adaptation.get('response_style', 'normal')}"
            
            state["current_step"] = "output_generated"
            logger.info("输出文本生成完成")
            return state
            
        except Exception as e:
            error_msg = f"输出生成失败: {str(e)}"
            logger.error(error_msg)
            state["error"] = error_msg
            return state
    
    def _build_graph(self) -> StateGraph:
        """构建LangGraph工作流"""
        workflow = StateGraph(ReactAgentState)
        
        # 添加节点
        workflow.add_node("analyze", self._analyze_and_adapt)
        workflow.add_node("agent", self._call_model)
        workflow.add_node("tools", self._call_tools)
        workflow.add_node("output", self._generate_output)
        
        # 设置入口点
        workflow.set_entry_point("analyze")
        
        # 添加边
        workflow.add_edge("analyze", "agent")
        
        # 添加条件边
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "tools": "tools",
                END: "output"
            }
        )
        
        workflow.add_conditional_edges(
            "tools",
            self._should_continue,
            {
                "agent": "agent",
                END: "output"
            }
        )
        
        # 输出节点直接结束
        workflow.add_edge("output", END)
        
        return workflow.compile()
    
    def run(self, message: str, tools: Optional[List[BaseTool]] = None) -> Dict[str, Any]:
        """
        运行React Agent
        
        Args:
            message: 用户输入消息
            tools: 可选的工具列表（会覆盖已添加的工具）
        
        Returns:
            执行结果
        """
        # 准备工具列表
        if tools is not None:
            current_tools = tools
        else:
            current_tools = self.tools
        
        # 初始化状态
        initial_state = ReactAgentState(
            messages=[HumanMessage(content=message)],
            tools=current_tools,
            environment_events=self.environment_events.copy(),
            user_feedback=self.user_feedback.copy(),
            adaptive_rules=self.adaptive_rules.copy(),
            behavior_patterns=self.behavior_patterns.copy(),
            current_context={},
            reaction_history=[],
            adaptation_level=0.0,
            model_config=self.config.dict(),
            current_step="start",
            error=None,
            output_text=None,
            reaction_applied=None
        )
        
        try:
            # 执行工作流
            result = self.graph.invoke(initial_state)
            
            return {
                "success": True,
                "response": result["output_text"],
                "messages": result["messages"],
                "current_step": result["current_step"],
                "error": result.get("error"),
                "adaptation_level": result["adaptation_level"],
                "reaction_applied": result["reaction_applied"],
                "context_analysis": result["current_context"],
                "environment_events_count": len(result["environment_events"]),
                "user_feedback_count": len(result["user_feedback"]),
                "adaptive_rules_count": len(result["adaptive_rules"]),
                "behavior_patterns_count": len(result["behavior_patterns"])
            }
            
        except Exception as e:
            error_msg = f"React Agent执行失败: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "response": None,
                "messages": initial_state["messages"],
                "current_step": "error",
                "error": error_msg,
                "adaptation_level": 0.0,
                "reaction_applied": None,
                "context_analysis": {},
                "environment_events_count": 0,
                "user_feedback_count": 0,
                "adaptive_rules_count": 0,
                "behavior_patterns_count": 0
            }
    
    def get_config(self) -> Dict[str, Any]:
        """获取当前配置"""
        return {
            "model_config": self.config.dict(),
            "tools": [tool.name for tool in self.tools],
            "adaptive_rules": [rule.name for rule in self.adaptive_rules if rule.active],
            "behavior_patterns": [pattern.pattern_name for pattern in self.behavior_patterns],
            "environment_events_count": len(self.environment_events),
            "user_feedback_count": len(self.user_feedback),
            "graph_nodes": list(self.graph.nodes.keys())
        }
    
    def get_adaptation_stats(self) -> Dict[str, Any]:
        """获取适应统计信息"""
        if not self.user_feedback:
            return {"average_adaptation": 0.0, "feedback_distribution": {}}
        
        # 计算平均适应水平
        adaptation_scores = []
        for feedback in self.user_feedback:
            if feedback.feedback_type in [ReactionType.NEGATIVE, ReactionType.CORRECTION]:
                adaptation_scores.append(feedback.confidence)
            elif feedback.feedback_type == ReactionType.POSITIVE:
                adaptation_scores.append(-feedback.confidence * 0.5)
        
        average_adaptation = sum(adaptation_scores) / len(adaptation_scores) if adaptation_scores else 0.0
        
        # 反馈分布
        feedback_distribution = {}
        for feedback_type in ReactionType:
            count = sum(1 for f in self.user_feedback if f.feedback_type == feedback_type)
            feedback_distribution[feedback_type.value] = count
        
        return {
            "average_adaptation": average_adaptation,
            "feedback_distribution": feedback_distribution,
            "total_feedback": len(self.user_feedback),
            "total_events": len(self.environment_events)
        }
    
    def clear_history(self, clear_type: str = "all"):
        """清除历史记录"""
        if clear_type in ["all", "events"]:
            self.environment_events.clear()
            logger.info("清除环境事件历史")
        
        if clear_type in ["all", "feedback"]:
            self.user_feedback.clear()
            logger.info("清除用户反馈历史")
        
        if clear_type in ["all", "rules"]:
            self.adaptive_rules.clear()
            logger.info("清除自适应规则")
        
        if clear_type in ["all", "patterns"]:
            self.behavior_patterns.clear()
            logger.info("清除行为模式")

# 便捷函数
def create_react_agent(
    model_name: str = DEFAULT_MODEL_NAME,
    temperature: float = DEFAULT_TEMPERATURE,
    top_p: float = DEFAULT_TOP_P,
    top_k: int = DEFAULT_TOP_K,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    provider: str = DEFAULT_PROVIDER,
    tools: Optional[List[BaseTool]] = None,
    adaptive_rules: Optional[List[AdaptiveRule]] = None,
    behavior_patterns: Optional[List[BehaviorPattern]] = None
) -> ReactAgent:
    """
    创建React Agent的便捷函数
    
    Args:
        model_name: 模型名称
        temperature: 温度参数
        top_p: Top-p参数
        top_k: Top-k参数
        max_tokens: 最大token数
        provider: 模型提供商
        tools: 工具列表
        adaptive_rules: 自适应规则列表
        behavior_patterns: 行为模式列表
    
    Returns:
        ReactAgent实例
    """
    config = ReactAgentConfig(
        model_name=model_name,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        max_tokens=max_tokens,
        provider=provider
    )
    
    agent = ReactAgent(config)
    
    if tools:
        agent.add_tools(tools)
    
    if adaptive_rules:
        for rule in adaptive_rules:
            agent.add_adaptive_rule(rule)
    
    if behavior_patterns:
        for pattern in behavior_patterns:
            agent.add_behavior_pattern(pattern)
    
    return agent 