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

Reference Implementation v0.1 — compatible with Tang OS Specification v1.0.
See ADR-0042 RI-007 for version binding rules.
"""

import sys
from tests.conformance.conformance_harness import run_all, run_rig_tests, run_negative_tests

if __name__ == "__main__":
    args = set(sys.argv[1:])

    if "--rig" in args:
        result = run_rig_tests()
    elif "--neg" in args:
        result = run_negative_tests()
    else:
        result = run_all()

    sys.exit(0 if result.get("passed", False) else 1)
