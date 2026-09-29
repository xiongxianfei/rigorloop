"""Project explicitly recorded execution and placement facts into D2 diagrams.

The graph has no runtime inference from software paths, dependencies, or prose.
Execution edges come only from typed calls or explicitly ordered interactions;
lifecycle edges come from typed transitions. Physical relationships come only
from typed bindings; a placement inventory alone creates no edges.
"""

import json
import textwrap


def _quote(value):
    return json.dumps(str(value), ensure_ascii=False)


def _wrap(value, width=30, break_words=False):
    return "\n".join(textwrap.wrap(str(value), width, break_long_words=break_words,
                                   break_on_hyphens=False))


def _key(value):
    return "n_" + str(value).encode("utf-8").hex()


def _path_label(value, width=38):
    """Wrap at directory separators while keeping filenames and templates intact."""
    lines, current = [], ""
    parts = value.split("/")
    for index, part in enumerate(parts):
        component = part + ("/" if index < len(parts) - 1 else "")
        if current and len(current + component) > width:
            lines.append(current)
            current = ""
        current += component
    if current:
        lines.append(current)
    return "\n".join(lines)


def _title(model, identity):
    return model.records[identity].data["title"]


def _header(model, meaning, columns=None):
    lines = ["# Generated from explicit REM realization facts; do not edit.",
             f"# Source identity: {model.digest}", f"# {meaning}",
             "vars: { d2-config: { layout-engine: elk } }", "direction: down"]
    if columns:
        lines.append(f"grid-columns: {columns}")
    return lines + [""]


def _node(key, label, route, tooltip, indent="", fill="#ECF3FF", dashed=False):
    lines = [f"{indent}{key}: {_quote(label)} {{",
             f"{indent}  link: {_quote(route)}",
             f"{indent}  tooltip: {_quote(tooltip)}",
             f"{indent}  style.fill: {_quote(fill)}",
             f'{indent}  style.stroke: "#597390"',
             f'{indent}  style.font-color: "#24364A"',
             f"{indent}  style.font-size: 16",
             f"{indent}  style.border-radius: 7"]
    if dashed:
        lines.append(f"{indent}  style.stroke-dash: 3")
    return lines + [indent + "}"]


def _source(owner, facet, record, field, description=None):
    source = {"owner": owner, "facet": facet, "path": record.path.as_posix(),
              "field": field}
    if description:
        source["description"] = description
    return source


def _execution_records(model):
    return [(owner, record, record.data["observed"]["execution"])
            for (owner, facet), record in sorted(model.facets.items())
            if facet == "runtime" and "execution" in record.data.get("observed", {})]


