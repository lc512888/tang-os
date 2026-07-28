"""xiaotang -- Tang OS app layer: lightweight companion chat.

Architecture: ADR-0001

Usage:
    python xiaotang/app.py
    python xiaotang/app.py "zui jin hen lei"

First run:
    export DEEPSEEK_API_KEY="sk-..."
"""

import sys
import os

# Tang OS uses "from src.tang_os import ..." style imports.
# The project root (parent of src/) must be on sys.path.
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from xiaotang.src.app.cli import interactive_loop, single_message
from xiaotang.src.services.tang_bridge import TangBridge
from xiaotang.src.conversation.service import ConversationService


def main():
    bridge = TangBridge()
    conversation = ConversationService()

    if len(sys.argv) > 1:
        single_message(bridge, sys.argv[1])
    else:
        interactive_loop(bridge, conversation)


if __name__ == "__main__":
    main()
