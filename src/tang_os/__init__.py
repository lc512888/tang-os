"""Tang OS Reference Implementation v0.1.

A minimal, transparent, verifiable implementation of Tang OS Specification v1.0.

Author: 上海群阅信息科技有限公司
Contact: lc512888@gmail.com

Usage:
    from tang_os import Tang

    tang = Tang()
    result = tang.process("我今天很难过")
"""

from src.tang_os.tang import Tang
from src.tang_os.version import get_version_info, MANIFEST

__author__ = "上海群阅信息科技有限公司"
__contact__ = "lc512888@gmail.com"
__version__ = "0.1.0"
__spec_version__ = "1.0"
__all__ = ["Tang", "get_version_info", "MANIFEST"]
