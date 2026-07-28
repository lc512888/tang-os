"""Conversation Service — 多轮对话管理。

职责:
    - 管理对话历史
    - 上下文窗口裁剪
    - 提供历史给 Tang OS Bridge

非职责:
    - 不包含人格逻辑
    - 不修改 Tang OS 决策
    - 不替代 Tang OS Memory Runtime
"""


class ConversationService:
    """轻量对话管理器。

    管理用户和助手之间的多轮对话历史。
    仅保留最近 N 轮，防止上下文溢出。
    """

    def __init__(self, max_turns: int = 10):
        self._history: list[dict] = []
        self._max_turns = max_turns

    @property
    def history(self) -> list[dict]:
        """获取当前对话历史（只读视图）。"""
        return list(self._history)

    def add_user_message(self, message: str):
        """记录用户消息。"""
        self._history.append({"role": "user", "content": message})

    def add_assistant_message(self, message: str):
        """记录助理回复。"""
        self._history.append({"role": "assistant", "content": message})

    def get_context_window(self) -> list[dict]:
        """获取最近 N 轮对话作为上下文。

        Returns:
            适合传入 ExpressionContext.conversation_history 的列表。
        """
        if len(self._history) > self._max_turns * 2:
            return self._history[-(self._max_turns * 2):]
        return self._history

    def reset(self):
        """重置对话（保留最近一轮作为上下文种子）。"""
        if self._history:
            # 保留最后一条用户消息作为上下文衔接
            last = self._history[-1]
            self._history = [last]
        else:
            self._history = []

    def clear(self):
        """清空所有历史。"""
        self._history = []