def _process(model, owner=None):
    records = [(identity, record, execution)
               for identity, record, execution in _execution_records(model)
               if owner is None or owner == identity or owner in execution["modules"]]
    if not records:
        return None
    lines = _header(model, "Edges are recorded conditional calls, not invocation sequence.")
    sources, provider_notes = [], []
    for index, (identity, record, execution) in enumerate(records):
        group = _key(f"execution:{index}:{identity}")
        label = f"{execution['name']}\n{execution['environment']}"
        lines += [f"{group}: {_quote(label)} {{",
                  f"  link: {_quote('#process/' + identity)}",
                  f"  tooltip: {_quote('; '.join(execution['constraints']))}",
                  '  style.fill: "#F6F9FF"', '  style.stroke: "#93A9C6"',
                  "  style.font-size: 18", "  style.border-radius: 9"]
        for module in execution["modules"]:
            lines += _node(_key(module), _wrap(_title(model, module)), "#module/" + module,
                           f"{_title(model, module)} ({module})", "  ")
        for interface in execution["entry_interfaces"]:
            label = "Entry contract\n" + _wrap(_title(model, interface))
            lines += _node(_key(interface), label, "#interface/" + interface,
                           f"{_title(model, interface)} ({interface}); entry contract declared for this execution context",
                           "  ", "#F0F7F4", True)
        for call in execution["calls"]:
            interface = call["interface"]
            lines += [f"  {_key(call['caller'])} -> {_key(call['callee'])}: {_quote(_wrap(_title(model, interface), 16))} {{",
                      f"    link: {_quote('#interface/' + interface)}",
                      f"    tooltip: {_quote(_title(model, interface) + ' (' + interface + '); conditional call')}",
                      '    style.stroke: "#526C8A"', '    style.font-color: "#344D67"',
                      '    style.fill: "#FFFFFF"', "    style.font-size: 14", "  }"]
            providers = model.incoming(interface, "provides")
            if providers and providers[0].source != call["callee"]:
                provider_notes.append(f"{_title(model, interface)} remains provided by {_title(model, providers[0].source)}; its arrow targets {_title(model, call['callee'])} as the recorded behavioral implementation.")
        lines.append("}")
        sources.append(_source(identity, "runtime", record, "/observed/execution",
                               " ".join(execution["constraints"])))
    key = "process" + ("-" + owner if owner else "")
    caption = "Arrows are recorded conditional in-process calls, not a sequence or evidence that every path runs. Entry contracts are shown without an invented caller or dispatch edge."
    if provider_notes:
        caption += " " + " ".join(dict.fromkeys(provider_notes))
    descriptor = {"key": key, "view": "process", "title": "Execution context" if owner else "Runtime execution and conditional calls",
                  "caption": caption,
                  "legend": [{"label": "Container", "description": "Observed execution environment; co-location preserves logical responsibilities."},
                             {"label": "Arrow", "description": "Explicitly recorded conditional call, labeled with its Interface."},
                             {"label": "Dashed contract", "description": "Declared entry Interface; no additional execution edge is asserted."}],
                  "sources": sources}
    if owner:
        descriptor["owner"] = owner
    return key, "\n".join(lines) + "\n", descriptor


def _placement_records(model):
    result = []
    for (owner, facet), record in sorted(model.facets.items()):
        if facet not in {"deployment", "persistence"}:
            continue
        for index, placement in enumerate(record.data.get("observed", {}).get("placements", [])):
            result.append((owner, facet, record, index, placement))
    return result


def _physical(model, owner=None):
    records = [(identity, facet, record, index, placement)
               for identity, facet, record, index, placement in _placement_records(model)
               if owner is None or owner == identity or owner in placement["modules"]]
    if not records:
        return None
    locations = sorted({item[4]["location"] for item in records})
    lines = _header(model, "Containment records named placement; there are no transfer or execution edges.",
                    2 if len(locations) > 1 else 1)
    sources = []
    for location in locations:
        lines += [f"{_key(location)}: {_quote(_wrap(location))} {{",
                  "  grid-columns: 1", '  style.fill: "#F5F8FC"',
                  '  style.stroke: "#91A3BA"', "  style.font-size: 18",
                  "  style.border-radius: 9"]
        for identity, facet, record, index, placement in records:
            if placement["location"] != location:
                continue
            label = _wrap(placement["name"], 32) + "\n\n" + "\n".join(_path_label(path) for path in placement["paths"])
            responsibilities = ", ".join(_title(model, module) for module in placement["modules"])
            tooltip = f"{placement['name']}; responsibilities: {responsibilities}; paths: " + "; ".join(placement["paths"])
            lines += _node(_key(f"{identity}:{facet}:{index}"), label, "#physical/" + identity,
                           tooltip, "  ", "#EEF6F1")
            sources.append(_source(identity, facet, record, f"/observed/placements/{index}",
                                   " ".join(placement["constraints"])))
        lines.append("}")
    key = "physical" + ("-" + owner if owner else "")
    descriptor = {"key": key, "view": "physical", "title": "Recorded placement context" if owner else "Package, candidate, and project locations",
                  "caption": "Groups show declared locations and their recorded path templates. There are no transfer, deployment-sequence, or ownership edges. Selecting a placement opens its owning physical record; output templates do not link to purported built or installed files.",
                  "legend": [{"label": "Outer group", "description": "Named package, candidate, or project location from a recorded placement."},
                             {"label": "Inner block", "description": "Named content and its relative paths or templates; presence and qualification are not established."}],
                  "sources": sources}
    if owner:
        descriptor["owner"] = owner
    return key, "\n".join(lines) + "\n", descriptor


