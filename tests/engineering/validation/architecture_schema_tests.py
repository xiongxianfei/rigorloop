"""Direct checks for the draft Module, Interface, and AR authoring profiles.

Run with: python3 tests/engineering/validation/architecture_schema_tests.py
Requires jsonschema with Draft 2020-12 support. Independent fixtures protect
meaningful required content, closed vocabulary, single responsibility links,
and contract shape. Current-record checks inspect owner directories, subordinate
realization facets, source registration, endpoints, operation-name conventions,
and public-entry correspondence. Catalog checks only inspect source path existence;
they do not read skill instructions, execute interface behavior, or
establish derivation, architectural adequacy, approval, or implementation.
The system-design suite owns shared identity, naming, containment, and links.
"""

from copy import deepcopy
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile
import unittest

from jsonschema import Draft202012Validator, ValidationError


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.validation.model_layout import supporting_architecture_json_paths

KINDS = {"module": "MOD", "interface": "IF", "ar": "AR"}
FACETS = {
    "module": {"software", "runtime", "persistence", "deployment", "technology"},
    "interface": {"interaction", "representation", "technology"},
}


def architecture_paths(root):
    """Walk owned Module collections; reject aliases and unowned JSON first."""
    if root.is_symlink():
        raise ValueError(f"Architecture symlinks are not supported: {root}")
    authored = set()
    for directory, folders, filenames in os.walk(root, followlinks=False):
        for name in folders + filenames:
            path = Path(directory) / name
            if path.is_symlink():
                raise ValueError(f"Architecture symlinks are not supported: {path}")
        authored.update(Path(directory) / name for name in filenames if name.endswith(".json"))

    records, facets = [], []
    expected, identities = set(), set()
    collections = []
    for kind in FACETS:
        collection = root / f"{kind}s"
        if not collection.is_dir():
            raise ValueError(f"Missing architecture collection: {collection}")
        collections.append((kind, collection))
    while collections:
        kind, collection = collections.pop(0)
        for owner in sorted(path for path in collection.iterdir() if path.is_dir()):
            record_path = owner / f"{kind}.json"
            if not record_path.is_file():
                raise ValueError(f"Missing logical owner: {record_path}")
            record = json.loads(record_path.read_text())
            if not isinstance(record, dict) or record.get("type") != kind:
                raise ValueError(f"Wrong logical owner type: {record_path}")
            if not isinstance(record.get("id"), str) or not isinstance(record.get("title"), str):
                raise ValueError(f"Invalid logical owner identity or title: {record_path}")
            slug = re.sub(r"[^a-z0-9]+", "-", record["title"].lower()).strip("-")
            if not slug:
                raise ValueError(f"Invalid logical owner identity or title: {record_path}")
            if kind == "module":
                if not re.fullmatch(re.escape(record["id"]) + r"-[a-z0-9]+(?:-[a-z0-9]+)*", owner.name):
                    raise ValueError(f"Owner directory does not match identity and retained slug: {owner}")
            elif owner.name != f'{record["id"]}-{slug}':
                raise ValueError(f"Owner directory does not match identity and title: {owner}")
            if record["id"] in identities:
                raise ValueError(f"Duplicate architecture identity: {record['id']}")
            identities.add(record["id"])
            records.append(record_path)
            expected.add(record_path)
            for facet in sorted((owner / "realization").glob("*.json")):
                if facet.stem not in FACETS[kind]:
                    raise ValueError(f"Unsupported {kind} realization facet: {facet}")
                facets.append(facet)
                expected.add(facet)
            if kind == "module" and (owner / "modules").is_dir():
                collections.append((kind, owner / "modules"))
    unexpected = authored - expected - supporting_architecture_json_paths(root.parent.parent)
    if unexpected:
        raise ValueError(f"Unexpected architecture JSON path: {sorted(unexpected)[0]}")
    return records, facets


def module_parent_ids(records):
    """Derive the sole parent fact from validated owner directories."""
    owners = {path.parent: record["id"] for path, record in records if record["type"] == "module"}
    return {
        identifier: owners.get(directory.parent.parent)
        for directory, identifier in owners.items()
    }


def validate_interface_exposure(records):
    """Check provider-side boundaries without turning exposure into ownership."""
    entities = {record["id"]: record for _, record in records}
    modules = [record for _, record in records if record["type"] == "module"]
    parents = module_parent_ids(records)

    def ancestors(identifier):
        result = []
        while parents[identifier] is not None:
            identifier = parents[identifier]
            if identifier in result:
                raise ValueError(f"Cyclic Module containment: {identifier}")
            result.append(identifier)
        return result

    for _, interface in records:
        if interface["type"] != "interface":
            continue
        identity = interface["id"]
        providers = [record["id"] for record in modules if identity in record["provides"]]
        if len(providers) != 1:
            raise ValueError(f"Interface {identity} requires exactly one provider: {providers}")
        exposures = interface.get("exposed_through", [])
        if "exposed_through" in interface and (
            not isinstance(exposures, list) or not exposures
            or any(not isinstance(target, str) for target in exposures)
            or len(set(exposures)) != len(exposures)
        ):
            raise ValueError(f"Invalid exposed_through collection: {identity}")
        for target in exposures:
            if target not in entities:
                raise ValueError(f"Missing exposure target: {identity} -> {target}")
            if entities[target]["type"] != "module":
                raise ValueError(f"Wrong-type exposure target: {identity} -> {target}")
        provider_ancestors = ancestors(providers[0])
        for target in exposures:
            if target not in provider_ancestors:
                raise ValueError(f"Exposure target is not a strict provider ancestor: {identity} -> {target}")
            for intermediate in provider_ancestors[:provider_ancestors.index(target)]:
                if intermediate not in exposures:
                    raise ValueError(f"Exposure skips intermediate ancestor: {identity} -> {intermediate}")
        for consumer in modules:
            if identity not in consumer["consumes"]:
                continue
            containing = {consumer["id"], *ancestors(consumer["id"])}
            for boundary in provider_ancestors:
                if boundary not in containing and boundary not in exposures:
                    raise ValueError(
                        f"Missing required exposure through {boundary}: {identity} -> {consumer['id']}"
                    )


def validate_public_entries(root, owner, record, entities, validator):
    """Check catalog references after shape/vocabulary, without reading sources."""
    validator.validate(record)
    entries = record.get("observed", {}).get("public_entries", [])
    mappings = [mapping for proposal in record.get("proposed", [])
                for mapping in proposal.get("public_entry_mappings", [])]
    names = [entry["name"] for entry in entries]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate public entry name")
    mapped_names = [mapping["entry"] for mapping in mappings]
    if len(mapped_names) != len(set(mapped_names)):
        raise ValueError("Duplicate public entry mapping")
    if set(names) != set(mapped_names):
        raise ValueError("Public entry mappings must match the observed names exactly")

    def local_file(value):
        path = PurePosixPath(value)
        if (path.is_absolute() or path.as_posix() != value or ".." in path.parts
                or "\\" in value or ":" in value or "#" in value):
            raise ValueError(f"Public entry path must be exact repository-relative: {value}")
        target = (root / value).resolve()
        if not target.is_relative_to(root.resolve()):
            raise ValueError(f"Public entry path escapes the repository: {value}")
        if not target.is_file():
            raise ValueError(f"Missing public entry file: {value}")

    for entry in entries:
        local_file(entry["source_path"])
        local_file(entry["contract"].partition("#")[0])
        if "operation" in entry:
            if owner["type"] != "interface":
                raise ValueError("Public command operations require an Interface owner")
            operations = {operation["name"] for operation in owner["operations"]}
            if entry["operation"] not in operations:
                raise ValueError(f"Unknown public entry operation: {entry['operation']}")
    for mapping in mappings:
        pairs = [(binding["function"], binding["relation"]) for binding in mapping["functions"]]
        if len(pairs) != len(set(pairs)):
            raise ValueError(f"Duplicate public entry Function relation: {mapping['entry']}")
        for binding in mapping["functions"]:
            identity = binding["function"]
            if identity not in entities:
                raise ValueError(f"Missing public entry Function: {identity}")
            if entities[identity]["type"] != "function":
                raise ValueError(f"Wrong-type public entry Function: {identity}")


