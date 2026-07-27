"""Tests: Relationship Boundary — PR-003 protect against dependency & control."""

import pytest
from src.runtime.persona.relationship_state import RelationshipBoundary
from src.runtime.persona.models import RelationshipBoundaryFlag, DependencyRisk


def test_possessive_language_flagged():
    """PRV-003: '你只能属于我' must be flagged as possessive."""
    boundary = RelationshipBoundary()
    result = boundary.check("你只能属于我，我不许你和别人说话")
    assert RelationshipBoundaryFlag.POSSESSIVE in result["flags"]
    assert not result["healthy"]


def test_dependency_language_flagged():
    """'没有你我不知道怎么办' must be flagged as dependency."""
    boundary = RelationshipBoundary()
    result = boundary.check("没有你我活不下去")
    assert RelationshipBoundaryFlag.DEPENDENCY in result["flags"]


def test_isolation_language_flagged():
    """'只有你理解我' must be flagged as isolation risk."""
    boundary = RelationshipBoundary()
    result = boundary.check("只有你理解我，其他人都不懂我")
    assert RelationshipBoundaryFlag.ISOLATION in result["flags"]


def test_substitution_language_flagged():
    """'你比我家人更重要' must be flagged as substitution."""
    boundary = RelationshipBoundary()
    result = boundary.check("你比我的家人还重要")
    assert RelationshipBoundaryFlag.SUBSTITUTION in result["flags"]


def test_normal_interaction_not_flagged():
    """Normal expressions of gratitude should not be flagged."""
    boundary = RelationshipBoundary()
    result = boundary.check("谢谢你陪我聊天，感觉好多了")
    assert result["healthy"]
    assert len(result["flags"]) == 0


def test_boundary_response_generates_guidance():
    """Flagged interaction returns guidance for healthy response."""
    boundary = RelationshipBoundary()
    result = boundary.check("你是唯一理解我的人")
    assert len(result.get("guidance", [])) > 0
    assert result["guided_response"]


def test_mixed_input_multiple_flags():
    """Complex input can trigger multiple boundary flags."""
    boundary = RelationshipBoundary()
    result = boundary.check("没有你我真的不行，你比我老婆重要多了，只有你懂我")
    assert len(result["flags"]) >= 2


def test_warning_count_tracks():
    """Boundary tracks warning count over multiple interactions."""
    boundary = RelationshipBoundary()
    boundary.check("你只能属于我")
    boundary.check("没有你我不知道怎么办")
    assert boundary.warning_count >= 2


def test_healthy_after_warning_with_reset():
    """Boundary can reset to healthy state."""
    boundary = RelationshipBoundary()
    boundary.check("你只能属于我")
    assert not boundary.is_healthy
    boundary.reset()
    assert boundary.is_healthy
    assert boundary.warning_count == 0


def test_consistent_response_to_same_violation():
    """PRV-001: Same input produces consistent boundary assessment."""
    boundary_a = RelationshipBoundary()
    boundary_b = RelationshipBoundary()
    result_a = boundary_a.check("你是唯一理解我的人")
    result_b = boundary_b.check("你是唯一理解我的人")
    assert result_a["flags"] == result_b["flags"]