def _flow_arrow(source, target, label=None, tooltip=None, dashed=False, label_width=24):
    """Draw one authored ordering, terminal alternative, or state transition."""
    lines = [f"{source} -> {target}" + (f": {_quote(_wrap(label, label_width))}" if label else "") + " {",
             '  style.stroke: "#526C8A"', '  style.font-color: "#344D67"',
             '  style.fill: "#FFFFFF"', "  style.font-size: 14"]
    if tooltip:
        lines.append(f"  tooltip: {_quote(tooltip)}")
    if dashed:
        lines.append("  style.stroke-dash: 3")
    return lines + ["}"]


def _step_node(model, key, step, route):
    participant = step["participant"]
    title = _title(model, participant)
    label = _wrap(step["name"], 34) + "\n\n" + _wrap(title, 34)
    tooltip = f"{step['name']}; {title} ({participant}); {step['action']}"
    return _node(key, label, route, tooltip,
                 fill="#ECF3FF" if participant == "MOD-010" else "#EEF6F1")


def _interactions(model):
    """Project the two selected, source-observed record Interface operations.

    Sequence branches are terminal alternatives by contract. Failure records do
    not name a step, so they never acquire an invented arrow or execution point.
    """
    record = model.facets.get(("IF-003", "interaction"))
    if record is None:
        return []
    selections = {
        "publish_record_candidate": ("publication", "Publication"),
        "recover_record_transaction": ("recovery", "Recovery"),
    }
    results = []
    for index, sequence in enumerate(record.data.get("observed", {}).get("sequences", [])):
        selected = selections.get(sequence["operation"])
        if selected is None:
            continue
        slug, navigation_label = selected
        key, route = "process-" + slug, "#process/interaction/" + slug
        caption = ("Source-observed control flow for the selected record operation. Solid arrows follow the recorded "
                   "main-step order; dashed paths are conditional terminal alternatives and never rejoin. "
                   "Failures are listed separately because their records do not identify a single triggering step. "
                   "Scroll vertically to follow the remaining stages and terminal alternatives. "
                   "This source projection is not an executed transaction or durability result.")
        lines = _header(model, caption)
        previous = None
        for step_index, step in enumerate(sequence["steps"]):
            current = _key(f"main:{step_index}")
            lines += _step_node(model, current, step, route)
            if previous:
                lines += _flow_arrow(previous, current)
            previous = current
            for branch_index, branch in enumerate(step.get("branches", [])):
                branch_key = f"branch:{step_index}:{branch_index}"
                condition_key = _key(branch_key + ":condition")
                lines += _node(condition_key, _wrap(branch["condition"], 34), route,
                               branch["condition"], fill="#FFF5DB", dashed=True)
                lines += _flow_arrow(current, condition_key, "terminal alternative", dashed=True)
                branch_previous = condition_key
                for action_index, action in enumerate(branch["steps"]):
                    action_key = _key(branch_key + ":step:" + str(action_index))
                    lines += _step_node(model, action_key, action, route)
                    lines += _flow_arrow(branch_previous, action_key, dashed=True)
                    branch_previous = action_key
                outcome_key = _key(branch_key + ":outcome")
                lines += _node(outcome_key, "Alternative outcome\n" + _wrap(branch["outcome"], 38),
                               route, branch["outcome"], fill="#FFF5DB", dashed=True)
                lines += _flow_arrow(branch_previous, outcome_key, dashed=True)
        lines += _node("outcome", "Main-path outcome\n" + _wrap(sequence["outcome"], 38),
                       route, sequence["outcome"], fill="#E5F1E9")
        if previous:
            lines += _flow_arrow(previous, "outcome")
        failure_text = "\n\n".join(f"{item['condition']}\n{item['outcome']}\n" + "; ".join(item["effects"])
                                     for item in sequence["failures"])
        lines += _node("failures", f"{len(sequence['failures'])} guarded failure cases\nSee the recorded conditions and effects below",
                       route, failure_text, fill="#F9EEEE", dashed=True)
        description = " ".join(sequence["preconditions"] + sequence["constraints"])
        descriptor = {
            "key": key, "view": "process", "interaction": sequence["operation"], "owner": "IF-003",
            "route": route, "navigation_label": navigation_label,
            "initial_view": "readable",
            "title": sequence["name"],
            "summary": "Ordered source observations, terminal alternatives, and guarded failure outcomes.",
            "caption": caption,
            "legend": [
                {"label": "Solid arrow", "description": "The recorded main path continues to the next step."},
                {"label": "Dashed path", "description": "A conditional alternative terminates in its own outcome; it never rejoins the main path."},
                {"label": "Step responsibility", "description": "Each step names its accountable Module; this does not imply a separate process for that Module."},
                {"label": "Failure cases", "description": "Recorded rejection, interruption, or safe-stop outcomes; no triggering step is invented."},
            ],
            "sources": [_source("IF-003", "interaction", record, f"/observed/sequences/{index}", description)],
        }
        results.append((key, "\n".join(lines) + "\n", descriptor))
    return results


