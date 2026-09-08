#!/usr/bin/env python3
"""Reject the retired YAML projection helper without reading a change root."""
import json
import sys


def main(argv=None):
    print(json.dumps({
        "status": "error", "code": "unsupported-record-interface",
        "message": "Legacy change-record queries are retired. Use rigorloop status, context or show with an explicit v2 change.",
    }))
    return 2


if __name__ == "__main__":
    sys.exit(main())
