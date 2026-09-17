"""Read-only admission of explicitly declared test-design documents.

JSON supplies descriptive data and references, never an executable command.
Structural admission precedes cross-file consistency and native discovery.
"""
from __future__ import annotations

import ast
import importlib.util
import inspect
import json
import math
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit

from lib.validation.boundary_first_validation import _issue, validate_model_path
from lib.validation.model_layout import (
    PROJECT_MODEL_PATHS, SHARED_TEST_DESIGN_PATHS, TEST_DESIGN_PACKAGES, test_design_paths,
)

ID = re.compile(r'[A-Za-z][A-Za-z0-9-]*\Z')
LOWER_ID = re.compile(r'[a-z][a-z0-9-]*\Z')
METHODS = ('automated-test', 'independent-review')
BOUNDARIES = ('contract', 'public-command', 'composition', 'review')
TECHNIQUES = ('equivalence-partition', 'boundary-values', 'decision-table', 'state-transition',
              'property', 'fault-injection', 'walkthrough')
STATES = ('existing', 'partial', 'proposed')


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


def _pairs(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f'duplicate JSON key: {key}')
        value[key] = item
    return value


def _constant(value):
    raise ValueError(f'non-finite JSON number: {value}')


def _finite(value):
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError('non-finite JSON number')
    if isinstance(value, dict):
        for item in value.values():
            _finite(item)
    elif isinstance(value, list):
        for item in value:
            _finite(item)


# Compact structural schema. Descriptive objects intentionally have open keys.
def _object(required, optional=None):
    return ('object', required, optional or {})


def _array(item, minimum=1):
    return ('array', item, minimum)


STRING = ('string',)
IDENTIFIER = ('id',)
LOCAL_ID = ('local-id',)
PATH = ('path',)
REFERENCE = _object({'path': PATH, 'symbol': STRING})
OWNER = _object({'model': ('enum', tuple(TEST_DESIGN_PACKAGES)), 'design': PATH, 'test_design': PATH})
SCOPE = _object({k: STRING for k in ('model', 'boundary', 'entrypoint', 'coverage_claim')})
FIXTURE_RULES = _object({k: STRING for k in ('isolation', 'independent_expectations', 'negative_setup', 'version_roles', 'resource_boundary')})
FIXTURE = _object({'id': LOCAL_ID, 'initial_state': _array(STRING)}, {
    'builder': REFERENCE, 'reference_test': REFERENCE, 'profile': PATH, 'facts': ('data',),
    'expected_changed_paths': _array(PATH), 'extends': LOCAL_ID, 'limitation': STRING,
})
CASE = _object({
    'id': IDENTIFIER, 'title': STRING, 'risk': STRING, 'requirements': _array(IDENTIFIER),
    'technique': ('enum', TECHNIQUES), 'method': ('enum', METHODS), 'boundary': ('enum', BOUNDARIES),
    'target': _object({'path': PATH}, {'symbol': STRING, 'section': STRING}),
    'given': _object({'fixture': LOCAL_ID, 'conditions': _array(STRING)}),
    'when': _array(STRING), 'then': _array(STRING),
    'realization': _object({'state': ('enum', STATES), 'tests': _array(REFERENCE, 0), 'gaps': _array(STRING, 0)}),
}, {'variants': _array(_object({'id': LOCAL_ID, 'parameters': ('data',)}))})


