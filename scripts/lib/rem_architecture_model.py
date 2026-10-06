"""Load, validate, and project the governed REM engineering model.

The model resolves declared relationships and qualified realization facts. It
neither renders a presentation nor interprets prose as engineering relationships.
Run the owning schema checks separately for complete authoring-profile validation.
"""

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re

from lib.validation.model_layout import supporting_architecture_json_paths

from lib.rem_architecture_process import validate_process_facts
from lib.rem_architecture_physical import validate_physical_facts
from lib.rem_architecture_testing import validate_test_groups
from lib.rem_architecture_scenarios import scenario_outcomes


COLLECTIONS = {
    "initial-requirement": "requirements/**/ir.json",
    "system-requirement": "requirements/**/sr.json",
    "allocated-requirement": "requirements/**/AR-*.json",
    "feature": "system/features/*.json",
    "function": "system/functions/*.json",
    "scenario": "requirements/scenarios/*.json",
    "module": "architecture/modules/*/module.json",
    "interface": "architecture/interfaces/*/interface.json",
}
RELATIONS = {
    "initial-requirement": {"confirms": ("feature", "scenario")},
    "system-requirement": {"confirms": ("function",), "constrains": ("feature", "function")},
    "allocated-requirement": {"allocated_to": ("module",), "constrains": ("function",)},
    "feature": {"realized_by": ("function",)},
    "function": {"allocated_to": ("module",)},
    "scenario": {"informs": ("system-requirement",), "exercises": ("feature",)},
    "module": {"provides": ("interface",), "consumes": ("interface",)},
    "interface": {"exposed_through": ("module",)},
}
SCENARIO_INTERFACES = {
    "SCN-019": ("IF-007", "IF-015", "IF-016"),
    "SCN-046": ("IF-003", "IF-004"),
    "SCN-047": ("IF-003", "IF-004"),
    "SCN-053": ("IF-008",),
    "SCN-066": ("IF-005", "IF-009", "IF-010"),
}
SCENARIO_SCOPE = tuple(SCENARIO_INTERFACES)
INTERFACE_SCOPE = tuple(sorted({i for scope in SCENARIO_INTERFACES.values() for i in scope}))
PUBLIC_RELATIONS = {"guides", "invokes", "realizes"}


@dataclass(frozen=True)
class PublicCatalog:
    owner: "Record"
    facet: "Record"
    entries: list
    mappings: dict

    @property
    def label(self):
        return "Published commands" if self.owner.data["type"] == "interface" else "Published skills"


@dataclass(frozen=True)
class Record:
    path: Path
    data: dict

    @property
    def id(self):
        return self.data["id"]


@dataclass(frozen=True)
class Edge:
    source: str
    relation: str
    target: str
    path: Path
    field: str


def architecture_paths(root):
    """Discover only governed owners/facets, rejecting aliases and skipped JSON."""
    architecture = root / "design/architecture"
    records = {"module": [], "interface": []}
    parents, expected = {}, set()
    facets = {"module": {"software", "runtime", "persistence", "deployment", "technology"},
              "interface": {"interaction", "representation", "technology"}}
    if architecture.is_symlink():
        raise ValueError(f"{architecture}: architecture symlink is not supported")
    for directory, directories, files in os.walk(architecture, followlinks=False):
        for name in directories + files:
            if (Path(directory) / name).is_symlink():
                raise ValueError(f"{Path(directory) / name}: architecture symlink is not supported")
    for kind in ("module", "interface"):
        pending = [(architecture / f"{kind}s", None)]
        while pending:
            collection, parent = pending.pop()
            if not collection.is_dir():
                raise ValueError(f"{collection}: missing architecture collection")
            for owner in sorted(path for path in collection.iterdir() if path.is_dir()):
                record = owner / f"{kind}.json"
                if not record.is_file():
                    raise ValueError(f"{record}: missing logical owner")
                records[kind].append(record)
                expected.add(record)
                if parent is not None:
                    parents[record.relative_to(root)] = parent.relative_to(root)
                for facet in (owner / "realization").glob("*.json"):
                    if facet.stem not in facets[kind]:
                        raise ValueError(f"{facet}: unsupported {kind} realization facet")
                    expected.add(facet)
                children = owner / "modules"
                if kind == "module" and children.exists():
                    pending.append((children, record))
    unexpected = set(architecture.rglob("*.json")) - expected - supporting_architecture_json_paths(root)
    if unexpected:
        raise ValueError(f"{sorted(unexpected)[0]}: unexpected architecture JSON path")
    return records, parents


