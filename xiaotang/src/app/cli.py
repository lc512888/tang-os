"""xiaotang CLI — 命令行陪聊界面。

Usage:
    python xiaotang/app.py              # 交互模式
    python xiaotang/app.py "今天好累"    # 单条消息
"""

import sys
from xiaotang.src.services.tang_bridge import TangBridge
from xiaotang.src.conversation.service import ConversationService

PROMPT = "\033[1;36m你:\033[0m "
REPLY_PREFIX = "\033[1;33m小唐:\033[0m"
DIVIDER = "\033[90m" + "─" * 48 + "\033[0m"
ERROR_COLOR = "\033[1;31m"
RESET = "\033[0m"


def print_banner():
    """Print startup banner."""
    print()
    print("\033[1;33m  ╭" + "─" * 26 + "╮\033[0m")
    print("\033[1;33m  ┃     \U0001f375  小唐 · 轻陪聊    ┃\033[0m")
    print("\033[1;33m  ┃  Tang OS + DeepSeek 驱动  ┃\033[0m")
    print("\033[1;33m  ╰" + "─" * 26 + "╯\033[0m")
    print()
    print("  输入你的话，和小唐聊天吧。")
    print("  输入 \033[90mexit\033[0m、\033[90mquit\033[0m 或 \033[90mCtrl+C\033[0m 退出。")
    print(DIVIDER)
    print()


def check_config_and_warn(bridge: TangBridge):
    """Check DeepSeek config on startup, show warning if needed."""
    issues = bridge.check_config()
    key_issues = [i for i in issues if "DEEPSEEK_API_KEY" in i]
    if key_issues:
        print(ERROR_COLOR + "!" * 48 + RESET)
        print(ERROR_COLOR + "  DeepSeek API Key 未配置" + RESET)
        print()
        print("  请设置环境变量: export DEEPSEEK_API_KEY='sk-...'")
        print("  或从 platform.deepseek.com 获取 Key")
        print()
        print("  当前仅展示 Tang OS 决策（无 LLM 回复）" + RESET)
        print(ERROR_COLOR + "!" * 48 + RESET)
        print()


def interactive_loop(bridge: TangBridge, conversation: ConversationService):
    """Interactive chat loop."""
    print_banner()
    check_config_and_warn(bridge)

    while True:
        try:
            user_input = input(PROMPT).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            print(DIVIDER)
            print("  下次再聊 \U0001f64b")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "q"):
            print(DIVIDER)
            print("  下次再聊 \U0001f64b")
            break

        conversation.add_user_message(user_input)

        print(DIVIDER)
        result = bridge.process(user_input, history=conversation.get_context_window())
        reply = result["response"]
        print(f"{REPLY_PREFIX} {reply}")
        print(DIVIDER)
        print()

        conversation.add_assistant_message(reply)


def single_message(bridge: TangBridge, message: str):
    """Single message mode."""
    print(DIVIDER)
    print(f"你: {message}")
    result = bridge.process(message)
    print(f"小唐: {result['response']}")
    print(DIVIDER)
