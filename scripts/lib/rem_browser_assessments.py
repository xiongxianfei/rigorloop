"""Validate explicitly selected operational disclosures for an offline reader.

This boundary compares supplied judgments; it neither discovers records nor
turns code/tests into an assessment. Original selected bytes stay reproducible.
"""
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator
import re

SNAPSHOT = 'assessment-snapshot.data'
DESIGN_LIMIT = 4 * 1024 * 1024
EMPTY = {'format_version': 1, 'assessments': []}
STATES = {
    'implementation': {'unknown', 'not-started', 'partial', 'implemented'},
    'verification': {'not-assessed', 'passed', 'failed', 'needs-reassessment'},
}


def fail(message):
    raise ValueError('Assessment: ' + message)


def fields(value, names):
    if not isinstance(value, dict) or set(value) != set(names.split()):
        fail('missing or unknown fields; expected ' + names)


def text(value):
    if not isinstance(value, str) or not value.strip():
        fail('expected nonempty text')


def texts(value):
    if not isinstance(value, list):
        fail('expected text array')
    for item in value:
        text(item)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            fail('duplicate JSON key ' + key)
        result[key] = value
    return result


def _read_disclosure(path, limit, limit_label):
    with path.open('rb') as source:
        content = source.read(limit + 1)
    if len(content) > limit:
        fail('selected ' + limit_label)
    try:
        return decode_json(content.decode('utf-8'), depth=32 if limit == DELIVERY_LIMIT else None)
    except (UnicodeError, json.JSONDecodeError) as error:
        fail('invalid JSON: ' + str(error))


def read_assessments(path):
    return _read_disclosure(path, DELIVERY_LIMIT, 'disclosure exceeds 1 MiB')


def read_design_reviews(path):
    return _read_disclosure(path, DESIGN_LIMIT, 'Design disclosure exceeds 4 MiB')


def identity(value):
    if not isinstance(value, str) or not re.fullmatch(r'sha256:[0-9a-f]{64}', value):
        fail('invalid SHA-256 identity')


def path_in(root, value):
    text(value)
    path = PurePosixPath(value)
    if (not path.parts or path.is_absolute() or path.as_posix() != value or
            any(p in ('.', '..') or p.startswith('.') for p in path.parts) or
            '\\' in value or ':' in value or any(ord(c) < 32 or 127 <= ord(c) <= 159 for c in value) or
            value.startswith('design/architecture/views/browser/')):
        fail('unsafe or private subject path ' + value)
    target = root / value
    resolved = target.resolve()
    if not resolved.is_relative_to(root.resolve()):
        fail('subject path escapes repository')
    relative = resolved.relative_to(root.resolve())
    if any(p.startswith('.') for p in relative.parts) or relative.as_posix().startswith('design/architecture/views/browser/'):
        fail('subject path resolves to private or generated data')
    return target


def state(value, kind):
    if not isinstance(value, str) or value not in STATES[kind]:
        fail('unknown ' + kind + ' state')


