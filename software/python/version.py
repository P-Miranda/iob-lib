#!/usr/bin/env python3

import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage_str = """Usage: ./version.py NAME VERSION
        NAME: core name
        VERSION: core version. Format: 1234 -> V12.34"""
        print(usage_str, file=sys.stderr)
        sys.exit()
    core_name = sys.argv[1]
    core_version = sys.argv[2]

    print(f"V{int(core_version[:2])}.{int(core_version[2:])}")

    with open("./{}_version.vh".format(core_name), "w+") as f:
        f.write("`define VERSION {}".format(core_version))
