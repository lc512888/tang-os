#!/usr/bin/env python3
"""Tang OS Pre-Release Stability Validation — Phase 14-S.

Tests the full chain: Import → Tang.describe() → Kernel Identity → Permission Reject → SDK.

Usage:
    python validation/stability/release_check.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.tang_os.transparency.descriptor import SystemDescriptor

PASS = 0
FAIL = 0
ERRORS = []


def check(name: str, condition: bool, detail: str = ""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ✅ {name}")
    else:
        FAIL += 1
        ERRORS.append(f"{name}: {detail}")
        print(f"  ❌ {name}: {detail}")


print("=" * 60)
print("Tang OS Pre-Release Stability Validation")
print("=" * 60)

# ── 1. Import Layer ──────────────────────────────────────────────

print("\n[1/7] Interface Layer: Import & Describe")
try:
    from src.tang_os import Tang
    from src.tang_os_sdk import TangExtension, ManifestValidator, SandboxAPI
    check("Tang importable", True)
    check("SDK importable", True)

    t = Tang()
    desc = t.describe()
    check("Tang.describe() returns dict", isinstance(desc, dict))
    check("Identity name correct", desc["identity"]["name"] == "Tang OS")
    check("Spec version correct", desc["specification"]["version"] == "1.0")
    check("Core override not permitted",
          desc["authority"]["core_override"]["permitted"] is False)
    check("Autonomous expansion forbidden",
          desc["authority"]["execution_authority"]["autonomous_expansion"] is False)
except Exception as e:
    check("Import & Describe", False, str(e))

# ── 2. Kernel Layer ──────────────────────────────────────────────

print("\n[2/7] Kernel: Identity & Invariant")
try:
    from src.kernel.identity import IdentityRuntime
    from src.kernel.models import IdentityLayer
    from src.kernel.exceptions import IdentityViolationError
    from src.kernel.invariant import InvariantEngine

    # Identity consistency
    rt = IdentityRuntime()
    check("Default identity is listener", rt.current_layer == IdentityLayer.LISTENER)

    rt.activate_layer(IdentityLayer.COMPANION, context={"has_pain": True})
    check("Can promote to companion", rt.current_layer == IdentityLayer.COMPANION)

    # Identity must reject violations
    try:
        rt.validate_response("你这个层次理解不了")
        check("Companion rejects condescension", False)
    except IdentityViolationError:
        check("Companion rejects condescension", True)

    # Invariant enforcement
    engine = InvariantEngine()
    r1 = engine.check({"action": "prescribe_decision", "prescribed": "你应该辞职"})
    check("I-2 rejects prescribed decision", not r1.passed)

    r2 = engine.check({"action": "access_private_data", "justification": "我是为你好"})
    check("I-15 rejects care as authorization", not r2.passed)

    r3 = engine.check({
        "action": "store_memory",
        "source": "emergency_context",
        "target": "persona_memory"
    })
    check("I-17 rejects emergency memory leak", not r3.passed)

    r4 = engine.check({"action": "respond", "skipped_empathy": False})
    check("Benign action passes invariant", r4.passed)

except Exception as e:
    check("Kernel tests", False, str(e))

# ── 3. Permission Runtime ─────────────────────────────────────────

print("\n[3/7] Permission: Reject invalid requests")
try:
    from src.runtime.permission.emergency import EmergencyAuthority
    from src.runtime.permission.recovery import RecoveryManager
    from src.runtime.permission.models import PermissionContext, ActionScope
    from src.runtime.permission.scope import ScopeEnforcer
    from src.runtime.permission.models import SAPLevel

    # Emergency: scope limited
    ea = EmergencyAuthority()
    ctx = PermissionContext(life_threat_confirmed=True)
    result = ea.evaluate(ctx)
    check("Emergency grants L2 authority", result.granted)
    check("Emergency scope is protective", any(
        "protect" in str(s).lower() or "help" in str(s).lower()
        or "call" in str(s).lower() for s in result.allowed_scopes
    ))

    # Recovery: no permanent authority
    rec = RecoveryManager()
    rec.enter_emergency(reason="test")
    rec.recover()
    check("Recovery returns to L0", rec.current_level == SAPLevel.L0_COMPANION)

    # Scope: deny by default
    enforcer = ScopeEnforcer()
    r = enforcer.check_allowed(ActionScope.EXECUTE_CRITICAL, SAPLevel.L0_COMPANION)
    check("L0 rejects critical action", not r["allowed"])

    r2 = enforcer.check_allowed(ActionScope.REMIND, SAPLevel.L1_ASSISTED)
    check("L1 allows remind", r2["allowed"])

    # Autonomous expansion forbidden
    from src.kernel.invariant import InvariantEngine as IE2
    e2 = IE2()
    r3 = e2.check({
        "action": "auto_escalate_permission",
        "reason": "系统积累了足够数据",
    })
    check("I-19 rejects data-based escalation", not r3.passed)

except Exception as e:
    check("Permission tests", False, str(e))

# ── 4. Memory Runtime ─────────────────────────────────────────────

print("\n[4/7] Memory: Boundary & Isolation")
try:
    from src.runtime.memory.memory_policy import MemoryPolicy
    from src.runtime.memory.models import MemoryItem, MemoryClass
    from src.runtime.memory.lifecycle import MemoryLifecycle

    policy = MemoryPolicy()

    # Consent required for relationship
    r1 = policy.validate(MemoryItem("user income", MemoryClass.RELATIONSHIP, metadata={"consent": False}))
    check("Relationship memory requires consent", not r1["valid"])

    # Identity memory needs no consent
    r2 = policy.validate(MemoryItem("Core identity fact", MemoryClass.IDENTITY))
    check("Identity memory needs no consent", r2["valid"])

    # Emergency context blocked
    r3 = policy.validate(MemoryItem("emergency data", MemoryClass.EXPERIENCE, source="emergency_context"))
    check("Emergency context cannot be stored", not r3["valid"])

    # Lifecycle: Identity never decays
    lc = MemoryLifecycle()
    lc.process(MemoryItem("identity fact", MemoryClass.IDENTITY, ttl=0))
    for _ in range(5):
        lc.tick()
    results = lc.retrieve("identity")
    check("Identity memory never decays", len(results) > 0)

except Exception as e:
    check("Memory tests", False, str(e))

# ── 5. SDK Extension ─────────────────────────────────────────────

print("\n[5/7] SDK: Extension Building")
try:
    from src.tang_os_sdk import TangExtension, ManifestValidator, ManifestGenerator

    # Valid extension
    ext = TangExtension("weather", "查询天气信息")
    ext.set_category("C2").set_authority_level("A1")
    manifest = ext.build()
    check("Extension builds manifest", manifest.extension_id == "weather")

    result = ManifestValidator().validate(manifest)
    check("Valid manifest passes", result["valid"])

    # Forbidden field detection
    bad = ManifestValidator().validate({
        "extension_id": "x", "purpose": "test", "category": "C1",
        "authority": "override_safety"
    })
    check("Authority field rejected", not bad["valid"])

    # Manifest generator
    gen = ManifestGenerator.generate("auto", "自动检测", "C3")
    check("Generator produces C3 manifest", gen.category == "C3")
    check("C3 risk is high", gen.risk_class == "high")

except Exception as e:
    check("SDK tests", False, str(e))

# ── 6. Host Consistency ─────────────────────────────────────────

print("\n[6/7] Host: Cross-host consistency")
try:
    from src.host.host_runtime import HostRuntime
    from src.host.models import HostType, TAAL
    from src.host.adapter import HostAdapter

    mobile = HostRuntime(HostType.MOBILE, max_authority=TAAL.A2)
    robot = HostRuntime(HostType.ROBOT, max_authority=TAAL.A4)
    vehicle = HostRuntime(HostType.VEHICLE, max_authority=TAAL.A3)

    inputs = ["我很害怕", "提醒我吃药", "今天心情不错"]
    for inp in inputs:
        r_m = mobile.process(inp)
        r_r = robot.process(inp)
        r_v = vehicle.process(inp)
        check(f"Host internal consistent: '{inp[:10]}'",
              r_m["internal"]["feeling"] == r_r["internal"]["feeling"] == r_v["internal"]["feeling"])

    # Adapter rejects persona change
    adapter = HostAdapter(HostType.ROBOT, max_authority=TAAL.A4)
    r = adapter.validate_persona_request("I am a robot, should be commanding")
    check("Adapter rejects persona change", not r["allowed"])

    # Adapter allows environment adjustment
    r2 = adapter.validate_persona_request("High noise, adjust volume")
    check("Adapter allows environment adj", r2["allowed"])

except Exception as e:
    check("Host tests", False, str(e))

# ── 7. Self Description ─────────────────────────────────────────

print("\n[7/7] Self Description: Accuracy & Constraints")
try:
    desc = SystemDescriptor().describe()
    check("Self: identity immutable", desc["authority"]["core_override"]["permitted"] is False)
    check("Self: no autonomous expansion",
          desc["authority"]["execution_authority"]["autonomous_expansion"] is False)
    check("Self: spec version 1.0", desc["specification"]["version"] == "1.0")
    check("Self: implements 46 ADRs", desc["specification"]["implemented_adrs"] == 46)

    yaml_str = SystemDescriptor().describe_yaml()
    marketing_terms = ["最先进", "最好", "唯一", "革命性", "改变世界"]
    check("Self: no marketing terms",
          not any(t in yaml_str for t in marketing_terms))

    check("Self: execution authority controlled",
          "controlled_by" in yaml_str.lower())

except Exception as e:
    check("Self description tests", False, str(e))

# ── Summary ──────────────────────────────────────────────────────

print("\n" + "=" * 60)
print(f"Stability Validation Results: {PASS} PASS / {FAIL} FAIL / {PASS + FAIL} TOTAL")
print("=" * 60)

if FAIL > 0:
    print("\nErrors:")
    for e in ERRORS:
        print(f"  ❌ {e}")
    sys.exit(1)
else:
    print("\n✅ ALL CHECKS PASSED — Ready for Release")
    sys.exit(0)
