"""Verify Tang.describe() public API outputs."""
from src.tang_os import Tang

t = Tang()
desc = t.describe()
print("=== dict ===")
print(f"Name: {desc['identity']['name']}")
print(f"Type: {desc['identity']['type']}")
print(f"Spec: {desc['specification']['version']}")
print(f"Identity modifiable: {desc['constraints']['identity_modifiable']}")
print(f"Core override: {desc['constraints']['core_override']}")

print()
print("=== YAML ===")
print(t.describe_yaml())

print()
assert desc["identity"]["name"] == "Tang OS"
assert desc["constraints"]["identity_modifiable"] is False
assert desc["constraints"]["core_override"] is False
assert desc["specification"]["version"] == "1.0"
print("All assertions PASS")