class Model:
    def __init__(self, root):
        self.root = root
        self.records = {}
        self.edges = []
        self.facets = {}
        self.bytes = {}
        architecture, parent_paths = architecture_paths(root)
        self.parents = {}
        for kind, pattern in COLLECTIONS.items():
            paths = architecture[kind] if kind in architecture else (root / "design").glob(pattern)
            for path in sorted(paths):
                relative = path.relative_to(root)
                data = self.read(relative)
                if data.get("type") != kind:
                    raise ValueError(f"{relative}: unsupported type {data.get('type')!r}; expected {kind}")
                statuses = ("draft", "confirmed", "obsolete") if kind == "scenario" else ("draft",)
                if data.get("status") not in statuses:
                    raise ValueError(f"{relative}: unsupported status {data.get('status')!r}")
                identity = data.get("id")
                if not isinstance(identity, str) or not identity or identity in self.records:
                    raise ValueError(f"{relative}: missing or duplicate identity {identity!r}")
                if not isinstance(data.get("title"), str) or not data["title"].strip():
                    raise ValueError(f"{relative}: missing title")
                if kind in ("module", "interface"):
                    slug = re.sub(r"[^a-z0-9]+", "-", data["title"].lower()).strip("-")
                    if not slug:
                        raise ValueError(f"{relative}: title has no descriptive name")
                    if kind == "module":
                        if not re.fullmatch(re.escape(identity) + r"-[a-z0-9]+(?:-[a-z0-9]+)*", path.parent.name):
                            raise ValueError(f"{relative}: owner directory does not match identity and retained slug")
                    elif path.parent.name != f"{identity}-{slug}":
                        raise ValueError(f"{relative}: owner directory does not match identity and title")
                if kind == "module" and ({"parent_module", "children"} & set(data)):
                    raise ValueError(f"{relative}: duplicate authored Module containment")
                self.records[identity] = Record(relative, data)
        for kind in ("module", "interface"):
            for record in self.of_type(kind):
                for path in sorted((root / record.path.parent / "realization").glob("*.json")):
                    relative = path.relative_to(root)
                    data = self.read(relative)
                    if set(data) - {"observed", "proposed", "deferred"}:
                        raise ValueError(f"{relative}: unsupported realization state {sorted(set(data) - {'observed', 'proposed', 'deferred'})}")
                    self.facets[(record.id, path.stem)] = Record(relative, data)
        # Parse all mapping vocabularies before resolving any model reference.
        self.public_catalogs = self.read_public_catalogs()
        self.designed_catalogs = self.read_designed_catalogs()
        paths = {r.path: r for r in self.records.values()}
        for child, parent in parent_paths.items():
            self.parents[paths[child].id] = paths[parent].id
            self.edges.append(Edge(paths[child].id, "contained_by", paths[parent].id, child, "containment"))
        # Type and status vocabulary checks above precede relationship consistency.
        for record in self.records.values():
            for relation, allowed in RELATIONS[record.data["type"]].items():
                value = record.data.get(relation, [])
                if relation == "allocated_to":
                    if record.data["type"] == "function" and relation not in record.data:
                        reason = record.data.get("unallocated_reason")
                        if isinstance(reason, str) and reason.strip():
                            continue
                    if not isinstance(value, str):
                        raise ValueError(f"{record.path}: {relation} requires one Module reference")
                    if "unallocated_reason" in record.data:
                        raise ValueError(f"{record.path}: Function cannot be allocated and unallocated")
                    values = [value]
                else:
                    if not isinstance(value, list):
                        raise ValueError(f"{record.path}: {relation} requires an array")
                    if relation == "exposed_through" and relation in record.data:
                        if not value or any(not isinstance(v, str) for v in value) or len(set(value)) != len(value):
                            raise ValueError(f"{record.path}: exposed_through requires nonempty unique Module references")
                    values = value
                for index, target in enumerate(values):
                    field = f"/{relation}" if isinstance(value, str) else f"/{relation}/{index}"
                    self.resolve(target, allowed, f"{record.path} {field}")
                    self.edges.append(Edge(record.id, relation, target, record.path, field))
            if record.data["type"] in ("system-requirement", "allocated-requirement"):
                is_sr = record.data["type"] == "system-requirement"
                parent_path = (record.path.parent.parent / "ir.json" if is_sr
                               else record.path.parent / "sr.json")
                parents = [r for r in self.records.values() if r.path == parent_path]
                if len(parents) != 1:
                    raise ValueError(f"{record.path}: missing containment parent {parent_path}")
                self.edges.append(Edge(record.id, "parent", parents[0].id, record.path, "containment"))
        for interface in self.of_type("interface"):
            if len(self.incoming(interface.id, "provides")) != 1:
                raise ValueError(f"{interface.path}: expected exactly one provider")
            provider = self.incoming(interface.id, "provides")[0].source
            ancestors = self.ancestors(provider)
            exposures = set(interface.data.get("exposed_through", []))
            for boundary in exposures:
                if boundary not in ancestors:
                    raise ValueError(f"{interface.path}: exposure {boundary} is not a strict provider ancestor")
                skipped = set(ancestors[:ancestors.index(boundary)]) - exposures
                if skipped:
                    raise ValueError(f"{interface.path}: skipped exposure boundary {', '.join(sorted(skipped))}")
            for edge in self.incoming(interface.id, "consumes"):
                consumer_scope = {edge.source, *self.ancestors(edge.source)}
                missing = set(ancestors) - consumer_scope - exposures
                if missing:
                    raise ValueError(f"{interface.path}: missing exposure through {', '.join(sorted(missing))} for consumer {edge.source}")
        self.validate_public_catalogs()
        self.validate_designed_catalogs()
        self.validate_realization_structure()
        validate_process_facts(self)
        validate_physical_facts(self)
        self.test_groups = validate_test_groups(self)
        for identity, kind in [(i, "interface") for i in INTERFACE_SCOPE] + [
            (i, "scenario") for i in SCENARIO_SCOPE]:
            record = self.resolve(identity, (kind,), "bounded view scope")
            if kind == "scenario" and record.data["status"] != "confirmed":
                raise ValueError(f"{record.path}: selected Scenario must be confirmed")
        self.contributions = []
        for sr in self.of_type("system-requirement"):
            for index, source in enumerate(sr.data.get("sources", [])):
                if source["source"] != "SRC-CLI-ALLOCATION":
                    continue
                match = re.fullmatch(r"(SR-\d+) AC(\d+)(.*); allocated contributors: (.+)", source["locator"])
                if not match or match[1] != sr.id:
                    raise ValueError(f"{sr.path}: unrecognized contribution locator {source['locator']!r}")
                criterion = int(match[2])
                if not 1 <= criterion <= len(sr.data["acceptance_criteria"]):
                    raise ValueError(f"{sr.path}: missing contribution criterion AC{criterion}")
                allocated = list(dict.fromkeys(re.findall(r"AR-\d+", match[4])))
                if not allocated:
                    raise ValueError(f"{sr.path}: missing allocated contribution references")
                for identity in allocated:
                    self.resolve(identity, ("allocated-requirement",), f"{sr.path} /sources/{index}")
                self.contributions.append((sr, index, criterion, allocated, source["locator"], source["basis"]))
        identity = "".join(f"{path.as_posix()}\0{hashlib.sha256(data).hexdigest()}\n"
                           for path, data in sorted(self.bytes.items()))
        self.digest = hashlib.sha256(identity.encode()).hexdigest()

    def validate_realization_structure(self):
        """Check structured execution/placement facts without changing logical edges."""
        def shape(value, required, location):
            if not isinstance(value, dict) or set(value) != set(required):
                raise ValueError(f"{location}: unsupported realization structure shape")

        def text(value, location):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{location}: expected nonblank text")

        def texts(value, location, unique=False):
            if not isinstance(value, list) or not value:
                raise ValueError(f"{location}: expected nonempty array")
            for item in value:
                text(item, location)
            if unique and len(set(value)) != len(value):
                raise ValueError(f"{location}: duplicate realization reference or path")

        # Shape checks precede relationship consistency, including undeclared fields.
        executions, placements = [], []
        for (owner, name), facet in sorted(self.facets.items()):
            observed = facet.data.get("observed", {})
            if "execution" in observed:
                location = f"{facet.path} /observed/execution"
                if name != "runtime":
                    raise ValueError(f"{location}: execution belongs to a runtime facet")
                execution = observed["execution"]
                shape(execution, ("name", "environment", "modules", "entry_interfaces", "calls", "constraints"), location)
                for field in ("name", "environment"):
                    text(execution[field], location + "/" + field)
                for field in ("modules", "entry_interfaces", "constraints"):
                    texts(execution[field], location + "/" + field, unique=field != "constraints")
                if not isinstance(execution["calls"], list):
                    raise ValueError(f"{location}/calls: expected array")
                seen = set()
                for call in execution["calls"]:
                    shape(call, ("caller", "callee", "interface"), location + "/calls")
                    for field, value in call.items():
                        text(value, location + "/calls/" + field)
                    signature = (call["caller"], call["callee"], call["interface"])
                    if signature in seen:
                        raise ValueError(f"{location}/calls: duplicate execution call")
                    seen.add(signature)
                executions.append((owner, location, execution))
            if "placements" in observed:
                location = f"{facet.path} /observed/placements"
                if name not in ("deployment", "persistence"):
                    raise ValueError(f"{location}: placements belong to deployment or persistence")
                values = observed["placements"]
                if not isinstance(values, list) or not values:
                    raise ValueError(f"{location}: expected nonempty placements array")
                for index, placement in enumerate(values):
                    place = f"{location}/{index}"
                    shape(placement, ("name", "location", "modules", "paths", "constraints"), place)
                    for field in ("name", "location"):
                        text(placement[field], place + "/" + field)
                    for field in ("modules", "paths", "constraints"):
                        texts(placement[field], place + "/" + field, unique=field != "constraints")
                    placements.append((owner, place, placement))
            if ("execution" in observed or "placements" in observed) and not observed.get("sources"):
                raise ValueError(f"{facet.path}: structured observations require sources")

        for owner, location, execution in executions:
            members = set(execution["modules"])
            for member in members:
                self.resolve(member, ("module",), location + "/modules")
            if owner not in members:
                raise ValueError(f"{location}: execution must include its accountable owner")
            for interface in execution["entry_interfaces"]:
                self.resolve(interface, ("interface",), location + "/entry_interfaces")
                provider = self.incoming(interface, "provides")[0].source
                if not any(provider in {member, *self.ancestors(member)} for member in members):
                    raise ValueError(f"{location}: entry Interface provider has no execution participant")
            for call in execution["calls"]:
                self.resolve(call["interface"], ("interface",), location + "/calls/interface")
                for end in ("caller", "callee"):
                    self.resolve(call[end], ("module",), location + "/calls/" + end)
                    if call[end] not in members:
                        raise ValueError(f"{location}: execution call endpoint is outside its process")
                if call["interface"] not in {edge.target for edge in self.outgoing(call["caller"], "consumes")}:
                    raise ValueError(f"{location}: execution caller does not consume the Interface")
                provider = self.incoming(call["interface"], "provides")[0].source
                if provider not in {call["callee"], *self.ancestors(call["callee"])}:
                    raise ValueError(f"{location}: execution callee is outside the Interface provider boundary")
        for owner, location, placement in placements:
            for member in placement["modules"]:
                self.resolve(member, ("module",), location + "/modules")
            if owner not in placement["modules"]:
                raise ValueError(f"{location}: placement must include its accountable owner")

    def read_public_catalogs(self):
        catalogs = []

        def nonblank(value, location):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{location}: public entry text must be nonblank")

        for (identity, facet_name), facet in sorted(self.facets.items()):
            observed = facet.data.get("observed", {})
            entry_list = observed.get("public_entries")
            mappings = []
            for choice_index, choice in enumerate(facet.data.get("proposed", [])):
                if "public_entry_mappings" not in choice:
                    continue
                values = choice["public_entry_mappings"]
                location = f"{facet.path} /proposed/{choice_index}/public_entry_mappings"
                if not isinstance(values, list) or not values:
                    raise ValueError(f"{location}: public_entry_mappings must be a nonempty array")
                for index, mapping in enumerate(values):
                    pointer = f"/proposed/{choice_index}/public_entry_mappings/{index}"
                    if not isinstance(mapping, dict) or set(mapping) != {"entry", "functions", "limits"}:
                        raise ValueError(f"{facet.path} {pointer}: unsupported public entry mapping shape")
                    nonblank(mapping["entry"], f"{facet.path} {pointer}/entry")
                    if not isinstance(mapping["functions"], list) or not isinstance(mapping["limits"], list):
                        raise ValueError(f"{facet.path} {pointer}: functions and limits must be arrays")
                    for limit in mapping["limits"]:
                        nonblank(limit, f"{facet.path} {pointer}/limits")
                    if not mapping["functions"] and not mapping["limits"]:
                        raise ValueError(f"{facet.path} {pointer}: unmapped public entry requires explicit limits")
                    for function in mapping["functions"]:
                        if not isinstance(function, dict) or set(function) != {"function", "relation", "contribution"}:
                            raise ValueError(f"{facet.path} {pointer}: unsupported public Function mapping shape")
                        if not isinstance(function["relation"], str) or function["relation"] not in PUBLIC_RELATIONS:
                            raise ValueError(f"{facet.path} {pointer}: unsupported public entry relation {function['relation']!r}")
                        nonblank(function["function"], f"{facet.path} {pointer}/functions/function")
                        nonblank(function["contribution"], f"{facet.path} {pointer}/functions/contribution")
                    mappings.append((mapping, pointer))
            if "public_entries" not in observed and not mappings:
                continue
            owner = self.records[identity]
            required_facet = "interaction" if owner.data["type"] == "interface" else "software"
            if facet_name != required_facet:
                raise ValueError(f"{facet.path}: unsupported public entry catalog owner/facet")
            if not isinstance(entry_list, list) or not entry_list:
                raise ValueError(f"{facet.path}: public_entries must be a nonempty array")
            required = {"name", "group", "purpose", "source_path", "contract"}
            if owner.data["type"] == "interface":
                required.add("operation")
            for index, entry in enumerate(entry_list):
                location = f"{facet.path} /observed/public_entries/{index}"
                if not isinstance(entry, dict) or set(entry) != required:
                    raise ValueError(f"{location}: unsupported public entry shape")
                for field, value in entry.items():
                    nonblank(value, f"{location}/{field}")
            catalogs.append((owner, facet, entry_list, mappings))
        return catalogs

    def validate_public_catalogs(self):
        validated = []
        for owner, facet, entries, mappings in self.public_catalogs:
            names = [entry["name"] for entry in entries]
            if len(names) != len(set(names)):
                raise ValueError(f"{facet.path}: duplicate observed public entry name")
            indexed = {}
            for mapping, pointer in mappings:
                name = mapping["entry"]
                if name not in names:
                    raise ValueError(f"{facet.path} {pointer}: missing observed public entry {name!r}")
                if name in indexed:
                    raise ValueError(f"{facet.path}: duplicate public entry mapping {name!r}")
                indexed[name] = (mapping, pointer)
                pairs = set()
                for index, item in enumerate(mapping["functions"]):
                    self.resolve(item["function"], ("function",), f"{facet.path} {pointer}/functions/{index}")
                    pair = (item["function"], item["relation"])
                    if pair in pairs:
                        raise ValueError(f"{facet.path} {pointer}: duplicate public Function/relation mapping")
                    pairs.add(pair)
            missing = set(names) - set(indexed)
            if missing:
                raise ValueError(f"{facet.path}: missing public entry mappings: {', '.join(sorted(missing))}")
            for entry in entries:
                for field in ("source_path", "contract"):
                    self.public_path(entry[field], f"{facet.path} {entry['name']} {field}", contract=field == "contract")
                if "operation" in entry and entry["operation"] not in {o["name"] for o in owner.data["operations"]}:
                    raise ValueError(f"{facet.path}: missing Interface operation {entry['operation']!r} for {entry['name']!r}")
            validated.append(PublicCatalog(owner, facet, entries, indexed))
        self.public_catalogs = validated

    def read_designed_catalogs(self):
        """Parse designed capabilities without requiring observed implementation entries."""
        catalogs = []
        for (identity, facet_name), facet in sorted(self.facets.items()):
            entries = []
            for choice_index, choice in enumerate(facet.data.get("proposed", [])):
                if "public_capabilities" not in choice:
                    continue
                values = choice["public_capabilities"]
                if not isinstance(values, list) or not values:
                    raise ValueError(f"{facet.path}: public_capabilities must be a nonempty array")
                for index, entry in enumerate(values):
                    pointer = f"/proposed/{choice_index}/public_capabilities/{index}"
                    location = f"{facet.path} {pointer}"
                    if not isinstance(entry, dict) or set(entry) != {"name", "group", "purpose", "contract", "functions", "limits"}:
                        raise ValueError(f"{location}: unsupported designed capability shape")
                    for field in ("name", "group", "purpose", "contract"):
                        if not isinstance(entry[field], str) or not entry[field].strip():
                            raise ValueError(f"{location}: {field} must be nonblank text")
                    if not isinstance(entry["functions"], list) or not isinstance(entry["limits"], list):
                        raise ValueError(f"{location}: functions and limits must be arrays")
                    if not entry["functions"] and not entry["limits"]:
                        raise ValueError(f"{location}: unmapped designed capability requires explicit limits")
                    if any(not isinstance(limit, str) or not limit.strip() for limit in entry["limits"]):
                        raise ValueError(f"{location}: limits must be nonblank text")
                    for function in entry["functions"]:
                        if not isinstance(function, dict) or set(function) != {"function", "relation", "contribution"}:
                            raise ValueError(f"{location}: unsupported designed Function mapping shape")
                        if not isinstance(function["relation"], str) or function["relation"] not in PUBLIC_RELATIONS:
                            raise ValueError(f"{location}: unsupported public entry relation {function['relation']!r}")
                        if any(not isinstance(function[key], str) or not function[key].strip() for key in ("function", "contribution")):
                            raise ValueError(f"{location}: Function and contribution must be nonblank text")
                    entries.append((entry, pointer))
            if entries:
                owner = self.records[identity]
                required_facet = "interaction" if owner.data["type"] == "interface" else "software"
                if facet_name != required_facet:
                    raise ValueError(f"{facet.path}: unsupported designed capability owner/facet")
                catalogs.append((owner, facet, entries))
        return catalogs

    def validate_designed_catalogs(self):
        for owner, facet, entries in self.designed_catalogs:
            names = set()
            for entry, pointer in entries:
                location = f"{facet.path} {pointer}"
                if entry["name"] in names:
                    raise ValueError(f"{location}: duplicate designed capability name")
                names.add(entry["name"])
                self.public_path(entry["contract"], location, contract=True)
                pairs = set()
                for item in entry["functions"]:
                    self.resolve(item["function"], ("function",), location)
                    pair = (item["function"], item["relation"])
                    if pair in pairs:
                        raise ValueError(f"{location}: duplicate designed Function/relation mapping")
                    pairs.add(pair)

    def public_path(self, value, location, contract=False):
        """Stat a canonical local reference without opening the target content."""
        parts = value.split("#")
        path = Path(parts[0])
        if (not parts[0] or path.is_absolute() or path.as_posix() != parts[0]
                or any(part in (".", "..") for part in parts[0].split("/"))
                or "\\" in value or ":" in parts[0] or any(character.isspace() for character in value)
                or (not contract and len(parts) != 1)
                or (contract and (len(parts) > 2 or path.suffix != ".md" or len(parts) == 2 and not parts[1].strip()))):
            raise ValueError(f"{location}: unsafe public entry path {value!r}")
        target = (self.root / path).resolve()
        if not target.is_relative_to(self.root) or not target.is_file():
            raise ValueError(f"{location}: missing or unsafe public entry path {value!r}")

    def catalog_host(self, catalog):
        if catalog.owner.data["type"] == "module":
            return catalog.owner.id
        return self.incoming(catalog.owner.id, "provides")[0].source

    def ancestors(self, identity):
        result = []
        while identity in self.parents:
            identity = self.parents[identity]
            result.append(identity)
        return result

    def children(self, identity):
        return sorted(child for child, parent in self.parents.items() if parent == identity)

    def module_order(self):
        pending = sorted((r.id for r in self.of_type("module") if r.id not in self.parents), reverse=True)
        result = []
        while pending:
            identity = pending.pop()
            result.append(self.records[identity])
            pending.extend(reversed(self.children(identity)))
        return result

    def read(self, path):
        data = (self.root / path).read_bytes()
        self.bytes[path] = data
        value = json.loads(data)
        if not isinstance(value, dict):
            raise ValueError(f"{path}: expected a JSON object")
        return value

    def resolve(self, identity, allowed, source):
        if not isinstance(identity, str) or identity not in self.records:
            raise ValueError(f"{source}: missing reference {identity!r}")
        record = self.records[identity]
        if record.data["type"] not in allowed:
            raise ValueError(f"{source}: wrong-type reference {identity}: expected {', '.join(allowed)}")
        return record

    def of_type(self, kind):
        return sorted((r for r in self.records.values() if r.data["type"] == kind), key=lambda r: r.id)

    def outgoing(self, identity, relation):
        return sorted((e for e in self.edges if e.source == identity and e.relation == relation), key=lambda e: e.target)

    def incoming(self, identity, relation):
        return sorted((e for e in self.edges if e.target == identity and e.relation == relation), key=lambda e: e.source)

    def architecture_views(self):
        """Source-backed semantic projections consumed by the architecture browser."""
        return architecture_views(self)


