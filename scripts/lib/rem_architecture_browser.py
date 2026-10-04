"""Bounded browser projections of the validated REM model.

The source model owns relationships. These helpers add navigation and visual
aggregation only; public-entry correspondences never become collaboration edges.
"""

import hashlib
import json
import posixpath
import re
import textwrap
import tomllib


def _edge(edge):
    return {"source": edge.source, "relation": edge.relation,
            "target": edge.target, "path": edge.path.as_posix(),
            "field": edge.field}


def _descendants(model, identity):
    return sorted(record.id for record in model.of_type("module")
                  if identity in model.ancestors(record.id))


def _provider(model, identity):
    return model.incoming(identity, "provides")[0].source


def _top(model, identity):
    ancestors = model.ancestors(identity)
    return ancestors[-1] if ancestors else identity


def _visible_provider(interface, provider, displayed):
    """A collapsed provider boundary must explicitly expose its child contract."""
    return provider == displayed or displayed in interface.data.get("exposed_through", [])


def overview_collaborations(model):
    """Cross-root collaborations, retaining exact owners behind each projection."""
    result = []
    for interface in model.of_type("interface"):
        provider = _provider(model, interface.id)
        provider_boundary = _top(model, provider)
        if not _visible_provider(interface, provider, provider_boundary):
            continue
        for edge in model.incoming(interface.id, "consumes"):
            consumer_boundary = _top(model, edge.source)
            if consumer_boundary != provider_boundary:
                result.append({"interface": interface.id, "consumer": edge.source,
                               "provider": provider,
                               "consumer_boundary": consumer_boundary,
                               "provider_boundary": provider_boundary})
    return result


# Presentation selections, not additional Scenario relationships. These retain
# the bounded CLI review scopes previously presented in the dependency view.
# Statements, observations, allocations and contribution arguments remain owned
# by the selected canonical records and are resolved afresh at generation time.
CLI_WALKTHROUGH_ALLOCATIONS = {
    "SCN-041": ("AR-013", "AR-014"),
    "SCN-042": ("AR-013", "AR-014", "AR-024"),
    "SCN-043": ("AR-015",),
    "SCN-044": ("AR-017", "AR-019", "AR-020"),
    "SCN-045": ("AR-016", "AR-017"),
    "SCN-046": ("AR-020", "AR-021", "AR-025", "AR-026"),
    "SCN-047": ("AR-022", "AR-023"),
    "SCN-048": ("AR-011", "AR-012"),
    "SCN-049": ("AR-027", "AR-028"),
}


def cli_cooperation(model):
    """Resolve a bounded logical-contract reading profile from source records.

    Topic labels and pointer selections aid reading; they establish neither
    execution order nor a new allocation or satisfaction claim. Named operation
    lookup avoids binding the selection to an operation's array position.
    """
    def source(owner, field):
        record = model.records.get(owner)
        if record is None:
            raise ValueError(f"CLI cooperation: missing selected record {owner}")
        value = record.data
        try:
            for token in field.lstrip("/").split("/"):
                token = token.replace("~1", "/").replace("~0", "~")
                value = value[int(token)] if isinstance(value, list) else value[token]
        except (KeyError, IndexError, ValueError, TypeError) as error:
            raise ValueError(f"{record.path}: missing CLI cooperation selection {field}") from error
        return {"owner": owner, "path": record.path.as_posix(), "field": field}

    def operation(owner, name, *fields):
        record = model.records.get(owner)
        matches = [index for index, item in enumerate(record.data.get("operations", []))
                   if item.get("name") == name] if record else []
        if len(matches) != 1:
            raise ValueError(f"CLI cooperation: expected one {owner} operation {name}")
        prefix = f"/operations/{matches[0]}"
        return [source(owner, prefix + ("/" + field if field else ""))
                for field in fields or ("",)]

    public = lambda *fields: operation("IF-004", "execute_public_request", *fields)
    topics = [
        {"key":"admission","title":"Admit an explicit public request","sources":public("purpose","inputs","preconditions")},
        {"key":"selected-records","title":"Read and present selected current records","sources":operation("IF-003","inspect_records")},
        {"key":"decision-basis","title":"Check the supplied decision basis","sources":operation("IF-003","execute_record_task","inputs","preconditions")},
        {"key":"candidate-construction","title":"Construct and preview a task candidate","sources":operation("IF-003","preview_record_task")},
        {"key":"guarded-execution","title":"Execute against current revision and declared reads","sources":operation("IF-003","execute_record_task","behavior")},
        {"key":"publication","title":"Commit coherent durable current state","sources":operation("IF-003","execute_record_task","outputs","failure_behavior")},
        {"key":"actual-outcomes","title":"Report actual effects independently of diagnostics","sources":[source("IF-004","/consistency_rules/0")]},
        {"key":"recovery","title":"Inspect interrupted updates; explicitly recover maintenance","sources":operation("IF-003","inspect_records")+operation("IF-003","restore_operational_scope")},
    ]
    walkthroughs = []
    for identity, allocated in CLI_WALKTHROUGH_ALLOCATIONS.items():
        scenario = model.records.get(identity)
        if scenario is None or scenario.data.get("type") != "scenario":
            raise ValueError(f"CLI cooperation: missing selected Scenario {identity}")
        functions, owners, requirements = set(), set(), set()
        for allocation in allocated:
            record = model.records.get(allocation)
            if record is None or record.data.get("type") != "allocated-requirement":
                raise ValueError(f"CLI cooperation: missing selected allocation {allocation}")
            parent = model.outgoing(allocation, "parent")[0].target
            if parent not in scenario.data.get("informs", []):
                raise ValueError(f"CLI cooperation: {identity} does not inform parent of {allocation}")
            requirements.add(parent)
            owners.add(record.data["allocated_to"])
            functions.update(record.data.get("constrains", []))
        selected_contracts = {"IF-004"} if identity == "SCN-049" else {"IF-003", "IF-004"}
        contracts = {edge.target for owner in owners
                     for edge in model.outgoing(owner, "provides") + model.outgoing(owner, "consumes")
                     if edge.target in selected_contracts}
        # The parent-owned public contract remains context, not a second child
        # provider. Restrict this profile to the two selected record contracts.
        for owner in owners:
            for ancestor in model.ancestors(owner):
                contracts.update(edge.target for edge in model.outgoing(ancestor, "provides")
                                 if edge.target in selected_contracts)
        context = {_provider(model, contract) for contract in contracts} - owners
        walkthroughs.append({
            "scenario": identity, "allocated_requirements": list(allocated),
            "requirements": sorted(requirements), "functions": sorted(functions),
            "modules": sorted(owners), "interfaces": sorted(contracts),
            "context_modules": sorted(context),
            "sources": [source(identity, "/informs")] +
                       [source(allocation, "/allocated_to") for allocation in allocated],
        })
    return {"topics": topics, "walkthroughs": walkthroughs,
            "interfaces": ["IF-003", "IF-004"]}


