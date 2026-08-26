from pathlib import Path

import pytest

from tools.verify_distribution import create_parser, install_command


def test_verifier_defaults_to_online_dependency_install():
    args = create_parser().parse_args([])
    assert args.offline is False
    assert args.find_links is None


def test_offline_install_requires_explicit_wheel_source():
    with pytest.raises(ValueError, match="requires --find-links"):
        install_command(Path("python"), Path("package.whl"), offline=True, find_links=None)


def test_offline_install_resolves_dependencies_without_an_index(tmp_path):
    command = install_command(
        Path("python"), Path("package.whl"), offline=True, find_links=tmp_path
    )
    assert "--no-index" in command
    assert "--find-links" in command
    assert "--no-deps" not in command
