"""Transparency Module — Self Description Runtime (Phase 14-D).

Machine-readable, developer-understandable, externally-verifiable system description.
Not a personality marketing module.

Usage:
    from tang_os.transparency import SystemDescriptor
    desc = SystemDescriptor().describe()
"""

from src.tang_os.transparency.descriptor import SystemDescriptor

__all__ = ["SystemDescriptor"]
