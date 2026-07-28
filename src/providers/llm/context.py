"""ExpressionContext — The input contract for all LLM Providers.

Transforms Tang OS Core's structured ResponseDecision into a complete
context that an LLM Provider can consume to generate natural language.

This is the bridge between:
    Tang OS Core (decision) → Expression Layer → LLM Provider (utterance)

Architecture principle (LP-002):
    ExpressionContext is the ONLY interface through which Tang OS Core
    output reaches an LLM. No direct Core → LLM path exists.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExpressionContext:
    """Complete context an LLM Provider needs to generate a response.

    This is a read-only data object — Providers must not modify it.
    Tang OS Core produces it; LLM Provider consumes it.

    Fields:
        response_decision: Structured decision from Tang OS Core.
            Contains detected_feeling, need, response_mode, constraints,
            candidate_intent, avoid_patterns.
        user_input: Original user message that triggered this response.
        identity: Current identity layer and constitution rules.
            e.g. {"current_layer": "companion", "constitution": [...]}
        conversation_history: Optional recent conversation turns.
        memory_context: Optional retrieved memory context.
        system_instructions: Optional personality/custom instructions.
    """

    # Required: Tang OS Core output
    response_decision: dict  # ResponseDecision as serializable dict

    # Required: Original user input
    user_input: str

    # Required: Identity context
    identity: dict

    # Optional: Conversation state
    conversation_history: list[dict] | None = None

    # Optional: Memory context (I-17: Memory ≠ Context enforced here)
    memory_context: dict | None = None

    # Optional: Extra provider-specific instructions
    system_instructions: str | None = None

    # Reserved for future fields — no breaking changes
    _metadata: dict[str, Any] = field(default_factory=dict)

    def to_chat_messages(self) -> list[dict]:
        """Convert context to standard chat message format for LLM APIs.

        This is a serialization helper, NOT a prompt template.
        Providers MAY use this or construct their own format from the raw fields.

        Returns a list of message dicts with 'role' and 'content' keys,
        compatible with OpenAI, Anthropic, and most chat-based LLM APIs.
        """
        messages = []

        # System message: identity + constraints
        system_parts = []

        # Identity layer
        layer = self.identity.get("current_layer", "companion")
        system_parts.append(f"You are currently in {layer} mode.")

        # Response mode guidance
        decision = self.response_decision
        mode = decision.get("response_mode", "comfort")
        intent = decision.get("candidate_intent", "acknowledge")
        system_parts.append(f"Response mode: {mode}. Intent: {intent}.")

        # Constraints
        constraints = decision.get("constraints", [])
        if constraints:
            system_parts.append("Constraints: " + "; ".join(constraints))

        # Avoid patterns
        avoid = decision.get("avoid_patterns", [])
        if avoid:
            system_parts.append("Do NOT use these phrases: " + ", ".join(avoid))

        # Custom instructions
        if self.system_instructions:
            system_parts.append(self.system_instructions)

        messages.append({"role": "system", "content": "\n".join(system_parts)})

        # Conversation history (if provided)
        if self.conversation_history:
            messages.extend(self.conversation_history)

        # User input
        messages.append({"role": "user", "content": self.user_input})

        return messages