def _shape(value, schema, location, errors):
    kind = schema[0]
    if kind == 'object':
        if not isinstance(value, dict):
            errors.append(f'{location}: expected object')
            return
        required, optional = schema[1:]
        for key in sorted(value.keys() - required.keys() - optional.keys()):
            errors.append(f'{location}.{key}: unknown field')
        for key in sorted(required.keys() - value.keys()):
            errors.append(f'{location}.{key}: missing field')
        for key, field in (required | optional).items():
            if key in value:
                _shape(value[key], field, location+'.'+key, errors)
    elif kind == 'array':
        if not isinstance(value, list) or len(value) < schema[2]:
            errors.append(f'{location}: expected array of at least {schema[2]} items')
            return
        for position, item in enumerate(value):
            _shape(item, schema[1], f'{location}[{position}]', errors)
    elif kind == 'enum':
        if not isinstance(value, str) or value not in schema[1]:
            errors.append(f'{location}: unknown value {value!r}')
    elif kind == 'version':
        if type(value) is not int or value != 2:
            errors.append(f'{location}: unknown format version {value!r}')
    elif kind == 'data':
        if not isinstance(value, dict) or not value:
            errors.append(f'{location}: expected nonempty descriptive object')
    elif not isinstance(value, str) or not value.strip():
        errors.append(f'{location}: expected nonempty string')
    elif kind == 'id' and not ID.fullmatch(value):
        errors.append(f'{location}: invalid stable ID')
    elif kind == 'local-id' and not LOWER_ID.fullmatch(value):
        errors.append(f'{location}: invalid lowercase ID')
    elif kind == 'path' and not _relative(value):
        errors.append(f'{location}: invalid normalized relative path')


def _schema(model, index):
    fields = {'format': ('enum', (model+('-test-catalog-draft' if index else '-test-cases-draft'),)),
              'format_version': ('version',), 'owner': OWNER}
    if index:
        fields.update(scope=SCOPE, fixture_rules=FIXTURE_RULES,
                      groups=_array(_object({'id': LOCAL_ID, 'title': STRING, 'path': PATH})))
    else:
        case_schema = CASE
        if model == 'authoring':
            required = dict(CASE[1])
            required.update(method=('enum', ('independent-review',)),
                            boundary=('enum', ('review',)), technique=('enum', ('walkthrough',)))
            realization = dict(required['realization'][1])
            realization['state'] = ('enum', ('proposed',))
            required['realization'] = _object(realization)
            case_schema = _object(required, CASE[2])
        fields.update(scope=_object({k: STRING for k in ('group', 'title', 'boundary')}),
                      fixtures=_array(FIXTURE), cases=_array(case_schema))
    return _object(fields)


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


def _symbol(root, reference):
    tree = ast.parse(_read(root, reference['path']))
    nodes = tree.body
    for part in reference['symbol'].split('.'):
        found = next((node for node in nodes if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == part), None)
        if found is None:
            raise ValueError(f"missing callable {reference['path']}:{reference['symbol']}")
        nodes = found.body


def collect_native(root, model, destination):
    """Trusted subprocess target; the catalog cannot select its module or command."""
    from lib.validation.validation_execution import unittest_adapter
    root = Path(root).resolve()
    found = []
    def observe(test):
        method = getattr(test, test._testMethodName)
        source = inspect.getsourcefile(method)
        if source is None:
            raise ValueError('discovered method has no source identity')
        path = Path(source).absolute().relative_to(root).as_posix()
        _read(root, path)
        found.append({'path': path, 'symbol': type(test).__name__+'.'+test._testMethodName})
    entrypoint = root / TEST_DESIGN_PACKAGES[model]['entrypoint']
    with tempfile.TemporaryDirectory() as temporary:
        unittest_adapter('collect', Path(temporary)/'receipt.json', [str(entrypoint)], case_observer=observe)
    Path(destination).write_text(json.dumps(found))


def _discovery(root, model):
    scripts = str(Path(__file__).resolve().parents[2])
    bootstrap = ('import sys; sys.path.insert(0,sys.argv[1]); '
                 'from lib.validation.test_design_validation import collect_native; '
                 'collect_native(sys.argv[2],sys.argv[3],sys.argv[4])')
    with tempfile.TemporaryDirectory() as temporary:
        receipt = Path(temporary)/'methods.json'
        result = subprocess.run([sys.executable, '-B', '-c', bootstrap, scripts, str(root), model, str(receipt)],
                                cwd=root, capture_output=True, text=True, timeout=60)
        if result.returncode:
            raise ValueError('trusted native discovery failed: '+result.stderr[-2000:])
        return {(item['path'], item['symbol']) for item in json.loads(receipt.read_text())}


def _duplicate(items, key, label, errors):
    seen = {}
    for position, item in enumerate(items):
        value = item[key]
        if value in seen:
            errors.append(f'{label}: duplicate {key} {value!r} at [{seen[value]}] and [{position}]')
        seen[value] = position


