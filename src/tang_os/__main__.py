"""Tang OS CLI — python -m tang_os

Usage:
    python -m tang_os describe        # YAML system description
    python -m tang_os describe --json  # JSON system description
    python -m tang_os version          # Version info
"""

import sys
import json
from src.tang_os.transparency.descriptor import SystemDescriptor
from src.tang_os.version import get_version_info


def main():
    args = sys.argv[1:]

    if not args:
        print("Usage: python -m tang_os [describe|version]")
        return

    if args[0] == "describe":
        desc = SystemDescriptor()
        if "--json" in args:
            print(json.dumps(desc.describe(), indent=2, ensure_ascii=False))
        else:
            print(desc.describe_yaml())

    elif args[0] == "version":
        from src.tang_os.version import AUTHOR, CONTACT_EMAIL
        info = get_version_info()
        print(f"Tang OS Reference Implementation v{info['implementation_version']}")
        print(f"Compatible with Tang OS Specification v{info['specification_version']}")
        print(f"Bound ADRs: {', '.join(info['bound_adrs'])}")
        print(f"Author: {AUTHOR}")
        print(f"Contact: {CONTACT_EMAIL}")

    else:
        print(f"Unknown command: {args[0]}")


if __name__ == "__main__":
    main()
