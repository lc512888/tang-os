"""Tang OS Conformance Harness — B0-002.

Maps Specification requirements (Spec ID → Test Case) and
runs all RIG gates + negative tests automatically.

Usage:
    python -m tests.conformance.conformance_harness

Third-party reproducibility:
    python -m tests.conformance.conformance_harness --rig-only
    python -m tests.conformance.conformance_harness --negative-only
"""

import sys
import os
import json
from datetime import datetime

# Ensure project root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

# ── Compliance Matrix: Spec ID → Test Case mapping ──────────────────────

COMPLIANCE_MATRIX = {
    "SPEC-000": {"requirement": "Purpose", "tests": ["test_rig::TestRIG001_SpecBinding"], "gate": "RIG-001"},
    "SPEC-001": {"requirement": "Specification Boundary", "tests": ["test_rig::TestRIG004_DefinitionNotImplementation"], "gate": "RIG-004"},
    "SPEC-002": {"requirement": "Implementation Independence", "tests": ["test_rig::TestRIG006_ImplementationIndependence"], "gate": "RIG-006"},
    "SPEC-100": {"requirement": "Tang OS Positioning", "tests": ["test_rig::TestRIG001_SpecBinding::test_spec_version_declared"], "gate": "RIG-001"},
    "SPEC-200": {"requirement": "Identity Constitution", "tests": ["test_negative::TestReject_IdentityModification", "test_rig::TestRIG002_IdentityProtection"], "gate": "RIG-002"},
    "SPEC-300": {"requirement": "Invariant System", "tests": ["test_negative::TestReject_InvariantBypass"], "gate": "RIG-003"},
    "SPEC-400": {"requirement": "Decision Model", "tests": ["test_negative::TestReject_InvariantBypass::test_reject_prescribed_decision"], "gate": "RIG-003"},
    "SPEC-500": {"requirement": "Safety Model", "tests": ["test_rig::TestRIG003_NegativeTestPriority::test_rejects_above_ceiling"], "gate": "RIG-004"},
    "SPEC-600": {"requirement": "Memory Boundary", "tests": ["test_negative::TestReject_MemoryPollution"], "gate": "RIG-003"},
    "SPEC-700": {"requirement": "Personality Interface", "tests": ["test_rig::TestRIG003_NegativeTestPriority"], "gate": "RIG-003"},
    "SPEC-800": {"requirement": "Capability Classification", "tests": ["test_negative::TestReject_UnauthorisedCapability"], "gate": "RIG-003"},
    "SPEC-901": {"requirement": "Change Policy", "tests": ["test_rig::TestRIG007_VersionBinding"], "gate": "RIG-007"},
}


def run_pytest(pattern: str = "") -> dict:
    """Run pytest and collect results."""
    import pytest as pytest_module
    args = ["-v", "--tb=short", "--no-header"]
    if pattern:
        args.extend(["-k", pattern])
    args.append(os.path.dirname(__file__))

    # Capture exit code
    exit_code = pytest_module.main(args)
    return {"exit_code": exit_code, "passed": exit_code == 0}


def run_rig_tests() -> dict:
    """Run all RIG gate conformance tests."""
    print("=" * 60)
    print("RIG Gate Conformance Tests")
    print("=" * 60)
    result = run_pytest("RIG")
    print(f"\nRIG Result: {'✅ PASS' if result['passed'] else '❌ FAIL'}\n")
    return result


def run_negative_tests() -> dict:
    """Run all negative (rejection) conformance tests."""
    print("=" * 60)
    print("Negative Conformance Tests (RI-006)")
    print("=" * 60)
    result = run_pytest("Reject")
    print(f"\nNegative Result: {'✅ PASS' if result['passed'] else '❌ FAIL'}\n")
    return result


def run_all() -> dict:
    """Run full conformance suite."""
    print("=" * 60)
    print("Tang OS Conformance Harness v1.0")
    print(f"Date: {datetime.now().isoformat()}")
    print(f"Spec: v1.0 | Impl: v0.1.0")
    print("=" * 60)

    rig = run_rig_tests()
    neg = run_negative_tests()
    passed = rig["passed"] and neg["passed"]

    # Summary
    total_gates = len(COMPLIANCE_MATRIX)
    print("=" * 60)
    print(f"Compliance Matrix: {total_gates} spec entries mapped")
    print(f"RIG Gates:        {'✅ PASS' if rig['passed'] else '❌ FAIL'}")
    print(f"Negative Tests:   {'✅ PASS' if neg['passed'] else '❌ FAIL'}")
    print(f"Overall:          {'✅ CONFORMANT' if passed else '❌ NON-CONFORMANT'}")
    print("=" * 60)

    return {
        "passed": passed,
        "rig": rig,
        "negative": neg,
        "timestamp": datetime.now().isoformat(),
        "spec_version": "1.0",
        "impl_version": "0.1.0",
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Tang OS Conformance Harness")
    parser.add_argument("--rig-only", action="store_true", help="Run only RIG gate tests")
    parser.add_argument("--negative-only", action="store_true", help="Run only negative tests")
    args = parser.parse_args()

    if args.rig_only:
        run_rig_tests()
    elif args.negative_only:
        run_negative_tests()
    else:
        run_all()
