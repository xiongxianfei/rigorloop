"""Direct checks for the draft Module, Interface, and AR authoring profiles.

Run with: python3 tests/engineering/validation/architecture_schema_tests.py
Requires jsonschema with Draft 2020-12 support. Independent fixtures protect
meaningful required content, closed vocabulary, single responsibility links,
and contract shape. Current-record checks inspect the pilot's endpoint and
operation-name conventions. These checks do not execute interface behavior or
establish derivation, architectural adequacy, approval, or implementation.
The system-design suite owns shared identity, naming, containment, and links.
"""

import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[3]
KINDS = {"module": "MOD", "interface": "IF", "ar": "AR"}


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


class ArchitectureSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schemas = {
            kind: json.loads((ROOT / "design/support/schemas" / f"{kind}.schema.json").read_text())
            for kind in KINDS
        }
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
        collections = {
            "module": (ROOT / "design/architecture/modules").glob("MOD-*.json"),
            "interface": (ROOT / "design/architecture/interfaces").glob("IF-*.json"),
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

    def test_reverse_links_parent_copies_and_camelcase_aliases_are_rejected(self):
        fields = {
            "module": ("functions", "allocated_requirements", "provided_by", "ownedState"),
            "interface": ("provider", "consumers", "provided_by", "compatibilityRules"),
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


class CurrentArchitectureConnectionsTests(unittest.TestCase):
    def test_pilot_interfaces_have_unambiguous_providers_consumers_and_operation_names(self):
        modules = [json.loads(path.read_text()) for path in
                   sorted((ROOT / "design/architecture/modules").glob("MOD-*.json"))]
        interfaces = [json.loads(path.read_text()) for path in
                      sorted((ROOT / "design/architecture/interfaces").glob("IF-*.json"))]
        self.assertTrue(interfaces, "No pilot Interfaces found")
        for interface in interfaces:
            with self.subTest(interface=interface["id"]):
                providers = [m["id"] for m in modules if interface["id"] in m["provides"]]
                consumers = [m["id"] for m in modules if interface["id"] in m["consumes"]]
                self.assertEqual(len(providers), 1, f"Providers: {providers}")
                self.assertTrue(consumers, "No consumer for the pilot contract")
                names = [operation["name"] for operation in interface["operations"]]
                self.assertEqual(len(names), len(set(names)), "Operation names must be unique")


if __name__ == "__main__":
    unittest.main()
