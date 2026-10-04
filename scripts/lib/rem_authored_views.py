"""Explicit source-owned view topics for the repository browser.

This is repository authoring input, not admission of arbitrary customer Markdown.
Registration is local to a Module; the compiler is an explicit build dependency.
"""
import base64
import hashlib
import json
import math
import re
import tomllib
import xml.etree.ElementTree as ET

FIELDS = {'id', 'title', 'view', 'kind', 'qualification', 'source', 'anchor', 'description'}
KINDS = {'topology', 'flowchart', 'sequence', 'state'}
VIEWS = {'logical', 'process', 'development', 'physical', 'scenarios'}


def fail(message):
    raise ValueError('Authored view: ' + message)


def validate_d2_source(source, kind):
    """Admit plain, self-contained D2 before any renderer can read resources.

    This deliberately small repository authoring grammar permits labelled nodes,
    containers, connections, directions and selected shapes. It does not admit
    D2 imports, variables, resources, markup, configuration or arbitrary styles.
    """
    path = r'[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)*'
    quoted = r'"(?:[^"\\\n]|\\["\\nrt])*"'
    reserved = {'shape', 'label', 'icon', 'link', 'tooltip', 'style', 'class',
                'classes', 'vars', 'direction', 'near', 'width', 'height', 'constraint',
                'layers', 'scenarios', 'steps'}
    depth, sequence = 0, False
    for number, raw in enumerate(source.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if line == '}':
            depth -= 1
            if depth < 0:
                fail('unbalanced D2 container')
            continue
        if re.fullmatch(r'direction: (?:right|down|left|up)', line):
            continue
        if re.fullmatch(r'shape: (?:rectangle|diamond|circle|oval|sequence_diagram)', line):
            if line == 'shape: sequence_diagram':
                if kind != 'sequence' or depth or sequence:
                    fail('diagram kind disagrees with D2 sequence shape')
                sequence = True
            continue
        edge = re.fullmatch(fr'({path})\s+(?:->|--|<->|<-)\s+({path})(?:\s*:\s*({quoted}))?', line)
        node = re.fullmatch(fr'({path}):\s*({quoted})(\s*\{{)?', line)
        if not edge and not node:
            fail(f'unsupported D2 syntax on line {number}')
        identifiers = edge.group(1, 2) if edge else (node.group(1),)
        if any(part in reserved for identifier in identifiers for part in identifier.split('.')):
            fail('unsupported D2 property or resource')
        label = edge.group(3) if edge else node.group(2)
        if label:
            value = json.loads(label)
            if any(token in value for token in ('${', '<', '>')):
                fail('unsupported D2 substitution or markup')
        if node and node.group(3):
            depth += 1
    if depth:
        fail('unbalanced D2 container')
    if sequence != (kind == 'sequence'):
        fail('diagram kind disagrees with D2 sequence shape')


def read_authored_topics(model):
    pending = []
    for record in model.of_type('module'):
        owner = model.root / record.path.parent
        path = owner / 'browser-views.toml'
        if not path.exists():
            continue
        if path.is_symlink():
            fail('symlinked registration is unsupported')
        raw = path.read_bytes()
        registration = tomllib.loads(raw.decode())
        if set(registration) != {'version', 'topics'} or type(registration['version']) is not int or registration['version'] != 1:
            fail('unsupported registration shape or version')
        if not isinstance(registration['topics'], list) or not registration['topics']:
            fail('unsupported empty topic collection')
        seen = set()
        for item in registration['topics']:
            if not isinstance(item, dict) or not FIELDS <= set(item) or set(item) - FIELDS - {'previous_kind'} or any(not isinstance(v, str) or not v.strip() for v in item.values()):
                fail('unsupported topic fields')
            # Closed vocabularies precede source consistency and access.
            if item['view'] not in VIEWS or item['kind'] not in KINDS or item['qualification'] not in {'proposed', 'observed'}:
                fail('unsupported view, diagram kind or qualification')
            if 'previous_kind' in item and item['previous_kind'] not in KINDS:
                fail('unsupported previous diagram kind')
            if not all(re.fullmatch(r'[a-z][a-z0-9-]*', item[k]) for k in ('id', 'anchor')):
                fail('unsupported topic identity or anchor')
            identity = (item['view'], item['qualification'], item['kind'], item['id'])
            identities = [identity]
            if 'previous_kind' in item:
                identities.append((item['view'], item['qualification'], item['previous_kind'], item['id']))
            for identity in identities:
                if identity in seen:
                    fail('duplicate qualified topic or previous route')
                seen.add(identity)
            pending.append((record, path, raw, item))
    topics = []
    for record, registry, raw, item in pending:
        # One explicit same-owner document; no traversal, includes or remote source.
        if item['source'] != 'README.md':
            fail('source must be the owning README.md')
        source_path = registry.parent / item['source']
        if source_path.is_symlink() or not source_path.is_file():
            fail('missing or symlinked source')
        content = source_path.read_bytes()
        marker = '<!-- architecture-diagram: ' + item['anchor'] + ' -->'
        text = content.decode()
        if text.count(marker) != 1:
            fail('source anchor must occur exactly once')
        match = re.search(re.escape(marker) + r'\s*```d2\n(.*?)\n```', text, re.S)
        if not match:
            fail('source anchor must directly select a D2 block')
        source = match[1]
        validate_d2_source(source, item['kind'])
        qualified = '-'.join((record.id, item['view'], item['qualification'], item['kind'], item['id']))
        previous = ['#' + '/'.join((item['view'], record.id, item['qualification'], item['previous_kind'], item['id']))] if 'previous_kind' in item else []
        topics.append({**item, 'owner': record.id, 'path': source_path.relative_to(model.root).as_posix(),
                       'registration': registry.relative_to(model.root).as_posix(),
                       'document_digest': hashlib.sha256(content).hexdigest(),
                       'registration_digest': hashlib.sha256(raw).hexdigest(),
                       'source': source, 'source_digest': hashlib.sha256(source.encode()).hexdigest(),
                       'key': 'authored-' + qualified,
                       'previous_routes': previous,
                       'route': '#' + '/'.join((item['view'], record.id, item['qualification'], item['kind'], item['id']))})
    return topics


def validate_svg(svg):
    root = ET.fromstring(svg)
    if root.tag != '{http://www.w3.org/2000/svg}svg':
        fail('compiler did not return SVG')
    for element in root.iter():
        tag = element.tag.rsplit('}', 1)[-1].lower()
        if tag in {'script', 'foreignobject', 'iframe', 'image', 'audio', 'video', 'object', 'embed', 'animate', 'animatetransform', 'animatemotion', 'set'}:
            fail('unsafe rendered SVG element')
        for key, value in element.attrib.items():
            name = key.rsplit('}', 1)[-1].lower()
            safe_urls = re.sub(r"url\(\s*['\"]?#[a-zA-Z0-9_.:-]+['\"]?\s*\)", '', value, flags=re.I)
            if re.search(r'url\(', safe_urls, re.I):
                fail('external rendered SVG resource')
            if name.startswith('on') or (name in {'href', 'src'} and not value.startswith('#')):
                fail('unsafe rendered SVG attribute')
        if tag == 'style' or 'style' in element.attrib:
            css = (element.text or '') + element.attrib.get('style', '')
            css = re.sub(r"url\(\s*['\"]?#[a-zA-Z0-9_.:-]+['\"]?\s*\)", '', css, flags=re.I)
            # Pinned D2 embeds subsetted fonts for portable SVG text. Permit only
            # literal WOFF data, never arbitrary data URLs or remote resources.
            def embedded_font(match):
                payload = base64.b64decode(match[1], validate=True)
                if not payload.startswith(b'wOFF'):
                    fail('invalid embedded D2 font')
                return ''
            css = re.sub(r'url\("data:application/font-woff;base64,([A-Za-z0-9+/=]+)"\)', embedded_font, css)
            if re.search(r'@import|url\(', css, re.I):
                fail('external rendered SVG style')
    box = [float(n) for n in root.attrib.get('viewBox', '').split()]
    if len(box) != 4 or not all(math.isfinite(n) for n in box) or min(box[2:]) <= 0:
        fail('invalid SVG dimensions')
    return box[2:]


def compile_authored_topics(topics, compile_svg):
    """Use the generator's same pinned D2 compiler for every admitted topic."""
    rendered, outputs = [], {}
    for topic in topics:
        key = topic['key']
        svg = compile_svg(key, topic['source']).encode()
        width, height = validate_svg(svg)
        rendered.append({**topic, 'width': width, 'height': height,
                         'image': 'data:image/svg+xml;base64,' + base64.b64encode(svg).decode()})
        outputs['diagrams/' + key + '.d2'] = (topic['source'] + '\n').encode()
        outputs['diagrams/' + key + '.svg'] = svg
    return rendered, outputs