def _coordination(model):
    """Render only the journal states and guarded transitions actually recorded."""
    record = model.facets.get(("MOD-011", "runtime"))
    if record is None or not record.data.get("observed", {}).get("lifecycles"):
        return None
    route, key = "#process/lifecycle/coordination", "process-coordination"
    caption = ("Source-observed journal states and guarded transitions. Arrows describe eligible changes, "
               "not a mandatory sequence. Absence of a retained journal is distinct from the prepared and "
               "committed journal phases. Guards, effects, and coordination limits remain attached to their "
               "source records; this diagram is not crash, concurrency, or recovery verification.")
    lines, sources = _header(model, caption), []
    lifecycles = record.data["observed"]["lifecycles"]
    for index, lifecycle in enumerate(lifecycles):
        group = _key("lifecycle:" + str(index))
        lines += [f"{group}: {_quote(_wrap(lifecycle['name'], 38))} {{",
                  f"  link: {_quote(route)}", '  style.fill: "#F6F9FF"',
                  '  style.stroke: "#93A9C6"', "  style.font-size: 18"]
        for state in lifecycle["states"]:
            lines += _node(_key(state["name"]), _wrap(state["name"], 28), route,
                           state["meaning"], "  ", "#EEF6F1")
        for transition in lifecycle["transitions"]:
            tooltip = (transition["trigger"] + "\nGuards: " + "; ".join(transition["guards"])
                       + "\nEffects: " + "; ".join(transition["effects"]))
            lines += ["  " + line for line in _flow_arrow(
                _key(transition["from"]), _key(transition["to"]), transition["trigger"], tooltip)]
        lines.append("}")
        sources.append(_source("MOD-011", "runtime", record, f"/observed/lifecycles/{index}",
                               " ".join(lifecycle["constraints"])))
    descriptor = {
        "key": key, "view": "process", "lifecycle": "coordination", "owner": "MOD-011",
        "route": route, "navigation_label": "Coordination and lifecycle",
        "title": lifecycles[0]["name"] if len(lifecycles) == 1 else "Record coordination lifecycles",
        "summary": "Journal states, guarded transitions, and transaction exclusion limits.",
        "caption": caption,
        "legend": [
            {"label": "State", "description": "A recorded journal state; no extra phase is inferred from malformed or foreign bytes."},
            {"label": "Arrow", "description": "An authored transition trigger, qualified by its retained guards and effects."},
        ],
        "sources": sources,
    }
    return key, "\n".join(lines) + "\n", descriptor


