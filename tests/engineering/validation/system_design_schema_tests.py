"""Direct schema checks for scenarios, features, and functions.

Run with: python3 tests/engineering/validation/system_design_schema_tests.py
Requires jsonschema with Draft 2020-12 support. This suite checks record shape
and the current model's naming, containment, references, and analysis connections.
Lifecycle transitions, semantic coverage, and architecture adequacy need review.
"""

import json
from pathlib import Path
import re
import unittest

from jsonschema import Draft202012Validator

from architecture_schema_tests import architecture_paths


ROOT = Path(__file__).resolve().parents[3]
PROFILES = {
    "scenario": ("SCN", "requirements/scenarios"),
    "feature": ("FEAT", "system/features"),
    "function": ("FUNC", "system/functions"),
}


def design_fixture(kind, populated=False):
    """Create an independent small authoring record, without reading a schema."""
    prefix, _ = PROFILES[kind]
    record = {
        "id": f"{prefix}-1",
        "type": kind,
        "title": "Retrieve saved engineering definitions",
        "status": "draft",
        "sources": [{
            "source": "SRC-REM",
            "locator": "Section 31",
            "basis": "Current definitions are accessible independently of history.",
        }],
    }
    if kind == "scenario":
        record.update({
            "actor": "An engineering reviewer",
            "goal": "Understand the current saved definition without the original session.",
            "context": "The original authoring session has ended.",
            "trigger": "The reviewer requests a saved definition.",
            "preconditions": [],
            "interaction": [{
                "actor": "Reviewer",
                "action": "Requests the definition using its identity.",
            }, {
                "actor": "System",
                "action": "Presents the current saved definition.",
            }],
            "expected_outcome": "The current saved definition is displayed.",
            "alternatives": [],
            "failures": [],
            "exercises": ["FEAT-1"],
            "informs": ["SR-1"],
        })
        if populated:
            record["alternatives"] = [{
                "condition": "The identity is unknown.",
                "outcome": "The reviewer receives an explicit absence result.",
            }]
            record["failures"] = [{
                "condition": "Engineering information is unavailable.",
                "outcome": "The reviewer is told that the definition cannot be presented.",
            }]
            record["coverage_note"] = "The existing retrieval obligation covers this situation."
    elif kind == "feature":
        record.update({
            "description": "Readers can retrieve the current engineering definition.",
            "scope": {"includes": ["Saved definitions"], "excludes": []},
            "realized_by": ["FUNC-1"],
        })
        if populated:
            record["scope"]["excludes"] = ["Private conversation state"]
    else:
        record.update({
            "description": "Resolve a stable identity to a saved definition.",
            "inputs": ["The requested entity identity"],
            "preconditions": [],
            "outputs": ["The current saved definition or an absence result"],
            "behavior": ["Retrieve the definition associated with the requested identity."],
            "failure_behavior": [],
            "unallocated_reason": "Architecture responsibilities are still being analyzed.",
        })
        if populated:
            record["failure_behavior"] = [{
                "condition": "The model cannot be read.",
                "outcome": "Report unavailable data without fabricating a definition.",
            }]
    if populated:
        if kind == "scenario":
            record["open_questions"] = ["What response-time limit is required?"]
        if "preconditions" in record:
            record["preconditions"] = ["The reader can access the governed model."]
    return record


def at_path(record, path):
    for part in path:
        record = record[part]
    return record


class SystemDesignSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schemas = {}
        cls.validators = {}
        for kind in PROFILES:
            path = ROOT / "design/support/schemas" / f"{kind}.schema.json"
            cls.schemas[kind] = json.loads(path.read_text(encoding="utf-8"))
            cls.validators[kind] = Draft202012Validator(cls.schemas[kind])

    def valid_fixture(self, kind, populated=False):
        record = design_fixture(kind, populated=populated)
        self.assert_valid(kind, record)
        return record

    def assert_valid(self, kind, record):
        errors = list(self.validators[kind].iter_errors(record))
        self.assertEqual(errors, [], msg="; ".join(
            f"{list(error.path)}: {error.message}" for error in errors
        ))

    def assert_rejected(self, kind, record, path, validator=None):
        errors = list(self.validators[kind].iter_errors(record))
        self.assertTrue(any(
            tuple(error.path) == path and (validator is None or error.validator == validator)
            for error in errors
        ), msg="; ".join(f"{list(error.path)}: {error.message}" for error in errors))

    def test_schemas_and_independent_fixtures_are_valid(self):
        for kind in PROFILES:
            with self.subTest(kind=kind):
                Draft202012Validator.check_schema(self.schemas[kind])
                self.valid_fixture(kind)
                self.valid_fixture(kind, populated=True)
        record = self.valid_fixture("function")
        del record["unallocated_reason"]
        record["allocated_to"] = "MOD-1"
        self.assert_valid("function", record)
        for kind, field in (
            ("scenario", "exercises"), ("scenario", "informs"), ("feature", "realized_by")
        ):
            with self.subTest(early_draft=kind):
                record = self.valid_fixture(kind)
                record[field] = []
                self.assert_valid(kind, record)

    def test_current_records_conform(self):
        for kind, (prefix, directory) in PROFILES.items():
            paths = sorted((ROOT / "design" / directory).glob(f"{prefix}-*.json"))
            self.assertTrue(paths, f"No {kind} records found")
            for path in paths:
                with self.subTest(path=str(path.relative_to(ROOT))):
                    self.assert_valid(kind, json.loads(path.read_text(encoding="utf-8")))

    def test_open_questions_are_optional_single_question_for_scenarios_only(self):
        for kind in ("feature", "function"):
            for questions in ([], ["What response-time limit is required?"]):
                with self.subTest(kind=kind, questions=questions):
                    record = self.valid_fixture(kind)
                    record["open_questions"] = questions
                    self.assert_rejected(kind, record, (), "additionalProperties")
        self.valid_fixture("scenario")
        self.valid_fixture("scenario", populated=True)
        for questions, path, validator in (
            ([], ("open_questions",), "minItems"),
            (["What response-time limit is required?", "What model size must be supported?"],
             ("open_questions",), "maxItems"),
            ([""], ("open_questions", 0), "pattern"),
            ("What response-time limit is required?", ("open_questions",), "type"),
        ):
            with self.subTest(questions=questions):
                record = self.valid_fixture("scenario")
                record["open_questions"] = questions
                self.assert_rejected("scenario", record, path, validator)

    def test_required_fields_cannot_be_omitted(self):
        for kind in PROFILES:
            paths = [(name,) for name in design_fixture(kind) if name != "unallocated_reason"]
            paths += [("sources", 0, name) for name in ("source", "locator", "basis")]
            if kind == "feature":
                paths += [("scope", name) for name in ("includes", "excludes")]
            else:
                field = "alternatives" if kind == "scenario" else "failure_behavior"
                paths += [(field, 0, name) for name in ("condition", "outcome")]
            if kind == "scenario":
                paths += [("failures", 0, name) for name in ("condition", "outcome")]
                paths += [("interaction", 0, name) for name in ("actor", "action")]
            for path in paths:
                with self.subTest(kind=kind, missing=path):
                    record = self.valid_fixture(kind, populated=True)
                    del at_path(record, path[:-1])[path[-1]]
                    self.assert_rejected(kind, record, path[:-1], "required")

    def test_unknown_vocabulary_and_object_fields_are_rejected(self):
        for kind in PROFILES:
            for field, value in (("type", "unknown"), ("status", "approved"), ("status", "unknown")):
                with self.subTest(kind=kind, field=field):
                    record = self.valid_fixture(kind)
                    record[field] = value
                    validator = "enum" if kind == "scenario" and field == "status" else "const"
                    self.assert_rejected(kind, record, (field,), validator)
            nested = {
                "scenario": ("alternatives", 0),
                "feature": ("scope",),
                "function": ("failure_behavior", 0),
            }[kind]
            objects = [(), ("sources", 0), nested]
            if kind == "scenario":
                objects += [("interaction", 0), ("failures", 0)]
            for path in objects:
                with self.subTest(kind=kind, object=path):
                    record = self.valid_fixture(kind, populated=True)
                    at_path(record, path)["unexpected"] = "unsupported"
                    self.assert_rejected(kind, record, path, "additionalProperties")

    def test_required_collections_reject_empty_values(self):
        collections = {
            "scenario": [("interaction",)],
            "feature": [("scope", "includes")],
            "function": [("inputs",), ("outputs",), ("behavior",)],
        }
        for kind, paths in collections.items():
            for path in paths + [("sources",)]:
                with self.subTest(kind=kind, path=path):
                    record = self.valid_fixture(kind)
                    at_path(record, path[:-1])[path[-1]] = []
                    self.assert_rejected(kind, record, path, "minItems")

    def test_content_rejects_blank_text_and_null(self):
        content = {
            "scenario": [
                ("actor",), ("goal",), ("context",), ("trigger",), ("expected_outcome",),
                ("interaction", 0, "actor"), ("interaction", 0, "action"),
                ("alternatives", 0, "outcome"), ("failures", 0, "condition"),
                ("failures", 0, "outcome"), ("coverage_note",),
            ],
            "feature": [("description",), ("scope", "includes", 0), ("scope", "excludes", 0)],
            "function": [
                ("description",), ("inputs", 0), ("outputs", 0), ("behavior", 0),
                ("failure_behavior", 0, "condition"), ("unallocated_reason",),
            ],
        }
        for kind, paths in content.items():
            paths += [("title",), ("sources", 0, "basis")]
            if kind == "scenario":
                paths.append(("open_questions", 0))
            for path in paths:
                for value, validator in ((" \t\n", "pattern"), (None, "type")):
                    with self.subTest(kind=kind, path=path, value=value):
                        record = self.valid_fixture(kind, populated=True)
                        at_path(record, path[:-1])[path[-1]] = value
                        self.assert_rejected(kind, record, path, validator)
            nested = {
                "scenario": ("alternatives", 0),
                "feature": ("scope",),
                "function": ("failure_behavior", 0),
            }[kind]
            containers = [(), ("sources",), ("sources", 0), nested]
            if kind == "scenario":
                containers += [("open_questions",), ("interaction", 0), ("failures", 0)]
            for path in containers:
                with self.subTest(kind=kind, null_container=path):
                    record = self.valid_fixture(kind, populated=True)
                    if path:
                        at_path(record, path[:-1])[path[-1]] = None
                    else:
                        record = None
                    self.assert_rejected(kind, record, path, "type")

    def test_identifiers_reject_wrong_prefix_nonascii_digits_and_whitespace(self):
        for kind, (prefix, _) in PROFILES.items():
            for value, validator in (
                ("IR-1", "pattern"), (f"{prefix}-", "pattern"),
                (f"{prefix}-１", "pattern"), (f"{prefix}-1\n", "not"),
            ):
                with self.subTest(kind=kind, id=repr(value)):
                    record = self.valid_fixture(kind)
                    record["id"] = value
                    self.assert_rejected(kind, record, ("id",), validator)

    def test_relationship_targets_reject_wrong_types_and_duplicates(self):
        relationships = (
            ("scenario", "exercises", "FEAT-1", "FUNC-1"),
            ("scenario", "informs", "SR-1", "IR-1"),
            ("feature", "realized_by", "FUNC-1", "MOD-1"),
        )
        for kind, field, target, wrong in relationships:
            for value, path, validator in (
                ([wrong], (field, 0), "pattern"),
                ([target + "\n"], (field, 0), "not"),
                ([target.replace("1", "１")], (field, 0), "pattern"),
                ([target, target], (field,), "uniqueItems"),
                ([None], (field, 0), "type"),
                (target, (field,), "type"),
            ):
                with self.subTest(kind=kind, field=field, value=value):
                    record = self.valid_fixture(kind)
                    record[field] = value
                    self.assert_rejected(kind, record, path, validator)

    def test_function_requires_exactly_one_allocation_disposition(self):
        for both in (False, True):
            with self.subTest(both=both):
                record = self.valid_fixture("function")
                if both:
                    record["allocated_to"] = "MOD-1"
                else:
                    del record["unallocated_reason"]
                self.assert_rejected("function", record, ())
        for value, validator in (("FUNC-1", "pattern"), ("MOD-1\n", "not"), (None, "type")):
            with self.subTest(allocation=value):
                record = self.valid_fixture("function")
                del record["unallocated_reason"]
                record["allocated_to"] = "MOD-1"
                self.assert_valid("function", record)
                record["allocated_to"] = value
                self.assert_rejected("function", record, ("allocated_to",), validator)

    def test_scenario_feature_cardinality_depends_on_lifecycle(self):
        for status in ("draft", "confirmed", "obsolete"):
            with self.subTest(status=status):
                record = self.valid_fixture("scenario")
                record["status"] = status
                record["informs"] = []
                self.assert_valid("scenario", record)
                record["exercises"] = ["FEAT-1", "FEAT-2"]
                self.assert_rejected("scenario", record, ("exercises",), "maxItems")
                record["exercises"] = []
                if status == "draft":
                    self.assert_valid("scenario", record)
                else:
                    self.assert_rejected("scenario", record, ("exercises",), "minItems")

    def test_scenario_rejects_retired_fields_and_duplicate_owner(self):
        for field, value in (
            ("flow", ["An old interaction step"]),
            ("candidate_behavior", ["An internal design step"]),
            ("ir_id", "IR-1"),
        ):
            with self.subTest(field=field):
                record = self.valid_fixture("scenario")
                record[field] = value
                self.assert_rejected("scenario", record, (), "additionalProperties")


