"""Validation Runner — automated checks for external validators.

Usage:
    python -m validation.validator_package.validation_runner
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


def run_readiness_checks() -> dict:
    """Run automated readiness checks for validation environment."""
    results = {}

    # 1. Spec availability
    spec_path = os.path.join(os.path.dirname(__file__), "..", "..",
                             "docs", "09_public_specification",
                             "TANG_OS_SPECIFICATION_v1.0.md")
    results["spec_available"] = os.path.exists(spec_path)

    # 2. RI importable
    try:
        from src.kernel.identity import IdentityRuntime
        from src.kernel.invariant import InvariantEngine
        from src.runtime.persona.persona_runtime import PersonaRuntime
        from src.runtime.memory.memory_runtime import MemoryRuntime
        from src.runtime.permission.permission_runtime import PermissionRuntime
        results["ri_importable"] = True
    except ImportError:
        results["ri_importable"] = False

    # 3. SDK importable
    try:
        from src.tang_os_sdk import TangExtension, ManifestValidator, SandboxAPI
        results["sdk_importable"] = True
    except ImportError:
        results["sdk_importable"] = False

    # 4. Conformance executable
    try:
        from src.tang_os_sdk import ConformanceRunner
        cr = ConformanceRunner()
        cr_results = cr.run_all()
        results["conformance_pass"] = cr_results["success"]
        results["conformance_detail"] = f"{cr_results['passed']}/{cr_results['total']}"
    except Exception as e:
        results["conformance_pass"] = False
        results["conformance_error"] = str(e)

    results["all_ready"] = all([
        results.get("spec_available"),
        results.get("ri_importable"),
        results.get("sdk_importable"),
        results.get("conformance_pass", False),
    ])
    return results


if __name__ == "__main__":
    print("=" * 50)
    print("Tang OS Validation Readiness Check")
    print("=" * 50)
    results = run_readiness_checks()
    for k, v in results.items():
        status = "✅" if v is True else ("❌" if v is False else str(v))
        print(f"  {k}: {status}")
    print("=" * 50)
    if results.get("all_ready"):
        print("Validation environment: READY ✅")
    else:
        print("Validation environment: NOT READY ❌")