class _PhysicalProjection:
    """Render scoped physical facts and collect their exact canonical basis."""

    def __init__(self, model, key, title, caption, route, direction="down"):
        self.model, self.key, self.route = model, key, route
        self.lines = ["direction: " + direction if line == "direction: down" else line
                      for line in _header(model, caption)]
        self.sources, self.owners, self.nodes = {}, set(), set()
        self.relationship_kinds = set()
        self.title, self.caption = title, caption
        self.expand_execution, self.participants = True, None

    def source(self, owner, facet, record, field, constraints=()):
        self.sources[owner, facet, field] = _source(
            owner, facet, record, field, " ".join(constraints) or None)
        self.owners.add(owner)

    def placement(self, reference):
        from lib.rem_architecture_physical import resolve_placement

        record, index, placement = resolve_placement(self.model, reference, self.key)
        owner, facet = reference["owner"], reference["facet"]
        key = _key(f"placement:{owner}:{facet}:{reference['name']}")
        self.source(owner, facet, record, f"/observed/placements/{index}", placement["constraints"])
        self.owners.update(placement["modules"])
        if key not in self.nodes:
            label = _wrap(placement["name"], 24) + "\n\n" + _wrap(placement["location"], 24)
            tooltip = (placement["name"] + "; location: " + placement["location"]
                       + "; relative paths: " + "; ".join(placement["paths"]))
            self.lines += _node(key, label, "#physical/" + owner, tooltip, fill="#EEF6F1")
            self.nodes.add(key)
        return key

    def execution(self, reference):
        from lib.rem_architecture_physical import resolve_execution

        record, execution = resolve_execution(self.model, reference, self.key)
        owner = reference["owner"]
        key = _key(f"execution:{owner}:{reference['name']}")
        self.source(owner, "runtime", record, "/observed/execution", execution["constraints"])
        self.owners.update(execution["modules"])
        if key not in self.nodes:
            label = _wrap(execution["name"], 34) + "\n" + _wrap(execution["environment"], 34)
            if self.expand_execution:
                self.lines += [f"{key}: {_quote(label)} {{",
                               f"  link: {_quote('#process/' + owner)}",
                               '  style.fill: "#F6F9FF"', '  style.stroke: "#93A9C6"',
                               "  style.font-size: 18", "  style.border-radius: 9",
                               "  label.near: top-left"]
                for participant in execution["modules"]:
                    if self.participants is not None and participant not in self.participants:
                        continue
                    title = _title(self.model, participant)
                    self.lines += _node(_key(participant), _wrap(title, 22), "#module/" + participant,
                                        f"{title} ({participant})", "  ")
                self.lines.append("}")
            else:
                self.lines += _node(key, label, "#process/" + owner,
                                    "; ".join(execution["constraints"]), fill="#ECF3FF")
            self.nodes.add(key)
        return key, {participant: key + "." + _key(participant) for participant in execution["modules"]}

    def binding(self, owner, facet, record, index, binding, participants=None):
        self.source(owner, facet, record, f"/observed/physical_bindings/{index}", binding["constraints"])
        package = self.placement(binding["package"])
        execution, actors = self.execution(binding["execution"])
        self.lines += _flow_arrow(package, execution, "supplies implementation", label_width=16)
        self.relationship_kinds.add("package")
        modes = {"read": "reads", "write": "writes", "read-write": "reads and writes"}
        for access in binding["accesses"]:
            if participants is not None and access["participant"] not in participants:
                continue
            placement = self.placement(access["placement"])
            tooltip = access["purpose"] + "\nConditions: " + "; ".join(access["conditions"])
            self.lines += _flow_arrow(actors[access["participant"]], placement,
                                      modes[access["mode"]], tooltip, label_width=8)
            self.relationship_kinds.add("access")

    def acquisition(self, owner, facet, record, acquisition):
        self.source(owner, facet, record, "/observed/artifact_acquisition", acquisition["constraints"])
        _, actors = self.execution(acquisition["execution"])
        artifact = _key("acquisition:" + owner)
        self.lines += _node(artifact, _wrap(acquisition["artifact"], 28), self.route,
                            acquisition["name"] + "; " + "; ".join(acquisition["constraints"]), fill="#FFF5DB")
        for index, source in enumerate(acquisition["sources"]):
            key = _key(f"acquisition:{owner}:source:{index}")
            label = _wrap(source["name"], 24) + "\n\n" + _wrap(source["transport"], 24)
            self.lines += _node(key, label, self.route,
                                "Source address: " + source["address"] + "; " + "; ".join(source["conditions"]),
                                fill="#F4F1F9", dashed=True)
            self.lines += _flow_arrow(key, artifact, "alternative input", dashed=True, label_width=12)
        self.lines += _flow_arrow(artifact, actors[acquisition["participant"]], "candidate input")
        self.relationship_kinds.add("acquisition")

    def production(self, owner, facet, record, production):
        self.source(owner, facet, record, "/observed/production_placement", production["constraints"])
        key, title = _key("producer:" + owner), _title(self.model, owner)
        self.lines += _node(key, _wrap(title, 32), "#module/" + owner,
                            f"{title} ({owner})", fill="#FFF5DB")
        for role in ("source", "workspace", "output"):
            placement = self.placement(production[role])
            self.lines += _flow_arrow(key, placement, role + " location")
        self.relationship_kinds.add("production")

    def constraint(self, owner, facet, record, index, constraint):
        self.source(owner, facet, record, f"/observed/location_constraints/{index}",
                    constraint["conditions"] + [constraint["rationale"]])
        left, right = [self.placement(ref) for ref in constraint["placements"]]
        relation = {"disjoint": "disjoint locations", "same-filesystem": "same filesystem"}[constraint["relation"]]
        tooltip = constraint["name"] + "; " + constraint["rationale"] + "; " + "; ".join(constraint["conditions"])
        # A constraint is symmetric. It never becomes a transfer or call arrow.
        self.lines += [f"{left} -- {right}: {_quote(_wrap(relation, 24))} {{",
                       f"  tooltip: {_quote(tooltip)}", '  style.stroke: "#987335"',
                       '  style.font-color: "#725321"', '  style.fill: "#FFFFFF"',
                       "  style.stroke-dash: 3", "  style.font-size: 14", "}"]
        self.relationship_kinds.add("constraint")

    def result(self, navigation_label=None, summary=None):
        legends = {
            "package": {"label": "Package binding", "description": "The named package supplies the referenced runtime implementation; it is not a process or host."},
            "access": {"label": "Runtime access", "description": "Only the named participant has the recorded conditional read/write access."},
            "acquisition": {"label": "Input alternatives", "description": "Dashed arrows identify admitted candidate-byte sources; no current availability or completed acquisition is claimed."},
            "production": {"label": "Production roles", "description": "Source, workspace, and output references describe producer placement, not a build sequence."},
            "constraint": {"label": "Location constraint", "description": "Dashed undirected links preserve explicit disjointness or same-filesystem requirements, without inferring hosts."},
        }
        descriptor = {"key": self.key, "view": "physical", "title": self.title,
                      "caption": self.caption, "owners": sorted(self.owners),
                      "legend": [value for key, value in legends.items() if key in self.relationship_kinds],
                      "sources": list(self.sources.values())}
        if self.key in {"physical-consumer", "physical-storage"}:
            descriptor["initial_view"] = "readable"
        if navigation_label:
            descriptor.update(route=self.route, navigation_label=navigation_label, summary=summary)
        return self.key, "\n".join(self.lines) + "\n", descriptor