def _admit_legacy(model, selected):
    fields(selected, 'format_version assessments')
    if type(selected['format_version']) is not int or selected['format_version'] != 1:
        fail('unknown format version')
    if not isinstance(selected['assessments'], list):
        fail('expected assessments array')
    # Validate all closed state vocabularies before cross-field consistency work.
    for account in selected['assessments']:
        fields(account, 'requirement definition scope record implementation verification criteria')
        for kind in STATES:
            fields(account[kind], 'state actor reported_at summary limitations subjects')
            state(account[kind]['state'], kind)
        if not isinstance(account['criteria'], list):
            fail('expected criteria array')
        for criterion in account['criteria']:
            fields(criterion, 'number implementation verification evidence gaps')
            for kind in STATES:
                state(criterion[kind], kind)
    result = {}
    for original in selected['assessments']:
        account = deepcopy(original)
        rid = account['requirement']
        text(rid)
        if rid in result:
            fail('duplicate requirement selection ' + rid)
        if rid not in model.records or model.records[rid].data['type'] != 'allocated-requirement':
            fail('selected requirement must be an existing AR')
        text(account['scope'])
        fields(account['record'], 'change evidence')
        for value in account['record'].values():
            if not isinstance(value, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', value):
                fail('invalid operational record reference')
        definition = account['definition']
        fields(definition, 'path identity content')
        path = path_in(model.root, definition['path'])
        current_path = model.root / model.records[rid].path
        identity(definition['identity'])
        text(definition['content'])
        if 'sha256:' + hashlib.sha256(definition['content'].encode('utf-8')).hexdigest() != definition['identity']:
            fail('captured definition bytes do not match identity')
        try:
            captured = json.loads(definition['content'], object_pairs_hook=unique_object)
        except json.JSONDecodeError:
            fail('invalid captured definition JSON')
        if not isinstance(captured, dict) or captured.get('id') != rid or captured.get('type') != 'allocated-requirement':
            fail('captured definition is not the selected AR')
        criteria = captured.get('acceptance_criteria')
        texts(criteria)
        if not criteria:
            fail('captured definition has no criteria')
        numbers = [c['number'] for c in account['criteria']]
        if (any(type(n) is not int for n in numbers) or len(numbers) != len(criteria) or
                set(numbers) != set(range(1, len(criteria) + 1))):
            fail('incomplete or duplicate criterion coverage')
        account['criteria'].sort(key=lambda c: c['number'])
        for criterion in account['criteria']:
            texts(criterion['evidence']); texts(criterion['gaps'])
            criterion['text'] = criteria[criterion['number'] - 1]
        account['definition_current'] = (path == current_path and
            'sha256:' + hashlib.sha256(current_path.read_bytes()).hexdigest() == definition['identity'])
        for kind in STATES:
            claim = account[kind]
            for key in ('actor', 'reported_at', 'summary'):
                text(claim[key])
            try:
                datetime.strptime(claim['reported_at'], '%Y-%m-%dT%H:%M:%SZ')
            except ValueError:
                fail('reported_at must be a valid UTC timestamp YYYY-MM-DDTHH:MM:SSZ')
            texts(claim['limitations'])
            if not isinstance(claim['subjects'], list):
                fail('expected material subjects array')
            stale = [] if account['definition_current'] else ['AR definition changed or moved since assessment.']
            paths = set()
            for subject in claim['subjects']:
                fields(subject, 'path identity')
                target = path_in(model.root, subject['path']); identity(subject['identity'])
                if subject['path'] in paths:
                    fail('duplicate material subject')
                paths.add(subject['path'])
                if not target.is_file() or 'sha256:' + hashlib.sha256(target.read_bytes()).hexdigest() != subject['identity']:
                    stale.append('Material subject missing or changed: ' + subject['path'])
            complete = 'implemented' if kind == 'implementation' else 'passed'
            if claim['state'] == complete:
                if (not claim['subjects'] or claim['limitations'] or
                        any(c[kind] != complete or c['gaps'] or not c['evidence'] for c in account['criteria'])):
                    fail('complete claim requires all criteria, evidence, subjects and no gaps or limitations')
            if kind == 'implementation' and claim['state'] == 'partial':
                if (not claim['subjects'] or not any(c[kind] in ('partial', 'implemented') for c in account['criteria']) or
                        not (claim['limitations'] or any(c['gaps'] for c in account['criteria']))):
                    fail('partial claim requires material subjects, implemented contribution and named remaining scope')
            if kind == 'implementation' and claim['state'] == 'not-started' and any(c[kind] != 'not-started' for c in account['criteria']):
                fail('not-started claim contradicts criterion progress')
            if kind == 'verification' and claim['state'] == 'not-assessed' and any(c[kind] == 'failed' for c in account['criteria']):
                fail('not-assessed claim hides an identified failed criterion')
            if kind == 'verification' and claim['state'] == 'failed' and not any(c[kind] == 'failed' and c['evidence'] for c in account['criteria']):
                fail('failed verification requires identified failed criterion and evidence')
            claim['current_state'] = ('unknown' if kind == 'implementation' else 'needs-reassessment') if stale else claim['state']
            claim['applicability'] = stale
        result[rid] = account
    return result


DESIGN_SNAPSHOT = 'design-review-snapshot.data'
EMPTY_DESIGN = {'format_version': 1, 'reviews': []}
DESIGN_STATES = {'covered', 'gap'}
ALLOCATION_STATES = {'review-needed', 'deferred', 'required', 'not-required'}


def design_identity(value):
    """Identity of a disclosed outcome basis or original selected account."""
    return 'sha256:' + hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def outcome_basis(account):
    basis = account.get('outcome_basis')
    fields(basis, 'identity outcomes sr_children support')
    identity(basis['identity'])
    if basis['identity'] != design_identity({k: v for k, v in basis.items() if k != 'identity'}):
        fail('outcome basis bytes do not match identity')
    outcomes = basis['outcomes']
    if not isinstance(outcomes, list) or not outcomes:
        fail('IR requires nonempty assessed stakeholder outcomes')
    for outcome in outcomes:
        fields(outcome, 'number text sources'); text(outcome['text'])
        if not isinstance(outcome['sources'], list) or not outcome['sources']:
            fail('outcome requires exact source attribution')
        seen = set()
        for source in outcome['sources']:
            fields(source, 'path identity'); text(source['path']); identity(source['identity'])
            if source['path'] in seen or source not in account['subjects']:
                fail('outcome source must be a unique declared material subject')
            seen.add(source['path'])
    if any(type(o['number']) is not int for o in outcomes) or [o['number'] for o in outcomes] != list(range(1, len(outcomes) + 1)):
        fail('invalid stakeholder outcome numbering')
    children = basis['sr_children']
    if not isinstance(children, list) or not children or any(not isinstance(c, str) or not re.fullmatch(r'SR-\d+', c) for c in children) or children != sorted(set(children)):
        fail('invalid captured SR membership')
    if not isinstance(basis['support'], list):
        fail('expected outcome support array')
    for support in basis['support']:
        fields(support, 'requirement identity'); text(support['requirement']); identity(support['identity'])
    if sorted(s['requirement'] for s in basis['support']) != children:
        fail('outcome support must identify every captured SR exactly once')
    return [o['text'] for o in outcomes]


def project_design_reviews(model, selected, capture=None):
    """Project caller-selected actual Design judgments with exact applicability."""
    fields(selected, 'format_version reviews')
    if type(selected['format_version']) is not int or selected['format_version'] not in (1, 2):
        fail('unknown design review format version')
    if not isinstance(selected['reviews'], list):
        fail('expected reviews array')
    for account in selected['reviews']:
        fields(account, 'requirement definition state scope actor reported_at review summary limitations subjects criteria allocation ar_children' +
               (' outcome_basis' if selected['format_version'] == 2 else ''))
        if not isinstance(account['state'], str) or account['state'] not in DESIGN_STATES:
            fail('unknown design state')
        if not isinstance(account['criteria'], list):
            fail('expected design criteria array')
        for criterion in account['criteria']:
            fields(criterion, 'number state explanation')
            if not isinstance(criterion['state'], str) or criterion['state'] not in DESIGN_STATES:
                fail('unknown design criterion state')
        if account['allocation'] is not None:
            fields(account['allocation'], 'state explanation')
            if not isinstance(account['allocation']['state'], str) or account['allocation']['state'] not in ALLOCATION_STATES:
                fail('unknown allocation state')
    result = {}
    for original in selected['reviews']:
        account = deepcopy(original)
        rid = account['requirement']; text(rid)
        if rid in result:
            fail('duplicate design requirement selection')
        record = model.records.get(rid)
        kinds = ('system-requirement', 'allocated-requirement') + (('initial-requirement',) if selected['format_version'] == 2 else ())
        if record is None or record.data['type'] not in kinds:
            fail('design selection must identify a supported requirement kind')
        is_ir = record.data['type'] == 'initial-requirement'
        if not is_ir and account.get('outcome_basis') is not None:
            fail('only IR accounts may declare a stakeholder outcome basis')
        for key in ('scope', 'actor', 'reported_at', 'summary'):
            text(account[key])
        if not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ', account['reported_at']):
            fail('design reported_at must be a UTC timestamp')
        try:
            datetime.strptime(account['reported_at'], '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            fail('invalid design reported_at')
        texts(account['limitations'])
        fields(account['review'], 'change id')
        for value in account['review'].values():
            if not isinstance(value, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', value):
                fail('invalid design review reference')
        definition = account['definition']; fields(definition, 'path identity content')
        path = path_in(model.root, definition['path']); identity(definition['identity']); text(definition['content'])
        if 'sha256:' + hashlib.sha256(definition['content'].encode()).hexdigest() != definition['identity']:
            fail('captured design definition bytes do not match identity')
        try:
            captured = json.loads(definition['content'], object_pairs_hook=unique_object)
        except json.JSONDecodeError:
            fail('invalid captured design definition')
        if not isinstance(captured, dict) or captured.get('id') != rid or captured.get('type') != record.data['type']:
            fail('captured design definition kind or ID mismatch')
        if not isinstance(account['subjects'], list) or not account['subjects']:
            fail('design review requires material subjects')
        criteria = outcome_basis(account) if is_ir else captured.get('acceptance_criteria'); texts(criteria)
        numbers = [c['number'] for c in account['criteria']]
        if not criteria or any(type(n) is not int for n in numbers) or len(numbers) != len(criteria) or set(numbers) != set(range(1, len(criteria) + 1)):
            fail('incomplete or duplicate design criterion coverage')
        account['criteria'].sort(key=lambda c: c['number'])
        for c in account['criteria']:
            text(c['explanation']); c['text'] = criteria[c['number'] - 1]
        current_path = model.root / record.path
        current_content = capture.read(record.path.as_posix()) if capture else current_path.read_bytes()
        account['definition_current'] = path == current_path and current_content is not None and 'sha256:' + hashlib.sha256(current_content).hexdigest() == definition['identity']
        stale = [] if account['definition_current'] else ['Requirement definition changed or moved since review.']
        if not isinstance(account['subjects'], list) or not account['subjects']:
            fail('design review requires material subjects')
        paths = set()
        for subject in account['subjects']:
            fields(subject, 'path identity')
            target = path_in(model.root, subject['path']); identity(subject['identity'])
            if subject['path'] in paths:
                fail('duplicate design material subject')
            paths.add(subject['path'])
            content = capture.read(subject['path']) if capture else (target.read_bytes() if target.is_file() else None)
            if content is None or 'sha256:' + hashlib.sha256(content).hexdigest() != subject['identity']:
                stale.append('Material subject missing or changed: ' + subject['path'])
        allocation = account['allocation']
        if allocation is not None:
            text(allocation['explanation'])
        children = account['ar_children']
        if is_ir:
            if children is not None or allocation is not None:
                fail('IR design review cannot declare SR allocation')
            current = sorted(e.source for e in model.edges if e.relation == 'parent' and e.target == rid and model.records[e.source].data['type'] == 'system-requirement')
            if account['outcome_basis']['sr_children'] != current:
                stale.append('Direct SR membership changed since review.')
        elif record.data['type'] == 'allocated-requirement':
            if children is not None or allocation is not None:
                fail('AR design review cannot declare SR allocation')
        else:
            if not isinstance(children, list) or any(not isinstance(c, str) or not re.fullmatch(r'AR-\d+', c) for c in children) or children != sorted(set(children)):
                fail('invalid captured AR membership')
            current = sorted(e.source for e in model.edges if e.relation == 'parent' and e.target == rid and model.records[e.source].data['type'] == 'allocated-requirement')
            if children != current:
                stale.append('Direct AR membership changed since review.')
            if account['state'] == 'covered' and not children and (allocation is None or allocation['state'] != 'not-required'):
                fail('covered SR without ARs requires reviewed no-further-AR-needed disposition')
        criterion_gap = any(c['state'] == 'gap' for c in account['criteria'])
        allocation_gap = allocation is not None and allocation['state'] in ('review-needed', 'deferred', 'required')
        if account['state'] == 'covered' and (criterion_gap or allocation_gap):
            fail('covered design contradicts criterion or allocation gap')
        if account['state'] == 'gap' and not (criterion_gap or allocation_gap):
            fail('design gap requires criterion or allocation gap')
        account['current_state'] = 'needs-reassessment' if stale else account['state']
        account['applicability'] = stale
        result[rid] = account
    # Evaluate reliance only after all accounts have their own source applicability.
    originals = {a['requirement']: a for a in selected['reviews']}
    for account in result.values():
        if account.get('outcome_basis') is None:
            continue
        for support in account['outcome_basis']['support']:
            child = result.get(support['requirement'])
            if child is None or design_identity(originals[support['requirement']]) != support['identity']:
                account['applicability'].append('Relied-upon SR account missing or changed: ' + support['requirement'])
            elif child['applicability']:
                account['applicability'].append('Relied-upon SR account needs reassessment: ' + support['requirement'])
            elif account['state'] == 'covered' and child['current_state'] != 'covered':
                account['applicability'].append('Covered IR conflicts with relied-upon SR gap: ' + support['requirement'])
        if account['applicability']:
            account['current_state'] = 'needs-reassessment'
    return result


# Delivery v1 is an external compatibility boundary. Both versions leave this
# module in the same representation; neither the reader nor callers branch on it.
DELIVERY_LIMIT = 1024 * 1024
NORMALIZED_LIMIT = 4 * 1024 * 1024
FILE_LIMIT = 16 * 1024 * 1024
TOTAL_LIMIT = 128 * 1024 * 1024
PATH_LIMIT = 1024
REASONS = ('no-account', 'reported-noncurrent', 'definition-changed',
           'outcome-basis-changed', 'subject-unavailable', 'subject-changed',
           'membership-changed', 'design-support-unavailable',
           'child-support-unavailable', 'child-support-adverse', 'open-concern',
           'conflicting-claims', 'resolution-unavailable', 'superseded')
KINDS = {'initial-requirement': 'IR', 'system-requirement': 'SR', 'allocated-requirement': 'AR'}
SCHEMA = json.loads((Path(__file__).resolve().parents[2] /
                    'design/support/requirement-delivery-v2.schema.json').read_text())


def decode_json(content, depth=None):
    # Inspect lexical nesting before JSON constructs recursive containers.
    level = 0
    quoted = escaped = False
    for char in content:
        if quoted:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char in '[{':
            level += 1
            if depth is not None and level > depth:
                fail('JSON nesting exceeds 32 containers')
        elif char in ']}':
            level -= 1
    try:
        return json.loads(content, object_pairs_hook=unique_object,
                          parse_constant=lambda _: fail('nonfinite JSON number'))
    except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
        fail('invalid JSON: ' + str(error))


def compact(value):
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(',', ':'), allow_nan=False).encode('utf-8')
    except (UnicodeError, ValueError):
        fail('invalid Unicode or number')


def without_identity(value):
    return {k: v for k, v in value.items() if k != 'identity'}


def check_identity(value):
    if value['identity'] != design_identity(without_identity(value)):
        fail('structured identity mismatch')


def claim_identity(account, kind):
    return design_identity({'requirement': account['requirement'], 'kind': account['kind'],
        'definition_path': account['definition']['path'],
        'definition_identity': account['definition']['identity'], 'scope': account['scope'],
        'outcome_basis_identity': account['outcome_basis']['identity'] if account['outcome_basis'] else None,
        'claim_kind': kind, 'claim': without_identity(account[kind])})


def ordered(values):
    return [r for r in REASONS if r in values]


def unique(values, label):
    if len(values) != len(set(values)):
        fail('duplicate ' + label)


def timestamp(value):
    try:
        datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        fail('invalid UTC timestamp')


class DeliveryCapture:
    """A bounded, immutable observation reused throughout admission/comparison."""
    def __init__(self, model):
        self.model = model
        self.contents = {}
        self.total = 0

    def read(self, value):
        target = path_in(self.model.root, value)
        if value not in self.contents:
            if len(self.contents) >= PATH_LIMIT:
                fail('material path count exceeds 1024')
            content = self._bytes(target)
            if content is not None:
                self.total += len(content)
                if self.total > TOTAL_LIMIT:
                    fail('total material bytes exceed 128 MiB')
            self.contents[value] = content
            captured = self.model.bytes.get(Path(value))
            if captured is not None and captured != content:
                fail('model capture changed: ' + value)
        return self.contents[value]

    @staticmethod
    def _bytes(target):
        if not target.is_file():
            return None
        with target.open('rb') as stream:
            content = stream.read(FILE_LIMIT + 1)
        if len(content) > FILE_LIMIT:
            fail('material file exceeds 16 MiB')
        return content

    def subjects(self, subjects):
        unique([s['path'] for s in subjects], 'material subject')
        reasons, messages = [], []
        for subject in subjects:
            content = self.read(subject['path'])
            code = ('subject-unavailable' if content is None else
                    'subject-changed' if 'sha256:' + hashlib.sha256(content).hexdigest() != subject['identity'] else None)
            if code:
                reasons.append(code); messages.append(code + ': ' + subject['path'])
        return reasons, messages

    def verify(self):
        # Re-observation is a publication guard, never a replacement capture.
        for path, content in self.contents.items():
            if self._bytes(path_in(self.model.root, path)) != content:
                fail('material capture changed before publication: ' + path)
        for path, content in self.model.bytes.items():
            if (self.model.root / path).read_bytes() != content:
                fail('model capture changed before publication: ' + str(path))


def _report(account, kind, claim, criteria, version):
    return dict(identity=claim['identity'], source_format=version,
        definition=deepcopy(account['definition']), scope=account['scope'],
        actor=claim['actor'], reported_at=claim['reported_at'], state=claim['state'],
        summary=claim['summary'], limitations=deepcopy(claim['limitations']),
        subjects=deepcopy(claim['subjects']), source=deepcopy(claim.get('source')),
        legacy_record=None, criteria=criteria, outcome_basis=deepcopy(account['outcome_basis']),
        membership=deepcopy(claim['membership']), child_support=deepcopy(claim['child_support']),
        nonreliance=deepcopy(claim['nonreliance']), design_support=deepcopy(claim['design_support']),
        concerns=deepcopy(claim['concerns']), applicability=deepcopy(claim['applicability']),
        reason_codes=[], dispositions=[])


def _indicator(reports, selected=None, reasons=(), messages=(), kind='implementation'):
    codes = ordered(reasons if reports else [*reasons, 'no-account'])
    fallback = 'unknown' if kind == 'implementation' else ('needs-reassessment' if reports else 'not-assessed')
    return {'state': selected['state'] if selected else fallback,
        'reason_codes': codes, 'explanation': ' '.join(dict.fromkeys(messages)) or
            ('Selected attributable assessment.' if selected else 'No account is selected for this requirement.'),
        'selected': selected, 'history': [r for r in reports if r is not selected]}


def _legacy_projection(model, selected):
    admitted = _admit_legacy(model, selected)
    result = {}
    for rid, account in admitted.items():
        entry = {'requirement': rid, 'kind': 'allocated-requirement'}
        original = next(a for a in selected['assessments'] if a['requirement'] == rid)
        for kind in STATES:
            claim = account[kind]
            criterion_source = [{'number': c['number'], 'state': c[kind],
                'evidence': c['evidence'], 'gaps': c['gaps']} for c in original['criteria']]
            ident = design_identity({'source_format': 1, 'requirement': rid,
                'definition_path': account['definition']['path'],
                'definition_identity': account['definition']['identity'], 'scope': account['scope'],
                'claim_kind': kind, 'record': account['record'], 'claim': original[kind],
                'criteria': criterion_source})
            criteria = [{'key': 'C' + str(c['number']), 'text': c['text'], 'state': c[kind],
                'explanation': 'Legacy version 1 criterion account.', 'gaps': c['gaps'],
                'evidence': [{'source': None, 'summary': e, 'subjects': [], 'limitations': []} for e in c['evidence']]}
                for c in account['criteria']]
            shaped = {**claim, 'identity': ident, 'membership': None, 'child_support': [],
                'nonreliance': [], 'design_support': [], 'concerns': [],
                'applicability': {'state': 'current', 'explanation': 'Legacy version 1 account; currentness is bounded by its original admission and material comparisons.'}}
            report = _report({**account, 'outcome_basis': None}, kind, shaped, criteria, 1)
            report['legacy_record'] = account['record']
            codes = []
            if not account['definition_current']:
                codes.append('definition-changed')
            if any(m.startswith('Material subject') for m in claim['applicability']):
                codes.append('subject-changed')
            report['reason_codes'] = ordered(codes)
            entry[kind] = _indicator([report], None if codes else report, codes,
                                     claim['applicability'], kind)
        result[rid] = entry
    return result


def _validate_v2(selected):
    # Entire closed vocabulary is checked before any cross-field comparison/read.
    if type(selected.get('format_version')) is not int:
        fail('unknown format version')
    compact(selected)  # Reject surrogates/nonfinite values supplied by direct callers.
    error = next(Draft202012Validator(SCHEMA).iter_errors(selected), None)
    if error:
        fail('invalid delivery v2 structure at ' + '/'.join(map(str, error.absolute_path)) + ': schema rule ' + str(error.validator))
    unique([compact(a) for a in selected['assessments']], 'assessment account')
    unique([compact(r) for r in selected['resolutions']], 'resolution')
    stack = [selected]
    while stack:
        value = stack.pop()
        if isinstance(value, dict):
            if 'reported_at' in value:
                timestamp(value['reported_at'])
            stack.extend(value.values())
        elif isinstance(value, list):
            stack.extend(value)


def _admit_v2(model, selected, capture):
    reports = {}
    for account in selected['assessments']:
        rid, kind = account['requirement'], account['kind']
        if not rid.startswith(KINDS[kind] + '-') or rid not in model.records or model.records[rid].data['type'] != kind:
            fail('selected requirement kind or ID mismatch')
        definition = account['definition']
        path_in(model.root, definition['path'])
        if definition['identity'] != 'sha256:' + hashlib.sha256(definition['content'].encode()).hexdigest():
            fail('captured definition identity mismatch')
        captured = decode_json(definition['content'], depth=32)
        compact(captured)
        if not isinstance(captured, dict) or captured.get('id') != rid or captured.get('type') != kind:
            fail('captured definition kind or ID mismatch')
        basis = account['outcome_basis']
        basis_reasons, basis_messages = [], []
        if basis:
            check_identity(basis)
            if basis['review']['source']['kind'] != 'review':
                fail('outcome basis requires Review source')
            reasons, messages = capture.subjects(basis['review']['subjects'])
            if reasons:
                basis_reasons.append('outcome-basis-changed'); basis_messages.extend(messages)
            if {'path': definition['path'], 'identity': definition['identity']} not in basis['review']['subjects']:
                fail('IR definition must be in reviewed outcome subjects')
            units = basis['outcomes']
            if [u['key'] for u in units] != ['O' + str(n) for n in range(1, len(units) + 1)]:
                fail('invalid outcome numbering')
            for unit in units:
                unique([s['path'] for s in unit['sources']], 'outcome source')
                if any(s not in basis['review']['subjects'] for s in unit['sources']):
                    fail('outcome sources outside reviewed basis')
        elif kind != 'initial-requirement':
            criteria = captured.get('acceptance_criteria')
            texts(criteria)
            if not criteria:
                fail('captured definition has no criteria')
            units = [{'key': 'C' + str(i + 1), 'text': v} for i, v in enumerate(criteria)]
        else:
            units = []
        current_path = model.records[rid].path.as_posix()
        current_bytes = capture.read(current_path)
        if current_bytes is None:
            fail('required current definition unavailable')
        definition_current = (current_path == definition['path'] and
            'sha256:' + hashlib.sha256(current_bytes).hexdigest() == definition['identity'])
        for claim_kind in STATES:
            claim = account[claim_kind]
            if claim is None:
                continue
            if claim['identity'] != claim_identity(account, claim_kind):
                fail('claim identity mismatch')
            if claim['source']['kind'] != ('evidence' if claim_kind == 'implementation' else 'verification'):
                fail('wrong claim source kind')
            if [c['key'] for c in claim['criteria']] != [u['key'] for u in units]:
                fail('incomplete or duplicate criterion coverage')
            reasons, messages = capture.subjects(claim['subjects'])
            reasons += basis_reasons; messages += basis_messages
            if not definition_current:
                reasons.append('definition-changed'); messages.append('Requirement definition changed or moved: ' + definition['path'])
            if claim['applicability']['state'] != 'current':
                reasons.append('reported-noncurrent'); messages.append(claim['applicability']['explanation'])
            complete = 'implemented' if claim_kind == 'implementation' else 'passed'
            for c in claim['criteria']:
                for evidence in c['evidence']:
                    unique([s['path'] for s in evidence['subjects']], 'evidence subject')
                    if any(s not in claim['subjects'] for s in evidence['subjects']):
                        fail('evidence subjects outside claim material basis')
            states = [c['state'] for c in claim['criteria']]
            if claim['state'] == complete and (not claim['subjects'] or claim['limitations'] or
                    any(c['state'] != complete or c['gaps'] or not c['evidence'] for c in claim['criteria'])):
                fail('complete claim requires all criteria, evidence, subjects and no gaps or limitations')
            if claim_kind == 'implementation':
                if claim['state'] in ('unknown', 'not-started') and any(v != claim['state'] for v in states):
                    fail('implementation state contradicts criterion progress')
                if claim['state'] == 'partial' and (not claim['subjects'] or
                        not any(v in ('partial', 'implemented') for v in states) or
                        not (claim['limitations'] or any(c['gaps'] for c in claim['criteria']))):
                    fail('partial claim requires contribution and remaining scope')
            else:
                if claim['state'] in ('not-assessed', 'needs-reassessment') and 'failed' in states and not reasons:
                    fail('verification state hides applicable failed criterion')
                if claim['state'] == 'not-assessed' and 'failed' in states:
                    fail('not-assessed claim hides failed criterion')
                if claim['state'] == 'failed' and not any(c['state'] == 'failed' and c['evidence'] for c in claim['criteria']):
                    fail('failed verification requires identified failed criterion and evidence')
            unique([c['id'] for c in claim['concerns']], 'concern')
            for concern in claim['concerns']:
                if (concern['state'] == 'resolved') != (concern['disposition'] is not None):
                    fail('concern disposition contradicts state')
            membership = claim['membership']
            if kind == 'allocated-requirement' and (membership or claim['child_support'] or claim['nonreliance']):
                fail('AR cannot declare child membership or reliance')
            needs_membership = kind != 'allocated-requirement' and (claim['state'] == complete or claim['child_support'] or claim['nonreliance'])
            if needs_membership and membership is None:
                fail('parent claim requires captured membership')
            if membership is not None:
                check_identity(membership)
                child_ids = [c['requirement'] for c in membership['children']]
                if child_ids != sorted(set(child_ids)):
                    fail('membership must be sorted and unique')
                prefix = 'SR-' if kind == 'initial-requirement' else 'AR-'
                if any(not c.startswith(prefix) or c not in model.records for c in child_ids):
                    fail('unsupported captured child identity or kind')
                accounted = [c['requirement'] for c in claim['child_support'] + claim['nonreliance']]
                if sorted(accounted) != child_ids:
                    fail('every captured child must have exactly one support or nonreliance')
                current = [{'requirement': e.source, 'definition_identity': 'sha256:' + hashlib.sha256(capture.read(model.records[e.source].path.as_posix())).hexdigest()}
                    for e in model.edges if e.relation == 'parent' and e.target == rid]
                if sorted(current, key=lambda c: c['requirement']) != membership['children']:
                    reasons.append('membership-changed'); messages.append('Captured direct-child membership changed.')
            for support in claim['child_support']:
                unique(support['coverage'], 'child coverage key')
                if any(key not in [u['key'] for u in units] for key in support['coverage']):
                    fail('child coverage outside parent units')
            unique([s['requirement'] for s in claim['design_support']], 'Design dependency')
            criteria = [{**deepcopy(c), 'text': u['text']} for c, u in zip(claim['criteria'], units)]
            report = _report(account, claim_kind, claim, criteria, 2)
            report['reason_codes'] = ordered(reasons)
            key = (rid, claim_kind, claim['identity'])
            if key not in reports:
                reports[key] = (report, messages)
    # Reference admission uses captured membership, independent of current edges.
    for (rid, kind, _), (report, _) in reports.items():
        for support in report['child_support']:
            child = reports.get((support['requirement'], kind, support['claim']))
            member = next(c for c in report['membership']['children'] if c['requirement'] == support['requirement'])
            if child is None or child[0]['definition']['identity'] != member['definition_identity']:
                fail('missing or mismatched captured child claim')
    return reports


def _resolve_reports(rid, kind, group, resolutions, capture):
    candidates = [r for r, _ in group if not set(r['reason_codes']) - {'child-support-adverse'}]
    messages = [m for _, ms in group for m in ms]
    reasons = [code for r, _ in group for code in r['reason_codes']]
    reports = [r for r, _ in group]
    by_id = {r['identity']: r for r in reports}
    valid = []
    for resolution in resolutions:
        if resolution['requirement'] != rid or resolution['kind'] != kind:
            continue
        refs = [resolution['selected']] + [s['claim'] for s in resolution['superseded']]
        unique(refs, 'resolution reference')
        if any(ref not in by_id for ref in refs):
            fail('unknown resolution claim reference')
        expected_source = 'evidence' if kind == 'implementation' else 'verification'
        if resolution['source']['kind'] != expected_source or any(s['disposition']['kind'] != expected_source for s in resolution['superseded']):
            fail('wrong resolution source kind')
        codes, notes = capture.subjects(resolution['subjects'])
        if resolution['applicability']['state'] != 'current':
            codes.append('reported-noncurrent'); notes.append(resolution['applicability']['explanation'])
        status = 'stale' if codes else 'current'
        if set(refs) != {r['identity'] for r in candidates}:
            status = 'insufficient' if not codes else 'stale'
            notes.append('Resolution does not cover the complete current competing set.')
        for superseded in resolution['superseded']:
            unique(superseded['addressed'], 'adverse disposition token')
            adverse = by_id[superseded['claim']]
            tokens = {'criterion:' + c['key'] for c in adverse['criteria'] if c['state'] == 'failed'}
            tokens |= {'concern:' + c['id'] for c in adverse['concerns'] if c['state'] != 'resolved'}
            if not tokens.issubset(superseded['addressed']):
                status = 'insufficient' if not codes else 'stale'
                notes.append('Resolution omits adverse criterion or concern dispositions.')
        if status == 'current':
            valid.append(by_id[resolution['selected']])
        else:
            codes.append('resolution-unavailable')
        disposition = {'resolution': deepcopy(resolution), 'status': status,
            'reason_codes': ordered(codes), 'explanation': ' '.join(notes) or 'Explicit complete-set disposition.'}
        for ref in refs:
            by_id[ref]['dispositions'].append(disposition)
        messages.extend(notes)
    chosen = candidates[0] if len(candidates) == 1 else None
    inadequate = any(d['status'] != 'current' for r in reports for d in r['dispositions'])
    if len(valid) == 1:
        chosen = valid[0]
        for r in candidates:
            if r is not chosen:
                r['reason_codes'] = ordered(r['reason_codes'] + ['superseded'])
    elif len(valid) > 1:
        chosen = None; reasons.append('conflicting-claims'); messages.append('Multiple applicable resolutions conflict.')
    elif len(candidates) > 1:
        reasons += ['conflicting-claims', 'resolution-unavailable']
        messages.append('Competing assessments require an explicit complete disposition; no timestamp winner.')
    if chosen and inadequate and not valid and chosen['state'] in ('implemented', 'passed'):
        reasons.append('resolution-unavailable'); chosen = None
    if chosen:
        # Open concerns stay candidates; only positive presentation is restricted.
        open_concerns = [c for c in chosen['concerns'] if c['state'] != 'resolved']
        if 'child-support-adverse' in chosen['reason_codes'] and chosen['state'] in ('implemented', 'passed'):
            reasons.append('child-support-adverse')
            chosen = None
        if open_concerns and chosen is not None:
            chosen['reason_codes'] = ordered(chosen['reason_codes'] + ['open-concern'])
            messages.extend('Unresolved concern ' + c['id'] + ': ' + c['explanation'] for c in open_concerns)
            if chosen['state'] in ('implemented', 'passed'):
                reasons.append('open-concern'); chosen = None
    if chosen:
        reasons = chosen['reason_codes']
    return _indicator(reports, chosen, reasons, messages, kind)


def project_assessments(model, selected, design_reviews=None, capture=None):
    if not isinstance(selected, dict) or type(selected.get('format_version')) is not int:
        fail('unknown format version')
    if selected['format_version'] == 1:
        result = _legacy_projection(model, selected)
    elif selected['format_version'] == 2:
        _validate_v2(selected)
        if len(compact(selected)) > DELIVERY_LIMIT:
            fail('disclosure exceeds 1 MiB')
        capture = capture or DeliveryCapture(model)
        reports = _admit_v2(model, selected, capture)
        designs = {} if design_reviews is None else design_reviews
        design_data = project_design_reviews(model, designs, capture) if designs else {}
        design_originals = {a['requirement']: design_identity(a) for a in designs.get('reviews', [])}
        result = {a['requirement']: {'requirement': a['requirement'], 'kind': a['kind']} for a in selected['assessments']}
        # Resolution references must be checked even when the selected group is empty.
        for r in selected['resolutions']:
            if (r['requirement'], r['kind'], r['selected']) not in reports:
                fail('unknown resolution claim reference')
        for rid in sorted(result, key=lambda r: {'AR': 0, 'SR': 1, 'IR': 2}[r[:2]]):
            for kind in STATES:
                group = [(r, ms) for (req, ck, _), (r, ms) in reports.items() if req == rid and ck == kind]
                for report, messages in group:
                    for support in report['design_support']:
                        current = design_data.get(support['requirement'])
                        if current is None or current['current_state'] == 'needs-reassessment' or design_originals.get(support['requirement']) != support['identity']:
                            report['reason_codes'].append('design-support-unavailable'); messages.append('Relied-upon Design account unavailable: ' + support['requirement'])
                    for support in report['child_support']:
                        child = result[support['requirement']][kind]
                        if child['selected'] is None or child['selected']['identity'] != support['claim']:
                            report['reason_codes'].append('child-support-unavailable'); messages.append('Relied-upon child claim unavailable: ' + support['requirement'])
                        if child['state'] == 'failed' or any((r['state'] == 'failed' or any(c['state'] != 'resolved' for c in r['concerns'])) for r in ([child['selected']] if child['selected'] else []) + child['history'] if not set(r['reason_codes']) - {'open-concern', 'child-support-adverse'}):
                            report['reason_codes'].append('child-support-adverse'); messages.append('Relied-upon child has adverse support: ' + support['requirement'])
                    report['reason_codes'] = ordered(report['reason_codes'])
                result[rid][kind] = _resolve_reports(rid, kind, group, selected['resolutions'], capture)
        # Explicitly absent claims have the same normalized shape as no selection.
    else:
        fail('unknown format version')
    if len(compact(result)) > NORMALIZED_LIMIT:
        fail('normalized delivery exceeds 4 MiB')
    return result


def assessment_snapshot(selected):
    if selected['format_version'] == 1:
        return (json.dumps(selected, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()
    snapshot = compact(selected) + b'\n'
    if len(snapshot) > DELIVERY_LIMIT:
        fail('serialized delivery companion exceeds 1 MiB')
    return snapshot
