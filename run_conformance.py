#!/usr/bin/env python3
"""Tang OS Conformance Harness — Entry point for third-party reproducibility.

Usage:
    python run_conformance.py          # Full suite
    python run_conformance.py --rig    # RIG gates only
    python run_conformance.py --neg    # Negative tests only

Install:
    pip install -e .
    from tang_os import Tang

Exit code: 0 = CONFORMANT, 1 = NON-CONFORMANT

Reference Implementation v0.2 — compatible with Tang OS Specification v1.0.
See ADR-0042 RI-007 for version binding rules.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "src"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(SOURCE))

from tang_os.version import __version__  # noqa: E402
from tests.conformance.conformance_harness import (  # noqa: E402
    run_all, run_negative_tests, run_rig_tests,
)


def _verify_checkout_version() -> None:
    expected = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if __version__ != expected or expected != "0.2.0":
        raise SystemExit(
            f"Checkout/version mismatch: expected 0.2.0, VERSION={expected!r}, "
            f"imported={__version__!r}"
        )

if __name__ == "__main__":
    _verify_checkout_version()
    args = set(sys.argv[1:])

    if "--rig" in args:
        result = run_rig_tests()
    elif "--neg" in args:
        result = run_negative_tests()
    else:
        result = run_all()

    sys.exit(0 if result.get("passed", False) else 1)
