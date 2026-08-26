"""Build/release contract check for both Tang OS distribution formats.

Run from the repository root after ``python -m build`` or pass ``--build``.
The checks execute outside the checkout and never depend on its VERSION file.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import venv


ROOT = Path(__file__).resolve().parents[1]
IMPORT_CHECK = r"""
from importlib.metadata import metadata, version
from pathlib import Path
import sys
import yaml
from tang_os import Tang, __version__
from runtime.personality_loader import PersonalityLoader

for name in ('creator', 'extensions', 'host', 'kernel', 'providers',
             'relationship', 'runtime', 'tang_os', 'tang_os_sdk'):
    __import__(name)
assert Tang.__module__.startswith('tang_os')
assert PersonalityLoader.__module__ == 'runtime.personality_loader.loader'
assert version('tang-os') == __version__
requirements = metadata('tang-os').get_all('Requires-Dist') or []
assert any('PyYAML' in item and '>=6.0' in item and '<7' in item for item in requirements)
assert not any(name == 'src' or name.startswith('src.') for name in sys.modules)
assert not (Path.cwd() / 'VERSION').exists()
"""


def run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> None:
    subprocess.run(command, cwd=cwd, env=env, check=True)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifacts", type=Path, default=ROOT / "dist")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--offline", action="store_true",
                        help="disable indexes; requires --find-links")
    parser.add_argument("--find-links", type=Path,
                        help="directory containing all build and runtime wheels")
    return parser


def install_command(
    python: Path, artifact: Path, *, offline: bool, find_links: Path | None
) -> list[str]:
    command = [str(python), "-m", "pip", "install"]
    if offline:
        if find_links is None:
            raise ValueError("--offline requires --find-links")
        command.extend(["--no-index", "--find-links", str(find_links.resolve())])
    command.append(str(artifact.resolve()))
    return command


def verify(
    artifact: Path, *, offline: bool = False, find_links: Path | None = None
) -> None:
    with tempfile.TemporaryDirectory(prefix="tang-os-dist-") as raw:
        temp = Path(raw)
        local_artifact = temp / artifact.name
        shutil.copy2(artifact.resolve(), local_artifact)
        environment = temp / "venv"
        venv.EnvBuilder(with_pip=True, system_site_packages=False).create(environment)
        python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        console = environment / ("Scripts/tang-os.exe" if os.name == "nt" else "bin/tang-os")
        clean_env = os.environ.copy()
        clean_env.pop("PYTHONPATH", None)
        clean_env["PIP_CACHE_DIR"] = str(temp / "pip-cache")
        clean_env["PYTHONNOUSERSITE"] = "1"
        run(
            install_command(python, local_artifact, offline=offline, find_links=find_links),
            cwd=temp,
            env=clean_env,
        )
        run([str(python), "-c", IMPORT_CHECK], cwd=temp, env=clean_env)
        run([str(python), "-m", "tang_os", "version"], cwd=temp, env=clean_env)
        run([str(console), "version"], cwd=temp, env=clean_env)


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    if args.offline and args.find_links is None:
        parser.error("--offline requires --find-links with all dependencies")
    if args.build:
        run([sys.executable, "-m", "build", "--no-isolation", "--outdir", str(args.artifacts)], cwd=ROOT)
    artifacts = [*args.artifacts.glob("*.whl"), *args.artifacts.glob("*.tar.gz")]
    if len(artifacts) != 2 or not any(p.suffix == ".whl" for p in artifacts):
        raise SystemExit(f"Expected one wheel and one sdist in {args.artifacts}; found {artifacts}")
    for artifact in artifacts:
        verify(artifact, offline=args.offline, find_links=args.find_links)
    print("Verified isolated wheel and sdist installs.")


if __name__ == "__main__":
    main()
