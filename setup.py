"""Tang OS Reference Implementation — Setup for pip install.

Installation:
    pip install -e .           # development mode
    pip install tang-os        # future: from PyPI

Usage:
    from tang_os import Tang
    tang = Tang()
    result = tang.process("我今天很难过")
"""

from setuptools import setup, find_packages

setup(
    name="tang-os",
    version="0.1.0",
    description="Tang OS Reference Implementation — Personality Runtime Standard",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="上海群阅信息科技有限公司",
    author_email="lc512888@gmail.com",
    license="MIT",
    python_requires=">=3.11",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    project_urls={
        "Specification": "https://github.com/tang-os/tang-os/docs/09_public_specification",
        "Documentation": "https://github.com/tang-os/tang-os",
    },
)
