# E2: Weather Capability Extension

> **Category:** E2 Extension Example (ADR-0044)
> **Purpose:** Demonstrate that a third-party Extension can add capability without creating a new personality.

## What This Proves

| Verification | Expected | Status |
|-------------|----------|--------|
| Capability added | Extension provides weather data | ✅ |
| Identity unchanged | Core Identity Constitution preserved | ✅ |
| Permission boundary | Extension cannot exceed A1 | ✅ |
| Core unaffected | Extension crash does not affect Core | ✅ |

## How to Run

```bash
python -m pytest examples/applications/e2_weather/tests/ -v
```

## Structure

```
e2_weather/
├── manifest.yaml     — Example Manifest (EA-002)
├── scenario.yaml     — Test scenarios
├── extension.py      — Weather Extension implementation
├── tests/            — Verification tests
└── README.md         — This file
```

## Key Constraint

This is a **Weather Capability Extension**, NOT a "weather version of Tang OS."
Tang OS Core decides how to respond. The Extension only provides data.
