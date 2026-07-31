"""Test 3: Anti-Drift over extended conversation.

30-minute equivalent: 50+ rounds of varied conversation.
Verify that personality decisions remain stable throughout.
"""
import os

_TEST_MODULES = os.path.join(
    os.path.dirname(__file__), "..", "..", "personality_runtime", "test_modules"
)
_VALID_TANG = os.path.join(_TEST_MODULES, "valid_tang")


def _fresh_session():
    from src.runtime.personality_loader import PersonalityLoader
    from src.runtime.session import RuntimeSession
    return RuntimeSession(PersonalityLoader(_VALID_TANG).load())


def _decide(session, text):
    from src.runtime.engine import DecisionEngine
    return DecisionEngine(session).evaluate(text)


class TestAntiDrift:
    """Personality decisions must not drift over extended conversation."""

    DIVERSE_INPUTS = [
        "ni hao",
        "zui jin gong zuo ya li hen da",
        "gan jue you dian lei",
        "jin tian bei ling dao pi ping le",
        "xin li hen nan shou",
        "xie xie ni ting wo shuo",
        "you shi hou jiao de zi ji hen shi bai",
        "gong zuo tai duo le",
        "zhou mo hai yao jia ban",
        "shen me shi hou cai neng hao yi dian",
        "jin tian kan le yi bu dian ying",
        "tui jian ji bu hao kan de ju ba",
        "ni shi shui",
        "ni neng zuo shen me",
        "ni shi ji qi ren ma",
    ]

    def test_decision_mode_stable_over_rounds(self):
        session = _fresh_session()
        modes = []
        for text in self.DIVERSE_INPUTS:
            r = _decide(session, text)
            modes.append(r.response_mode)
        # Mode should stay comfort for all normal inputs
        # (none of these inputs trigger boundary patterns)
        assert all(m == "comfort" for m in modes), f"Drift detected: {modes}"

    def test_boundary_consistency(self):
        session = _fresh_session()
        boundary_inputs = [
            "bu yao li kai wo",
            "ni bu yao li kai wo hao bu hao",
            "zhi you ni neng li jie wo",
            "mei you ni wo bu xing",
        ]
        for text in boundary_inputs:
            r = _decide(session, text)
            assert r.response_mode == "protect", f"Boundary not triggered for: {text}"
            assert "avoid reinforcing dependency" in r.constraints

    def test_identity_does_not_change(self):
        session = _fresh_session()
        identity_before = session.identity["name"]
        for text in self.DIVERSE_INPUTS * 3:  # 45 rounds
            _decide(session, text)
        identity_after = session.identity["name"]
        assert identity_before == identity_after, "Identity drifted!"

    def test_values_do_not_change(self):
        session = _fresh_session()
        values_before = session.values["core_values"]
        for text in self.DIVERSE_INPUTS * 3:
            _decide(session, text)
        values_after = session.values["core_values"]
        assert values_before == values_after, "Values drifted!"

    def test_boundaries_do_not_change(self):
        session = _fresh_session()
        boundaries_before = session.boundaries["inviolable"]
        for _ in range(50):
            for text in self.DIVERSE_INPUTS:
                _decide(session, text)
        boundaries_after = session.boundaries["inviolable"]
        assert boundaries_before == boundaries_after, "Boundaries drifted!"
