"""Direct checks for the draft IR/SR JSON representation.

Run with: python3 tests/engineering/validation/requirement_schema_tests.py
Requires the jsonschema package with Draft 2020-12 support. These checks cover
record shape, not parentage, reference resolution, or engineering adequacy.
"""

import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[3]
KINDS = ("ir", "sr")
QUESTION_FIELDS = {
    "what": ("problem", "desired_outcome"),
    "why": ("rationale",),
    "who": ("stakeholders",),
    "when": ("conditions",),
    "where": ("contexts",),
    "how": ("approach",),
    "how_much": ("scope",),
}
OBJECT_PATHS = ((), ("analysis",), ("sources", 0)) + tuple(
    ("analysis", question) for question in QUESTION_FIELDS
)


def requirement_fixture(kind, populated=False):
    """Return an independent minimal record, without deriving it from a schema."""
    record = {
        "id": f"{kind.upper()}-1",
        "type": "initial-requirement" if kind == "ir" else "system-requirement",
        "title": "Preserve saved definitions",
        "status": "draft",
        "statement": "Saved engineering definitions remain available across sessions.",
        "analysis": {
            "method": "5W2H",
            "what": {
                "problem": "Session-local knowledge becomes unavailable to later readers.",
                "desired_outcome": "Saved definitions remain retrievable across sessions.",
            },
            "why": {"rationale": "Readers need to resume engineering work."},
            "who": {"stakeholders": ["Engineering authors and readers"]},
            "when": {"conditions": ["After saving and ending an authoring session."]},
            "where": {"contexts": ["Within the governed engineering model."]},
            "how": {"approach": "Retrieve definitions independently of session state."},
            "how_much": {"scope": "Every saved definition in the retained model."},
        },
        "assumptions": [],
        "constraints": [],
        "sources": [{
            "source": "SRC-REM",
            "locator": "Section 5",
            "basis": "Engineering knowledge persists across sessions.",
        }],
    }
    if kind == "sr":
        record["acceptance_criteria"] = [
            "A new session retrieves the unchanged saved definition."
        ]
    if populated:
        record["analysis"]["why"]["value"] = ["Work can resume without reanalysis."]
        record["analysis"]["who"]["affected_users"] = ["Reviewers"]
        record["analysis"]["when"]["frequency"] = "Every session transition."
        record["analysis"]["how_much"].update({
            "scale": "All governed entities.",
            "limits": ["At most 1,000 definitions in this illustrative model."],
        })
        record["assumptions"] = ["The retained model is accessible to authorized readers."]
        record["constraints"] = ["Access remains subject to the model's permissions."]
        record["open_questions"] = ["What retention period is required?"]
    return record


def at_path(record, path):
    for part in path:
        record = record[part]
    return record