def web_capabilities(model):
    """Read explicit presentation bindings; never infer availability from Features."""
    result, seen = [], set()
    fields = {"version", "kind", "id", "title", "feature", "source", "sections", "related"}
    sections = {"purpose", "access", "interactions", "limits"}
    for owner in model.of_type("module"):
        binding = model.root / owner.path.parent / "browser-capability.toml"
        if binding.is_symlink():
            raise ValueError("Web capability: symlinked binding is unsupported")
        if not binding.exists():
            continue
        raw = binding.read_bytes()
        spec = tomllib.loads(raw.decode())
        # Closed vocabularies reject before source access or reference consistency.
        if set(spec) != fields or type(spec["version"]) is not int or spec["version"] != 1 or spec["kind"] != "web":
            raise ValueError("Web capability: unsupported binding fields, version or kind")
        if any(not isinstance(spec[k], str) or not spec[k].strip() for k in ("id", "title", "feature", "source")):
            raise ValueError("Web capability: invalid identity or source")
        if not re.fullmatch(r"[a-z][a-z0-9-]*", spec["id"]) or spec["id"] in seen:
            raise ValueError("Web capability: invalid or duplicate identity")
        seen.add(spec["id"])
        if not isinstance(spec["sections"], dict) or set(spec["sections"]) != sections or any(
                not isinstance(v, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", v) for v in spec["sections"].values()):
            raise ValueError("Web capability: invalid section selectors")
        if not isinstance(spec["related"], list) or not all(isinstance(v, str) for v in spec["related"]):
            raise ValueError("Web capability: invalid related definitions")
        feature = model.records.get(spec["feature"])
        if not feature or feature.data["type"] != "feature" or any(v not in model.records for v in spec["related"]):
            raise ValueError("Web capability: missing or invalid engineering basis")
        if spec["source"] != "README.md":
            raise ValueError("Web capability: source must be the owning README.md")
        source = binding.parent / spec["source"]
        if source.is_symlink() or not source.is_file():
            raise ValueError("Web capability: missing or symlinked source")
        content = source.read_bytes()
        document, selected = content.decode(), {}
        for name, anchor in spec["sections"].items():
            start, end = f"<!-- browser-capability: {anchor} -->", f"<!-- /browser-capability: {anchor} -->"
            if document.count(start) != 1 or document.count(end) != 1:
                raise ValueError("Web capability: missing or ambiguous section")
            match = re.search(re.escape(start) + r"(.*?)" + re.escape(end), document, re.S)
            if not match or not match[1].strip():
                raise ValueError("Web capability: empty or invalid section")
            selected[name] = match[1].strip()
        rows = [line.strip().split("|")[1:-1] for line in selected["interactions"].splitlines()]
        if len(rows) < 3 or any(len(row) != 2 or any(not cell.strip() for cell in row) for row in rows):
            raise ValueError("Web capability: invalid interaction table")
        if [v.strip() for v in rows[0]] != ["Reader interaction", "Available behavior and destination"] or any(
                not re.fullmatch(r":?-{3,}:?", v.strip()) for v in rows[1]):
            raise ValueError("Web capability: unsupported interaction table")
        result.append({"id": spec["id"], "kind": "web", "title": spec["title"], "owner": owner.id,
                       "feature": spec["feature"], "related": spec["related"],
                       "route": "#capability/" + spec["id"],
                       "content": {k: v for k, v in selected.items() if k != "interactions"},
                       "interactions": [{"title": a.strip(), "description": b.strip()} for a, b in rows[2:]],
                       "source": source.relative_to(model.root).as_posix(), "selectors": spec["sections"],
                       "source_digest": hashlib.sha256(content).hexdigest(),
                       "binding": binding.relative_to(model.root).as_posix(),
                       "binding_digest": hashlib.sha256(raw).hexdigest()})
    return result


def development_tables(model, marker, label):
    """Project explicitly selected owner tables without creating a second mapping."""
    result = {}
    start, end = f'<!-- {marker} -->', f'<!-- /{marker} -->'
    def fail(message):
        raise ValueError(label + ': ' + message)
    for owner in model.of_type('module'):
        source = model.root / owner.path.parent / 'README.md'
        if source.is_symlink():
            fail('symlinked owning README is unsupported')
        if not source.exists():
            continue
        raw = source.read_bytes()
        document = raw.decode()
        if start not in document and end not in document:
            continue
        if document.count(start) != 1 or document.count(end) != 1:
            fail('missing or ambiguous markers')
        match = re.search(re.escape(start) + r'(.*?)' + re.escape(end), document, re.S)
        if not match:
            fail('reversed markers')
        parts = match[1].strip().split('\n\n', 1)
        lines = parts[0].splitlines()
        rows = [[cell.strip() for cell in line.strip()[1:-1].split('|')] for line in lines]
        if len(rows) < 3 or any(not line.strip().startswith('|') or not line.strip().endswith('|') for line in lines) or any(len(row) != 3 or not all(row) for row in rows):
            fail('expected one nonempty three-column table')
        if any(not re.fullmatch(r':?-{3,}:?', cell) for cell in rows[1]):
            fail('invalid table separator')
        def cell_content(cell):
            segments, offset = [], 0
            for link in re.finditer(r'\[([^\[\]\n]+)\]\(([^\s()]+)\)', cell):
                segments.append({'text': cell[offset:link.start()]})
                target = link[2]
                if re.match(r'^(?:[a-z][a-z\d+.-]*:|/)', target, re.I) or '\\' in target:
                    fail('links must be repository-relative')
                file, separator, fragment = target.partition('#')
                path = posixpath.normpath(posixpath.join(owner.path.parent.as_posix(), file))
                if path == '..' or path.startswith('../'):
                    fail('link leaves repository')
                segments.append({'text': link[1], 'path': path + (separator + fragment if separator else '')})
                offset = link.end()
            segments.append({'text': cell[offset:]})
            return segments
        result[owner.id] = {'headers': rows[0],
                            'rows': [[cell_content(cell) for cell in row] for row in rows[2:]],
                            'explanation': parts[1].strip() if len(parts) > 1 else '',
                            'source': source.relative_to(model.root).as_posix(),
                            'source_digest': hashlib.sha256(raw).hexdigest()}
    return result


def build_model(model):
    """Return lossless source records plus explicitly derived browser indexes."""
    modules = {}
    for record in model.of_type("module"):
        identity = record.id
        descendants = _descendants(model, identity)
        subtree = {identity, *descendants}
        allocations = model.incoming(identity, "allocated_to")
        modules[identity] = {
            "parent": model.parents.get(identity),
            "children": model.children(identity),
            "ancestors": model.ancestors(identity),
            "descendants": descendants,
            "functions": [edge.source for edge in allocations
                          if model.records[edge.source].data["type"] == "function"],
            "allocated_requirements": [edge.source for edge in allocations
                                       if model.records[edge.source].data["type"] == "allocated-requirement"],
            "subtree_functions": [item.id for item in model.of_type("function")
                                  if item.data.get("allocated_to") in subtree],
            "subtree_allocated_requirements": [item.id for item in model.of_type("allocated-requirement")
                                               if item.data.get("allocated_to") in subtree],
            "provides": [edge.target for edge in model.outgoing(identity, "provides")],
            "consumes": [edge.target for edge in model.outgoing(identity, "consumes")],
            "exposed_interfaces": [edge.source for edge in model.incoming(identity, "exposed_through")],
            "collaborations": module_collaborations(model, identity),
        }
    interfaces = {
        record.id: {"provider": _provider(model, record.id),
                    "consumers": [edge.source for edge in model.incoming(record.id, "consumes")],
                    "exposed_through": list(record.data.get("exposed_through", []))}
        for record in model.of_type("interface")
    }
    catalogs = []
    for catalog in model.public_catalogs:
        entries = []
        for index, entry in enumerate(catalog.entries):
            mapping, pointer = catalog.mappings[entry["name"]]
            functions = {item["function"] for item in mapping["functions"]}
            features = {edge.source for identity in functions
                        for edge in model.incoming(identity, "realized_by")}
            owners = {edge.target for identity in functions
                      for edge in model.outgoing(identity, "allocated_to")}
            entries.append({**entry, "mapping": mapping, "mapping_pointer": pointer,
                            "entry_pointer": f"/observed/public_entries/{index}",
                            "features": sorted(features), "modules": sorted(owners)})
        catalogs.append({"owner": catalog.owner.id, "host": model.catalog_host(catalog),
                         "path": catalog.facet.path.as_posix(),
                         "label": catalog.label, "entries": entries})
    designed_catalogs = []
    for owner, facet, capabilities in model.designed_catalogs:
        entries = []
        for capability, pointer in capabilities:
            functions = {item["function"] for item in capability["functions"]}
            entries.append({**capability, "entry_pointer": pointer,
                            "mapping": {"functions": capability["functions"], "limits": capability["limits"]},
                            "features": sorted({edge.source for identity in functions
                                                for edge in model.incoming(identity, "realized_by")}),
                            "modules": sorted({edge.target for identity in functions
                                               for edge in model.outgoing(identity, "allocated_to")})})
        host = owner.id if owner.data["type"] == "module" else model.incoming(owner.id, "provides")[0].source
        designed_catalogs.append({"owner": owner.id, "host": host, "path": facet.path.as_posix(),
                                  "entries": entries})
    contributions = [
        {"requirement": sr.id, "path": sr.path.as_posix(),
         "source_pointer": f"/sources/{index}", "criterion": criterion,
         "criterion_text": sr.data["acceptance_criteria"][criterion - 1],
         "allocated_requirements": allocated, "locator": locator, "basis": basis}
        for sr, index, criterion, allocated, locator, basis in model.contributions
    ]
    return {
        "format_version": 1,
        "source_digest": model.digest,
        "records": {identity: {"path": record.path.as_posix(), "data": record.data}
                    for identity, record in sorted(model.records.items())},
        "parents": dict(sorted(model.parents.items())),
        "roots": sorted(identity for identity in modules if identity not in model.parents),
        "relationships": [_edge(edge) for edge in sorted(
            model.edges, key=lambda edge: (edge.source, edge.relation, edge.target, str(edge.path), edge.field))],
        "facets": [{"owner": identity, "facet": name, "path": record.path.as_posix(),
                    "data": record.data} for (identity, name), record in sorted(model.facets.items())],
        "modules": modules,
        "interfaces": interfaces,
        "catalogs": catalogs,
        "designed_catalogs": designed_catalogs,
        "development_implementations": development_tables(model, "development-implementation", "Development implementation"),
        "development_build_resources": development_tables(model, "development-build-resources", "Development build resources"),
        "cli_contributions": contributions,
        "cli_cooperation": cli_cooperation(model),
        "overview_collaborations": overview_collaborations(model),
        "views": model.architecture_views(),
        "view_diagrams": _additional_diagrams(model)[1],
    }


def _quoted(value):
    """D2 double-quoted strings use JSON-compatible escapes for source text."""
    return json.dumps(str(value), ensure_ascii=False)


def _key(identity):
    # Hex avoids collisions between punctuation variants and reserved D2 words.
    return "m_" + identity.encode("utf-8").hex()


def _label(title, width=28):
    return "\n".join(textwrap.wrap(
        title, width, break_long_words=False, break_on_hyphens=False))


def _node(model, identity, indent="", context=False, children=None, grid_columns=None, width=None):
    record = model.records[identity]
    lines = [f"{indent}{_key(identity)}: {_quoted(_label(record.data['title']))} {{",
             f"{indent}  link: {_quoted('#module/' + identity)}",
             f"{indent}  tooltip: {_quoted(record.data['title'] + ' (' + identity + ')')}",
             f"{indent}  style.fill: {_quoted('#F6F8FB' if context else '#ECF3FF')}",
             f"{indent}  style.stroke: {_quoted('#8292A9' if context else '#426898')}",
             f"{indent}  style.font-color: {_quoted('#23334A')}",
             f"{indent}  style.font-size: 18",
             f"{indent}  style.border-radius: 8"]
    if context:
        lines.append(f"{indent}  style.stroke-dash: 3")
    if grid_columns is not None:
        lines.append(f"{indent}  grid-columns: {grid_columns}")
    if width is not None:
        lines.append(f"{indent}  width: {width}")
    for child in children or []:
        lines.extend(_node(model, child, indent + "  "))
    lines.append(indent + "}")
    return lines


def _interface_names(model, collaborations):
    """Shorten exact current titles only, without concealing distinct contracts."""
    titles = {identity: model.records[identity].data["title"]
              for identity in sorted({item["interface"] for item in collaborations})}
    substitutions = {
        "Applicable engineering authoring guidance": "Engineering authoring guidance",
        "Applicable governed-action authority": "Governed-action authority",
    }
    names = {identity: substitutions.get(title, title) for identity, title in titles.items()}

    def collisions():
        groups = {}
        for identity, name in names.items():
            groups.setdefault(" ".join(name.split()), []).append(identity)
        return [identities for identities in groups.values() if len(identities) > 1]

    while True:
        shortened = [identity for group in collisions() for identity in group
                     if names[identity] != titles[identity]]
        if not shortened:
            break
        for identity in shortened:
            names[identity] = titles[identity]
    # Identical canonical names remain distinct through a secondary identity.
    # Repeat only if a literal title itself matches a suffixed presentation name.
    while collisions():
        for group in collisions():
            for identity in group:
                names[identity] += f" ({identity})"
    return names


def _connection(model, collaboration, node_paths, names):
    interface = model.records[collaboration["interface"]]
    source = node_paths[collaboration["consumer_boundary"]]
    target = node_paths[collaboration["provider_boundary"]]
    # Keep the contract name visible. Narrow wrapping prevents parallel incoming
    # contracts from obscuring each other or nearby Module labels.
    label = _label(names[interface.id], 18)
    lines = [f"{source} -> {target}: {_quoted(label)} {{",
             f"  link: {_quoted('#interface/' + interface.id)}",
             f"  tooltip: {_quoted(interface.data['title'] + ' (' + interface.id + ')')}"]
    return lines + ['  style.stroke: "#667A96"',
                    '  style.font-color: "#34445B"',
                    '  style.fill: "#FFFFFF"',
                    "  style.font-size: 14", "}"]


def _header(model):
    return ["# Generated from canonical REM records; do not edit.",
            f"# Source identity: {model.digest}",
            "# Arrows show consumer -> provider; they do not show execution order.",
            "vars: {", "  d2-config: {", "    layout-engine: elk", "  }", "}",
            "direction: down", ""]


def _display_boundary(model, selected, identity):
    """Select one visible level without changing the exact relation owner."""
    chain = [identity, *model.ancestors(identity)]
    if selected in chain:
        position = chain.index(selected)
        return selected if position == 0 else chain[position - 1]
    selected_chain = [selected, *model.ancestors(selected)]
    shared = next((item for item in selected_chain if item in chain), None)
    if shared is not None:
        position = chain.index(shared)
        return shared if position == 0 else chain[position - 1]
    return chain[-1]


def module_collaborations(model, selected):
    """Relevant declared collaborations at a Module's immediate visual level."""
    subtree = {selected, *_descendants(model, selected)}
    result = []
    for interface in model.of_type("interface"):
        provider = _provider(model, interface.id)
        for edge in model.incoming(interface.id, "consumes"):
            if provider not in subtree and edge.source not in subtree:
                continue
            provider_boundary = _display_boundary(model, selected, provider)
            consumer_boundary = _display_boundary(model, selected, edge.source)
            if provider_boundary == consumer_boundary:
                continue
            if not _visible_provider(interface, provider, provider_boundary):
                continue
            result.append({"interface": interface.id, "consumer": edge.source,
                           "provider": provider, "consumer_boundary": consumer_boundary,
                           "provider_boundary": provider_boundary})
    return result


def _draw_connections(model, collaborations, node_paths):
    lines, seen = [], set()
    names = _interface_names(model, collaborations)
    for item in collaborations:
        key = (item["interface"], item["consumer_boundary"], item["provider_boundary"])
        # Exact consumers remain separate in model data; collapsed visual repeats do not.
        if key not in seen:
            lines.extend(_connection(model, item, node_paths, names))
            seen.add(key)
    return lines


def diagram_sources(model):
    """Produce Logical diagrams and the source-backed 4+1 projections."""
    roots = sorted(record.id for record in model.of_type("module")
                   if record.id not in model.parents)
    lines = _header(model)
    for identity in roots:
        lines.extend(_node(model, identity))
    lines.extend(_draw_connections(model, overview_collaborations(model),
                                   {identity: _key(identity) for identity in roots}))
    result = {"overview": "\n".join(lines) + "\n"}
    for record in model.of_type("module"):
        identity = record.id
        children = model.children(identity)
        visible = {identity, *children}
        collaborations = module_collaborations(model, identity)
        neighbors = sorted({item[field] for item in collaborations
                            for field in ("consumer_boundary", "provider_boundary")} - visible)
        lines = _header(model)
        # A sparse child set needs a compact inventory layout. Grid routing is
        # unsuitable for internal collaborations, so those retain ELK's layout.
        internal = any(item["consumer_boundary"] in visible and item["provider_boundary"] in visible
                       for item in collaborations)
        columns = 2 if len(children) > 3 and not internal else None
        visual_edges = {(item["interface"], item["consumer_boundary"], item["provider_boundary"])
                        for item in collaborations}
        # ELK can crowd several named contracts onto a narrow leaf's ports.
        # Reserve space on that selected node; context nodes retain natural size.
        width = 420 if not children and len(visual_edges) > 1 else None
        lines.extend(_node(model, identity, children=children, grid_columns=columns, width=width))
        for neighbor in neighbors:
            lines.extend(_node(model, neighbor, context=True))
        paths = {item: _key(item) for item in [identity, *neighbors]}
        paths.update({child: _key(identity) + "." + _key(child) for child in children})
        lines.extend(_draw_connections(model, collaborations, paths))
        result["module-" + identity] = "\n".join(lines) + "\n"
    result.update(_additional_diagrams(model)[0])
    return result


def _projection_header(model, description):
    return ["# Generated from canonical REM records; do not edit.",
            f"# Source identity: {model.digest}", "# " + description,
            "vars: {d2-config: {layout-engine: elk}}", "direction: down"]


def _box(key, title, link, tooltip=None, *, children=None, columns=None,
         fill="#ECF3FF", dashed=False, path=False):
    label = "\n".join(_label(line, 38 if path else 28)
                      for line in title.split("\n"))
    if path:
        # Prefer directory boundaries; never split a file name or template.
        label = "\n".join(_label(line.replace("/", "/ "), 38).replace("/ ", "/")
                          for line in title.split("\n"))
    lines = [f"{key}: {_quoted(label)} {{", f"  link: {_quoted(link)}",
             f"  tooltip: {_quoted(tooltip or title)}", f"  style.fill: {_quoted(fill)}",
             '  style.stroke: "#7C8FA9"', '  style.font-color: "#23334A"',
             f"  style.font-size: {14 if path else 17}", "  style.border-radius: 6"]
    if dashed:
        lines.append("  style.stroke-dash: 3")
    if columns:
        lines.append(f"  grid-columns: {columns}")
    lines.extend("  " + line for line in children or [])
    return lines + ["}"]


def _relation(source, target, label, *, dashed=False):
    lines = [f"{source} -> {target}: {_quoted(label)} {{",
             '  style.stroke: "#667A96"', '  style.fill: "#FFFFFF"',
             "  style.font-size: 13"]
    if dashed:
        lines.append("  style.stroke-dash: 3")
    return lines + ["}"]


def _facet_source(model, owner, facet, field):
    return {"owner": owner, "facet": facet,
            "path": model.facets[owner, facet].path.as_posix(), "field": field}


def _development_diagrams(model):
    """Show static implementation mappings and typed production inputs/outputs."""
    mappings = {}
    for ref in model.architecture_views()["development"]["facet_refs"]:
        owner, facet = ref["owner"], ref["facet"]
        observed = model.facets[owner, facet].data.get("observed", {})
        for field in ("software_units", "bindings", "production_paths"):
            if observed.get(field):
                mappings.setdefault(owner, []).append((facet, field, observed[field]))
        if facet == "software" and observed.get("public_entries"):
            mappings.setdefault(owner, []).append((facet, "public_entries", observed["public_entries"]))
    sources, descriptors = {}, {}
    caption = ("Static mappings from accountable Modules and contracts to implementation sources. "
               "Production arrows mean declared inputs and candidate outputs, not software dependencies "
               "or evidence that a build ran. Open an owner to inspect its complete mapping.")
    legend = [{"label": "Source mapping", "description": "Authored software units or Interface implementation bindings."},
              {"label": "Production mapping", "description": "Recorded input → transformation → candidate output layout."}]
    overview = _projection_header(model, caption)
    overview_groups, all_sources = [], []
    for owner, groups in sorted(mappings.items()):
        title = model.records[owner].data["title"]
        route = "#development/" + owner
        own_sources = [_facet_source(model, owner, facet, "/observed/" + field)
                       for facet, field, _ in groups]
        all_sources.extend(own_sources)
        focus = _projection_header(model, caption)
        focus.extend(_box("owner", title, route, title + " (" + owner + ")"))
        compact = []
        for group_index, (facet, field, items) in enumerate(groups):
            group_key = "g" + str(group_index)
            if field == "production_paths":
                for index, production in enumerate(items):
                    key = group_key + "p" + str(index)
                    members = []
                    for kind in ("inputs", "outputs"):
                        files = []
                        for file_index, item in enumerate(production[kind]):
                            files.extend(_box("f" + str(file_index), item["path"], route,
                                              item["role"], path=True,
                                              fill="#F3F6FA" if kind == "inputs" else "#FFF5DB"))
                        members.extend(_box(kind, "Source inputs" if kind == "inputs" else "Candidate output layouts",
                                            route, children=files, columns=1, fill="#FFFFFF"))
                    transformation = production["transformation"]
                    members.extend(_box("transform", transformation["path"], route,
                                        transformation["description"], path=True, fill="#E9F4EE"))
                    members.extend(_relation("inputs", "transform", "inputs"))
                    members.extend(_relation("transform", "outputs", "candidate outputs"))
                    focus.extend(_box(key, production["name"], route, children=members, fill="#F8FAFD"))
                    focus.extend(_relation("owner", key, "production responsibility"))
                    compact.extend(_box(key, production["name"], route, fill="#E9F4EE"))
            else:
                group_title = {"software_units": "Implementation sources",
                               "bindings": "Contract implementation bindings",
                               "public_entries": "Published procedure sources"}[field]
                members = []
                for index, item in enumerate(items):
                    label = item["name"] + "\n" + item["source_path"] if field == "public_entries" else item["path"]
                    members.extend(_box("f" + str(index), label, route,
                                        item["purpose"] if field == "public_entries" else item["role"],
                                        path=True, fill="#FFFFFF"))
                focus.extend(_box(group_key, group_title, route, children=members,
                                  columns=2 if len(items) > 4 else 1, fill="#F8FAFD"))
                focus.extend(_relation("owner", group_key, "source mapping"))
                compact.extend(_box(group_key, f"{group_title}\n{len(items)} recorded paths", route,
                                    "\n".join(item["source_path"] if field == "public_entries" else item["path"]
                                              for item in items), fill="#F8FAFD"))
        key = "development-" + owner
        sources[key] = "\n".join(focus) + "\n"
        descriptors[key] = {"key": key, "view": "development", "owner": owner,
                            "title": title + " — implementation mapping", "caption": caption,
                            "legend": legend, "sources": own_sources}
        overview_groups.extend(_box(_key(owner), title, route, title + " (" + owner + ")",
                                    children=compact, columns=1, fill="#ECF3FF"))
    if overview_groups:
        overview.extend(_box("mappings", "Recorded implementation mappings", "#development",
                             children=overview_groups, columns=2, fill="#FFFFFF"))
    else:
        overview.extend(_box("missing", "No typed implementation mappings recorded", "#development"))
    sources["development"] = "\n".join(overview) + "\n"
    descriptors["development"] = {"key": "development", "view": "development",
                                   "title": "Implementation and production map", "caption": caption,
                                   "legend": legend, "sources": all_sources}
    return sources, descriptors


def _scenario_diagrams(model):
    """Summarize exact Scenario slices without inventing an execution sequence."""
    from lib.rem_architecture_scenario_diagrams import outcome_diagram
    slices = model.architecture_views()["scenarios"]["scenarios"]
    sources, descriptors, cards, all_sources = {}, {}, [], []
    caption = ("Traceability, not execution order. Requirement and behavior sets are collapsed by "
               "their exact accountable Module; arrows summarize the selected authored relationships. "
               "Dashed Modules provide contract context without receiving behavior allocations. "
               "The traceability details and source links below retain the selected entities and their authored basis.")
    legend = [{"label": "Confirms / derives", "description": "Selected system obligations confirm Functions or parent allocated requirements."},
              {"label": "Allocated to", "description": "Every member of the displayed set allocates to this exact Module."},
              {"label": "Provides / consumes", "description": "Exact contract ownership and declared consumption; no call sequence is implied."}]
    for item in slices:
        scenario = item["scenario"]
        route = "#scenario/" + scenario
        title = model.records[scenario].data["title"]
        lines = _projection_header(model, caption)
        lines.extend(_box("scenario", title, route, title + " (" + scenario + ")", fill="#E9F4EE"))
        requirements = item["requirements"]
        lines.extend(_box("requirements", f"System obligations\n{len(requirements)} selected requirements", route,
                          "\n".join(model.records[identity].data["title"] + " (" + identity + ")"
                                    for identity in requirements), fill="#FFF5DB"))
        lines.extend(_relation("scenario", "requirements", "informs"))
        groups = []
        for owner in item["modules"]:
            for field, kind, relation in (("functions", "Functions", "confirms"),
                                           ("allocated_requirements", "allocated requirements", "derives")):
                members = [identity for identity in item[field]
                           if model.records[identity].data.get("allocated_to") == owner]
                if not members:
                    continue
                key = _key(owner + field)
                display_kind = kind[:-1] if len(members) == 1 else kind
                lines.extend(_box(key, f"{len(members)} {display_kind}", route,
                                  "\n".join(model.records[identity].data["title"] + " (" + identity + ")"
                                            for identity in members), fill="#FFF5DB" if field == "allocated_requirements" else "#ECF3FF"))
                lines.extend(_relation("requirements", key, relation))
                lines.extend(_relation(key, _key(owner), "allocated to"))
                groups.append({"kind": field, "module": owner, "members": members})
        for owner in [*item["modules"], *item["context_modules"]]:
            name = model.records[owner].data["title"]
            context = owner in item["context_modules"]
            lines.extend(_box(_key(owner), name, "#module/" + owner, name + " (" + owner + ")",
                              dashed=context, fill="#F3F6FA" if context else "#ECF3FF"))
        interface_names = _interface_names(model, [{"interface": identity} for identity in item["interfaces"]])
        for identity in item["interfaces"]:
            lines.extend(_box(_key(identity), interface_names[identity], "#interface/" + identity,
                              model.records[identity].data["title"] + " (" + identity + ")", fill="#E9F4EE"))
        contracts = [edge for edge in item["relationships"] if edge["relation"] in ("provides", "consumes")]
        contracts += [context["relationship"] for context in item["contract_context"]]
        seen = set()
        for edge in contracts:
            key = edge["source"], edge["relation"], edge["target"]
            if key not in seen:
                lines.extend(_relation(_key(edge["source"]), _key(edge["target"]), edge["relation"]))
                seen.add(key)
        own_sources = [{"owner": scenario, "facet": "scenario", "path": model.records[scenario].path.as_posix(),
                        "field": "/informs"}]
        # A provenance entry for every selected trace record includes its exact
        # field. The UI may collapse this list, but the projection loses no basis.
        for edge in [*item["relationships"], *contracts]:
            source = {"owner": edge["source"], "facet": "record", "path": edge["path"], "field": edge["field"]}
            if source not in own_sources:
                own_sources.append(source)
        key = "scenario-" + scenario
        sources[key] = "\n".join(lines) + "\n"
        descriptors[key] = {"key": key, "view": "scenarios", "scenario": scenario,
                            "title": title + " — architecture trace", "caption": caption,
                            "legend": legend, "sources": own_sources, "groups": groups}
        outcome_projection = outcome_diagram(model, item)
        if outcome_projection is not None:
            sources[key], descriptors[key] = outcome_projection
            # Broader traceability is retained for source inspection; it is not
            # the narrower accountability selection drawn for each outcome.
            descriptors[key]["groups"] = groups
        all_sources.append(own_sources[0])
        participants = []
        for owner in item["modules"]:
            name = model.records[owner].data["title"]
            participants.extend(_box(_key(owner), name, "#module/" + owner,
                                     name + " (" + owner + ")", fill="#ECF3FF"))
        cards.extend(_box(_key(scenario), title, route, title + " (" + scenario + ")",
                          children=participants, columns=1, fill="#E9F4EE"))
    overview_caption = ("Each walkthrough groups only the Modules reached through its selected behavioral "
                        "allocations. Boxes are Scenario scope, not architectural containment or execution order. "
                        "Open a walkthrough for requirement allocation and selected contract-provider context.")
    overview = _projection_header(model, overview_caption)
    overview.extend(_box("walkthroughs", "Selected Scenario responsibilities", "#scenarios",
                         children=cards, columns=2, fill="#FFFFFF"))
    sources["scenarios"] = "\n".join(overview) + "\n"
    descriptors["scenarios"] = {"key": "scenarios", "view": "scenarios", "title": "Scenario participation map",
                                 "caption": overview_caption, "legend": [], "sources": all_sources}
    return sources, descriptors


def _additional_diagrams(model):
    from lib.rem_architecture_realization_diagrams import realization_diagrams
    from lib.rem_architecture_test_diagrams import test_diagrams

    sources, descriptors = {}, {}
    for projection in (_development_diagrams, _scenario_diagrams, realization_diagrams, test_diagrams):
        diagrams, metadata = projection(model)
        if sources.keys() & diagrams.keys() or descriptors.keys() & metadata.keys():
            raise ValueError("Duplicate architecture projection key")
        sources.update(diagrams)
        descriptors.update(metadata)
    return sources, descriptors
