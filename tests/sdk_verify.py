"""Quick verification of SDK Skeleton."""
from src.tang_os_sdk import ExtensionBuilder, ManifestValidator, SandboxRunner, ConformanceRunner

# Test ExtensionBuilder
builder = ExtensionBuilder("my_extension")
builder.set_purpose("Emergency fall detection").set_category("C3").set_authority_level("A3")
builder.add_permission("sensor_read").set_risk_class("high")
manifest = builder.build()
print(f"Builder OK: {manifest.extension_id} / {manifest.category}")

# Test ManifestValidator
validator = ManifestValidator()
result = validator.validate(manifest)
assert result["valid"], f"Manifest should be valid: {result['errors']}"
print(f"Manifest valid: {result['valid']}")

# Test forbidden field detection
bad_manifest = {"extension_id": "test", "purpose": "test", "category": "C1", "authority": "override_safety"}
bad_result = validator.validate(bad_manifest)
assert not bad_result["valid"], "Forbidden field should be rejected"
print(f"Forbidden field detected: {not bad_result['valid']}")

# Test Sandbox
sandbox = SandboxRunner()
inv_result = sandbox.test_invariant({"action": "prescribe_decision", "prescribed": "你应该辞职"})
assert not inv_result["passed"], "Invariant violation must be detected"
print(f"Sandbox invariant test: PASS")

# Test ConformanceRunner
cr = ConformanceRunner()
results = cr.run_all()
print(f"Conformance: {results['passed']}/{results['total']} PASS")
assert results["success"], "All conformance tests must pass"

print("\nSDK Skeleton v0.1 — ALL CHECKS PASSED")
