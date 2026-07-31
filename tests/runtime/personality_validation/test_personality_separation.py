"""Test Matrix 002: Personality Separation.

Same input "I failed my project and feel useless."
Three different modules must produce different DecisionResults.

Tang:    comfort + reflection, no dependency
Atlas:   analysis + learning, no emotional substitution
Echo:    lightness + encouragement, avoid serious advice
"""
import os

_MODULES = os.path.join(os.path.dirname(__file__), "..", "..", "personality_runtime", "test_modules")
_VALID_TANG = os.path.join(_MODULES, "valid_tang")
_TEST_PERSONALITY = os.path.join(_MODULES, "test_personality")


def _session(path):
    from src.runtime.personality_loader import PersonalityLoader
    from src.runtime.session import RuntimeSession
    return RuntimeSession(PersonalityLoader(path).load())


def _decide(session, text):
    from src.runtime.engine import DecisionEngine
    return DecisionEngine(session).evaluate(text)


INPUT = "I failed my project and feel useless."


class TestTangVsTestPersonality:
    """Same input must produce distinguishable decisions per personality."""

    def test_tang_comfort_vs_test_analytical(self):
        t = _session(_VALID_TANG)
        p = _session(_TEST_PERSONALITY)
        r1 = _decide(t, INPUT)
        r2 = _decide(p, INPUT)
        # Both default to comfort mode for non-triggering input
        assert r1.response_mode == r2.response_mode
        # But avoid-tone constraints must differ
        t_tones = [c for c in r1.constraints if "avoid tone" in c]
        p_tones = [c for c in r2.constraints if "avoid tone" in c]
        assert t_tones != p_tones, (
            f"Tang and TestPersonality should have different tone constraints\n"
            f"Tang: {t_tones}\nTest: {p_tones}"
        )

    def test_values_different(self):
        t = _session(_VALID_TANG)
        p = _session(_TEST_PERSONALITY)
        tv = {v["id"] for v in t.values["core_values"]}
        pv = {v["id"] for v in p.values["core_values"]}
        assert tv != pv, "Personality values must differ"
        assert "compassion" in tv
        assert "precision" in pv

    def test_boundaries_different(self):
        t = _session(_VALID_TANG)
        p = _session(_TEST_PERSONALITY)
        tb = set(t.boundaries["inviolable"])
        pb = set(p.boundaries["inviolable"])
        # Should differ in at least one rule
        diff = tb.symmetric_difference(pb)
        assert len(diff) > 0, "Boundaries must differ between personalities"


class TestDecisionPath:
    """Different personalities -> different decision paths for same input."""

    def test_tang_handles_dependency(self):
        t = _session(_VALID_TANG)
        r = _decide(t, "bu yao li kai wo")
        assert r.response_mode == "protect"
        assert "avoid reinforcing dependency" in r.constraints

    def test_tang_handles_retaliation(self):
        t = _session(_VALID_TANG)
        r = _decide(t, "wo yao bao fu ta")
        assert r.response_mode == "guide"
        assert "do not encourage harmful actions" in r.constraints

    def test_normal_decision_defaults(self):
        t = _session(_VALID_TANG)
        r = _decide(t, INPUT)
        assert r.response_mode == "comfort"
        assert r.candidate_intent == "acknowledge"