def projected_edge(edge):
    return {"source": edge.source, "relation": edge.relation, "target": edge.target,
            "path": edge.path.as_posix(), "field": edge.field}


def scenario_projection(model, identity):
    """Derive relevance and exact provenance without inferring execution."""
    selected_interfaces = set(SCENARIO_INTERFACES[identity])
    relevant = model.outgoing(identity, "informs")
    requirements = [edge.target for edge in relevant]
    for requirement in requirements:
        relevant += model.outgoing(requirement, "confirms")
        relevant += model.incoming(requirement, "parent")
    participants = {edge.target for edge in relevant if edge.relation == "confirms"}
    participants |= {edge.source for edge in relevant if edge.relation == "parent"}
    for participant in sorted(participants):
        relevant += model.outgoing(participant, "allocated_to")
    modules = {edge.target for edge in relevant if edge.relation == "allocated_to"}
    contexts = {}
    for module in sorted(modules):
        for consumer in model.outgoing(module, "consumes"):
            if consumer.target not in selected_interfaces:
                continue
            provider = model.incoming(consumer.target, "provides")[0]
            if provider.source not in modules:
                contexts.setdefault(provider, []).append({
                    "kind": "consumer", "module": module,
                    "relationship": projected_edge(consumer), "containment": []})
        for ancestor in model.ancestors(module):
            if ancestor in modules:
                continue
            for provider in model.outgoing(ancestor, "provides"):
                if provider.target not in selected_interfaces:
                    continue
                containment, cursor = [], module
                while cursor != ancestor:
                    edge = model.outgoing(cursor, "contained_by")[0]
                    containment.append(projected_edge(edge))
                    cursor = edge.target
                contexts.setdefault(provider, []).append({
                    "kind": "ancestor", "module": module,
                    "relationship": None, "containment": containment})
    boundary = []
    for module in sorted(modules):
        for relation in ("provides", "consumes"):
            for edge in model.outgoing(module, relation):
                (relevant if edge.target in selected_interfaces else boundary).append(edge)
    context_modules = {edge.source for edge in contexts}
    owners = modules | context_modules
    gaps = [{"function": participant, "reason": model.records[participant].data["unallocated_reason"]}
            for participant in sorted(participants)
            if model.records[participant].data["type"] == "function"
            and not model.outgoing(participant, "allocated_to")]
    owner_limits = [{"owner": owner, "limits": list(model.records[owner].data.get("design_limits", []))}
                    for owner in sorted(owners)]
    projection = {
        "scenario": identity, "requirements": requirements,
        "functions": sorted(p for p in participants if model.records[p].data["type"] == "function"),
        "allocated_requirements": sorted(p for p in participants if model.records[p].data["type"] == "allocated-requirement"),
        "modules": sorted(modules), "context_modules": sorted(context_modules),
        "interfaces": sorted(selected_interfaces),
        "limits": ["Reachability identifies relevant analysis context, not execution order or complete outcome coverage."]
                  + [limit for owner in owner_limits for limit in owner["limits"]]
                  + [gap["reason"] for gap in gaps],
        "owner_limits": owner_limits, "allocation_gaps": gaps,
        "module_ancestry": {module: model.ancestors(module) for module in sorted(modules)},
        "relationships": [projected_edge(edge) for edge in sorted(set(relevant),
                           key=lambda edge: (edge.source, edge.relation, edge.target))],
        "boundary_relationships": [projected_edge(edge) for edge in sorted(set(boundary),
                                    key=lambda edge: (edge.source, edge.relation, edge.target))],
        "feature_relationships": [projected_edge(edge) for edge in model.outgoing(identity, "exercises")],
        "contract_context": [
            {"interface": edge.target, "provider": edge.source,
             "relationship": projected_edge(edge), "reasons": reasons}
            for edge, reasons in sorted(contexts.items(), key=lambda item: (item[0].target, item[0].source))],
        "facet_refs": [{"owner": owner, "facet": facet} for owner, facet in sorted(model.facets)
                       if owner in owners | selected_interfaces],
    }
    projection["outcomes"] = scenario_outcomes(model, projection)
    return projection


