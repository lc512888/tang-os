"""Repository-wide test isolation for Tang's production state-file default."""

import os
from pathlib import Path

import pytest

REPOSITORY_STATE = Path(__file__).resolve().parent / ".tang_state.json"


@pytest.fixture(scope="session", autouse=True)
def isolate_tang_state_and_assert_no_pollution(tmp_path_factory):
    assert not REPOSITORY_STATE.exists(), "test run started with repository state pollution"
    previous = os.environ.get("TANG_OS_STATE_PATH")
    os.environ["TANG_OS_STATE_PATH"] = str(
        tmp_path_factory.mktemp("tang-state") / ".tang_state.json"
    )
    try:
        yield
        assert not REPOSITORY_STATE.exists(), "test run created repository state pollution"
    finally:
        if previous is None:
            os.environ.pop("TANG_OS_STATE_PATH", None)
        else:
            os.environ["TANG_OS_STATE_PATH"] = previous