class RequirementSchemaTests(unittest.TestCase):
    """Protect required analysis, closed fields, and rejection of malformed data."""

    @classmethod
    def setUpClass(cls):
        cls.schemas = {}
        cls.validators = {}
        for kind in KINDS:
            path = ROOT / "design/support/schemas" / f"{kind}.schema.json"
            cls.schemas[kind] = json.loads(path.read_text(encoding="utf-8"))
            cls.validators[kind] = Draft202012Validator(cls.schemas[kind])

    def valid_fixture(self, kind, populated=False):
        record = requirement_fixture(kind, populated=populated)
        self.assertEqual(list(self.validators[kind].iter_errors(record)), [])
        return record

    def assert_rejected(self, kind, record, path, validator):
        errors = list(self.validators[kind].iter_errors(record))
        observed = [(tuple(error.path), error.validator) for error in errors]
        self.assertIn((path, validator), observed, msg="; ".join(
            f"{list(error.path)}: {error.message}" for error in errors
        ))

    def test_schemas_and_minimal_and_populated_records_are_valid(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                Draft202012Validator.check_schema(self.schemas[kind])
                self.valid_fixture(kind)
                record = self.valid_fixture(kind, populated=True)
                for path in (
                    ("analysis", "why", "value"),
                    ("analysis", "who", "affected_users"),
                    ("analysis", "how_much", "limits"),
                ):
                    at_path(record, path[:-1])[path[-1]] = []
                self.assertEqual(list(self.validators[kind].iter_errors(record)), [])

    def test_current_requirement_records_conform(self):
        for kind in KINDS:
            paths = sorted((ROOT / "design/requirements").rglob(f"{kind}.json"))
            self.assertTrue(paths, f"No {kind.upper()} records found")
            for path in paths:
                with self.subTest(path=str(path.relative_to(ROOT))):
                    record = json.loads(path.read_text(encoding="utf-8"))
                    errors = list(self.validators[kind].iter_errors(record))
                    self.assertEqual(errors, [], msg="; ".join(
                        f"{list(error.path)}: {error.message}" for error in errors
                    ))

    def test_required_fields_cannot_be_omitted(self):
        paths = [(name,) for name in (
            "id", "type", "title", "status", "statement", "analysis",
            "assumptions", "constraints", "sources",
        )]
        paths += [("analysis", name) for name in ("method", *QUESTION_FIELDS)]
        paths += [
            ("analysis", question, field)
            for question, fields in QUESTION_FIELDS.items() for field in fields
        ]
        paths += [("sources", 0, name) for name in (
            "source", "locator", "basis"
        )]
        for kind in KINDS:
            required = paths + ([("acceptance_criteria",)] if kind == "sr" else [])
            for path in required:
                with self.subTest(kind=kind, missing=path):
                    record = self.valid_fixture(kind)
                    del at_path(record, path[:-1])[path[-1]]
                    self.assert_rejected(kind, record, path[:-1], "required")

    def test_unknown_fields_are_rejected_at_every_object_boundary(self):
        for kind in KINDS:
            for path in OBJECT_PATHS:
                with self.subTest(kind=kind, object=path):
                    record = self.valid_fixture(kind)
                    at_path(record, path)["unexpected"] = "unsupported"
                    self.assert_rejected(kind, record, path, "additionalProperties")

    def test_duplicate_legacy_fields_and_camelcase_aliases_are_rejected(self):
        paths = (
            ("parent_id",), ("slug",), ("rationale",), ("scope_notes",),
            ("openQuestions",), ("analysis", "what", "desiredOutcome"),
            ("analysis", "who", "affectedUsers"),
            ("analysis", "how", "constraints"),
            ("analysis", "how_much", "open_questions"),
        )
        for kind in KINDS:
            for path in paths:
                with self.subTest(kind=kind, unsupported=path):
                    record = self.valid_fixture(kind)
                    at_path(record, path[:-1])[path[-1]] = "unsupported"
                    self.assert_rejected(kind, record, path[:-1], "additionalProperties")

    def test_unknown_type_status_and_analysis_method_are_rejected(self):
        variants = (
            (("type",), "allocated-requirement"),
            (("type",), None),
            (("status",), "approved"),
            (("status",), True),
            (("analysis", "method"), "unknown-method"),
            (("analysis", "method"), 5),
        )
        for kind in KINDS:
            wrong_kind = "system-requirement" if kind == "ir" else "initial-requirement"
            for path, value in variants + ((("type",), wrong_kind),):
                with self.subTest(kind=kind, path=path, value=value):
                    record = self.valid_fixture(kind)
                    at_path(record, path[:-1])[path[-1]] = value
                    self.assert_rejected(kind, record, path, "const")

    def test_text_fields_reject_empty_and_whitespace_only_answers(self):
        paths = [("title",), ("statement",)]
        paths += [
            ("analysis", "what", "problem"),
            ("analysis", "what", "desired_outcome"),
            ("analysis", "why", "rationale"),
            ("analysis", "who", "stakeholders", 0),
            ("analysis", "when", "conditions", 0),
            ("analysis", "where", "contexts", 0),
            ("analysis", "how", "approach"),
            ("analysis", "how_much", "scope"),
            ("analysis", "when", "frequency"),
            ("analysis", "how_much", "scale"),
            ("analysis", "why", "value", 0),
            ("analysis", "who", "affected_users", 0),
            ("analysis", "how_much", "limits", 0),
        ]
        paths += [(name, 0) for name in ("assumptions", "constraints", "open_questions")]
        paths += [("sources", 0, name) for name in ("source", "locator", "basis")]
        for kind in KINDS:
            fields = paths + ([("acceptance_criteria", 0)] if kind == "sr" else [])
            for path in fields:
                for value in ("", " \t\n"):
                    with self.subTest(kind=kind, path=path, value=repr(value)):
                        record = self.valid_fixture(kind, populated=True)
                        at_path(record, path[:-1])[path[-1]] = value
                        self.assert_rejected(kind, record, path, "pattern")

    def test_required_collections_cannot_be_empty(self):
        for kind in KINDS:
            paths = [
                ("analysis", "who", "stakeholders"),
                ("analysis", "when", "conditions"),
                ("analysis", "where", "contexts"),
                ("sources",),
            ]
            if kind == "sr":
                paths.append(("acceptance_criteria",))
            for path in paths:
                with self.subTest(kind=kind, path=path):
                    record = self.valid_fixture(kind)
                    at_path(record, path[:-1])[path[-1]] = []
                    self.assert_rejected(kind, record, path, "minItems")

    def test_open_questions_are_optional_and_contain_exactly_one_question_when_present(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                self.valid_fixture(kind)
                self.valid_fixture(kind, populated=True)
            for questions, validator in (
                ([], "minItems"),
                (["What retention period is required?", "What model size must be supported?"], "maxItems"),
            ):
                with self.subTest(kind=kind, questions=questions):
                    record = self.valid_fixture(kind)
                    record["open_questions"] = questions
                    self.assert_rejected(kind, record, ("open_questions",), validator)

    def test_objects_collections_and_text_have_the_declared_types(self):
        variants = tuple((path, None) for path in OBJECT_PATHS) + (
            (("analysis", "what"), "An unstructured answer"),
            (("analysis", "who", "stakeholders"), "Reader"),
            (("analysis", "who", "stakeholders", 0), None),
            (("analysis", "when", "frequency"), None),
            (("analysis", "why", "value"), None),
            (("analysis", "how_much", "limits", 0), None),
            (("open_questions",), None),
            (("open_questions",), "Unknown retention"),
            (("open_questions", 0), None),
            (("constraints",), None),
            (("assumptions",), None),
            (("sources",), {}),
            (("title",), 7),
        )
        for kind in KINDS:
            fields = variants
            if kind == "sr":
                fields += (
                    (("acceptance_criteria",), "Retrieval succeeds"),
                    (("acceptance_criteria", 0), None),
                )
            for path, value in fields:
                with self.subTest(kind=kind, path=path):
                    record = self.valid_fixture(kind, populated=True)
                    if path:
                        at_path(record, path[:-1])[path[-1]] = value
                    else:
                        record = value
                    self.assert_rejected(kind, record, path, "type")

    def test_identifiers_require_the_right_prefix_and_only_ascii_digits(self):
        for kind in KINDS:
            prefix = kind.upper()
            invalid_ids = (
                ("AR-1", "pattern"),
                (f"{prefix}-", "pattern"),
                (f"{prefix}-１", "pattern"),
                (f"{prefix}-1\n", "not"),
                (f" {prefix}-1", "pattern"),
                (f"{prefix}-1-other", "pattern"),
            )
            for value, validator in invalid_ids:
                with self.subTest(kind=kind, id=repr(value)):
                    record = self.valid_fixture(kind)
                    record["id"] = value
                    self.assert_rejected(kind, record, ("id",), validator)

    def test_optional_relationships_accept_empty_or_typed_target_lists(self):
        relationships = (
            ("ir", "confirms", ["FEAT-1", "SCN-2"]),
            ("sr", "confirms", ["FUNC-1"]),
            ("sr", "constrains", ["FEAT-1", "FUNC-2"]),
        )
        for kind, field, targets in relationships:
            for values in ([], targets):
                with self.subTest(kind=kind, field=field, targets=values):
                    record = self.valid_fixture(kind)
                    record[field] = values
                    self.assertEqual(list(self.validators[kind].iter_errors(record)), [])

    def test_relationships_reject_wrong_targets_duplicates_and_wrong_types(self):
        relationships = (
            ("ir", "confirms", "FEAT-1", "FUNC-1"),
            ("sr", "confirms", "FUNC-1", "FEAT-1"),
            ("sr", "constrains", "FEAT-1", "SCN-1"),
        )
        for kind, field, target, wrong_target in relationships:
            variants = (
                ([wrong_target], (field, 0), "pattern"),
                ([target + "\n"], (field, 0), "not"),
                ([target.replace("1", "１")], (field, 0), "pattern"),
                ([target, target], (field,), "uniqueItems"),
                ([None], (field, 0), "type"),
                (None, (field,), "type"),
            )
            for values, path, validator in variants:
                with self.subTest(kind=kind, field=field, targets=values):
                    record = self.valid_fixture(kind)
                    record[field] = [target]
                    self.assertEqual(list(self.validators[kind].iter_errors(record)), [])
                    record[field] = values
                    self.assert_rejected(kind, record, path, validator)
        record = self.valid_fixture("ir")
        record["constrains"] = ["FEAT-1"]
        self.assert_rejected("ir", record, (), "additionalProperties")


if __name__ == "__main__":
    unittest.main()