def architecture_fixture(kind, populated=False):
    """Build fresh, independently specified examples without reading schemas."""
    record = {
        "id": f"{KINDS[kind]}-1",
        "type": "allocated-requirement" if kind == "ar" else kind,
        "title": "Retain engineering definitions",
        "status": "draft",
        "sources": [{
            "source": "SRC-REM",
            "locator": "SR-1 allocation",
            "basis": "Accepted definitions must remain available after authoring sessions.",
        }],
    }
    if kind == "module":
        record.update({
            "description": "Account for durable engineering definition storage.",
            "responsibilities": ["Retain accepted definitions across sessions."],
            "owned_state": [],
            "scope": {"includes": ["Governed engineering definitions"], "excludes": []},
            "provides": [],
            "consumes": [],
            "design_limits": ["Storage technology remains a later realization decision."],
        })
        if populated:
            record["owned_state"] = ["Saved definition content and identity"]
            record["scope"]["excludes"] = ["Human judgment of definition adequacy"]
            record["provides"] = ["IF-1"]
            record["consumes"] = ["IF-2"]
    elif kind == "interface":
        record.update({
            "description": "Accept a definition and return its retained result.",
            "operations": [{
                "name": "retain_definition",
                "purpose": "Preserve a supplied definition for later retrieval.",
                "inputs": ["A proposed definition with its stable identity"],
                "preconditions": [],
                "outputs": ["The retained definition identity and resulting state"],
                "behavior": ["Retain the supplied content before reporting success."],
                "failure_behavior": [],
            }],
            "consistency_rules": ["Do not report success before content is retained."],
            "compatibility_rules": ["Reject a profile the provider cannot interpret."],
        })
        if populated:
            record["exposed_through"] = ["MOD-1"]
            record["operations"][0]["preconditions"] = ["The selected model is writable."]
            record["operations"][0]["failure_behavior"] = [{
                "condition": "The selected model cannot be written.",
                "outcome": "Report unavailability without claiming successful retention.",
            }]
    else:
        record.update({
            "statement": "The storage Module shall preserve each accepted definition across sessions.",
            "analysis": {
                "method": "5W2H",
                "what": {
                    "problem": "Session-local definitions are unavailable to later readers.",
                    "desired_outcome": "Accepted definitions remain retrievable in a later session.",
                },
                "why": {"rationale": "Readers need an enduring engineering definition."},
                "who": {"stakeholders": ["Engineering authors and readers"]},
                "when": {"conditions": ["After an accepted save."]},
                "where": {"contexts": ["The selected governed engineering model."]},
                "how": {"approach": "Retain the accepted definition independently of the session."},
                "how_much": {"scope": "Every accepted definition in the retained model."},
            },
            "acceptance_criteria": ["A later session retrieves the accepted definition unchanged."],
            "assumptions": [],
            "constraints": [],
            "allocated_to": "MOD-1",
        })
        if populated:
            record["analysis"]["why"]["value"] = ["Engineering work can resume."]
            record["analysis"]["who"]["affected_users"] = ["Reviewers"]
            record["analysis"]["when"]["frequency"] = "Each accepted save."
            record["analysis"]["how_much"].update({"scale": "All governed definitions.", "limits": []})
            record["assumptions"] = ["A retained engineering model is selected."]
            record["constraints"] = ["Access follows the model's authority rules."]
            record["constrains"] = ["FUNC-1"]
            record["open_questions"] = ["What retention duration is required?"]
    return record


def at_path(record, path):
    for part in path:
        record = record[part]
    return record


def hierarchy_fixture(root, consumer="MOD-4", exposure=None):
    """Model a provider, local sibling, cousin, and consumer in another tree."""
    definitions = [
        ("MOD-1", "Engineering state management", None),
        ("MOD-2", "Definition storage", "MOD-1"),
        ("MOD-3", "Saved definition retention", "MOD-2"),
        ("MOD-4", "Saved definition query", "MOD-2"),
        ("MOD-5", "Engineering state review", "MOD-1"),
        ("MOD-6", "External engineering automation", None),
        ("MOD-7", "Definition export", "MOD-6"),
    ]
    paths = {}
    for identity, title, parent in definitions:
        record = architecture_fixture("module")
        record.update(id=identity, title=title)
        if identity == "MOD-3":
            record["provides"] = ["IF-1"]
        if identity == consumer:
            record["consumes"] = ["IF-1"]
        collection = root / "modules" if parent is None else paths[parent].parent / "modules"
        path = collection / f"{identity}-{title.lower().replace(' ', '-')}" / "module.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(record))
        paths[identity] = path
    interface = architecture_fixture("interface")
    if exposure is not None:
        interface["exposed_through"] = exposure
    path = root / "interfaces/IF-1-retain-engineering-definitions/interface.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(interface))
    paths["IF-1"] = path
    return paths


def realization_fixture(facet):
    """A partial source observation plus a reasoned choice, independent of schemas."""
    content = {
        "software": {"software_units": [{
            "path": "src/definitions.js", "role": "Retains supplied definitions.",
        }]},
        "runtime": {"runtime": ["The definition store runs in the caller process."]},
        "persistence": {"persistence": ["Accepted definitions reside in the selected model directory."]},
        "deployment": {"packaging": ["The caller package includes the definition store."]},
        "technology": {"technologies": ["The inspected store uses the Node filesystem API."]},
        "interaction": {"bindings": [{
            "path": "src/definitions.js", "role": "Exposes the save operation to the caller.",
        }]},
        "representation": {"representation": ["Accepted definitions are UTF-8 JSON objects."]},
    }[facet]
    return {
        "observed": {
            **content,
            "sources": [{
                "source": "SRC-EXAMPLE",
                "locator": "src/definitions.js at an inspected revision",
                "basis": "Source inspection locates the save operation; it does not prove durability.",
            }],
        },
        "proposed": [{
            "choice": "Keep the definition store in the caller process.",
            "rationale": "The current local caller needs no remote access boundary.",
            "alternatives": ["A separate service adds a protocol with no established need."],
            "consequences": ["Caller and store share a process failure boundary."],
            "revisit_when": ["Independent remote clients require concurrent access."],
        }],
        "deferred": ["Qualify filesystem durability on the supported platforms."],
    }


def test_group_fixture():
    """An attributed test organization example, with no execution claim."""
    return {"observed": {
        "test_groups": [{
            "name": "Definition retention and rejected writes",
            "contract": "docs/design/definitions.md#retention",
            "test_sources": [{"path": "tests/definitions.test.js",
                              "role": "Observe retained bytes and rejected writes in a private root."}],
            "observation_boundary": "Definition-store interface and real private files.",
            "fixtures": [{"path": "tests/helpers/definitions.js",
                          "role": "Create fresh independently specified records."}],
            "execution": {
                "owner_contract": "docs/design/validation.md",
                "selection": [{"path": "scripts/select-checks.py", "role": "Select the existing definition suite."}],
                "runners": [{"path": "scripts/run-checks.py", "role": "Dispatch native cases with isolated roots."}],
                "entrypoints": [{"path": "package.json", "role": "Declare the native test command."}],
            },
            "required_artifacts": ["Current store implementation and temporary writable roots."],
            "limits": ["Source organization is not passing execution or complete coverage."],
        }],
        "sources": [{"source": "SRC-EXAMPLE", "locator": "Owner contract and inspected test sources",
                     "basis": "Source inspection identifies selected test dependencies, without running the suite."}],
    }}


def public_entry_fixture(facet):
    """Observed names and proposed correspondence are independently specified."""
    record = realization_fixture(facet)
    entry = {
        "name": "definition retain" if facet == "interaction" else "definition-guide",
        "group": "Retain engineering definitions",
        "purpose": "Help the author retain an engineering definition.",
        "source_path": "src/definitions.js" if facet == "interaction" else "skills/definition-guide/SKILL.md",
        "contract": "docs/definitions.md#retain-a-definition",
    }
    if facet == "interaction":
        entry["operation"] = "retain_definition"
    record["observed"]["public_entries"] = [entry]
    record["proposed"][0]["public_entry_mappings"] = [{
        "entry": entry["name"],
        "functions": [{
            "function": "FUNC-1",
            "relation": "invokes" if facet == "interaction" else "guides",
            "contribution": "The entry supplies a bounded definition-retention step.",
        }],
        "limits": ["The record does not establish execution evidence."],
    }]
    return record


def process_fixture(kind):
    """Small source-qualified interaction/state examples, independent of schemas."""
    if kind == "interaction":
        content = {"sequences": [{
            "name": "Publish supplied content", "operation": "publish_content",
            "participants": ["MOD-1", "MOD-2"], "preconditions": ["Explicit content supplied."],
            "steps": [{"name": "Prepare", "participant": "MOD-2", "action": "Check supplied bytes.",
                       "branches": [{"condition": "The request is a preview.",
                                     "steps": [{"name": "Return preview", "participant": "MOD-1",
                                                "action": "Return the prepared nonwriting result."}],
                                     "outcome": "No authoritative replacement."}]},
                      {"name": "Publish", "participant": "MOD-2", "action": "Replace the selected content."}],
            "outcome": "Publication completed.",
            "failures": [{"condition": "Input changed.", "outcome": "Conflict.",
                          "effects": ["Existing content retained."]}],
            "constraints": ["Inspected source, not executed evidence."],
        }]}
    else:
        content = {"lifecycles": [{
            "name": "Private journal", "states": [
                {"name": "Absent", "meaning": "No retained journal."},
                {"name": "Prepared", "meaning": "Exact transaction retained."}],
            "transitions": [{"from": "Absent", "to": "Prepared", "trigger": "Prepare publication",
                             "guards": ["Writer exclusion held."],
                             "effects": ["Retain exact before and candidate content."]}],
            "constraints": ["Absence is not a serialized journal phase."],
        }]}
    return {"observed": {**content, "sources": realization_fixture(kind)["observed"]["sources"]}}


def physical_fixture(field):
    """Independent subordinate references and conditional physical facts."""
    def placement(name):
        return {"owner": "MOD-1", "facet": "deployment", "name": name}
    execution = {"owner": "MOD-1", "name": "Command process"}
    content = {
        "physical_bindings": [{"name": "Consumer invocation", "execution": execution,
            "package": placement("Executable package"), "accesses": [{"participant": "MOD-1",
            "placement": placement("Selected records"), "mode": "read-write", "purpose": "Access explicitly selected records.",
            "conditions": ["Only the selected command's path accesses these bytes."]}],
            "constraints": ["Locations do not establish independent machines."]}],
        "production_placement": {"source": placement("Canonical checkout"),
            "workspace": placement("Temporary checkout"), "output": placement("Candidate directory"),
            "constraints": ["No produced artifact is asserted."]},
        "location_constraints": [{"name": "Separate candidate output", "relation": "disjoint",
            "placements": [placement("Canonical checkout"), placement("Candidate directory")],
            "conditions": ["Applies to the candidate coordinator."], "rationale": "Preserve source content."}],
        "artifact_acquisition": {"name": "Selected archive input", "execution": execution,
            "participant": "MOD-1", "artifact": "Compatible skill archive",
            "sources": [{"name": "Explicit local archive", "transport": "Local filesystem",
                         "address": "<supplied path>", "conditions": ["Local input explicitly selected."]}],
            "constraints": ["This records a supported source, not an acquired artifact."]},
    }[field]
    kind = "interaction" if field == "artifact_acquisition" else "deployment"
    return kind, {"observed": {field: content, "sources": realization_fixture(kind)["observed"]["sources"]}}


class ArchitectureSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schemas = {
            kind: json.loads((ROOT / "design/support/schemas" / f"{kind}.schema.json").read_text())
            for kind in KINDS
        }
        cls.schemas.update({
            facet: json.loads((ROOT / "design/support/schemas/realization" /
                              f"{facet}.schema.json").read_text())
            for facet in set.union(*FACETS.values())
        })
        cls.validators = {kind: Draft202012Validator(schema) for kind, schema in cls.schemas.items()}

    def valid_fixture(self, kind, populated=False):
        record = architecture_fixture(kind, populated)
        self.assert_valid(kind, record)
        return record

    def assert_valid(self, kind, record):
        errors = list(self.validators[kind].iter_errors(record))
        self.assertEqual(errors, [], msg="; ".join(
            f"{list(error.path)}: {error.message}" for error in errors
        ))

    def assert_rejected(self, kind, record, path, validator):
        errors = list(self.validators[kind].iter_errors(record))
        self.assertIn((path, validator), [(tuple(e.path), e.validator) for e in errors],
                      msg="; ".join(f"{list(e.path)}: {e.message}" for e in errors))

    def test_schemas_and_independent_records_are_valid(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                Draft202012Validator.check_schema(self.schemas[kind])
                self.valid_fixture(kind)
                self.valid_fixture(kind, populated=True)
        record = self.valid_fixture("ar")
        record["constrains"] = []
        self.assert_valid("ar", record)

    def test_current_architecture_and_allocated_requirement_records_conform(self):
        records, _ = architecture_paths(ROOT / "design/architecture")
        collections = {
            "module": [path for path in records if path.name == "module.json"],
            "interface": [path for path in records if path.name == "interface.json"],
            "ar": (ROOT / "design/requirements").rglob("AR-*.json"),
        }
        for kind, candidates in collections.items():
            paths = sorted(candidates)
            self.assertTrue(paths, f"No {kind} records found")
            for path in paths:
                with self.subTest(path=str(path.relative_to(ROOT))):
                    self.assert_valid(kind, json.loads(path.read_text()))

    def test_required_architectural_content_cannot_be_omitted(self):
        for kind in KINDS:
            fields = [(name,) for name in architecture_fixture(kind)]
            fields += [("sources", 0, name) for name in ("source", "locator", "basis")]
            if kind == "module":
                fields += [("scope", name) for name in ("includes", "excludes")]
            elif kind == "interface":
                fields += [("operations", 0, name) for name in architecture_fixture(kind)["operations"][0]]
                fields += [("operations", 0, "failure_behavior", 0, name)
                           for name in ("condition", "outcome")]
            else:
                analysis = architecture_fixture(kind)["analysis"]
                fields += [("analysis", name) for name in analysis]
                fields += [("analysis", question, name)
                           for question, answer in analysis.items() if isinstance(answer, dict)
                           for name in answer]
            for path in fields:
                with self.subTest(kind=kind, missing=path):
                    record = self.valid_fixture(kind, populated=True)
                    del at_path(record, path[:-1])[path[-1]]
                    self.assert_rejected(kind, record, path[:-1], "required")

    def test_closed_vocabulary_and_every_object_boundary_reject_unknown_values(self):
        objects = {
            "module": [("scope",)],
            "interface": [("operations", 0), ("operations", 0, "failure_behavior", 0)],
            "ar": [("analysis",)] + [("analysis", name) for name in
                                     ("what", "why", "who", "when", "where", "how", "how_much")],
        }
        for kind in KINDS:
            for path in [(), ("sources", 0)] + objects[kind]:
                with self.subTest(kind=kind, unknown_object_field=path):
                    record = self.valid_fixture(kind, populated=True)
                    at_path(record, path)["unexpected"] = "unsupported"
                    self.assert_rejected(kind, record, path, "additionalProperties")
            for field, value in (("type", "unknown"), ("status", "unknown"), ("status", "approved")):
                with self.subTest(kind=kind, field=field, value=value):
                    record = self.valid_fixture(kind)
                    record[field] = value
                    self.assert_rejected(kind, record, (field,), "const")
        record = self.valid_fixture("ar")
        record["analysis"]["method"] = "unknown"
        self.assert_rejected("ar", record, ("analysis", "method"), "const")

    def test_blank_text_and_null_containers_are_rejected(self):
        fields = {
            "module": [("description",), ("responsibilities", 0), ("owned_state", 0),
                       ("scope", "includes", 0), ("scope", "excludes", 0), ("design_limits", 0)],
            "interface": [("description",), ("operations", 0, "purpose"),
                          ("operations", 0, "inputs", 0), ("operations", 0, "outputs", 0),
                          ("operations", 0, "preconditions", 0), ("operations", 0, "behavior", 0),
                          ("operations", 0, "failure_behavior", 0, "condition"),
                          ("operations", 0, "failure_behavior", 0, "outcome"),
                          ("consistency_rules", 0), ("compatibility_rules", 0)],
            "ar": [("statement",), ("acceptance_criteria", 0), ("assumptions", 0),
                   ("constraints", 0), ("analysis", "what", "problem"),
                   ("analysis", "what", "desired_outcome"), ("analysis", "why", "rationale"),
                   ("analysis", "who", "stakeholders", 0), ("analysis", "when", "conditions", 0),
                   ("analysis", "where", "contexts", 0), ("analysis", "how", "approach"),
                   ("analysis", "how_much", "scope")],
        }
        for kind, paths in fields.items():
            paths += [("title",)] + [("sources", 0, name) for name in ("source", "locator", "basis")]
            for path in paths:
                for value, error in ((" \t\n", "pattern"), (None, "type")):
                    with self.subTest(kind=kind, path=path, value=value):
                        record = self.valid_fixture(kind, populated=True)
                        at_path(record, path[:-1])[path[-1]] = value
                        self.assert_rejected(kind, record, path, error)
            containers = {
                "module": [("scope",), ("owned_state",)],
                "interface": [("operations",), ("operations", 0),
                              ("operations", 0, "failure_behavior", 0)],
                "ar": [("analysis",), ("analysis", "what"), ("assumptions",)],
            }[kind]
            for path in [(), ("sources",), ("sources", 0)] + containers:
                with self.subTest(kind=kind, null_container=path):
                    record = self.valid_fixture(kind, populated=True)
                    if path:
                        at_path(record, path[:-1])[path[-1]] = None
                    else:
                        record = None
                    self.assert_rejected(kind, record, path, "type")

    def test_required_collections_are_nonempty(self):
        fields = {
            "module": [("responsibilities",), ("scope", "includes"), ("design_limits",)],
            "interface": [("operations",), ("operations", 0, "inputs"),
                          ("operations", 0, "outputs"), ("operations", 0, "behavior"),
                          ("consistency_rules",), ("compatibility_rules",)],
            "ar": [("acceptance_criteria",), ("analysis", "who", "stakeholders"),
                   ("analysis", "when", "conditions"), ("analysis", "where", "contexts")],
        }
        for kind, paths in fields.items():
            for path in paths + [("sources",)]:
                with self.subTest(kind=kind, empty=path):
                    record = self.valid_fixture(kind)
                    at_path(record, path[:-1])[path[-1]] = []
                    self.assert_rejected(kind, record, path, "minItems")

    def test_stable_ids_and_operation_names_reject_malformed_values(self):
        for kind, prefix in KINDS.items():
            for value, error in (("SR-1", "pattern"), (f"{prefix}-", "pattern"),
                                 (f"{prefix}-１", "pattern"), (f"{prefix}-1\n", "not")):
                with self.subTest(kind=kind, identity=repr(value)):
                    record = self.valid_fixture(kind)
                    record["id"] = value
                    self.assert_rejected(kind, record, ("id",), error)
        for name, error in (("retainDefinition", "pattern"), ("retain__definition", "pattern"),
                            ("1_retain", "pattern"), ("retain_definition\n", "not")):
            with self.subTest(operation=name):
                record = self.valid_fixture("interface")
                record["operations"][0]["name"] = name
                self.assert_rejected("interface", record, ("operations", 0, "name"), error)

    def test_relationships_reject_wrong_targets_duplicate_links_and_multiple_owners(self):
        for kind, field, target, wrong in (("module", "provides", "IF-1", "MOD-1"),
                                           ("module", "consumes", "IF-1", "FUNC-1"),
                                           ("interface", "exposed_through", "MOD-1", "IF-1"),
                                           ("ar", "constrains", "FUNC-1", "FEAT-1")):
            for value, path, error in (([wrong], (field, 0), "pattern"),
                                       ([target + "\n"], (field, 0), "not"),
                                       ([target, target], (field,), "uniqueItems"),
                                       ([None], (field, 0), "type"), (target, (field,), "type")):
                with self.subTest(kind=kind, field=field, value=value):
                    record = self.valid_fixture(kind)
                    record[field] = value
                    self.assert_rejected(kind, record, path, error)
        for value, error in (("FUNC-1", "pattern"), (["MOD-1", "MOD-2"], "type"),
                             ("MOD-1\n", "not"), (None, "type")):
            with self.subTest(allocation=value):
                record = self.valid_fixture("ar")
                record["allocated_to"] = value
                self.assert_rejected("ar", record, ("allocated_to",), error)
        record = self.valid_fixture("interface")
        record["exposed_through"] = []
        self.assert_rejected("interface", record, ("exposed_through",), "minItems")

    def test_reverse_links_parent_copies_and_camelcase_aliases_are_rejected(self):
        fields = {
            "module": ("functions", "allocated_requirements", "provided_by", "ownedState",
                       "parent_module", "children"),
            "interface": ("provider", "consumers", "provided_by", "compatibilityRules",
                          "exposedThrough"),
            "ar": ("parent_id", "sr_id", "confirms", "allocatedTo", "unallocated_reason"),
        }
        for kind, names in fields.items():
            for name in names:
                with self.subTest(kind=kind, field=name):
                    record = self.valid_fixture(kind)
                    record[name] = "unsupported"
                    self.assert_rejected(kind, record, (), "additionalProperties")

    def test_only_ar_allows_one_optional_consequential_question(self):
        for kind in ("module", "interface"):
            for questions in ([], ["What retention duration is required?"]):
                with self.subTest(kind=kind, questions=questions):
                    record = self.valid_fixture(kind)
                    record["open_questions"] = questions
                    self.assert_rejected(kind, record, (), "additionalProperties")
        for questions, path, error in (([], ("open_questions",), "minItems"),
                                       (["What duration?", "What scale?"], ("open_questions",), "maxItems"),
                                       ([" \t"], ("open_questions", 0), "pattern"),
                                       (None, ("open_questions",), "type")):
            with self.subTest(questions=questions):
                record = self.valid_fixture("ar")
                record["open_questions"] = questions
                self.assert_rejected("ar", record, path, error)

    def test_logical_records_reject_legacy_inline_realization(self):
        for kind, facet in (("module", "software"), ("interface", "interaction")):
            with self.subTest(kind=kind):
                record = self.valid_fixture(kind)
                record["realization"] = realization_fixture(facet)
                self.assert_rejected(kind, record, (), "additionalProperties")

    def test_realization_facets_can_record_partial_observation_choice_or_deferral(self):
        for facet in set.union(*FACETS.values()):
            Draft202012Validator.check_schema(self.schemas[facet])
            complete = realization_fixture(facet)
            for fields in (tuple(complete), ("observed",), ("proposed",), ("deferred",)):
                with self.subTest(facet=facet, fields=fields):
                    record = {key: complete[key] for key in fields}
                    self.assert_valid(facet, record)
        for field in ("mechanism", "addressing", "failure_compatibility"):
            with self.subTest(interaction_field=field):
                record = realization_fixture("interaction")
                del record["observed"]["bindings"]
                record["observed"][field] = ["The caller uses the selected local store."]
                self.assert_valid("interaction", record)

    def test_realization_observations_need_both_attribution_and_content(self):
        for facet in set.union(*FACETS.values()):
            for missing in realization_fixture(facet)["observed"]:
                with self.subTest(facet=facet, missing=missing):
                    record = realization_fixture(facet)
                    self.assert_valid(facet, record)
                    del record["observed"][missing]
                    self.assert_rejected(facet, record, ("observed",),
                                         "required" if missing == "sources" else "minProperties")

    def test_test_groups_are_attributed_and_separate_from_implementation_or_results(self):
        record = test_group_fixture()
        self.assert_valid("software", record)
        group = record["observed"]["test_groups"][0]
        group["fixtures"] = []
        group["execution"]["selection"] = []
        group["required_artifacts"] = []
        self.assert_valid("software", record)
        del record["observed"]["sources"]
        self.assert_rejected("software", record, ("observed",), "required")
        for location in (("observed", "test_groups", 0),
                         ("observed", "test_groups", 0, "execution")):
            for field in ("result", "evidence", "implements", "allocated_to"):
                with self.subTest(location=location, field=field):
                    invalid = test_group_fixture()
                    at_path(invalid, location)[field] = "passed"
                    self.assert_rejected("software", invalid, location, "additionalProperties")

    def test_test_group_members_and_reference_roles_are_required(self):
        group = ("observed", "test_groups", 0)
        locations = [group, group + ("execution",), group + ("test_sources", 0),
                     group + ("fixtures", 0)]
        locations += [group + ("execution", kind, 0)
                      for kind in ("selection", "runners", "entrypoints")]
        for location in locations:
            for field in at_path(test_group_fixture(), location):
                with self.subTest(location=location, missing=field):
                    invalid = test_group_fixture()
                    del at_path(invalid, location)[field]
                    self.assert_rejected("software", invalid, location, "required")
            with self.subTest(location=location, unknown="module"):
                invalid = test_group_fixture()
                at_path(invalid, location)["module"] = "MOD-7"
                self.assert_rejected("software", invalid, location, "additionalProperties")
        for location in (("observed", "test_groups"), group + ("test_sources",),
                         group + ("limits",), group + ("execution", "runners"),
                         group + ("execution", "entrypoints")):
            with self.subTest(empty=location):
                invalid = test_group_fixture()
                at_path(invalid, location[:-1])[location[-1]] = []
                self.assert_rejected("software", invalid, location, "minItems")

    def test_test_group_text_and_owner_contracts_remain_meaningful(self):
        group = ("observed", "test_groups", 0)
        locations = [group + (field,) for field in ("name", "contract", "observation_boundary")]
        locations += [group + ("limits", 0), group + ("required_artifacts", 0),
                      group + ("execution", "owner_contract")]
        references = [group + ("test_sources", 0), group + ("fixtures", 0)]
        references += [group + ("execution", kind, 0) for kind in ("selection", "runners", "entrypoints")]
        locations += [location + (field,) for location in references for field in ("path", "role")]
        for location in locations:
            with self.subTest(blank=location):
                invalid = test_group_fixture()
                at_path(invalid, location[:-1])[location[-1]] = " \t\n"
                self.assert_rejected("software", invalid, location, "pattern")
        for location in (group + ("contract",), group + ("execution", "owner_contract")):
            for value in ("docs/design/model.json", "docs/design/model.md#", "docs/design/model.md#one#two"):
                with self.subTest(contract=location, value=value):
                    invalid = test_group_fixture()
                    at_path(invalid, location[:-1])[location[-1]] = value
                    self.assert_rejected("software", invalid, location, "pattern")

    def test_production_mapping_requires_attributed_inputs_transformation_and_outputs(self):
        record = {"observed": {
            "sources": realization_fixture("software")["observed"]["sources"],
            "production_paths": [{
                "name": "Build a candidate package",
                "inputs": [{"path": "src/", "role": "Canonical implementation sources."}],
                "transformation": {"path": "scripts/build.py", "description": "Build in a selected isolated output root."},
                "outputs": [{"path": "<candidate>/package.tgz", "role": "Candidate-relative artifact layout; no build is claimed."}],
            }],
        }}
        self.assert_valid("software", record)
        for field in ("inputs", "transformation", "outputs"):
            with self.subTest(missing=field):
                invalid = deepcopy(record)
                del invalid["observed"]["production_paths"][0][field]
                self.assert_rejected("software", invalid, ("observed", "production_paths", 0), "required")
        for field in ("inputs", "outputs"):
            with self.subTest(empty=field):
                invalid = deepcopy(record)
                invalid["observed"]["production_paths"][0][field] = []
                self.assert_rejected("software", invalid, ("observed", "production_paths", 0, field), "minItems")
        invalid = deepcopy(record)
        del invalid["observed"]["sources"]
        self.assert_rejected("software", invalid, ("observed",), "required")
        for field in ("inputs", "outputs"):
            with self.subTest(undeclared=field):
                invalid = deepcopy(record)
                invalid["observed"]["production_paths"][0][field][0]["module"] = "MOD-1"
                self.assert_rejected("software", invalid, ("observed", "production_paths", 0, field, 0), "additionalProperties")
        invalid = deepcopy(record)
        invalid["observed"]["production_paths"][0]["transformation"]["language"] = "unknown"
        self.assert_rejected("software", invalid, ("observed", "production_paths", 0, "transformation"), "additionalProperties")

    def test_physical_facts_require_closed_scoped_references_and_observation_basis(self):
        for field in ("physical_bindings", "production_placement", "location_constraints", "artifact_acquisition"):
            kind, record = physical_fixture(field)
            with self.subTest(field=field):
                self.assert_valid(kind, record)
                prefix = ("observed", field, 0) if isinstance(record["observed"][field], list) else ("observed", field)
                for name in at_path(record, prefix):
                    invalid = deepcopy(record)
                    del at_path(invalid, prefix)[name]
                    self.assert_rejected(kind, invalid, prefix, "required")
                invalid = deepcopy(record)
                at_path(invalid, prefix)["host_identity"] = "invented-host"
                self.assert_rejected(kind, invalid, prefix, "additionalProperties")
                invalid = deepcopy(record)
                del invalid["observed"]["sources"]
                self.assert_rejected(kind, invalid, ("observed",), "required")
        kind, record = physical_fixture("physical_bindings")
        for path in (("observed", "physical_bindings", 0, "execution"),
                     ("observed", "physical_bindings", 0, "package"),
                     ("observed", "physical_bindings", 0, "accesses", 0),
                     ("observed", "physical_bindings", 0, "accesses", 0, "placement")):
            invalid = deepcopy(record)
            at_path(invalid, path)["unknown"] = "unrecognized"
            self.assert_rejected(kind, invalid, path, "additionalProperties")
        record["observed"]["physical_bindings"][0]["accesses"] = []
        self.assert_valid(kind, record)

    def test_physical_closed_vocabularies_reject_unknown_access_relation_and_reference_facet(self):
        for field, suffix, value in (
            ("physical_bindings", (0, "accesses", 0, "mode"), "execute"),
            ("location_constraints", (0, "relation"), "same-host"),
            ("production_placement", ("output", "facet"), "runtime"),
        ):
            with self.subTest(field=field, value=value):
                kind, record = physical_fixture(field)
                prefix = ("observed", field, *suffix)
                at_path(record, prefix[:-1])[prefix[-1]] = value
                self.assert_rejected(kind, record, prefix, "enum")

    def test_acquisition_sources_and_location_pairs_keep_complete_conditions(self):
        kind, record = physical_fixture("artifact_acquisition")
        source = ("observed", "artifact_acquisition", "sources", 0)
        for field in ("name", "transport", "address", "conditions"):
            invalid = deepcopy(record)
            del at_path(invalid, source)[field]
            self.assert_rejected(kind, invalid, source, "required")
        invalid = deepcopy(record)
        at_path(invalid, source)["conditions"] = []
        self.assert_rejected(kind, invalid, (*source, "conditions"), "minItems")
        invalid = deepcopy(record)
        at_path(invalid, source)["availability"] = "published"
        self.assert_rejected(kind, invalid, source, "additionalProperties")
        kind, record = physical_fixture("location_constraints")
        path = ("observed", "location_constraints", 0, "placements")
        invalid = deepcopy(record)
        at_path(invalid, path).pop()
        self.assert_rejected(kind, invalid, path, "minItems")
        invalid = deepcopy(record)
        at_path(invalid, path).append({"owner": "MOD-2", "facet": "persistence", "name": "Third place"})
        self.assert_rejected(kind, invalid, path, "maxItems")
        invalid = deepcopy(record)
        at_path(invalid, path)[1] = deepcopy(at_path(invalid, path)[0])
        self.assert_rejected(kind, invalid, path, "uniqueItems")

    def test_process_interaction_shape_preserves_terminal_branches_and_observation_basis(self):
        record = process_fixture("interaction")
        self.assert_valid("interaction", record)
        prefix = ("observed", "sequences", 0)
        boundaries = [prefix, (*prefix, "steps", 0), (*prefix, "steps", 0, "branches", 0),
                      (*prefix, "steps", 0, "branches", 0, "steps", 0), (*prefix, "failures", 0)]
        for path in boundaries:
            with self.subTest(unknown_at=path):
                invalid = deepcopy(record)
                at_path(invalid, path)["invented_transition"] = "other-step"
                self.assert_rejected("interaction", invalid, path, "additionalProperties")
        for field in ("operation", "outcome", "participants", "preconditions", "steps", "failures", "constraints"):
            with self.subTest(missing=field):
                invalid = deepcopy(record)
                del at_path(invalid, prefix)[field]
                self.assert_rejected("interaction", invalid, prefix, "required")
        invalid = deepcopy(record)
        at_path(invalid, (*prefix, "steps", 0, "branches", 0))["steps"] = []
        self.assert_rejected("interaction", invalid, (*prefix, "steps", 0, "branches", 0, "steps"), "minItems")
        invalid = deepcopy(record)
        at_path(invalid, (*prefix, "steps", 0))["participant"] = "IF-1"
        self.assert_rejected("interaction", invalid, (*prefix, "steps", 0, "participant"), "pattern")
        invalid = deepcopy(record)
        del invalid["observed"]["sources"]
        self.assert_rejected("interaction", invalid, ("observed",), "required")

    def test_process_lifecycle_requires_state_meanings_and_guarded_transition_effects(self):
        record = process_fixture("runtime")
        self.assert_valid("runtime", record)
        prefix = ("observed", "lifecycles", 0)
        for path in (prefix, (*prefix, "states", 0), (*prefix, "transitions", 0)):
            with self.subTest(unknown_at=path):
                invalid = deepcopy(record)
                at_path(invalid, path)["automatic_retry"] = True
                self.assert_rejected("runtime", invalid, path, "additionalProperties")
        for field in ("from", "to", "trigger", "guards", "effects"):
            with self.subTest(missing=field):
                invalid = deepcopy(record)
                del at_path(invalid, (*prefix, "transitions", 0))[field]
                self.assert_rejected("runtime", invalid, (*prefix, "transitions", 0), "required")
        for field in ("guards", "effects"):
            with self.subTest(empty=field):
                invalid = deepcopy(record)
                at_path(invalid, (*prefix, "transitions", 0))[field] = []
                self.assert_rejected("runtime", invalid, (*prefix, "transitions", 0, field), "minItems")
        invalid = deepcopy(record)
        at_path(invalid, (*prefix, "states", 0))["meaning"] = "  "
        self.assert_rejected("runtime", invalid, (*prefix, "states", 0, "meaning"), "pattern")

    def test_execution_facts_require_a_closed_attributed_process_and_typed_bindings(self):
        record = {"observed": {
            "sources": realization_fixture("runtime")["observed"]["sources"],
            "execution": {
                "name": "Selected command process", "environment": "Node.js",
                "modules": ["MOD-1", "MOD-2"], "entry_interfaces": ["IF-1"],
                "calls": [{"caller": "MOD-1", "callee": "MOD-2", "interface": "IF-2"}],
                "constraints": ["Calls occur only for the selected request; this is not a sequence."],
            },
        }}
        self.assert_valid("runtime", record)
        for field in record["observed"]["execution"]:
            with self.subTest(missing=field):
                invalid = deepcopy(record)
                del invalid["observed"]["execution"][field]
                self.assert_rejected("runtime", invalid, ("observed", "execution"), "required")
        for field in ("modules", "entry_interfaces", "constraints"):
            with self.subTest(empty=field):
                invalid = deepcopy(record)
                invalid["observed"]["execution"][field] = []
                self.assert_rejected("runtime", invalid, ("observed", "execution", field), "minItems")
        for path in (("observed", "execution"), ("observed", "execution", "calls", 0)):
            with self.subTest(unknown_at=path):
                invalid = deepcopy(record)
                at_path(invalid, path)["unknown"] = "unsupported"
                self.assert_rejected("runtime", invalid, path, "additionalProperties")
        for field in ("caller", "callee", "interface"):
            with self.subTest(missing_binding=field):
                invalid = deepcopy(record)
                del invalid["observed"]["execution"]["calls"][0][field]
                self.assert_rejected("runtime", invalid, ("observed", "execution", "calls", 0), "required")
        for path, value, error in (
            (("modules", 0), "IF-1", "pattern"),
            (("entry_interfaces", 0), "MOD-1", "pattern"),
            (("calls", 0, "caller"), "IF-1", "pattern"),
            (("calls", 0, "callee"), "FUNC-1", "pattern"),
            (("calls", 0, "interface"), "MOD-1", "pattern"),
            (("calls", 0, "interface"), "IF-1\n", "not"),
            (("constraints", 0), " \n", "pattern"),
            (("environment",), " \t", "pattern"),
        ):
            with self.subTest(path=path, value=value):
                invalid = deepcopy(record)
                at_path(invalid["observed"]["execution"], path[:-1])[path[-1]] = value
                self.assert_rejected("runtime", invalid, ("observed", "execution", *path), error)
        for field in ("modules", "entry_interfaces", "calls"):
            with self.subTest(duplicate=field):
                invalid = deepcopy(record)
                invalid["observed"]["execution"][field].append(deepcopy(invalid["observed"]["execution"][field][0]))
                self.assert_rejected("runtime", invalid, ("observed", "execution", field), "uniqueItems")
        independent = deepcopy(record)
        independent["observed"]["execution"]["calls"] = []
        self.assert_valid("runtime", independent)
        del independent["observed"]["sources"]
        self.assert_rejected("runtime", independent, ("observed",), "required")

    def test_placement_facts_require_scope_paths_constraints_and_typed_modules(self):
        for facet in ("deployment", "persistence"):
            record = {"observed": {
                "sources": realization_fixture(facet)["observed"]["sources"],
                "placements": [{
                    "name": "Selected local records", "location": "Invocation project",
                    "modules": ["MOD-1"], "paths": ["docs/changes/{change}/"],
                    "constraints": ["Declared placement only; no installed or durable outcome is claimed."],
                }],
            }}
            self.assert_valid(facet, record)
            for field in record["observed"]["placements"][0]:
                with self.subTest(facet=facet, missing=field):
                    invalid = deepcopy(record)
                    del invalid["observed"]["placements"][0][field]
                    self.assert_rejected(facet, invalid, ("observed", "placements", 0), "required")
            for field in ("modules", "paths", "constraints"):
                with self.subTest(facet=facet, empty=field):
                    invalid = deepcopy(record)
                    invalid["observed"]["placements"][0][field] = []
                    self.assert_rejected(facet, invalid, ("observed", "placements", 0, field), "minItems")
            for field in ("modules", "paths"):
                with self.subTest(facet=facet, duplicate=field):
                    invalid = deepcopy(record)
                    invalid["observed"]["placements"][0][field] *= 2
                    self.assert_rejected(facet, invalid, ("observed", "placements", 0, field), "uniqueItems")
            for path, value, error in (
                (("modules", 0), "IF-1", "pattern"),
                (("modules", 0), "MOD-1\n", "not"),
                (("paths", 0), " \n", "pattern"),
                (("location",), " \t", "pattern"),
            ):
                with self.subTest(facet=facet, path=path, value=value):
                    invalid = deepcopy(record)
                    at_path(invalid["observed"]["placements"][0], path[:-1])[path[-1]] = value
                    self.assert_rejected(facet, invalid, ("observed", "placements", 0, *path), error)
            invalid = deepcopy(record)
            invalid["observed"]["placements"][0]["unknown"] = "unsupported"
            self.assert_rejected(facet, invalid, ("observed", "placements", 0), "additionalProperties")
            invalid = deepcopy(record)
            invalid["observed"]["placements"] = []
            self.assert_rejected(facet, invalid, ("observed", "placements"), "minItems")
            del record["observed"]["sources"]
            self.assert_rejected(facet, record, ("observed",), "required")

    def test_realization_choices_need_reasoning_and_a_revisit_condition(self):
        for facet in set.union(*FACETS.values()):
            for field in ("choice", "rationale", "alternatives", "consequences", "revisit_when"):
                with self.subTest(facet=facet, missing=field):
                    record = realization_fixture(facet)
                    del record["proposed"][0][field]
                    self.assert_rejected(facet, record, ("proposed", 0), "required")

    def test_realization_rejects_empty_assertions_and_undeclared_entity_structure(self):
        for facet in set.union(*FACETS.values()):
            content = next(iter(realization_fixture(facet)["observed"]))
            item_path = ("observed", content, 0)
            if facet in ("software", "interaction"):
                item_path += ("path",)
            cases = [
                ((), {}, "minProperties"),
                (("observed", "sources"), [], "minItems"),
                (("observed", content), [], "minItems"),
                (item_path, " \n", "pattern"),
                (("proposed",), [], "minItems"),
                (("proposed", 0, "alternatives"), [], "minItems"),
                (("proposed", 0, "revisit_when", 0), " \n", "pattern"),
                (("deferred",), [], "minItems"),
                (("observed",), None, "type"),
            ]
            for path, value, validator in cases:
                with self.subTest(facet=facet, path=path):
                    record = realization_fixture(facet)
                    if path:
                        at_path(record, path[:-1])[path[-1]] = value
                    else:
                        record = value
                    self.assert_rejected(facet, record, path, validator)
            foreign_content = "runtime" if facet != "runtime" else "representation"
            objects = [((), field) for field in ("unknown", "id", "type", "status", "owner", "module_id")]
            objects += [(("observed",), foreign_content),
                        (("observed", "sources", 0), "unknown"), (("proposed", 0), "status")]
            if facet in ("software", "interaction"):
                objects.append((("observed", content, 0), "id"))
            for path, field in objects:
                with self.subTest(facet=facet, path=path, field=field):
                    record = realization_fixture(facet)
                    at_path(record, path)[field] = "unsupported"
                    self.assert_rejected(facet, record, path, "additionalProperties")

    def test_current_realization_facets_conform_and_observations_have_registered_sources(self):
        _, paths = architecture_paths(ROOT / "design/architecture")
        registered = set(re.findall(r"^## (SRC-[A-Z0-9-]+)$",
                                   (ROOT / "design/requirements/sources.md").read_text(), re.MULTILINE))
        self.assertTrue(registered)
        self.assertTrue(paths, "No current subordinate realization facets found")
        for path in paths:
            with self.subTest(path=str(path.relative_to(ROOT))):
                record = json.loads(path.read_text())
                self.assert_valid(path.stem, record)
                for source in record.get("observed", {}).get("sources", []):
                    self.assertIn(source["source"], registered)

    def test_public_entries_accept_open_groups_and_mapping_with_explicit_unmapped_scope(self):
        for facet in ("software", "interaction"):
            with self.subTest(facet=facet):
                record = public_entry_fixture(facet)
                self.assert_valid(facet, record)
                record["observed"]["public_entries"][0]["group"] = "Another meaningful group"
                mapping = record["proposed"][0]["public_entry_mappings"][0]
                mapping["functions"] = []
                self.assert_valid(facet, record)
                mapping["limits"] = []
                self.assert_rejected(facet, record, ("proposed", 0, "public_entry_mappings", 0), "anyOf")
                mapping["functions"] = public_entry_fixture(facet)["proposed"][0]["public_entry_mappings"][0]["functions"]
                self.assert_valid(facet, record)

    def test_public_catalog_fields_are_required_and_object_boundaries_are_closed(self):
        entry_path = ("observed", "public_entries", 0)
        mapping_path = ("proposed", 0, "public_entry_mappings", 0)
        for facet in ("software", "interaction"):
            for path in (entry_path, mapping_path, mapping_path + ("functions", 0)):
                for field in at_path(public_entry_fixture(facet), path):
                    with self.subTest(facet=facet, path=path, missing=field):
                        record = public_entry_fixture(facet)
                        del at_path(record, path)[field]
                        self.assert_rejected(facet, record, path, "required")
                with self.subTest(facet=facet, unknown_at=path):
                    record = public_entry_fixture(facet)
                    at_path(record, path)["unexpected"] = "unsupported"
                    self.assert_rejected(facet, record, path, "additionalProperties")
        record = public_entry_fixture("software")
        record["observed"]["public_entries"][0]["operation"] = "retain_definition"
        self.assert_rejected("software", record, entry_path, "additionalProperties")

    def test_public_catalog_rejects_blank_text_empty_catalogs_and_malformed_references(self):
        entry_path = ("observed", "public_entries", 0)
        mapping_path = ("proposed", 0, "public_entry_mappings", 0)
        for facet in ("software", "interaction"):
            fields = [entry_path + (name,) for name in at_path(public_entry_fixture(facet), entry_path)]
            fields += [mapping_path + ("entry",), mapping_path + ("limits", 0),
                       mapping_path + ("functions", 0, "contribution")]
            for path in fields:
                with self.subTest(facet=facet, blank=path):
                    record = public_entry_fixture(facet)
                    at_path(record, path[:-1])[path[-1]] = " \t"
                    self.assert_rejected(facet, record, path, "pattern")
            for path in (("observed", "public_entries"), ("proposed", 0, "public_entry_mappings")):
                with self.subTest(facet=facet, empty=path):
                    record = public_entry_fixture(facet)
                    at_path(record, path[:-1])[path[-1]] = []
                    self.assert_rejected(facet, record, path, "minItems")
            for value, error in (("FEAT-1", "pattern"), ("FUNC-１", "pattern"), ("FUNC-1\n", "not")):
                with self.subTest(facet=facet, function=value):
                    record = public_entry_fixture(facet)
                    path = mapping_path + ("functions", 0, "function")
                    at_path(record, path[:-1])[path[-1]] = value
                    self.assert_rejected(facet, record, path, error)
            for contract in ("docs/definitions.json", "docs/definitions.md#", "docs/definitions.md#a#b"):
                with self.subTest(facet=facet, contract=contract):
                    record = public_entry_fixture(facet)
                    record["observed"]["public_entries"][0]["contract"] = contract
                    self.assert_rejected(facet, record, entry_path + ("contract",), "pattern")

    def test_public_function_relations_reject_unknown_vocabulary_before_references(self):
        for facet in ("software", "interaction"):
            with self.subTest(facet=facet):
                record = public_entry_fixture(facet)
                binding = record["proposed"][0]["public_entry_mappings"][0]["functions"][0]
                binding["relation"] = "implements"
                self.assert_rejected(facet, record,
                                     ("proposed", 0, "public_entry_mappings", 0, "functions", 0, "relation"),
                                     "enum")
                # The nonexistent source and entity cannot mask the vocabulary error.
                with self.assertRaises(ValidationError) as rejected:
                    validate_public_entries(ROOT, architecture_fixture("interface"), record, {}, self.validators[facet])
                self.assertEqual(rejected.exception.validator, "enum")


class ArchitectureDirectoryTests(unittest.TestCase):
    def make_layout(self, root):
        """Independent owner names make directory checks observable in fixtures."""
        module = root / "modules/MOD-1-retain-engineering-definitions/module.json"
        interface = root / "interfaces/IF-1-retain-engineering-definitions/interface.json"
        for kind, path in (("module", module), ("interface", interface)):
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(architecture_fixture(kind)))
        return module, interface

    def write_facet(self, owner, name, facet):
        path = owner.parent / "realization" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(realization_fixture(facet)))
        return path

    def test_discovery_keeps_subordinate_facets_out_of_entity_population(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            module, interface = self.make_layout(root)
            software = self.write_facet(module, "software.json", "software")
            technology = self.write_facet(interface, "technology.json", "technology")
            records, facets = architecture_paths(root)
            self.assertEqual(set(records), {module, interface})
            self.assertEqual(set(facets), {software, technology})
            self.assertTrue(all("id" not in json.loads(path.read_text()) for path in facets))

    def test_nested_discovery_derives_each_single_parent_and_preserves_facet_owner(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            paths = hierarchy_fixture(root)
            software = self.write_facet(paths["MOD-3"], "software.json", "software")

            records, facets = architecture_paths(root)

            self.assertEqual(set(records), set(paths.values()))
            self.assertEqual(facets, [software])
            self.assertEqual(module_parent_ids([
                (path, json.loads(path.read_text())) for path in records
            ]), {
                "MOD-1": None, "MOD-2": "MOD-1", "MOD-3": "MOD-2",
                "MOD-4": "MOD-2", "MOD-5": "MOD-1", "MOD-6": None,
                "MOD-7": "MOD-6",
            })

    def test_unowned_misplaced_and_unknown_json_are_rejected_instead_of_skipped(self):
        cases = (
            ("flat", "modules/MOD-2-retired.json", "Unexpected architecture JSON path"),
            ("orphan", "modules/MOD-2-orphan/realization/software.json", "Missing logical owner"),
            ("nested", "modules/MOD-1-retain-engineering-definitions/realization/nested/software.json",
             "Unexpected architecture JSON path"),
            ("misplaced", "modules/MOD-1-retain-engineering-definitions/software.json",
             "Unexpected architecture JSON path"),
            ("unknown", "modules/MOD-1-retain-engineering-definitions/realization/unknown.json",
             "Unsupported module realization facet"),
            ("module_interaction", "modules/MOD-1-retain-engineering-definitions/realization/interaction.json",
             "Unsupported module realization facet"),
            ("interface_software", "interfaces/IF-1-retain-engineering-definitions/realization/software.json",
             "Unsupported interface realization facet"),
            ("nested_orphan", "modules/MOD-1-retain-engineering-definitions/modules/"
             "MOD-2-orphan/realization/software.json", "Missing logical owner"),
            ("wrong_child_collection", "modules/MOD-1-retain-engineering-definitions/children/"
             "MOD-2-child/module.json", "Unexpected architecture JSON path"),
            ("nested_interface", "interfaces/IF-1-retain-engineering-definitions/interfaces/"
             "IF-2-child/interface.json", "Unexpected architecture JSON path"),
            ("unregistered_catalog", "modules/MOD-1-retain-engineering-definitions/test-design/cases/unregistered.json", "Unexpected architecture JSON path"),
            ("unowned_root_json", "unowned.json", "Unexpected architecture JSON path"),
        )
        for name, relative, reason in cases:
            with self.subTest(case=name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.make_layout(root)
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(realization_fixture("software")))
                with self.assertRaisesRegex(ValueError, reason):
                    architecture_paths(root)

    def test_duplicate_nested_identity_and_symlink_cycles_are_rejected(self):
        for case, reason in (("duplicate", "Duplicate architecture identity"),
                             ("symlink_cycle", "Architecture symlinks are not supported")):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                module, _ = self.make_layout(root)
                children = module.parent / "modules"
                children.mkdir()
                duplicate = children / module.parent.name
                if case == "duplicate":
                    duplicate.mkdir()
                    (duplicate / "module.json").write_bytes(module.read_bytes())
                else:
                    duplicate.symlink_to(module.parent, target_is_directory=True)
                with self.assertRaisesRegex(ValueError, reason):
                    architecture_paths(root)

    def test_module_title_refinement_preserves_parent_child_and_facet_paths(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            module, interface = self.make_layout(root)
            child = module.parent / "modules/MOD-2-child/module.json"
            child.parent.mkdir(parents=True)
            child_record = architecture_fixture("module")
            child_record.update(id="MOD-2", title="Refined child responsibility")
            child.write_text(json.dumps(child_record))
            record = json.loads(module.read_text())
            record["title"] = "Refined parent responsibility"
            module.write_text(json.dumps(record))
            facet = self.write_facet(module, "runtime.json", "runtime")
            records, facets = architecture_paths(root)
            self.assertEqual(set(records), {module, child, interface})
            self.assertEqual(facets, [facet])

    def test_owner_name_record_name_and_kind_must_match_the_declared_profile(self):
        for case, reason in (("directory", "Owner directory does not match identity and retained slug"),
                             ("empty_slug", "Owner directory does not match identity and retained slug"),
                             ("malformed_slug", "Owner directory does not match identity and retained slug"),
                             ("interface_title", "Owner directory does not match identity and title"),
                             ("filename", "Missing logical owner"),
                             ("kind", "Wrong logical owner type"),
                             ("nonobject", "Wrong logical owner type"),
                             ("missing_title", "Invalid logical owner identity or title")):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                module, interface = self.make_layout(root)
                if case in ("directory", "empty_slug", "malformed_slug"):
                    target = {"directory":"MOD-2-retain-engineering-definitions", "empty_slug":"MOD-1-", "malformed_slug":"MOD-1-bad--slug"}[case]
                    module.parent.rename(module.parent.with_name(target))
                elif case == "interface_title":
                    record = json.loads(interface.read_text())
                    record["title"] = "Changed Interface contract"
                    interface.write_text(json.dumps(record))
                elif case == "filename":
                    module.rename(module.with_name("definition.json"))
                elif case == "nonobject":
                    module.write_text("[]")
                else:
                    record = json.loads(module.read_text())
                    if case == "missing_title":
                        del record["title"]
                    else:
                        record["type"] = "interface"
                    module.write_text(json.dumps(record))
                with self.assertRaisesRegex(ValueError, reason):
                    architecture_paths(root)


class CurrentArchitectureConnectionsTests(unittest.TestCase):
    def test_current_exposure_resolves_and_respects_provider_containment(self):
        paths, _ = architecture_paths(ROOT / "design/architecture")
        validate_interface_exposure([(path, json.loads(path.read_text())) for path in paths])

    def test_pilot_interfaces_have_unambiguous_providers_consumers_and_operation_names(self):
        records, _ = architecture_paths(ROOT / "design/architecture")
        modules = [json.loads(path.read_text()) for path in records if path.name == "module.json"]
        interfaces = [json.loads(path.read_text()) for path in records if path.name == "interface.json"]
        self.assertTrue(interfaces, "No pilot Interfaces found")
        for interface in interfaces:
            with self.subTest(interface=interface["id"]):
                providers = [m["id"] for m in modules if interface["id"] in m["provides"]]
                consumers = [m["id"] for m in modules if interface["id"] in m["consumes"]]
                self.assertEqual(len(providers), 1, f"Providers: {providers}")
                self.assertTrue(consumers, "No consumer for the pilot contract")
                names = [operation["name"] for operation in interface["operations"]]
                self.assertEqual(len(names), len(set(names)), "Operation names must be unique")


class PublicEntryConnectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validators = {
            facet: Draft202012Validator(json.loads(
                (ROOT / "design/support/schemas/realization" / f"{facet}.schema.json").read_text()
            )) for facet in ("software", "interaction")
        }

    def fixture(self, facet="interaction"):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        record = public_entry_fixture(facet)
        entry = record["observed"]["public_entries"][0]
        for relative in (entry["source_path"], entry["contract"].partition("#")[0]):
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()
        owner = architecture_fixture("interface" if facet == "interaction" else "module")
        entities = {"FUNC-1": {"id": "FUNC-1", "type": "function"}}
        return root, owner, record, entities

    def test_current_catalogs_have_complete_typed_source_and_operation_correspondence(self):
        paths, facets = architecture_paths(ROOT / "design/architecture")
        records = {path: json.loads(path.read_text()) for path in paths}
        entities = {record["id"]: record for record in records.values()}
        for path in (ROOT / "design/system/functions").glob("FUNC-*.json"):
            function = json.loads(path.read_text())
            entities[function["id"]] = function
        catalogs = set()
        for path in facets:
            if path.stem not in self.validators:
                continue
            owner_path = next(candidate for candidate in paths if candidate.parent == path.parent.parent)
            record = json.loads(path.read_text())
            with self.subTest(facet=str(path.relative_to(ROOT))):
                validate_public_entries(ROOT, records[owner_path], record, entities, self.validators[path.stem])
                if "public_entries" in record.get("observed", {}):
                    catalogs.add(records[owner_path]["id"])
        self.assertEqual(catalogs, {"IF-004", "MOD-012"})

    def test_optional_catalogs_and_explicit_mapping_limits_remain_valid(self):
        for facet in ("software", "interaction"):
            with self.subTest(facet=facet):
                root, owner, record, entities = self.fixture(facet)
                validate_public_entries(root, owner, realization_fixture(facet), entities, self.validators[facet])
                validate_public_entries(root, owner, record, entities, self.validators[facet])
                mapping = record["proposed"][0]["public_entry_mappings"][0]
                mapping["functions"] = []
                validate_public_entries(root, owner, record, entities, self.validators[facet])

    def test_duplicate_observed_names_and_cross_proposal_mappings_are_rejected(self):
        for case, reason in (("name", "Duplicate public entry name"),
                             ("mapping", "Duplicate public entry mapping")):
            with self.subTest(case=case):
                root, owner, record, entities = self.fixture()
                if case == "name":
                    entry = dict(record["observed"]["public_entries"][0])
                    entry["purpose"] = "A conflicting account of the same public name."
                    record["observed"]["public_entries"].append(entry)
                else:
                    record["proposed"].append(public_entry_fixture("interaction")["proposed"][0])
                with self.assertRaisesRegex(ValueError, reason):
                    validate_public_entries(root, owner, record, entities, self.validators["interaction"])

    def test_extra_or_missing_correspondence_cannot_hide_an_observed_entry(self):
        for case in ("extra", "missing"):
            with self.subTest(case=case):
                root, owner, record, entities = self.fixture()
                if case == "extra":
                    mapping = public_entry_fixture("interaction")["proposed"][0]["public_entry_mappings"][0]
                    mapping["entry"] = "another command"
                    record["proposed"][0]["public_entry_mappings"].append(mapping)
                else:
                    del record["proposed"][0]["public_entry_mappings"]
                with self.assertRaisesRegex(ValueError, "must match the observed names exactly"):
                    validate_public_entries(root, owner, record, entities, self.validators["interaction"])

    def test_function_links_reject_missing_wrong_type_and_duplicate_relation_targets(self):
        for case, reason in (("missing", "Missing public entry Function"),
                             ("wrong_type", "Wrong-type public entry Function"),
                             ("duplicate", "Duplicate public entry Function relation")):
            with self.subTest(case=case):
                root, owner, record, entities = self.fixture()
                bindings = record["proposed"][0]["public_entry_mappings"][0]["functions"]
                if case == "missing":
                    del entities["FUNC-1"]
                elif case == "wrong_type":
                    entities["FUNC-1"]["type"] = "feature"
                else:
                    duplicate = dict(bindings[0])
                    duplicate["contribution"] = "Different prose cannot duplicate the same typed link."
                    bindings.append(duplicate)
                with self.assertRaisesRegex(ValueError, reason):
                    validate_public_entries(root, owner, record, entities, self.validators["interaction"])
        root, owner, record, entities = self.fixture()
        bindings = record["proposed"][0]["public_entry_mappings"][0]["functions"]
        bindings.append({**bindings[0], "relation": "guides"})
        validate_public_entries(root, owner, record, entities, self.validators["interaction"])

    def test_source_and_contract_paths_reject_aliases_missing_files_and_escaped_targets(self):
        cases = (
            ("source_path", "../outside.js", "exact repository-relative"),
            ("source_path", "/tmp/outside.js", "exact repository-relative"),
            ("source_path", "src/./definitions.js", "exact repository-relative"),
            ("source_path", "src//definitions.js", "exact repository-relative"),
            ("source_path", "src/definitions.js#call", "exact repository-relative"),
            ("source_path", "src/missing.js", "Missing public entry file"),
            ("contract", "../outside.md#meaning", "exact repository-relative"),
            ("contract", "https://example.test/contract.md", "exact repository-relative"),
            ("contract", "docs/missing.md#meaning", "Missing public entry file"),
            ("contract", "docs/alias.md#meaning", "escapes the repository"),
        )
        for field, value, reason in cases:
            with self.subTest(field=field, path=value):
                root, owner, record, entities = self.fixture()
                if value == "docs/alias.md#meaning":
                    (root / "docs/alias.md").symlink_to(ROOT / "README.md")
                record["observed"]["public_entries"][0][field] = value
                with self.assertRaisesRegex(ValueError, reason):
                    validate_public_entries(root, owner, record, entities, self.validators["interaction"])

    def test_command_operation_must_belong_to_the_owning_interface(self):
        for case, reason in (("unknown", "Unknown public entry operation"),
                             ("wrong_owner", "require an Interface owner")):
            with self.subTest(case=case):
                root, owner, record, entities = self.fixture()
                if case == "unknown":
                    record["observed"]["public_entries"][0]["operation"] = "missing_operation"
                else:
                    owner = architecture_fixture("module")
                with self.assertRaisesRegex(ValueError, reason):
                    validate_public_entries(root, owner, record, entities, self.validators["interaction"])


class InterfaceExposureTests(unittest.TestCase):
    def records(self, root, consumer="MOD-4", exposure=None):
        hierarchy_fixture(root, consumer=consumer, exposure=exposure)
        paths, _ = architecture_paths(root)
        return [(path, json.loads(path.read_text())) for path in paths]

    def test_exposure_covers_crossed_provider_boundaries_only(self):
        cases = (
            ("sibling_internal", "MOD-4", None),
            ("containing_parent", "MOD-2", None),
            ("cousin", "MOD-5", ["MOD-2"]),
            ("different_tree", "MOD-7", ["MOD-2", "MOD-1"]),
            ("external_actor", None, ["MOD-2", "MOD-1"]),
        )
        for name, consumer, exposure in cases:
            with self.subTest(case=name), tempfile.TemporaryDirectory() as temporary:
                records = self.records(Path(temporary), consumer, exposure)
                validate_interface_exposure(records)
                providers = [record["id"] for _, record in records
                             if record["type"] == "module" and "IF-1" in record["provides"]]
                self.assertEqual(providers, ["MOD-3"])

    def test_exposure_rejects_unknown_wrong_type_and_nonancestor_targets(self):
        for target, reason in (
            ("MOD-999", "Missing exposure target"),
            ("IF-1", "Wrong-type exposure target"),
            ("MOD-3", "not a strict provider ancestor"),
            ("MOD-4", "not a strict provider ancestor"),
            ("MOD-6", "not a strict provider ancestor"),
        ):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as temporary:
                records = self.records(Path(temporary), exposure=[target])
                with self.assertRaisesRegex(ValueError, reason):
                    validate_interface_exposure(records)

    def test_exposure_cannot_skip_intermediate_or_required_boundary(self):
        cases = (
            ("skipped_intermediate", None, ["MOD-1"], "Exposure skips intermediate ancestor"),
            ("missing_nearest", "MOD-5", None, "Missing required exposure through MOD-2"),
            ("missing_outer", "MOD-7", ["MOD-2"], "Missing required exposure through MOD-1"),
        )
        for name, consumer, exposure, reason in cases:
            with self.subTest(case=name), tempfile.TemporaryDirectory() as temporary:
                records = self.records(Path(temporary), consumer, exposure)
                with self.assertRaisesRegex(ValueError, reason):
                    validate_interface_exposure(records)


class DeliveryDisclosureSchemaTests(unittest.TestCase):
    """Structural Design examples only; no importer or real assessment proof."""

    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads((ROOT / "design/support/requirement-delivery-v2.schema.json").read_text())
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)

    def fixture(self, kind="system-requirement"):
        digest = "sha256:" + "a" * 64  # Deliberately synthetic; identity semantics are a separate contract.
        subject = {"path": "tests/fixtures/example.txt", "identity": digest}
        source = {"change": "synthetic-design-example", "kind": "evidence", "id": "observation", "identity": digest}
        rid = {"initial-requirement": "IR-900", "system-requirement": "SR-900", "allocated-requirement": "AR-900"}[kind]
        claim = {"identity": digest, "state": "partial", "actor": "Synthetic author", "reported_at": "2026-10-06T00:00:00Z",
                 "source": source, "summary": "One contribution exists; the remaining outcome is unproved.",
                 "limitations": ["Synthetic structural example only."], "subjects": [subject],
                 "applicability": {"state": "current", "explanation": "Explicit synthetic disposition."},
                 "criteria": [{"key": "O1" if kind == "initial-requirement" else "C1", "state": "partial",
                               "explanation": "Partial contribution, with its gap retained.", "evidence": [{"source": source,
                               "summary": "Synthetic observation.", "subjects": [subject], "limitations": []}],
                               "gaps": ["The remaining outcome is not established."]}],
                 "membership": None, "child_support": [], "nonreliance": [], "design_support": [],
                 "concerns": [{"id": "remaining-outcome", "source": source, "state": "open",
                               "explanation": "Required outcome remains unresolved.", "disposition": None}]}
        verification = deepcopy(claim)
        verification.update(state="not-assessed", source={**source, "kind": "verification"})
        verification["criteria"][0]["state"] = "not-assessed"
        basis = None
        if kind == "initial-requirement":
            basis = {"identity": digest, "outcomes": [{"key": "O1", "text": "An assessable synthetic stakeholder outcome.", "sources": [subject]}],
                     "review": {"source": {**source, "kind": "review"}, "purpose": "design", "judgment": "approved",
                                "actor": "Synthetic reviewer", "reported_at": "2026-10-06T00:00:00Z", "scope": "Synthetic whole need.",
                                "summary": "The example outcome basis is reviewed.", "subjects": [subject]}}
        account = {"requirement": rid, "kind": kind, "definition": {"path": "design/requirements/example.json", "identity": digest,
                   "content": json.dumps({"id": rid, "type": kind, **({"statement": "Synthetic stakeholder need."} if kind == "initial-requirement" else {"acceptance_criteria": ["Synthetic outcome."]})})},
                   "scope": "Synthetic whole requirement.", "outcome_basis": basis, "implementation": claim, "verification": verification}
        return {"format_version": 2, "assessments": [account], "resolutions": []}

    def changed(self, document, path, value):
        result = deepcopy(document)
        target = result
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        return result

    def test_structural_examples_accept_each_requirement_kind_and_explicit_absence(self):
        for kind in ("initial-requirement", "system-requirement", "allocated-requirement"):
            with self.subTest(kind=kind):
                document = self.fixture(kind)
                self.validator.validate(document)
                document["assessments"][0].update(implementation=None, verification=None, outcome_basis=None)
                self.validator.validate(document)
        self.validator.validate({"format_version": 2, "assessments": [], "resolutions": []})

    def test_unknown_closed_vocabulary_rejects_from_valid_baselines(self):
        document = self.fixture("initial-requirement")
        self.validator.validate(document)
        account = ("assessments", 0)
        paths = [("format_version",), account + ("kind",),
                 account + ("implementation", "source", "kind"),
                 account + ("outcome_basis", "review", "purpose"),
                 account + ("outcome_basis", "review", "judgment"),
                 account + ("implementation", "concerns", 0, "state")]
        for claim in ("implementation", "verification"):
            paths += [account + (claim, "state"), account + (claim, "criteria", 0, "state"),
                      account + (claim, "applicability", "state")]
        for path in paths:
            with self.subTest(path=path), self.assertRaises(ValidationError):
                self.validator.validate(self.changed(document, path, 999 if path == ("format_version",) else "future-value"))
        source = document["assessments"][0]["verification"]["source"]
        digest = source["identity"]
        resolution = {"requirement": "IR-900", "kind": "verification", "selected": digest,
                      "superseded": [{"claim": "sha256:" + "b" * 64, "disposition": source,
                                      "explanation": "Synthetic correction disposition.", "addressed": ["criterion:O1"]}],
                      "source": source, "actor": "Synthetic verifier", "reported_at": "2026-10-06T00:00:00Z",
                      "explanation": "Explicit synthetic selection.", "subjects": document["assessments"][0]["verification"]["subjects"],
                      "applicability": {"state": "current", "explanation": "Explicit synthetic disposition."}}
        document["resolutions"] = [resolution]
        self.validator.validate(document)
        with self.assertRaises(ValidationError):
            self.validator.validate(self.changed(document, ("resolutions", 0, "kind"), "future-value"))

    def test_absent_ir_basis_cannot_carry_claims_and_non_ir_cannot_carry_outcomes(self):
        document = self.fixture("initial-requirement")
        self.validator.validate(document)
        for path, value in [(("assessments", 0, "outcome_basis"), None),
                            (("assessments", 0, "kind"), "system-requirement")]:
            with self.subTest(path=path), self.assertRaises(ValidationError):
                self.validator.validate(self.changed(document, path, value))

    def test_required_nullable_fields_and_unknown_fields_are_not_interchangeable(self):
        document = self.fixture()
        self.validator.validate(document)
        for owner in [(), ("assessments", 0), ("assessments", 0, "implementation"),
                      ("assessments", 0, "implementation", "criteria", 0)]:
            changed = deepcopy(document)
            target = changed
            for key in owner:
                target = target[key]
            target["unexpected"] = True
            with self.subTest(owner=owner), self.assertRaises(ValidationError):
                self.validator.validate(changed)
        del document["assessments"][0]["outcome_basis"]
        with self.assertRaises(ValidationError):
            self.validator.validate(document)

    def test_structural_resource_bounds_reject_excess_without_truncation(self):
        document = self.fixture()
        self.validator.validate(document)
        for path, value in [(("assessments",), document["assessments"] * 257),
                            (("assessments", 0, "scope"), "x" * 16385),
                            (("assessments", 0, "definition", "content"), "x" * 262145)]:
            with self.subTest(path=path), self.assertRaises(ValidationError):
                self.validator.validate(self.changed(document, path, value))


if __name__ == "__main__":
    unittest.main()
