#!/usr/bin/env python3
"""Generate the offline 4+1 architecture browser with D2 + ELK diagrams.

Install D2 0.9.0 separately, then use --d2 PATH if it is not on PATH.
Reading the generated page requires only a browser, with no network or server.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

from lib.rem_architecture_browser import build_model, diagram_sources
from lib.rem_architecture_model import Model


SCRIPTS = Path(__file__).resolve().parent
ASSETS = SCRIPTS / "resources/rem-architecture-browser"
OUTPUT = Path("design/architecture/views/browser")
D2_VERSION = "v0.9.0"
DIAGRAM_NAME = (r"(?:overview|module-[A-Za-z0-9-]+|process|development|physical|scenarios|"
                r"(?:process|development|physical)-(?:MOD|IF)-[0-9]+|scenario-SCN-[0-9]+|"
                r"process-(?:publication|recovery|coordination)|physical-(?:consumer|storage|production)|"
                r"development-testing(?:-MOD-[0-9]+)?)")

def digest(content):
    return hashlib.sha256(content).hexdigest()


def compile_svg(d2, name, source):
    spacing = ["--elk-nodeNodeBetweenLayers=30", "--elk-edgeNodeBetweenLayers=35",
               "--elk-padding=[top=90,left=70,bottom=50,right=70]"]
    result = subprocess.run(
        [d2, "--layout=elk", "--theme=0", "--pad=28", "--no-xml-tag",
         "--salt=" + name, "--timeout=45", *spacing, "-", "-"],
        input=source, text=True, capture_output=True, timeout=60,
    )
    if result.returncode:
        raise ValueError(f"D2 failed for {name}: {result.stderr.strip()}")
    svg = result.stdout
    if ET.fromstring(svg).tag != "{http://www.w3.org/2000/svg}svg":
        raise ValueError(f"D2 did not produce an SVG for {name}")
    # D2 links default to a new tab. Navigation belongs in the selected view.
    return re.sub(r'\s+target="[^"]*"', '', svg)


def render(model, d2):
    # Resolve every selected reading scope before invoking a compiler or writing.
    projected = build_model(model)
    version = subprocess.run([d2, "--version"], text=True, capture_output=True, timeout=10)
    if version.returncode or version.stdout.strip() != D2_VERSION:
        raise ValueError(f"D2 {D2_VERSION} is required; received {version.stdout.strip()!r}")
    sources = diagram_sources(model)
    if any(not re.fullmatch(DIAGRAM_NAME, name) for name in sources):
        raise ValueError("Unsafe generated diagram filename")
    with ThreadPoolExecutor(max_workers=4) as pool:
        svgs = dict(zip(sources, pool.map(lambda item: compile_svg(d2, *item), sources.items())))
    # D2 0.9.0 omits connection tooltips from SVG. Keep canonical identity
    # discoverable in standalone diagrams as well as the browser presentation.
    def interface_title(match):
        identity = match.group(2)
        title = model.records[identity].data["title"]
        return match.group(1) + "<title>" + html.escape(f"{title} ({identity})") + "</title>"
    svgs = {name: re.sub(r'(<a\b[^>]*\b(?:xlink:)?href="#interface/([^"]+)"[^>]*>)',
                         interface_title, svg) for name, svg in svgs.items()}
    data = json.dumps(projected, ensure_ascii=False, separators=(",", ":"))
    # Script elements are raw text even when their type is application/json.
    data = data.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    replacements = {
        "MODEL_JSON": data,
        "DIAGRAMS": "\n".join(f'<template data-diagram="{html.escape(name)}">{svg}</template>'
                               for name, svg in svgs.items()),
        "STYLE": (ASSETS / "viewer.css").read_text(),
        "SCRIPT": (ASSETS / "viewer.js").read_text(),
    }
    template = (ASSETS / "index.html").read_text()
    for key in replacements:
        if template.count("{{" + key + "}}") != 1:
            raise ValueError(f"Browser template requires exactly one {key} placeholder")
    page = re.sub(r"\{\{(MODEL_JSON|DIAGRAMS|STYLE|SCRIPT)\}\}",
                  lambda match: replacements[match.group(1)], template)
    outputs = {"index.html": page.encode()}
    for name, source in sources.items():
        outputs[f"diagrams/{name}.d2"] = source.encode()
        # Standalone SVGs return to the viewer; inline templates keep hash routes.
        svg = re.sub(r'((?:xlink:)?href=")#(?=(?:module|interface|entity|scenario|process|development|physical)/|(?:scenarios|process|development|physical)(?:"|$))',
                     r'\1../index.html#', svgs[name])
        outputs[f"diagrams/{name}.svg"] = svg.encode()
    manifest = ["# Generated browser artifacts; not canonical engineering records.",
                f"# Source SHA-256: {model.digest}", f"# D2 {D2_VERSION}; ELK layout"]
    manifest += [f"{digest(content)}  {name}" for name, content in sorted(outputs.items())]
    outputs["manifest.sha256"] = ("\n".join(manifest) + "\n").encode()
    return outputs


def obsolete_diagrams(directory, outputs):
    """Only this generator's strictly named diagram files can be retired."""
    return [path for path in sorted((directory / "diagrams").glob("*"))
            if re.fullmatch(DIAGRAM_NAME + r"\.(?:d2|svg)", path.name)
            and path.relative_to(directory).as_posix() not in outputs]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=SCRIPTS.parent)
    parser.add_argument("--d2", default="d2", help="path to D2 0.9.0")
    parser.add_argument("--check", action="store_true", help="regenerate and compare without writes")
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        model = Model(root)
        outputs = render(model, args.d2)
        directory = root / OUTPUT
        drift = [name for name, content in outputs.items()
                 if not (directory / name).is_file() or (directory / name).read_bytes() != content]
        obsolete = obsolete_diagrams(directory, outputs)
        if args.check:
            if drift or obsolete:
                names = drift + [path.relative_to(directory).as_posix() for path in obsolete]
                print("Architecture browser drift: " + ", ".join(names), file=sys.stderr)
                return 1
            print(f"Architecture browser and {len(outputs) // 2 - 1} diagrams current; source {model.digest}")
            return 0
        # Validate and compile the entire subject before publishing any output.
        for name in drift:
            target = directory / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(outputs[name])
        for path in obsolete:
            path.unlink()
        print(f"Generated architecture browser ({len(drift)} outputs changed); source {model.digest}")
        return 0
    except (ValueError, OSError, KeyError, TypeError, ET.ParseError, subprocess.TimeoutExpired) as error:
        print(f"Architecture browser failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
