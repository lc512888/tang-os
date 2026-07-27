## Tang OS Reference Implementation v{version}

**Compatible with Tang OS Specification v1.0.**

This release is a reference implementation.
It does not define the specification.
It does not claim to be "the official Tang OS implementation."

### What's Included

- Kernel Runtime: Identity, Invariant, State
- Persona Runtime: Emotional State, Response Policy, Relationship Boundary
- Memory Runtime: Three-tier Classification, Boundary, Lifecycle
- Permission Runtime: SAP L0~L3, TAAL A0~A4, Emergency Protocol
- Host Simulator: Manifest, Adapter, Sensor, Actuator, Isolation
- Developer SDK: ExtensionBuilder, ManifestValidator, SandboxAPI
- TPI Interface Package: 8 personality API contracts
- Conformance Harness: RIG-001~007, Negative Tests
- Example Applications: E2 Extension, E3 Host, E4 Emergency
- Self Description Runtime: Tang.describe(), CLI

### Installation

```bash
pip install tang-os=={version}
```

### Verification

```bash
python run_conformance.py
# Expected: ✅ CONFORMANT
```

### Tests

{tests} tests, 100% pass rate.

### Governance

46 Architecture Decision Records (ADR-0001~0046)

### Constraints

- This is a reference implementation (v0.x).
- It does NOT define the Tang OS specification.
- Core Identity is immutable.
- Extension cannot modify personality.
- Emergency authority is temporary and auditable.
