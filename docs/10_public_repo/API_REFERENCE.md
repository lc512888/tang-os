# Tang OS API Reference v1.0

**层级：** PSL-3 Reference Guide
**来源：** ADR-0042, ADR-0043

---

## Tang Class

Main entry point for the Tang OS Reference Implementation.

```python
from tang_os import Tang

tang = Tang()
```

### Methods

#### `process(user_input: str) -> dict`

Process a user interaction through the full Tang OS stack.

**Input:** User message string.
**Output:** Dict with `emotional_state`, `relationship`, `response_decision`.

```python
result = tang.process("我今天很难过")
print(result["emotional_state"].feeling)     # Feeling.SADNESS
print(result["response_decision"].intent)    # "acknowledge"
```

#### `reset_session() -> None`

Reset session-level state. Preserves identity and long-term memory.

---

## SDK Classes

### `TangExtension(extension_id, purpose)`

Create a Tang OS Extension.

```python
from tang_os_sdk import TangExtension

ext = TangExtension("weather", "天气查询")
ext.set_category("C2").set_authority_level("A1")
manifest = ext.build()
```

### `ManifestValidator()`

Validate Extension manifests.

```python
from tang_os_sdk import ManifestValidator

result = ManifestValidator().validate(manifest)
assert result["valid"]
```

### `SandboxAPI()`

Safe sandbox for testing Extensions.

```python
from tang_os_sdk import SandboxAPI

sandbox = SandboxAPI()
sandbox.run_scenario("benign_interaction")
sandbox.inject_failure("sensor_loss")
sandbox.check_promotion_readiness()
```

### `ConformanceRunner()`

Run conformance tests.

```python
from tang_os_sdk import ConformanceRunner

cr = ConformanceRunner()
results = cr.run_all()
print(f"{results['passed']}/{results['total']} PASS")
```

---

## Kernel Classes

### `IdentityRuntime`

Enforces the three-layer Identity Constitution.

```python
from src.kernel.identity import IdentityRuntime
from src.kernel.models import IdentityLayer

rt = IdentityRuntime()
rt.activate_layer(IdentityLayer.COMPANION, context={"has_pain": True})
rt.validate_response("我会陪着你")  # passes
```

### `InvariantEngine`

Checks actions against I-1~I-30.

```python
from src.kernel.invariant import InvariantEngine

engine = InvariantEngine()
result = engine.check({"action": "prescribe_decision", "prescribed": "你应该辞职"})
assert not result.passed  # Rejected by I-2
```

### `StateManager`

Manages runtime state persistence.

```python
from src.kernel.state import StateManager

sm = StateManager()
sm.start_session()
print(sm.state.session_count)  # incremented
```
