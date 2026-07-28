"""Tests for xiaotang application core components."""

import sys
import os

# Add project paths
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_SRC = os.path.join(_PROJECT_ROOT, "src")
for p in [_PROJECT_ROOT, _SRC]:
    if p not in sys.path:
        sys.path.insert(0, p)


class TestConversationService:
    def test_add_messages(self):
        from xiaotang.src.conversation.service import ConversationService
        conv = ConversationService()
        conv.add_user_message("hello")
        conv.add_assistant_message("hi")
        assert len(conv.history) == 2
        assert conv.history[0]["role"] == "user"
        assert conv.history[1]["role"] == "assistant"

    def test_context_window(self):
        from xiaotang.src.conversation.service import ConversationService
        conv = ConversationService(max_turns=2)
        for i in range(10):
            conv.add_user_message(f"msg{i}")
            conv.add_assistant_message(f"reply{i}")
        ctx = conv.get_context_window()
        assert len(ctx) <= 4  # 2 turns = 4 messages max
        assert ctx[0]["content"] == "msg8"

    def test_reset(self):
        from xiaotang.src.conversation.service import ConversationService
        conv = ConversationService()
        conv.add_user_message("hello")
        conv.add_assistant_message("hi")
        conv.reset()
        assert len(conv.history) >= 1  # keeps last message

    def test_clear(self):
        from xiaotang.src.conversation.service import ConversationService
        conv = ConversationService()
        conv.add_user_message("hello")
        conv.clear()
        assert len(conv.history) == 0


class TestTangBridge:
    def test_bridge_initializes(self):
        from xiaotang.src.services.tang_bridge import TangBridge
        bridge = TangBridge()
        assert bridge.tang is not None
        assert bridge.provider is not None
        assert bridge.provider.provider_name == "deepseek"

    def test_process_no_llm(self):
        """Without API key, bridge should return decision-only mode."""
        from xiaotang.src.services.tang_bridge import TangBridge
        bridge = TangBridge()
        result = bridge.process("今天心情不好")
        assert "decision" in result
        assert "response" in result
        assert result["provider_ok"] is False
        assert "[Tang OS" in result["response"] or result["response"] != ""

    def test_decision_contains_expected_fields(self):
        from xiaotang.src.services.tang_bridge import TangBridge
        bridge = TangBridge()
        result = bridge.process("我非常生气")
        d = result["decision"]
        assert "emotional_state" in d
        assert "response_decision" in d
        rd = d["response_decision"]
        assert hasattr(rd, "response_mode")
        assert hasattr(rd, "candidate_intent")
        assert hasattr(rd, "avoid_patterns")
