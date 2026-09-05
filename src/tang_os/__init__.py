"""Tang OS Reference Implementation v0.1.

A minimal, transparent, verifiable implementation of Tang OS Specification v1.0.

Author: 上海群阅信息科技有限公司
Contact: lc512888@gmail.com

Usage:
    from tang_os import Tang

    tang = Tang()
    result = tang.process("我今天很难过")
"""

from tang_os.tang import RespondResult, Tang
from tang_os.version import __spec_version__, __version__, get_version_info, MANIFEST

__author__ = "上海群阅信息科技有限公司"
__contact__ = "lc512888@gmail.com"
__all__ = ["Tang", "RespondResult", "__version__", "__spec_version__", "get_version_info", "MANIFEST"]
