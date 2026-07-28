"""DeepSeek Chat Demo — Tang OS → DeepSeek first end-to-end loop.

Purpose:
    Prove that Tang OS can drive a real LLM through the Expression Layer.

Flow:
    User Input
        ↓
    Tang OS Core (personality + cognitive framework)
        ↓
    ResponseDecision
        ↓
    ExpressionContext → to_chat_messages()
        ↓
    DeepSeek API
        ↓
    唐先生自然语言回复

Architecture invariant:
    Tang OS decides HOW to respond (mode, intent, constraints).
    DeepSeek decides HOW TO EXPRESS in natural language.
    Provider does NOT embed personality logic.

Usage:
    export DEEPSEEK_API_KEY="sk-..."
    python examples/deepseek_chat_demo.py

    Or specify a custom message:
    python examples/deepseek_chat_demo.py "我今天很焦虑，感觉什么都做不好"
"""

import os
import sys

# Ensure project root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tang_os import Tang
from src.providers.llm import DeepSeekProvider, ExpressionContext


def main():
    # Read user input (from CLI arg or stdin)
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        user_input = input("👤 你说：")

    print(f"\n👤 用户: {user_input}")
    print("─" * 50)

    # ================================================================== #
    # Step 1: Tang OS Core — personality + cognitive processing
    # ================================================================== #
    tang = Tang()
    decision = tang.process(user_input)

    print("🧠 Tang OS Core:")
    print(f"   情绪:      {decision['emotional_state'].feeling.value}")
    print(f"   回应模式:  {decision['response_decision'].response_mode.value}")
    print(f"   意图:      {decision['response_decision'].candidate_intent}")
    if decision["response_decision"].constraints:
        print(f"   约束:      {decision['response_decision'].constraints}")
    if decision["response_decision"].avoid_patterns:
        print(f"   避免:      {decision['response_decision'].avoid_patterns}")
    print("─" * 50)

    # ================================================================== #
    # Step 2: Expression Layer — wrap decision into LLM context
    # ================================================================== #
    context = ExpressionContext(
        response_decision={
            "detected_feeling": decision["emotional_state"].feeling.value,
            "response_mode": decision["response_decision"].response_mode.value,
            "candidate_intent": decision["response_decision"].candidate_intent,
            "constraints": decision["response_decision"].constraints,
            "avoid_patterns": decision["response_decision"].avoid_patterns,
        },
        user_input=user_input,
        identity={
            "current_layer": tang.identity.current_layer.value,
        },
    )

    # ================================================================== #
    # Step 3: DeepSeek Provider — natural language generation
    # ================================================================== #
    provider = DeepSeekProvider()

    # Validate config before calling
    issues = provider.validate_config()
    if issues:
        print("❌ DeepSeek Provider 配置错误:")
        for i in issues:
            print(f"   • {i}")
        print("\n请设置环境变量: export DEEPSEEK_API_KEY='sk-...'")
        sys.exit(1)

    print("🤖 DeepSeek 生成中...")
    print("─" * 50)

    try:
        response = provider.generate(context)
        print(f"\n💬 唐先生: {response}\n")
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")
        sys.exit(1)

    # ================================================================== #
    # Summary
    # ================================================================== #
    print("─" * 50)
    print("✅ 端到端闭环完成")
    print(f"   引擎: Tang OS Core → DeepSeek ({provider._model})")
    print(f"   ADR:  ADR-0047 (LLM Provider Interface)")

    return response


if __name__ == "__main__":
    main()
