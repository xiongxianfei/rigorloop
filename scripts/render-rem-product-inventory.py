#!/usr/bin/env python3
"""Regenerate the published-products skill inventory from the validated REM model.

Only the marked inventory region changes; the surrounding requirement analysis
remains authored content. --check compares the region without writing any file.
"""

import argparse
import html
from pathlib import Path
import sys
from urllib.parse import quote

# Audited runpy entrypoints also work independently of the caller's directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.rem_architecture_model import Model


INVENTORY = Path("design/requirements/published-products.md")


def plain(value):
    return html.escape(str(value), quote=False).replace("|", "&#124;").replace("\n", " ")


def source_link(target, label):
    return f"[{plain(label)}](../../{quote(target, safe='/#')})"


def skill_inventory(model):
    catalogs = [catalog for catalog in model.public_catalogs if catalog.owner.id == "MOD-012"]
    lines = ["Generated from MOD-012's observed public entries by `python3 scripts/render-rem-product-inventory.py`. "
             "Names, groups, purpose, and contract navigation share the architecture browser's canonical catalog; retained specialist obligations follow outside this generated block.", "",
             "| Group | Published skill | Purpose | Detailed contract |",
             "| --- | --- | --- | --- |"]
    for catalog in catalogs:
        for entry in sorted(catalog.entries, key=lambda item: (item["group"], item["name"])):
            lines.append(f"| {plain(entry['group'])} | {source_link(entry['source_path'], entry['name'])} | {plain(entry['purpose'])} | {source_link(entry['contract'], entry['contract'])} |")
    if not catalogs:
        lines += ["", "No published skill entries are recorded in MOD-012's software facet."]
    return "\n".join(lines)


def replace_inventory(model):
    """Preserve every byte outside the single ordered generated marker pair."""
    data = (model.root / INVENTORY).read_bytes()
    start = b"<!-- skill-inventory:start -->"
    end = b"<!-- skill-inventory:end -->"
    if data.count(start) != 1 or data.count(end) != 1 or data.index(start) >= data.index(end):
        raise ValueError(f"{INVENTORY}: expected one ordered skill-inventory marker pair")
    prefix, remainder = data.split(start, 1)
    _, suffix = remainder.split(end, 1)
    block = ("\n\n" + skill_inventory(model) + "\n\n").encode("utf-8")
    return prefix + start + block + end + suffix


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check", action="store_true", help="compare without writes")
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        model = Model(root)
        content = replace_inventory(model)
        path = root / INVENTORY
        changed = path.read_bytes() != content
        if args.check:
            if changed:
                print(f"Product inventory drift: {INVENTORY}", file=sys.stderr)
                return 1
            print(f"Product inventory current; source {model.digest}")
            return 0
        if changed:
            path.write_bytes(content)
        print(f"Generated product inventory ({int(changed)} output changed); source {model.digest}")
        return 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f"Product inventory failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
