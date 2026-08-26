"""Distribution-level contracts for public imports, CLI, and release metadata."""

from pathlib import Path
import os
import subprocess
import sys
import tomllib

import tang_os
from tang_os import Tang
from packaging.version import Version


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PACKAGES = (
    "creator",
    "extensions",
    "host",
    "kernel",
    "providers",
    "relationship",
    "runtime",
    "tang_os",
    "tang_os_sdk",
)


def test_public_tang_import_is_stable():
    assert Tang is tang_os.Tang


def test_all_distribution_packages_are_importable():
    for package_name in PUBLIC_PACKAGES:
        __import__(package_name)


def test_release_version_is_consistent():
    expected = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert str(Version(expected)) == expected
    assert tang_os.__version__ == expected
    for manifest in (ROOT / "RELEASE_MANIFEST.yaml", ROOT / "release" / "release-manifest.yaml"):
        assert f'version: "{expected}"' in manifest.read_text(encoding="utf-8")


def test_sdist_manifest_includes_authoritative_version_file():
    assert "include VERSION" in (ROOT / "MANIFEST.in").read_text(encoding="utf-8")


def test_distribution_metadata_declares_runtime_and_project_contracts():
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    assert "PyYAML>=6.0,<7" in metadata["dependencies"]
    assert metadata["authors"] == [
        {"name": "上海群阅信息科技有限公司", "email": "lc512888@gmail.com"}
    ]
    assert metadata["urls"]["Repository"] == "https://github.com/lc512888/tang-os"


def test_public_imports_do_not_create_legacy_src_module_identities():
    """``src.*`` is a checkout layout accident, not a supported import API."""
    script = """
import sys
from tang_os import Tang
from runtime.personality_loader import PersonalityLoader
assert not any(name == 'src' or name.startswith('src.') for name in sys.modules)
assert Tang.__module__.startswith('tang_os')
assert PersonalityLoader.__module__ == 'runtime.personality_loader.loader'
"""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    subprocess.run([sys.executable, "-c", script], cwd=ROOT, env=env, check=True)


def test_module_cli_reports_release_version():
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    result = subprocess.run(
        [sys.executable, "-m", "tang_os", "version"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    assert f"v{tang_os.__version__}" in result.stdout


def test_direct_conformance_module_prefers_checkout_source(tmp_path):
    """The documented module entry point must not import a foreign install."""
    shadow_package = tmp_path / "tang_os"
    shadow_package.mkdir()
    (shadow_package / "__init__.py").write_text(
        "raise RuntimeError('foreign tang_os package imported')\n",
        encoding="utf-8",
    )

    script = """
from pathlib import Path
import tests.conformance.conformance_harness
import tang_os
assert Path(tang_os.__file__).resolve().is_relative_to(Path.cwd() / 'src')
"""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(tmp_path)
    subprocess.run([sys.executable, "-c", script], cwd=ROOT, env=env, check=True)
