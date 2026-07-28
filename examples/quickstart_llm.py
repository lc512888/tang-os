"""Minimal Tang OS + LLM quickstart.

This is the SIMPLEST example showing the full pipeline:
Tang OS Core -> ExpressionContext -> LLM Provider -> Natural Language Reply

Prerequisites:
    pip install openai
    export DEEPSEEK_API_KEY="sk-..."

Usage:
    python examples/quickstart_llm.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tang_os import Tang
from src.providers.llm import DeepSeekProvider, ExpressionContext


def main():
    # 1. Tang OS Core: personality decision
    tang = Tang()
    decision = tang.process("我最近压力很大，感觉快撑不住了。")
    rd = decision["response_decision"]

    print("--- Tang OS Decision ---")
    print(f"  Emotion:     {decision['emotional_state'].feeling.value}")
    print(f"  Mode:        {rd.response_mode.value}")
    print(f"  Intent:      {rd.candidate_intent}")
    print(f"  Avoid these: {rd.avoid_patterns}")
    print()

    # 2. Build context for LLM
    ctx = ExpressionContext(
        response_decision={
            "detected_feeling": decision["emotional_state"].feeling.value,
            "response_mode": rd.response_mode.value,
            "candidate_intent": rd.candidate_intent,
            "constraints": rd.constraints,
            "avoid_patterns": rd.avoid_patterns,
        },
        user_input="我最近压力很大，感觉快撑不住了。",
        identity={"current_layer": tang.identity.current_layer.value},
    )

    # 3. LLM generates natural language
    provider = DeepSeekProvider()

    issues = provider.validate_config()
    if issues:
        print("ERROR: DeepSeek not configured.")
        for i in issues:
            print(f"  - {i}")
        print("\nSet: export DEEPSEEK_API_KEY='sk-...'")
        sys.exit(1)

    reply = provider.generate(ctx)
    print("--- Tang OS Reply ---")
    print(f"  {reply}")
    print()

    print("Done. Tang OS + LLM pipeline works.")


if __name__ == "__main__":
    main()