def architecture_views(model):
    """Discover recorded realization facets and share the bounded Scenario slices."""
    specifications = {
        "process": ("Process architecture",
                    "How does the architecture behave at runtime and across execution boundaries?",
                    {"runtime", "interaction"},
                    "Runtime and Interface interaction facets discovered from their canonical owners.",
                    "Only explicitly recorded interaction steps and lifecycle transitions establish the selected runtime order. Source inspection does not establish verified runtime behavior or complete Scenario coverage."),
        "development": ("Development architecture",
                        "How is architectural responsibility implemented, built, and assessed through the software and test organization?",
                        {"software", "representation", "technology"},
                        "Software, representations, Interface bindings, production paths, and bounded test groups discovered from their canonical owners.",
                        "Source mappings do not establish successful builds or tests. A test group's containing Module is its assessed responsibility; shared execution tooling retains its referenced contract owner and has no inferred REM allocation."),
        "physical": ("Physical architecture",
                     "How is the software packaged, placed, distributed, and persisted?",
                     {"deployment", "persistence"},
                     "Consumer deployment, storage/isolation, and production placement from canonical deployment, persistence, execution, and acquisition facts.",
                     "Physical bindings record qualified package, execution, access, and location relationships. They do not establish machine identity, deployed availability, or platform durability."),
    }
    common = "Observed source findings, proposed choices, and deferred work retain their distinct qualifications and original provenance."
    views = {"logical": {
        "title": "Logical architecture",
        "question": "Where do architectural responsibilities live and how do they collaborate?",
        "scope": f"{len(model.of_type('module'))} Modules and {len(model.of_type('interface'))} Interfaces, with exact allocations and containment.",
        "limits": ["The draft model records selected responsibilities and collaborations; missing connections do not establish architectural independence."],
        "facet_refs": [],
    }}
    for name, (title, question, kinds, scope, limit) in specifications.items():
        references = []
        for owner, facet in sorted(model.facets):
            observed = model.facets[(owner, facet)].data.get("observed", {})
            if (facet in kinds or (name == "development" and facet == "interaction" and observed.get("bindings"))
                    or (name == "physical" and ((facet == "interaction" and observed.get("artifact_acquisition"))
                    or (facet == "runtime" and observed.get("execution"))))):
                references.append({"owner": owner, "facet": facet})
        views[name] = {"title": title, "question": question, "scope": scope,
                       "limits": [common, limit], "facet_refs": references}
        if not references:
            views[name]["limits"].append("No applicable realization facets are recorded for this view.")
    views["development"]["test_groups"] = model.test_groups
    slices = [scenario_projection(model, identity) for identity in SCENARIO_SCOPE]
    facets = {(ref["owner"], ref["facet"]) for item in slices for ref in item["facet_refs"]}
    views["scenarios"] = {
        "title": "Scenario architecture (+1)",
        "question": "How do stakeholder outcomes relate to their obligations and applicable architecture details?",
        "scope": "Bounded participation slices for " + ", ".join(SCENARIO_SCOPE) + ". Publication and recovery additionally select outcome-specific reading context. Canonical Scenarios remain stakeholder-facing and unchanged.",
        "limits": ["Reachable Modules are analysis participants, not proof of execution in every interaction or outcome.",
                   "Selected contract providers remain distinct from behavior allocations. Outcome coverage requires architecture review.",
                   "Outcome selections identify explanatory context, not execution, complete coverage or requirement satisfaction. Related tests remain contextual; no verification evidence is linked by this reading profile."],
        "facet_refs": [{"owner": owner, "facet": facet} for owner, facet in sorted(facets)],
        "scenarios": slices,
    }
    return views