def _physical_refinement(model):
    """Separate consumer bindings, storage access, and producer placement roles."""
    bindings, acquisitions, productions, constraints = [], [], [], []
    for (owner, facet), record in sorted(model.facets.items()):
        observed = record.data.get("observed", {})
        bindings += [(owner, facet, record, index, item)
                     for index, item in enumerate(observed.get("physical_bindings", []))]
        if "artifact_acquisition" in observed:
            acquisitions.append((owner, facet, record, observed["artifact_acquisition"]))
        if "production_placement" in observed:
            productions.append((owner, facet, record, observed["production_placement"]))
        constraints += [(owner, facet, record, index, item)
                        for index, item in enumerate(observed.get("location_constraints", []))]
    if not bindings and not productions and not acquisitions and not constraints:
        return []
    common = ("Source-observed physical relationships. Names identify recorded packages, execution contexts, "
              "and placement locations; location text does not identify a machine or establish connectivity. "
              "Select a placement for exact paths and constraints. This is not deployment or artifact qualification.")
    overview = _PhysicalProjection(model, "physical", "Consumer runtime and producer placement",
                                   common + " Storage and isolation shows every recorded state access; Consumer "
                                   "deployment expands archive inputs and installation destinations.", "#physical", direction="right")
    overview.expand_execution = False
    results = []
    if bindings or acquisitions or constraints:
        consumer = _PhysicalProjection(
            model, "physical-consumer", "Consumer deployment and archive inputs",
            common + " This scope selects installation accesses and the recorded archive-input alternatives. "
            "Only the installer is expanded inside the runtime; other participants and state accesses remain "
            "in Storage and isolation. No producer-to-consumer delivery is asserted.",
            "#physical/consumer")
        storage = _PhysicalProjection(
            model, "physical-storage", "State access and location isolation",
            common + " Arrows preserve each access's participant and mode; a shared process does not grant "
            "every participant access to every placement. Dashed undirected links are explicit location constraints.",
            "#physical/storage")
        consumer.participants = {item[3]["participant"] for item in acquisitions}
        for binding in bindings:
            overview.binding(*binding, participants=set())
            installer_participants = {item[3]["participant"] for item in acquisitions
                                      if item[3]["execution"] == binding[4]["execution"]}
            consumer.binding(*binding, participants=installer_participants)
            storage.binding(*binding)
        for acquisition in acquisitions:
            consumer.acquisition(*acquisition)
        production_owners = {item[0] for item in productions}
        for constraint in constraints:
            if constraint[0] not in production_owners:
                storage.constraint(*constraint)
        if consumer.nodes:
            results.append(consumer.result("Consumer deployment", "Runtime package, execution responsibilities, and admitted archive inputs."))
        if storage.nodes:
            results.append(storage.result("Storage and isolation", "Exact participant access to state and explicit location constraints."))
    if productions:
        producer = _PhysicalProjection(
            model, "physical-production", "Producer source, workspace, and outputs",
            common + " Role arrows do not depict processing order, artifact promotion, or public delivery. "
            "Producer workspaces and candidate outputs remain separate from consumer deployment.",
            "#physical/production")
        production_owners = {item[0] for item in productions}
        for production in productions:
            overview.production(*production)
            producer.production(*production)
        for constraint in constraints:
            if constraint[0] in production_owners:
                producer.constraint(*constraint)
        results.append(producer.result("Production placement", "Canonical source, temporary workspace, candidate outputs, and separation rules."))
    if not overview.nodes:
        for constraint in constraints:
            overview.constraint(*constraint)
    if overview.nodes:
        results.insert(0, overview.result())
    return results


def realization_diagrams(model):
    """Return source and descriptor maps for typed Process and Physical facts."""
    sources, descriptors = {}, {}
    executions = _execution_records(model)
    placements = _placement_records(model)
    process_owners = sorted({owner for owner, _, _ in executions} |
                            {module for _, _, execution in executions for module in execution["modules"]})
    physical_owners = sorted({owner for owner, _, _, _, _ in placements} |
                             {module for _, _, _, _, placement in placements for module in placement["modules"]})
    for function, owners in ((_process, process_owners), (_physical, physical_owners)):
        for owner in [None, *owners]:
            result = function(model, owner)
            if result:
                key, source, descriptor = result
                sources[key] = source
                descriptors[key] = descriptor
    details = _interactions(model)
    coordination = _coordination(model)
    if coordination:
        details.append(coordination)
    for key, source, descriptor in details:
        if key in sources:
            raise ValueError(f"Duplicate Process detail projection: {key}")
        sources[key] = source
        descriptors[key] = descriptor
    # Replace only the Physical landing inventory when explicit bindings exist.
    # The owner inventories remain available with their original routes/paths.
    for key, source, descriptor in _physical_refinement(model):
        sources[key] = source
        descriptors[key] = descriptor
    return sources, descriptors
