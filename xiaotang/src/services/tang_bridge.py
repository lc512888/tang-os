"""Tang OS Bridge — xiaotang 调用 Tang OS Core 的唯一入口。

遵循 ADR-0001:
    xiaotang 不拥有人格逻辑，通过此桥调用 Tang OS Core。
    Tang OS Core 不在 xiaotang 中被修改或绕过。
"""

from tang_os import Tang
from src.providers.llm import DeepSeekProvider, ExpressionContext
from src.providers.llm.deepseek_provider import ProviderError, ProviderConfigError


class TangBridge:
    """Tang OS 调用桥 — 人格决策 + LLM 生成。

    职责:
        1. 调用 Tang.process() 获取人格决策
        2. 包装 ExpressionContext
        3. 调用 LLM Provider 生成自然语言

    非职责:
        - 不修改 Tang OS Core
        - 不复制人格逻辑
        - 不绕过 Decision Layer
    """

    def __init__(self):
        self.tang = Tang()
        self.provider = DeepSeekProvider()

    def check_config(self) -> list[str]:
        """检查 LLM Provider 配置，返回问题列表。"""
        return self.provider.validate_config()

    def process(self, user_input: str, history: list[dict] | None = None) -> dict:
        """完整处理一条用户消息。

        Args:
            user_input: 用户输入文本。
            history: 可选对话历史。

        Returns:
            dict with keys:
                - decision: Tang OS 原始决策
                - response: LLM 生成回复（或决策展示）
                - provider_ok: bool, LLM 是否可用
        """
        # Step 1: Tang OS Core 人格决策
        decision = self.tang.process(user_input)
        rd = decision["response_decision"]

        # Step 2: 包装 ExpressionContext
        ctx = ExpressionContext(
            response_decision={
                "detected_feeling": decision["emotional_state"].feeling.value,
                "response_mode": rd.response_mode.value,
                "candidate_intent": rd.candidate_intent,
                "constraints": rd.constraints,
                "avoid_patterns": rd.avoid_patterns,
            },
            user_input=user_input,
            identity={
                "current_layer": self.tang.identity.current_layer.value,
            },
            conversation_history=history,
        )

        # Step 3: LLM 生成
        issues = self.check_config()
        provider_ok = not any("DEEPSEEK_API_KEY" in i for i in issues)

        if not provider_ok:
            return {
                "decision": decision,
                "response": self._format_decision(decision),
                "provider_ok": False,
            }

        try:
            reply = self.provider.generate(ctx)
            return {
                "decision": decision,
                "response": reply,
                "provider_ok": True,
            }
        except (ProviderError, ProviderConfigError) as e:
            return {
                "decision": decision,
                "response": f"[生成回复失败: {e}]",
                "provider_ok": False,
                "error": str(e),
            }

    @staticmethod
    def _format_decision(decision: dict) -> str:
        """无 LLM 时展示 Tang OS 决策。"""
        es = decision["emotional_state"]
        rd = decision["response_decision"]
        parts = [
            "[Tang OS 决策]",
            f"  情绪: {es.feeling.value}",
            f"  回应模式: {rd.response_mode.value}",
            f"  意图: {rd.candidate_intent}",
        ]
        if rd.constraints:
            parts.append(f"  约束: {'; '.join(rd.constraints)}")
        if rd.avoid_patterns:
            parts.append(f"  避免: {', '.join(rd.avoid_patterns[:3])}...")
        return "\n".join(parts)