class CurrentEngineeringModelTests(unittest.TestCase):
    """Inspect authored references; this is not a lifecycle or semantic validator."""

    @classmethod
    def setUpClass(cls):
        requirements = ROOT / "design/requirements"
        paths = list(requirements.rglob("ir.json")) + list(requirements.rglob("sr.json"))
        paths += list(requirements.rglob("AR-*.json"))
        for prefix, directory in PROFILES.values():
            paths += list((ROOT / "design" / directory).glob(f"{prefix}-*.json"))
        architecture, _ = architecture_paths(ROOT / "design/architecture")
        paths += architecture
        cls.records = [
            (path, json.loads(path.read_text(encoding="utf-8"))) for path in sorted(paths)
        ]

    def test_current_entity_identities_are_unique(self):
        locations = {}
        for path, record in self.records:
            locations.setdefault(record["id"], []).append(str(path.relative_to(ROOT)))
        self.assertTrue(locations, "No current requirement or system-design entities found")
        duplicates = {identity: paths for identity, paths in locations.items() if len(paths) > 1}
        self.assertEqual(duplicates, {})

    def test_each_current_scenario_has_exactly_one_ir_owner(self):
        owners = {
            record["id"]: [] for _, record in self.records if record["type"] == "scenario"
        }
        self.assertTrue(owners, "No current scenarios found")
        for _, record in self.records:
            if record["type"] == "initial-requirement":
                for target in record.get("confirms", []):
                    if target.startswith("SCN-"):
                        self.assertIn(target, owners, f'{record["id"]} confirms an unknown Scenario')
                        owners[target].append(record["id"])
        for scenario, incoming in owners.items():
            with self.subTest(scenario=scenario):
                self.assertEqual(len(incoming), 1, f"{scenario} has IR owners {incoming}")

    def test_current_relationship_targets_resolve_to_compatible_entities(self):
        entities = {record["id"]: record for _, record in self.records}
        compatible = {
            "initial-requirement": {"confirms": {"feature", "scenario"}},
            "system-requirement": {"confirms": {"function"}, "constrains": {"feature", "function"}},
            "scenario": {"exercises": {"feature"}, "informs": {"system-requirement"}},
            "feature": {"realized_by": {"function"}},
            "function": {"allocated_to": {"module"}},
            "allocated-requirement": {"allocated_to": {"module"}, "constrains": {"function"}},
            "module": {"provides": {"interface"}, "consumes": {"interface"}},
            "interface": {"exposed_through": {"module"}},
        }
        for _, record in self.records:
            for relation, target_types in compatible[record["type"]].items():
                targets = record.get(relation, [])
                if isinstance(targets, str):
                    targets = [targets]
                for target in targets:
                    with self.subTest(entity=record["id"], relation=relation, target=target):
                        self.assertIn(target, entities, "Relationship references an unknown entity")
                        self.assertIn(entities[target]["type"], target_types)

    def test_current_names_and_requirement_containment_match_the_profile(self):
        ir_directories = {path.parent for path, record in self.records
                          if record["type"] == "initial-requirement"}
        sr_directories = {path.parent for path, record in self.records
                          if record["type"] == "system-requirement"}
        module_directories = {path.parent for path, record in self.records
                              if record["type"] == "module"}
        requirements = ROOT / "design/requirements"
        for path, record in self.records:
            with self.subTest(entity=record["id"]):
                slug = re.sub(r"[^a-z0-9]+", "-", record["title"].lower()).strip("-")
                self.assertTrue(slug)
                label = f'{record["id"]}-{slug}'
                if record["type"] == "initial-requirement":
                    self.assertEqual(path.parent.parent, requirements)
                    self.assertEqual(path.parent.name, label)
                elif record["type"] == "system-requirement":
                    self.assertIn(path.parent.parent, ir_directories)
                    self.assertEqual(path.parent.name, label)
                elif record["type"] == "allocated-requirement":
                    self.assertIn(path.parent, sr_directories)
                    self.assertEqual(path.name, label + ".json")
                elif record["type"] in ("module", "interface"):
                    kind = record["type"]
                    collection = path.parent.parent
                    top_level = ROOT / "design/architecture" / f"{kind}s"
                    if kind == "module" and collection != top_level:
                        self.assertEqual(collection.name, "modules")
                        self.assertIn(collection.parent, module_directories)
                    else:
                        self.assertEqual(collection, top_level)
                    self.assertEqual(path.parent.name, label)
                    self.assertEqual(path.name, f"{kind}.json")
                else:
                    self.assertEqual(path.name, label + ".json")

    def test_current_analysis_connections_are_accounted_for(self):
        entities = {record["id"]: record for _, record in self.records}
        sr_records = [record for _, record in self.records if record["type"] == "system-requirement"]
        scenarios = [record for _, record in self.records if record["type"] == "scenario"]
        features = [record for _, record in self.records if record["type"] == "feature"]
        confirmed_functions = {target for record in sr_records for target in record.get("confirms", [])}
        realized_functions = {target for feature in features for target in feature["realized_by"]}
        for path, record in self.records:
            with self.subTest(entity=record["id"]):
                if record["type"] == "initial-requirement":
                    owned = [entities[target] for target in record.get("confirms", [])]
                    self.assertTrue(any(item["type"] == "scenario" for item in owned))
                    self.assertTrue(any(item["type"] == "feature" for item in owned))
                    self.assertTrue(any(p.parent.parent == path.parent for p, r in self.records
                                        if r["type"] == "system-requirement"))
                elif record["type"] == "system-requirement":
                    self.assertTrue(record.get("confirms") or record.get("constrains"))
                elif record["type"] == "scenario":
                    self.assertEqual(len(record["exercises"]), 1)
                    self.assertTrue(record["informs"] or record.get("coverage_note"))
                elif record["type"] == "feature":
                    self.assertTrue(record["realized_by"])
                    self.assertTrue(any(record["id"] in s["exercises"] for s in scenarios))
                elif record["type"] == "function":
                    self.assertIn(record["id"], confirmed_functions)
                    self.assertIn(record["id"], realized_functions)

    def test_current_source_references_identify_registered_basis(self):
        source_text = (ROOT / "design/requirements/sources.md").read_text(encoding="utf-8")
        registered = set(re.findall(r"^## (SRC-[A-Z0-9-]+)$", source_text, re.MULTILINE))
        self.assertTrue(registered)
        for _, record in self.records:
            for source in record["sources"]:
                with self.subTest(entity=record["id"], source=source["source"]):
                    self.assertIn(source["source"], registered)


if __name__ == "__main__":
    unittest.main()