def validate_catalog(root, model):
    paths = test_design_paths(model)
    owner_path, strategy, index_path = paths[:3]
    documents, issues = {}, []
    # Load explicit declarations, never paths or imports selected by JSON data.
    for path in paths[2:]:
        try:
            value = json.loads(_read(root, path), object_pairs_hook=_pairs, parse_constant=_constant)
            _finite(value)
            documents[path] = value
        except (ValueError, OSError, UnicodeError, RuntimeError) as error:
            issues.append(_issue('BFR-TEST-READ', path, str(error)))
    shape_issues = []
    for path, value in documents.items():
        errors = []
        _shape(value, _schema(model, path == index_path), path, errors)
        shape_issues.extend(_issue('BFR-TEST-SHAPE', path, error) for error in errors)
    # Unknown structure takes precedence over missing-file/reference consistency.
    if shape_issues or issues:
        return tuple(shape_issues or issues)
    index = documents[index_path]
    errors = []
    expected_owner = {'model': model, 'design': owner_path, 'test_design': strategy}
    for path, value in documents.items():
        if value['owner'] != expected_owner:
            errors.append(f'{path}: owner does not match declared package')
    if index['scope']['model'] != model or index['scope']['entrypoint'] != TEST_DESIGN_PACKAGES[model]['entrypoint']:
        errors.append(f'{index_path}: scope does not match declared model/entrypoint')
    _duplicate(index['groups'], 'id', index_path, errors)
    _duplicate(index['groups'], 'path', index_path, errors)
    expected_groups = {group: TEST_DESIGN_PACKAGES[model]['directory']+'/cases/'+group+'.json'
                       for group in TEST_DESIGN_PACKAGES[model]['groups']}
    if {item['id']: item['path'] for item in index['groups']} != expected_groups:
        errors.append(f'{index_path}: group membership differs from exact declaration')
    # Extra adjacent files cannot acquire authority by directory membership.
    directory = root / TEST_DESIGN_PACKAGES[model]['directory'] / 'cases'
    for file in directory.iterdir():
        if file.relative_to(root).as_posix() not in paths[3:]:
            errors.append(f'{file.relative_to(root)}: unindexed adjacent group')
    try:
        owner_body = _read(root, owner_path)
        table = re.search(r'^## Requirements\s*\n(.*?)(?=^#{1,6} |\Z)', _unfenced(owner_body), re.M | re.S)
        requirements = set(re.findall(r'^\|\s*([A-Za-z][A-Za-z0-9-]*)\s*\|', table.group(1) if table else '', re.M))
        _read(root, strategy)
        if model == 'authoring':
            _read(root, TEST_DESIGN_PACKAGES['skill']['directory']+'/test-design.md')
        _read(root, TEST_DESIGN_PACKAGES[model]['entrypoint'])
    except (ValueError, OSError, UnicodeError, RuntimeError) as error:
        errors.append(str(error))
        return tuple(_issue('BFR-TEST-REFERENCE', index_path, error) for error in errors)
    case_locations, linked = {}, set()
    for path in paths[3:]:
        group = documents[path]
        entry = next((item for item in index['groups'] if item['path'] == path), None)
        if entry is None or group['scope']['group'] != entry['id'] or group['scope']['title'] != entry['title']:
            errors.append(f'{path}: group identity/title differs from index')
        _duplicate(group['fixtures'], 'id', path, errors)
        fixtures = {fixture['id']: fixture for fixture in group['fixtures']}
        for fixture in group['fixtures']:
            current, visited = fixture, set()
            while current is not None:
                if current['id'] in visited:
                    errors.append(f"{path}: cyclic fixture extends {fixture['id']}")
                    break
                visited.add(current['id'])
                parent = current.get('extends')
                if parent and parent not in fixtures:
                    errors.append(f'{path}: missing base fixture {parent}')
                current = fixtures.get(parent)
            for key in ('builder', 'reference_test'):
                if key in fixture:
                    try:
                        _symbol(root, fixture[key])
                    except (ValueError, OSError, UnicodeError, SyntaxError, RuntimeError) as error:
                        errors.append(f'{path}: {error}')
            if 'profile' in fixture:
                try:
                    _read(root, fixture['profile'])
                except (ValueError, OSError, UnicodeError, RuntimeError) as error:
                    errors.append(f'{path}: {error}')
        for case in group['cases']:
            location = f"{path}:{case['id']}"
            if case['id'] in case_locations:
                errors.append(f"duplicate case {case['id']}: {case_locations[case['id']]} and {location}")
            case_locations[case['id']] = location
            if len(case['requirements']) != len(set(case['requirements'])) or not set(case['requirements']) <= requirements:
                errors.append(f'{location}: invalid or duplicate requirement reference')
            if case['given']['fixture'] not in fixtures:
                errors.append(f'{location}: missing fixture reference')
            _duplicate(case.get('variants', []), 'id', location, errors)
            realization = case['realization']
            tests, gaps, state = realization['tests'], realization['gaps'], realization['state']
            if not ((state == 'existing' and tests and not gaps) or (state == 'partial' and tests and gaps) or (state == 'proposed' and not tests and gaps)):
                errors.append(f'{location}: inconsistent realization state/tests/gaps')
            pairs = [(test['path'], test['symbol']) for test in tests]
            if len(pairs) != len(set(pairs)):
                errors.append(f'{location}: duplicate test reference')
            target = case['target']
            try:
                if case['method'] == 'independent-review':
                    if case['boundary'] != 'review' or tests or state != 'proposed' or set(target) != {'path', 'section'}:
                        raise ValueError('review requires section target, review boundary and proposed realization without tests')
                    if target['section'] not in _headings(_read(root, target['path'])):
                        raise ValueError('missing review target section')
                else:
                    if case['boundary'] == 'review' or set(target) != {'path', 'symbol'}:
                        raise ValueError('automated case requires callable target and non-review boundary')
                    _symbol(root, target)
                for test in tests:
                    _read(root, test['path'])
                linked.update(pairs)
            except (ValueError, OSError, UnicodeError, SyntaxError, RuntimeError) as error:
                errors.append(f'{location}: {error}')
    if not errors and linked:
        try:
            discovered = _discovery(root, model)
            for path, symbol in sorted(linked - discovered):
                errors.append(f'{path}:{symbol}: linked test is not natively discovered at this source')
        except (ValueError, OSError, subprocess.TimeoutExpired) as error:
            errors.append(str(error))
    return tuple(_issue('BFR-TEST-REFERENCE', index_path, error) for error in errors)


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
    """Expand exact declarations; unknown requested members remain failures."""
    root = root.resolve()
    paths = set(requested)
    models = {model for model in TEST_DESIGN_PACKAGES if paths.intersection(test_design_paths(model))}
    shared = bool(paths.intersection((*SHARED_TEST_DESIGN_PATHS, PROJECT_MODEL_PATHS['system'])))
    for model in models:
        paths.update(test_design_paths(model))
        if model == 'authoring':
            paths.add(TEST_DESIGN_PACKAGES['skill']['directory']+'/test-design.md')
    if shared:
        paths.update((*SHARED_TEST_DESIGN_PATHS, PROJECT_MODEL_PATHS['system']))
    details = set(SHARED_TEST_DESIGN_PATHS)
    for model in TEST_DESIGN_PACKAGES:
        details.update(test_design_paths(model)[1:])
    issues = []
    for path in sorted(paths - details):
        if path.startswith("specs/"):
            issues.append(_issue("BFR-UNSUPPORTED-FORMAT", path,
                                 "feature/proof validation is unsupported; use living model documents"))
        else:
            issues.extend(validate_model_path(root, path))
    for model in sorted(models):
        issues.extend(validate_catalog(root, model))
    markdown = {path for path in paths & details if path.endswith('.md')}
    markdown.update(PROJECT_MODEL_PATHS[model] for model in models)
    if shared:
        markdown.add(PROJECT_MODEL_PATHS['system'])
    for path in sorted(markdown):
        issues.extend(_markdown(root, path))
    return tuple(issues), sorted(paths)
