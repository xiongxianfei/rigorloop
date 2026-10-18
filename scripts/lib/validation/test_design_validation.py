"""Read-only model and central system test-design Markdown admission.

References have no execution authority. Native runners own test discovery;
semantic review owns whether assertions establish the described outcomes.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import unquote, urlsplit

from lib.validation.boundary_first_validation import _issue, validate_model_path
from lib.validation.model_layout import PROJECT_MODEL_PATHS, SHARED_TEST_DESIGN_PATHS


def _relative(path):
    return (isinstance(path, str) and bool(path) and '\\' not in path
            and not path.startswith('/') and ':' not in path
            and all(part not in ('', '.', '..') for part in path.split('/')))


def _read(root, path):
    if not _relative(path):
        raise ValueError(f'non-normalized repository path: {path!r}')
    cursor = root
    for part in PurePosixPath(path).parts:
        cursor /= part
        if cursor.is_symlink():
            raise ValueError(f'symlink traversal: {path}')
    if not cursor.resolve().is_relative_to(root) or not cursor.is_file():
        raise ValueError(f'missing or uncontained regular file: {path}')
    return cursor.read_text(encoding='utf-8')


def _headings(text):
    return set(re.findall(r'^#{1,6}\s+(.+?)\s*#*\s*$', _unfenced(text), re.M))


def _unfenced(text):
    lines, fence = [], None
    for line in text.splitlines():
        match = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return '\n'.join(lines)


def _markdown(root, path):
    errors = []
    try:
        text = _read(root, path)
        # The repository-owned prose checker is loaded by its fixed source path.
        source = Path(__file__).resolve().parents[2] / 'validate-documentation-prose.py'
        spec = importlib.util.spec_from_file_location('test_design_prose', source)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        result = module.validate_path(root/path, mode='enforce')
        for issue in result.errors:
            errors.append(issue.format())
        visible = _unfenced(text)
        definitions = {label.casefold(): target for label, target in re.findall(
            r'^\s{0,3}\[([^\]\n]+)\]:\s*(<[^>]+>|\S+)', visible, re.M)}
        targets = list(definitions.values())
        targets.extend(re.findall(r'!?\[[^\]\n]+\]\((<[^>]+>|[^)\s]+)(?:\s+[^)]*)?\)', visible))
        for label, reference in re.findall(r'!?\[([^\]\n]+)\]\[([^\]\n]*)\]', visible):
            if (reference or label).casefold() not in definitions:
                errors.append(f'undefined local reference: {reference or label}')
        for target in targets:
            target = target.strip().strip('<>')
            if urlsplit(target).scheme or target.startswith('//'):
                continue
            relative, _, fragment = unquote(target).partition('#')
            if relative.startswith('/') or '\\' in relative:
                raise ValueError(f'non-relative local link: {target}')
            if not relative:
                destination = path
            else:
                # Check each lexical step before collapsing ..; a symlink must
                # not disappear through normalization of hop/../safe.md.
                parts = list(PurePosixPath(path).parent.parts)
                for part in relative.split('/'):
                    if part == '..':
                        if not parts:
                            raise ValueError(f'escaped local link: {target}')
                        parts.pop()
                    elif part not in ('', '.'):
                        parts.append(part)
                    cursor = root.joinpath(*parts)
                    if cursor.is_symlink() or not cursor.resolve().is_relative_to(root):
                        raise ValueError(f'symlink or escaped local link: {target}')
                destination = '/'.join(parts)
            linked = _read(root, destination)
            if fragment and destination.endswith('.md'):
                anchors = {re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-') for heading in _headings(linked)}
                if fragment not in anchors:
                    errors.append(f'missing local anchor: {target}')
    except (ValueError, OSError, UnicodeError, RuntimeError) as error:
        errors.append(str(error))
    return tuple(_issue('BFR-TEST-MARKDOWN', path, error) for error in errors)


def validate_documents(root, requested):
    """Check declared central documents and ordinary model contracts."""
    root = root.resolve()
    paths = set(requested)
    shared = bool(paths.intersection((*SHARED_TEST_DESIGN_PATHS, *PROJECT_MODEL_PATHS.values())))
    if shared:
        paths.update((*SHARED_TEST_DESIGN_PATHS, PROJECT_MODEL_PATHS['system']))
    details = set(SHARED_TEST_DESIGN_PATHS)
    issues = []
    for path in sorted(paths - details):
        if path.startswith("specs/"):
            issues.append(_issue("BFR-UNSUPPORTED-FORMAT", path,
                                 "feature/proof validation is unsupported; use living model documents"))
        else:
            issues.extend(validate_model_path(root, path))
    markdown = paths & details
    markdown.update(path for path in paths if path in PROJECT_MODEL_PATHS.values())
    for path in sorted(markdown):
        issues.extend(_markdown(root, path))
    return tuple(issues), sorted(paths)
