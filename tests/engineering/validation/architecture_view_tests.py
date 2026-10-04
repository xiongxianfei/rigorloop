"""Semantic REM model/browser projection and standalone product-inventory checks.

Run with: python3 tests/engineering/validation/architecture_view_tests.py

The browser-view-consolidation contract retains these model rejection and
projection cases after retiring Markdown architecture outputs. Browser compiler,
escaping, deterministic generation, freshness, and output-write protection are
covered in architecture_browser_tests.py. Private source fixtures establish no
runtime behavior or correctness of the recorded source observations.
"""

import hashlib
from copy import deepcopy
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.rem_architecture_model import Model
from lib import rem_architecture_browser as browser_projection
from lib import rem_architecture_scenarios as scenario_profiles

INVENTORY_RENDERER = ROOT / "scripts/render-rem-product-inventory.py"
INVENTORY = "design/requirements/published-products.md"


def snapshot(root):
    """Record content and modification times to detect even same-byte writes."""
    return {path.relative_to(root).as_posix():
            (hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_mtime_ns)
            for path in root.rglob("*") if path.is_file()}


class ArchitectureViewProjectionTests(unittest.TestCase):
    def fixture(self):
        temporary = tempfile.TemporaryDirectory(prefix="rem-view-projection-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        shutil.copytree(ROOT / "design", root / "design",
                        ignore=shutil.ignore_patterns("browser", "*.md"))
        inventory = root / INVENTORY
        inventory.parent.mkdir(parents=True, exist_ok=True)
        inventory.write_bytes((ROOT / INVENTORY).read_bytes())
        # Only path existence is relevant to catalogs. Never copy/read SKILL.md.
        for path in (root / "design/architecture").rglob("*.json"):
            facet = json.loads(path.read_text())
            source_paths = []
            for entry in facet.get("observed", {}).get("public_entries", []):
                source_paths.extend(entry[field] for field in ("source_path", "contract"))
            for choice in facet.get("proposed", []):
                source_paths.extend(entry["contract"] for entry in choice.get("public_capabilities", []))
            for group in facet.get("observed", {}).get("test_groups", []):
                source_paths.extend((group["contract"], group["execution"]["owner_contract"]))
                for items in (group["test_sources"], group["fixtures"],
                              *(group["execution"][key] for key in ("selection", "runners", "entrypoints"))):
                    source_paths.extend(item["path"] for item in items)
            for source_path in source_paths:
                target = root / source_path.split("#", 1)[0]
                if not target.exists():
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text("Private source-path fixture; no product behavior.\n")
        (root / "unrelated.txt").write_text("Preserve unrelated workspace content.\n")
        return root

    def entity_path(self, root, identifier):
        matches = []
        for path in (root / "design").rglob("*.json"):
            if json.loads(path.read_text()).get("id") == identifier:
                matches.append(path)
        self.assertEqual(len(matches), 1, f"Expected one canonical {identifier}")
        return matches[0]

    def write_record(self, path, record):
        path.write_text(json.dumps(record, indent=2) + "\n")

    def public_facet(self, root, identity):
        owner = self.entity_path(root, identity)
        name = "interaction" if identity.startswith("IF-") else "software"
        path = owner.parent / "realization" / f"{name}.json"
        return path, json.loads(path.read_text())

    def public_mappings(self, facet):
        return [mapping for choice in facet["proposed"]
                for mapping in choice.get("public_entry_mappings", [])]

    def inventory_parts(self, content):
        before, remaining = content.split(b"<!-- skill-inventory:start -->", 1)
        block, after = remaining.split(b"<!-- skill-inventory:end -->", 1)
        return before, block, after

    def select_child_provider(self, root, interface, child, exposure):
        """Explicitly author the distinct child-owned exposure fixture."""
        for path in (root / "design/architecture/modules").rglob("module.json"):
            record = json.loads(path.read_text())
            original = list(record["provides"])
            record["provides"] = [value for value in original if value != interface]
            if record["id"] == child:
                record["provides"].append(interface)
            if record["provides"] != original:
                self.write_record(path, record)
        path = self.entity_path(root, interface)
        record = json.loads(path.read_text())
        record["exposed_through"] = exposure
        self.write_record(path, record)

    def nested_command_group(self, root):
        """An independently named intermediate owner makes exposure depth material."""
        self.select_child_provider(root, "IF-004", "MOD-010", ["MOD-018"])
        outer = self.entity_path(root, "MOD-018").parent
        owner = outer / "modules/MOD-020-command-admission-and-presentation"
        owner.mkdir(parents=True)
        self.write_record(owner / "module.json", {
            "id": "MOD-020", "type": "module", "title": "Command admission and presentation",
            "status": "draft", "description": "Own the command admission and presentation boundary.",
            "responsibilities": ["Preserve explicit command admission and truthful command presentation."],
            "owned_state": [], "scope": {"includes": ["Public command interaction"], "excludes": ["Record publication"]},
            "provides": [], "consumes": [], "design_limits": ["Fixture for deeper containment."],
            "sources": [{"source": "SRC-REM", "locator": "Fixture", "basis": "Independent projection example."}],
        })
        (owner / "modules").mkdir()
        command = self.entity_path(root, "MOD-010").parent
        relocated = owner / "modules" / command.name
        command.rename(relocated)
        for path in (root / "design/architecture").rglob("*.json"):
            record = json.loads(path.read_text())
            changed = False
            for choice in record.get("proposed", []):
                for entry in choice.get("public_capabilities", []):
                    prefix = command.relative_to(root).as_posix() + "/"
                    if entry["contract"].startswith(prefix):
                        entry["contract"] = relocated.relative_to(root).as_posix() + "/" + entry["contract"][len(prefix):]
                        changed = True
            for entry in record.get("observed",{}).get("public_entries",[]):
                prefix=command.relative_to(root).as_posix()+"/"
                if entry["contract"].startswith(prefix):
                    entry["contract"]=relocated.relative_to(root).as_posix()+"/"+entry["contract"][len(prefix):]
                    changed=True
            # Owned coverage now moves with the Module's detailed contract.
            for group in record.get("observed", {}).get("test_groups", []):
                prefix = command.relative_to(root).as_posix() + "/"
                for container, field in ((group, "contract"), (group["execution"], "owner_contract")):
                    if container[field].startswith(prefix):
                        container[field] = relocated.relative_to(root).as_posix() + "/" + container[field][len(prefix):]
                        changed = True
            if changed:
                self.write_record(path, record)
        interface = self.entity_path(root, "IF-004")
        record = json.loads(interface.read_text())
        record["exposed_through"] = ["MOD-020", "MOD-018"]
        self.write_record(interface, record)
        return owner

    def projection_model(self, root):
        return Model(root), browser_projection

    def projected(self, root):
        return browser_projection.build_model(Model(root))

    def assert_invalid_model(self, root, message):
        before = snapshot(root)
        with self.assertRaisesRegex(ValueError, re.escape(message)) as caught:
            Model(root)
        self.assertEqual(snapshot(root), before)
        return str(caught.exception)

    def invoke_inventory(self, root, *arguments):
        return subprocess.run(
            [sys.executable, str(INVENTORY_RENDERER), "--root", str(root), *arguments],
            cwd=root, capture_output=True, text=True, check=False, timeout=30)

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def catalog_entry(self, projection, owner, name):
        catalog = next(item for item in projection["catalogs"] if item["owner"] == owner)
        return next(item for item in catalog["entries"] if item["name"] == name)

    def facet(self, projection, owner, name):
        return next(item for item in projection["facets"]
                    if (item["owner"], item["facet"]) == (owner, name))

    def resolve_outcome_source(self, model, reference):
        record = (model.records[reference["owner"]] if reference.get("facet") in (None, "scenario")
                  else model.facets[(reference["owner"], reference["facet"])])
        self.assertEqual(reference["path"], record.path.as_posix())
        value = record.data
        for token in reference["field"].lstrip("/").split("/"):
            token = token.replace("~1", "/").replace("~0", "~")
            value = value[int(token)] if isinstance(value, list) else value[token]
        return value

    def test_scenario_outcomes_preserve_every_canonical_result_and_unprofiled_scope(self):
        root = self.fixture()
        before = snapshot(root)
        model = Model(root)
        views = model.architecture_views()
        counts = {}
        for scenario in views["scenarios"]["scenarios"]:
            record = model.records[scenario["scenario"]]
            outcomes = scenario["outcomes"]
            expected_keys = ["expected"] + [f"alternative-{i}" for i in range(len(record.data["alternatives"]))] + [f"failure-{i}" for i in range(len(record.data["failures"]))]
            self.assertEqual([item["key"] for item in outcomes], expected_keys)
            counts[scenario["scenario"]] = sum(item["profiled"] for item in outcomes)
            for item in outcomes:
                canonical = self.resolve_outcome_source(model, item["source"])
                if item["kind"] == "expected":
                    self.assertEqual((item["condition"], item["outcome"]), ("", canonical))
                else:
                    self.assertEqual((item["condition"], item["outcome"]), (canonical["condition"], canonical["outcome"]))
                if not item["profiled"]:
                    self.assertEqual(item["title"], "Expected outcome" if item["kind"] == "expected" else item["condition"])
                    for field in ("obligations", "limit_sources", "requirements", "allocated_requirements", "modules", "interfaces", "test_context"):
                        self.assertEqual(item[field], [])
                    self.assertTrue(all(not refs for refs in item["realization"].values()))
                    self.assertIn("does not establish missing architecture or test coverage", " ".join(item["gaps"]))
        self.assertEqual(counts, {"SCN-019": 0, "SCN-046": 6, "SCN-047": 5, "SCN-053": 0, "SCN-066": 0})
        self.assertEqual(snapshot(root), before)

    def test_pilot_obligations_and_realization_keep_exact_responsibility_and_reading_limits(self):
        model = Model(self.fixture())
        scenarios = {item["scenario"]: item for item in model.architecture_views()["scenarios"]["scenarios"]}
        # Independent behavioral anchors: freshness before no-op, truthful durable
        # disposition, bounded detail, and exact action/state-dependent recovery.
        anchors = {
            ("SCN-046", "expected"): {("AR-019", 2), ("AR-021", 1), ("AR-021", 2)},
            ("SCN-046", "alternative-0"): {("AR-020", 4)},
            ("SCN-046", "alternative-1"): {("AR-024", 4), ("AR-025", 1), ("AR-025", 2)},
            ("SCN-046", "failure-0"): {("AR-020", 4)},
            ("SCN-046", "failure-1"): {("AR-020", 0), ("AR-020", 1), ("AR-020", 2)},
            ("SCN-046", "failure-2"): {("AR-021", 0), ("AR-021", 4)},
            ("SCN-047", "expected"): {("AR-022", 1), ("AR-022", 2), ("AR-023", 1)},
            ("SCN-047", "alternative-0"): {("AR-022", 1)},
            ("SCN-047", "alternative-1"): {("AR-022", 3)},
            ("SCN-047", "failure-0"): {("AR-022", 0)},
            ("SCN-047", "failure-1"): {("AR-022", 4), ("AR-023", 2)},
        }
        for identity in ("SCN-046", "SCN-047"):
            scenario = scenarios[identity]
            for item in scenario["outcomes"]:
                self.assertTrue({(owner, f"/acceptance_criteria/{index}") for owner, index in anchors[(identity, item["key"]) ]}
                                <= {(ref["owner"], ref["field"]) for ref in item["obligations"]})
                derived_requirements, derived_allocations, derived_modules = set(), set(), set()
                for obligation in item["obligations"]:
                    self.assertEqual(obligation["text"], self.resolve_outcome_source(model, obligation))
                    record = model.records[obligation["owner"]]
                    if record.data["type"] == "system-requirement":
                        parent = record.id
                    else:
                        parent = model.outgoing(record.id, "parent")[0].target
                        derived_allocations.add(record.id)
                        derived_modules.add(record.data["allocated_to"])
                    self.assertIn(parent, model.records[identity].data["informs"])
                    derived_requirements.add(parent)
                self.assertEqual(item["requirements"], sorted(derived_requirements))
                self.assertEqual(item["allocated_requirements"], sorted(derived_allocations))
                self.assertEqual(item["modules"], sorted(derived_modules))
                self.assertEqual(item["interfaces"], ["IF-003"])
                for reference in item["realization"]["physical"]:
                    detail = self.resolve_outcome_source(model, reference)
                    if "placement" in detail:
                        self.assertEqual(detail["participant"], "MOD-011")
                        self.assertIn(detail["placement"]["name"], ("Registered operational records", "Record transaction metadata"))
                for reference in item["test_context"]:
                    self.assertEqual(reference["facet"], "software")
                    self.assertRegex(reference["field"], r"^/observed/test_groups/\d+$")
                    self.assertNotIn("diagnostic", self.resolve_outcome_source(model, reference)["name"].lower())
                self.assertIn("not coverage or passing results", " ".join(item["gaps"]))
                if identity == "SCN-047":
                    files = [self.resolve_outcome_source(model, ref)["path"] for ref in item["realization"]["development"]]
                    self.assertIn("packages/rigorloop/dist/lib/operational-cli.js", files)
                    self.assertNotIn("packages/rigorloop/dist/lib/recording-result.js", files)
                    self.assertNotIn("AR-025", item["allocated_requirements"])
                    for obligation in item["obligations"]:
                        self.assertNotEqual((obligation["owner"], obligation["field"]), ("AR-026", "/acceptance_criteria/2"))
            self.assertIn("IF-004", scenario["interfaces"])
            self.assertIn("MOD-018", scenario["context_modules"])
        expected = scenarios["SCN-046"]["outcomes"][0]
        self.assertNotIn("AR-018", expected["allocated_requirements"])
        self.assertEqual(expected["limit_sources"], [])
        self.assertEqual([edge.source for edge in model.incoming("IF-003", "provides")], ["MOD-011"])
        self.assertEqual([edge.source for edge in model.incoming("IF-004", "provides")], ["MOD-018"])

    def test_scenario_named_selectors_follow_reordering_and_source_text_changes(self):
        model = Model(self.fixture())
        scenario = next(item for item in model.architecture_views()["scenarios"]["scenarios"] if item["scenario"] == "SCN-046")
        original = scenario_profiles.scenario_outcomes(model, scenario)
        model.records["SCN-046"].data["expected_outcome"] += " Updated canonical outcome."
        model.records["AR-021"].data["acceptance_criteria"][1] += " Updated canonical criterion."
        interaction = model.facets[("IF-003", "interaction")].data["observed"]
        interaction["sequences"].reverse()
        publication = next(item for item in interaction["sequences"] if item["operation"] == "execute_record_task")
        publication["steps"].reverse()
        for owner in ("MOD-010", "MOD-011"):
            observed = model.facets[(owner, "software")].data["observed"]
            observed["software_units"].reverse()
            observed["test_groups"].reverse()
        model.facets[("MOD-010", "deployment")].data["observed"]["physical_bindings"][0]["accesses"].reverse()
        changed = scenario_profiles.scenario_outcomes(model, scenario)
        self.assertTrue(changed[0]["outcome"].endswith(" Updated canonical outcome."))
        criterion = next(item for item in changed[0]["obligations"] if (item["owner"], item["field"]) == ("AR-021", "/acceptance_criteria/1"))
        self.assertTrue(criterion["text"].endswith(" Updated canonical criterion."))
        self.assertNotEqual(original[0]["realization"]["process"][0]["field"], changed[0]["realization"]["process"][0]["field"])
        self.assertEqual([self.resolve_outcome_source(model, ref)["name"] for ref in changed[0]["realization"]["process"]], ["Construct and recheck candidate", "Publish complete candidate", "Commit durable transaction", "Clean up and return receipt"])
        self.assertEqual([self.resolve_outcome_source(model, ref)["name"] for ref in changed[0]["test_context"]], ["Public recording interaction composition", "Guarded publication and exact recovery"])
        self.assertEqual([self.resolve_outcome_source(model, ref)["placement"]["name"] for ref in changed[0]["realization"]["physical"][:2]], ["Registered operational records", "Record transaction metadata"])

    def test_scenario_profile_admission_rejects_unknown_shapes_before_consistency(self):
        root = self.fixture()
        model = Model(root)
        scenario = next(item for item in model.architecture_views()["scenarios"]["scenarios"] if item["scenario"] == "SCN-046")
        cases = [
            (lambda p: p.update(unrecognized=True), "unsupported outcome profile shape"),
            (lambda p: p["realization"].update(sequence=[]), "unsupported outcome profile shape"),
            (lambda p: p["realization"]["process"][0].update(unknown=True), "unsupported source selector shape"),
            (lambda p: p["realization"]["process"][0].update(facet="invented"), "incompatible realization concern"),
            (lambda p: p["realization"]["process"][0].update(facet=[]), "owner and facet must be nonblank"),
            (lambda p: p["realization"]["process"][0].update(owner={}), "owner and facet must be nonblank"),
            (lambda p: p["realization"]["process"][0].update(selection=("observed", [])), "unsupported realization field"),
            (lambda p: p["realization"]["process"][0].update(selection=("observed", "sequences", ("/operation", None))), "unsupported named selector"),
            (lambda p: p["test_context"][0].update(selection=("observed", "test_groups")), "one whole named test group"),
            (lambda p: p["test_context"][0].update(selection=("observed", "test_groups", ("/name", "Public recording interaction composition"), "name")), "one whole named test group"),
            (lambda p: p["realization"]["development"][0].update(selection=("observed", "test_groups", 0)), "unsupported realization field"),
            (lambda p: p.update(gaps=[""]), "reading limits must be nonblank"),
        ]
        before = snapshot(root)
        for mutate, message in cases:
            with self.subTest(message=message):
                profiles = deepcopy(scenario_profiles.OUTCOME_PROFILES)
                # Earlier obligation consistency must not hide a later shape error.
                profiles["SCN-046"]["expected"]["obligations"] = [("SR-999", 0)]
                mutate(profiles["SCN-047"]["failure-1"])
                with patch.object(scenario_profiles, "OUTCOME_PROFILES", profiles):
                    with self.assertRaisesRegex(ValueError, message):
                        scenario_profiles.scenario_outcomes(model, scenario)
        for invalid_key in ("unknown_value", "alternative--1", "failure-01", 0):
            profiles = deepcopy(scenario_profiles.OUTCOME_PROFILES)
            profiles["SCN-046"]["expected"]["obligations"] = [("SR-999", 0)]
            profiles["SCN-047"][invalid_key] = deepcopy(profiles["SCN-047"]["expected"])
            with patch.object(scenario_profiles, "OUTCOME_PROFILES", profiles):
                with self.assertRaisesRegex(ValueError, "unsupported outcome selector vocabulary"):
                    scenario_profiles.scenario_outcomes(model, scenario)
        self.assertEqual(snapshot(root), before)

    def test_scenario_profile_missing_scope_criteria_and_sources_reject_without_writes(self):
        root = self.fixture()
        model = Model(root)
        scenario = next(item for item in model.architecture_views()["scenarios"]["scenarios"] if item["scenario"] == "SCN-046")
        cases = [
            (lambda p: p.update(obligations=[("FUNC-042", 0)]), "incompatible or missing obligation"),
            (lambda p: p.update(obligations=[("SR-001", 0)]), "outside informed requirement scope"),
            (lambda p: p.update(obligations=[("AR-022", 0)]), "outside informed requirement scope"),
            (lambda p: p.update(obligations=[("AR-021", 999)]), "missing criterion"),
            (lambda p: p.update(obligations=[("AR-021", 1), ("AR-021", 1)]), "duplicate criterion selector"),
            (lambda p: p.update(limit_sources=[("SR-001", 0)]), "outside informed requirement scope"),
            (lambda p: p["realization"]["process"][0].update(owner="MOD-014"), "outside selected scope"),
            (lambda p: p["realization"]["process"][0].update(selection=("observed", "sequences", ("/operation", "missing"))), "missing or ambiguous named detail"),
            (lambda p: p["realization"]["process"][0].update(selection=("observed", "sequences", 999)), "unresolved source selection"),
            (lambda p: p["realization"]["process"].append(deepcopy(p["realization"]["process"][0])), "duplicate source selector"),
        ]
        before = snapshot(root)
        for mutate, message in cases:
            with self.subTest(message=message):
                profiles = deepcopy(scenario_profiles.OUTCOME_PROFILES)
                mutate(profiles["SCN-046"]["expected"])
                with patch.object(scenario_profiles, "OUTCOME_PROFILES", profiles):
                    with self.assertRaisesRegex(ValueError, message):
                        scenario_profiles.scenario_outcomes(model, scenario)
        sequences = model.facets[("IF-003", "interaction")].data["observed"]["sequences"]
        sequences.append(deepcopy(sequences[0]))
        with self.assertRaisesRegex(ValueError, "missing or ambiguous named detail"):
            scenario_profiles.scenario_outcomes(model, scenario)
        self.assertEqual(snapshot(root), before)

    def test_scenario_profile_reconciles_outcome_set_and_labels_empty_selections_as_reading_gaps(self):
        model = Model(self.fixture())
        scenario = next(item for item in model.architecture_views()["scenarios"]["scenarios"] if item["scenario"] == "SCN-046")
        profiles = deepcopy(scenario_profiles.OUTCOME_PROFILES)
        del profiles["SCN-046"]["failure-2"]
        with patch.object(scenario_profiles, "OUTCOME_PROFILES", profiles):
            with self.assertRaisesRegex(ValueError, "exactly match canonical outcomes"):
                scenario_profiles.scenario_outcomes(model, scenario)
        profiles = deepcopy(scenario_profiles.OUTCOME_PROFILES)
        profiles["SCN-999"] = {}
        with patch.object(scenario_profiles, "OUTCOME_PROFILES", profiles):
            with self.assertRaisesRegex(ValueError, "unsupported profiled Scenario"):
                scenario_profiles.scenario_outcomes(model, scenario)
        model.records["SCN-046"].data["failures"].append({"condition": "New authored condition", "outcome": "New authored outcome"})
        with self.assertRaisesRegex(ValueError, "exactly match canonical outcomes"):
            scenario_profiles.scenario_outcomes(model, scenario)
        model.records["SCN-046"].data["failures"].pop()
        profiles = deepcopy(scenario_profiles.OUTCOME_PROFILES)
        profiles["SCN-046"]["expected"]["realization"] = {"process": [], "development": [], "physical": []}
        profiles["SCN-046"]["expected"]["test_context"] = []
        with patch.object(scenario_profiles, "OUTCOME_PROFILES", profiles):
            expected = scenario_profiles.scenario_outcomes(model, scenario)[0]
        for label in ("Process", "Development", "Physical", "contextual test group"):
            self.assertTrue(any(f"No {label} detail is selected" in gap and "does not establish absent" in gap for gap in expected["gaps"]))

    def test_physical_references_and_closed_modes_reject_without_writes(self):
        root = self.fixture()
        path = self.entity_path(root, "MOD-010").parent / "realization/deployment.json"
        original = json.loads(path.read_text())
        Model(root)
        cases = [
            (lambda b: b["execution"].update(name="Invented process"), "missing scoped execution reference"),
            (lambda b: b["package"].update(owner="IF-003"), "wrong-type reference IF-003"),
            (lambda b: b["package"].update(name="Unrecorded package"), "scoped placement reference"),
            (lambda b: b["package"].update(facet="unknown", owner="MOD-999"), "unknown placement reference facet"),
            (lambda b: b["accesses"][0].update(participant="MOD-013"), "access participant is outside"),
            (lambda b: b["accesses"][0].update(mode="execute", placement={"owner":"MOD-999", "facet":"persistence", "name":"Absent"}), "unknown Physical access mode"),
            (lambda b: b["accesses"][0]["placement"].update(name="Unrecorded storage"), "scoped placement reference"),
            (lambda b: b.update(host="assumed-host"), "unsupported Physical structure shape"),
        ]
        for mutate, expected in cases:
            with self.subTest(expected=expected):
                changed = deepcopy(original)
                mutate(changed["observed"]["physical_bindings"][0])
                self.write_record(path, changed)
                error = self.assert_invalid_model(root, expected)

    def test_physical_production_isolation_and_acquisition_resolve_exact_contexts(self):
        root = self.fixture()
        producer = self.entity_path(root, "MOD-013").parent / "realization/deployment.json"
        contract = self.entity_path(root, "IF-006").parent / "realization/interaction.json"
        producer_data, contract_data = json.loads(producer.read_text()), json.loads(contract.read_text())
        cases = [
            (producer, producer_data, lambda o: o["production_placement"].update(output=deepcopy(o["production_placement"]["source"])), "production roles require distinct"),
            (producer, producer_data, lambda o: o["location_constraints"][0].update(relation="same-host"), "unknown Physical location relation"),
            (producer, producer_data, lambda o: o["location_constraints"][0]["placements"].__setitem__(1, deepcopy(o["location_constraints"][0]["placements"][0])), "location relation requires distinct"),
            (producer, producer_data, lambda o: o["placements"].append(deepcopy(o["placements"][0])), "duplicate local Physical name"),
            (contract, contract_data, lambda o: o["artifact_acquisition"].update(participant="MOD-011"), "acquisition participant is outside the Interface provider boundary"),
        ]
        for path, original, mutate, expected in cases:
            with self.subTest(expected=expected):
                changed = deepcopy(original)
                mutate(changed["observed"])
                self.write_record(path, changed)
                error = self.assert_invalid_model(root, expected)
                self.write_record(path, original)

    def test_invalid_process_sequence_references_and_shapes_reject_without_writes(self):
        root = self.fixture()
        path = self.entity_path(root, "IF-003").parent / "realization/interaction.json"
        original = json.loads(path.read_text())
        Model(root)

        def change(field, value):
            return lambda record: record["observed"]["sequences"][0].__setitem__(field, value)

        cases = [
            (change("operation", "invented_operation"), "unknown Process operation"),
            (change("participants", ["MOD-010", "SR-001"]), "wrong-type reference SR-001"),
            (change("participants", ["MOD-010", "MOD-013"]), "outside the Interface provider/consumer boundaries"),
            (change("participants", ["MOD-010"]), "no provider participant"),
            (lambda r: r["observed"]["sequences"][0]["steps"][0].update(participant="MOD-014"), "step participant is not declared"),
            (lambda r: r["observed"]["sequences"][0]["steps"].append(deepcopy(r["observed"]["sequences"][0]["steps"][0])), "duplicate local Process name"),
            (lambda r: r["observed"].pop("sources"), "Process observations require sources"),
            # Unsupported fields must reject even when a later reference is also bad.
            (lambda r: r["observed"]["sequences"][0].update(automatic_retry=True, participants=["MOD-999"]), "unsupported Process structure shape"),
        ]
        for mutation, expected in cases:
            with self.subTest(expected=expected):
                record = deepcopy(original)
                mutation(record)
                self.write_record(path, record)
                error = self.assert_invalid_model(root, expected)

    def test_process_terminal_branch_participants_and_state_endpoints_resolve(self):
        root = self.fixture()
        interaction = self.entity_path(root, "IF-003").parent / "realization/interaction.json"
        runtime = self.entity_path(root, "MOD-011").parent / "realization/runtime.json"
        original = json.loads(interaction.read_text())
        changed = deepcopy(original)
        branch = next(step["branches"][0] for step in changed["observed"]["sequences"][0]["steps"]
                      if step.get("branches"))
        branch["steps"][0]["participant"] = "MOD-999"
        self.write_record(interaction, changed)
        error = self.assert_invalid_model(root, "step participant is not declared")
        self.write_record(interaction, original)
        original = json.loads(runtime.read_text())
        for mutation, expected in [
            (lambda r: r["observed"]["lifecycles"][0]["transitions"][0].update(to="Invented phase"), "unknown state"),
            (lambda r: r["observed"]["lifecycles"][0]["states"].append(deepcopy(r["observed"]["lifecycles"][0]["states"][0])), "duplicate local Process name"),
            (lambda r: r["observed"]["lifecycles"][0]["transitions"].append(deepcopy(r["observed"]["lifecycles"][0]["transitions"][0])), "duplicate Process transition"),
        ]:
            with self.subTest(expected=expected):
                changed = deepcopy(original)
                mutation(changed)
                self.write_record(runtime, changed)
                error = self.assert_invalid_model(root, expected)

    def test_invalid_execution_relationships_reject_without_writes(self):
        root = self.fixture()
        Model(root)
        path = self.entity_path(root, "MOD-010").parent / "realization/runtime.json"
        original = json.loads(path.read_text())
        cases = [
            ("unknown shape before broken reference", {"worker_id": "missing", "modules": ["MOD-999"]}, "unsupported realization structure shape"),
            ("incompatible participant", {"modules": ["MOD-010", "SR-001"]}, "wrong-type reference SR-001: expected module"),
            ("external call endpoint", {"calls": [{"caller": "MOD-010", "callee": "MOD-013", "interface": "IF-003"}]}, "outside its process"),
            ("callee outside provider", {"calls": [{"caller": "MOD-010", "callee": "MOD-014", "interface": "IF-003"}]}, "outside the Interface provider boundary"),
            ("unconsumed contract", {"calls": [{"caller": "MOD-010", "callee": "MOD-011", "interface": "IF-004"}]}, "does not consume the Interface"),
            ("unrelated entry", {"entry_interfaces": ["IF-005"]}, "entry Interface provider has no execution participant"),
        ]
        for title, changes, message in cases:
            with self.subTest(title=title):
                changed = deepcopy(original)
                changed["observed"]["execution"].update(changes)
                self.write_record(path, changed)
                error = self.assert_invalid_model(root, message)

    def test_placement_references_resolve_without_changing_state_authority(self):
        root = self.fixture()
        path = self.entity_path(root, "MOD-011").parent / "realization/persistence.json"
        original = json.loads(path.read_text())
        for members, message in [(["MOD-999"], "missing reference"), (["MOD-010"], "must include its accountable owner")]:
            with self.subTest(members=members):
                changed = deepcopy(original)
                changed["observed"]["placements"][0]["modules"] = members
                self.write_record(path, changed)
                error = self.assert_invalid_model(root, message)

    def test_invalid_exposure_is_rejected_without_writes(self):
        cases = (
            ("nonancestor", "IF-004", ["MOD-019"], "strict provider ancestor"),
            ("self", "IF-004", ["MOD-010"], "strict provider ancestor"),
            ("wrong_type", "IF-004", ["FEAT-001"], "wrong-type reference"),
            ("missing_target", "IF-004", ["MOD-999999"], "missing reference"),
            ("duplicate", "IF-004", ["MOD-018", "MOD-018"], "unique"),
            ("empty", "IF-004", [], "nonempty"),
            ("missing_boundary", "IF-006", None, "missing exposure"),
            ("skipped_boundary", "IF-004", ["MOD-018"], "skipped exposure"),
        )
        for name, identity, exposure, diagnostic in cases:
            with self.subTest(case=name):
                root = self.fixture()
                if identity == "IF-004":
                    self.select_child_provider(root, identity, "MOD-010", ["MOD-018"])
                else:
                    self.select_child_provider(root, identity, "MOD-014", ["MOD-019"])
                if name == "skipped_boundary":
                    self.nested_command_group(root)
                Model(root)
                path = self.entity_path(root, identity)
                record = json.loads(path.read_text())
                if exposure is None:
                    record.pop("exposed_through", None)
                else:
                    record["exposed_through"] = exposure
                self.write_record(path, record)
                error = self.assert_invalid_model(root, diagnostic)

    def test_invalid_nested_layout_is_rejected_without_writes(self):
        for malformed, diagnostic in (("stray", "unexpected architecture JSON"),
                                      ("catalog_neighbor", "unexpected architecture JSON"),
                                      ("orphan", "missing logical owner"),
                                      ("duplicate", "duplicate identity"),
                                      ("cycle", "symlink")):
            with self.subTest(case=malformed):
                root = self.fixture()
                Model(root)
                module = self.entity_path(root, "MOD-018").parent
                if malformed == "stray":
                    self.write_record(module / "unexpected.json", {})
                elif malformed == "catalog_neighbor":
                    owner = self.entity_path(root, "MOD-008").parent
                    self.write_record(owner / "test-design/cases/unregistered.json", {})
                elif malformed == "orphan":
                    (module / "modules/MOD-020-orphan/modules").mkdir(parents=True)
                elif malformed == "duplicate":
                    copied = self.entity_path(root, "MOD-004").parent
                    shutil.copytree(copied, module / "modules" / copied.name)
                else:
                    (module / "modules/cycle").symlink_to(module, target_is_directory=True)
                error = self.assert_invalid_model(root, diagnostic)

    def test_invalid_references_are_rejected_without_writes(self):
        for target, diagnostic in (
            ("MOD-999999", "missing reference"),
            ("FEAT-001", "wrong-type reference"),
        ):
            with self.subTest(target=target):
                root = self.fixture()
                Model(root)
                path = self.entity_path(root, "FUNC-001")
                function = json.loads(path.read_text())
                function["allocated_to"] = target
                self.write_record(path, function)
                error = self.assert_invalid_model(root, diagnostic)
                self.assertIn(target, error)

    def test_unknown_projection_vocabulary_is_rejected_without_writes(self):
        for field, value, diagnostic in (
            ("type", "unrecognized-entity", "unsupported type"),
            ("status", "unrecognized-state", "unsupported status"),
            ("facet_state", "asserted", "unsupported"),
        ):
            with self.subTest(field=field):
                root = self.fixture()
                path = self.entity_path(root, "MOD-010")
                if field == "facet_state":
                    path = path.parent / "realization/runtime.json"
                    record = json.loads(path.read_text())
                    record[value] = {}
                else:
                    record = json.loads(path.read_text())
                    record[field] = value
                self.write_record(path, record)
                error = self.assert_invalid_model(root, diagnostic)
                self.assertIn(value, error)

    def test_public_catalog_invalid_inputs_fail_without_writes(self):
        cases = (
            ("unknown_relation", "unsupported public entry relation"),
            ("wrong_function_type", "wrong-type reference"),
            ("missing_function", "missing reference"),
            ("duplicate_function_relation", "duplicate public Function/relation mapping"),
            ("duplicate_entry", "duplicate observed public entry name"),
            ("duplicate_mapping", "duplicate public entry mapping"),
            ("missing_mapping", "missing public entry mappings"),
            ("unknown_entry", "missing observed public entry"),
            ("missing_operation", "missing Interface operation"),
            ("unsafe_source", "unsafe public entry path"),
            ("missing_source", "missing or unsafe public entry path"),
            ("unmapped_without_limit", "unmapped public entry requires explicit limits"),
            ("explicit_null_entries", "public_entries must be a nonempty array"),
        )
        for case, diagnostic in cases:
            with self.subTest(case=case):
                root = self.fixture()
                Model(root)
                path, facet = self.public_facet(root, "IF-004")
                entries = facet["observed"]["public_entries"]
                mappings = next(choice["public_entry_mappings"] for choice in facet["proposed"] if "public_entry_mappings" in choice)
                mapping = mappings[0]
                if case == "unknown_relation":
                    mapping["functions"][0].update(relation="approves", function="FUNC-999999")
                elif case == "wrong_function_type":
                    mapping["functions"][0]["function"] = "MOD-010"
                elif case == "missing_function":
                    mapping["functions"][0]["function"] = "FUNC-999999"
                elif case == "duplicate_function_relation":
                    mapping["functions"].append(dict(mapping["functions"][0]))
                elif case == "duplicate_entry":
                    entries.append(dict(entries[0]))
                elif case == "duplicate_mapping":
                    mappings.append(json.loads(json.dumps(mapping)))
                elif case == "missing_mapping":
                    mappings.pop()
                elif case == "unknown_entry":
                    mapping["entry"] = "unobserved-command"
                elif case == "missing_operation":
                    entries[0]["operation"] = "unrecognized_operation"
                elif case == "unsafe_source":
                    entries[0]["source_path"] = "../outside.md"
                elif case == "missing_source":
                    entries[0]["source_path"] = "skills/missing-entry/SKILL.md"
                elif case == "explicit_null_entries":
                    facet["observed"]["public_entries"] = None
                    for choice in facet["proposed"]:
                        choice.pop("public_entry_mappings", None)
                else:
                    mapping.update(functions=[], limits=[])
                self.write_record(path, facet)
                error = self.assert_invalid_model(root, diagnostic)
                if case == "unknown_relation":
                    self.assertNotIn("missing reference", error)

    def test_containment_and_rollups_preserve_exact_accountable_owners(self):
        root = self.fixture()
        self.nested_command_group(root)
        before = snapshot(root)
        projected = self.projected(root)
        expected = {"MOD-016": None, "MOD-017": None, "MOD-018": None, "MOD-019": None,
                    **{f"MOD-{i:03}": "MOD-016" for i in range(1, 5)},
                    **{f"MOD-{i:03}": "MOD-017" for i in range(5, 10)},
                    "MOD-020": "MOD-018", "MOD-010": "MOD-020",
                    "MOD-011": "MOD-018", "MOD-012": "MOD-018",
                    **{f"MOD-{i:03}": "MOD-019" for i in range(13, 16)}}
        self.assertEqual({identity: item["parent"] for identity, item in projected["modules"].items()}, expected)
        self.assertEqual(projected["roots"], ["MOD-016", "MOD-017", "MOD-018", "MOD-019"])
        for identity, parent in expected.items():
            if parent:
                self.assertIn(identity, projected["modules"][parent]["children"])
            canonical = json.loads(self.entity_path(root, identity).read_text())
            self.assertEqual(projected["records"][identity]["data"], canonical)
        parent = projected["modules"]["MOD-018"]
        self.assertEqual(parent["functions"], [])
        self.assertEqual(parent["allocated_requirements"], [])
        self.assertEqual(parent["subtree_functions"],
                         [f"FUNC-{i:03}" for i in range(40, 56)] + ["FUNC-074", "FUNC-075", "FUNC-076"])
        self.assertEqual(parent["subtree_allocated_requirements"],
                         [f"AR-{i:03}" for i in range(11, 29)] +
                         ["AR-030", "AR-032", "AR-034", "AR-037", "AR-039", "AR-040", "AR-051", "AR-052", "AR-053", "AR-054", "AR-055"])
        self.assertIn("FUNC-046", projected["modules"]["MOD-011"]["functions"])
        self.assertIn("FUNC-046", parent["subtree_functions"])
        for identity in ("FUNC-074", "FUNC-075", "FUNC-076"):
            self.assertEqual([owner for owner, item in projected["modules"].items() if identity in item["functions"]], ["MOD-011"])
        for identity in ("AR-052", "AR-053", "AR-054", "AR-055"):
            self.assertEqual([owner for owner, item in projected["modules"].items() if identity in item["allocated_requirements"]], ["MOD-011"])
        self.assertEqual(snapshot(root), before)

    def test_overview_collaboration_keeps_parent_contract_ownership(self):
        projected = self.projected(self.fixture())
        collaboration = projected["overview_collaborations"]
        self.assertEqual({item["interface"] for item in collaboration},
                         {"IF-006", "IF-007", "IF-008", "IF-009", "IF-010", "IF-011", "IF-012"})
        self.assertEqual(len(collaboration), 9)
        self.assertEqual({(item["interface"], item["consumer"], item["provider"])
                          for item in collaboration if item["consumer"] == "MOD-012"},
                         {(identity, "MOD-012", "MOD-017")
                          for identity in ("IF-008", "IF-009", "IF-010", "IF-011")})
        self.assertTrue(all(item["consumer_boundary"] in projected["roots"] and
                            item["provider_boundary"] in projected["roots"] for item in collaboration))
        self.assertEqual(projected["interfaces"]["IF-004"]["provider"], "MOD-018")
        self.assertEqual(projected["interfaces"]["IF-006"]["provider"], "MOD-019")
        for owner, function in (("MOD-010", "FUNC-048"), ("MOD-011", "FUNC-046"), ("MOD-014", "FUNC-064")):
            self.assertIn(function, projected["modules"][owner]["functions"])
        for identity in ("SCN-046", "SCN-047"):
            selected = next(item for item in projected["views"]["scenarios"]["scenarios"] if item["scenario"] == identity)
            context = next(item for item in selected["contract_context"] if item["interface"] == "IF-004")
            self.assertEqual(context["provider"], "MOD-018")
            self.assertEqual(context["relationship"]["relation"], "provides")
            self.assertEqual(context["relationship"]["field"], "/provides/0")
            self.assertNotIn("MOD-018", selected["modules"])

    def test_limits_empty_allocations_and_owned_state_remain_source_facts(self):
        root = self.fixture()
        path = self.entity_path(root, "MOD-017")
        module = json.loads(path.read_text())
        limit = "Review the responsibilities across this boundary before extending its contracts."
        module["design_limits"].append(limit)
        self.write_record(path, module)
        projected = self.projected(root)
        self.assertIn(limit, projected["records"]["MOD-017"]["data"]["design_limits"])
        for identity in ("MOD-005", "MOD-009"):
            self.assertEqual(projected["modules"][identity]["allocated_requirements"], [])
            self.assertEqual(projected["modules"][identity]["subtree_allocated_requirements"], [])
        for identity, allocated in {
            "MOD-006": ["AR-035", "AR-038"],
            "MOD-007": ["AR-031", "AR-036"],
            "MOD-008": ["AR-029", "AR-033"],
            "MOD-012": ["AR-030", "AR-032", "AR-034", "AR-037", "AR-039"],
            "MOD-013": ["AR-041", "AR-049"],
            "MOD-015": ["AR-050"],
            "MOD-014": ["AR-042"],
        }.items():
            self.assertEqual(projected["modules"][identity]["allocated_requirements"], allocated)
            self.assertEqual(projected["modules"][identity]["subtree_allocated_requirements"], allocated)
        self.assertEqual(projected["modules"]["MOD-017"]["allocated_requirements"], [])
        self.assertEqual(projected["modules"]["MOD-017"]["subtree_allocated_requirements"],
                         ["AR-029", "AR-031", "AR-033", "AR-035", "AR-036", "AR-038"])
        self.assertEqual(projected["records"]["MOD-017"]["data"]["owned_state"], [])

    def test_deeper_hierarchy_and_direct_parent_allocation_are_supported(self):
        root = self.fixture()
        self.nested_command_group(root)
        path = self.entity_path(root, "FUNC-040")
        function = json.loads(path.read_text())
        function["allocated_to"] = "MOD-020"
        self.write_record(path, function)
        projected = self.projected(root)
        self.assertIn("FUNC-040", projected["modules"]["MOD-020"]["functions"])
        self.assertNotIn("FUNC-040", projected["modules"]["MOD-010"]["functions"])
        self.assertIn("FUNC-040", projected["modules"]["MOD-018"]["subtree_functions"])
        self.assertEqual(projected["interfaces"]["IF-004"]["provider"], "MOD-010")
        self.assertEqual(projected["interfaces"]["IF-004"]["exposed_through"], ["MOD-020", "MOD-018"])
        self.assertNotIn("IF-004", projected["modules"]["MOD-018"]["provides"])
        self.assertIn("IF-004", projected["modules"]["MOD-018"]["exposed_interfaces"])

    def test_current_names_and_allocations_replace_previous_derived_context(self):
        root = self.fixture()
        before = self.projected(root)
        self.assertIn("FUNC-001", before["modules"]["MOD-001"]["functions"])
        self.assertNotIn("FUNC-001", before["modules"]["MOD-002"]["functions"])
        path = self.entity_path(root, "MOD-001")
        module = json.loads(path.read_text())
        module["title"] = "Retained engineering definition repository"
        self.write_record(path, module)
        retained_path = path.relative_to(root).as_posix()
        path = self.entity_path(root, "FUNC-001")
        function = json.loads(path.read_text())
        function["allocated_to"] = "MOD-002"
        self.write_record(path, function)
        after = self.projected(root)
        self.assertEqual(after["records"]["MOD-001"]["data"]["title"], module["title"])
        self.assertEqual(after["records"]["MOD-001"]["path"], retained_path)
        self.assertNotIn("FUNC-001", after["modules"]["MOD-001"]["functions"])
        self.assertIn("FUNC-001", after["modules"]["MOD-002"]["functions"])
        self.assertNotEqual(before["source_digest"], after["source_digest"])

    def test_retained_module_paths_still_reject_wrong_identity_and_malformed_suffix(self):
        for dirname in ("MOD-999-definition-storage", "MOD-001-", "MOD-001-invalid--suffix"):
            with self.subTest(directory=dirname):
                root = self.fixture()
                path = self.entity_path(root, "MOD-001")
                path.parent.rename(path.parent.with_name(dirname))
                with self.assertRaisesRegex(ValueError, "owner directory does not match identity and retained slug"):
                    Model(root)

    def test_supported_obsolete_scenario_and_explicit_allocation_gap_are_preserved(self):
        root = self.fixture()
        path = self.entity_path(root, "SCN-001")
        scenario = json.loads(path.read_text())
        scenario["status"] = "obsolete"
        self.write_record(path, scenario)
        path = self.entity_path(root, "FUNC-001")
        function = json.loads(path.read_text())
        del function["allocated_to"]
        function["unallocated_reason"] = "Architecture responsibility awaits an agreed storage boundary."
        self.write_record(path, function)
        before = snapshot(root)
        projected = self.projected(root)
        self.assertEqual(projected["records"]["SCN-001"]["data"]["status"], "obsolete")
        self.assertEqual(projected["records"]["FUNC-001"]["data"]["unallocated_reason"], function["unallocated_reason"])
        self.assertNotIn("FUNC-001", projected["modules"]["MOD-001"]["functions"])
        self.assertFalse(any(edge["source"] == "FUNC-001" and edge["relation"] == "allocated_to"
                             for edge in projected["relationships"]))
        self.assertEqual(snapshot(root), before)

    def test_scenario_context_does_not_inherit_unselected_ancestor_contracts(self):
        root = self.fixture()
        path = self.entity_path(root, "IF-004")
        record = json.loads(path.read_text())
        record.update(id="IF-999", title="Other ancestor contract")
        extra = path.parent.parent / "IF-999-other-ancestor-contract/interface.json"
        extra.parent.mkdir()
        self.write_record(extra, record)
        path = self.entity_path(root, "MOD-018")
        parent = json.loads(path.read_text())
        parent["provides"].append("IF-999")
        self.write_record(path, parent)
        projected = self.projected(root)
        self.assertIn("IF-999", projected["interfaces"])
        for selected in projected["views"]["scenarios"]["scenarios"]:
            self.assertNotIn("IF-999", selected["interfaces"])
            self.assertNotIn("IF-999", [item["interface"] for item in selected["contract_context"]])

    def test_scenario_contracts_preserve_scope_providers_outcomes_and_provenance(self):
        root = self.fixture()
        projected = self.projected(root)
        slices = {item["scenario"]: item for item in projected["views"]["scenarios"]["scenarios"]}
        expected = {
            "SCN-019": ({"IF-007"}, {"IF-007": "MOD-016"}, {"MOD-005"}),
            "SCN-046": ({"IF-003", "IF-004"}, {"IF-004": "MOD-018"}, {"MOD-010", "MOD-011"}),
            "SCN-047": ({"IF-003", "IF-004"}, {"IF-004": "MOD-018"}, {"MOD-010", "MOD-011"}),
            "SCN-053": ({"IF-008"}, {"IF-008": "MOD-017"}, {"MOD-008", "MOD-012"}),
            "SCN-066": ({"IF-005", "IF-009", "IF-010"},
                        {"IF-005": "MOD-013", "IF-009": "MOD-017", "IF-010": "MOD-017"}, {"MOD-006", "MOD-015"}),
        }
        self.assertEqual(set(slices), set(expected))
        for identity, (interfaces, providers, participants) in expected.items():
            with self.subTest(scenario=identity):
                selected = slices[identity]
                self.assertEqual(set(selected["interfaces"]), interfaces)
                self.assertEqual(set(selected["modules"]), participants)
                self.assertEqual(set(selected["context_modules"]), set(providers.values()))
                self.assertEqual({item["interface"]: item["provider"] for item in selected["contract_context"]}, providers)
                self.assertFalse(set(selected["modules"]) & set(selected["context_modules"]))
                self.assertTrue({ref["owner"] for ref in selected["facet_refs"]} <= participants | set(providers.values()) | interfaces)
                canonical = json.loads(self.entity_path(root, identity).read_text())
                self.assertEqual(projected["records"][identity]["data"], canonical)
                self.assertTrue(canonical["expected_outcome"])
                for context in selected["contract_context"]:
                    self.assertEqual(context["relationship"]["relation"], "provides")
                    self.assertTrue(context["relationship"]["field"].startswith("/provides/"))
                    kinds = {reason["kind"] for reason in context["reasons"]}
                    if identity in ("SCN-046", "SCN-047"):
                        self.assertEqual(kinds, {"ancestor"})
                    else:
                        self.assertIn("consumer", kinds)
                    for reason in context["reasons"]:
                        if reason["kind"] == "ancestor":
                            self.assertTrue(reason["containment"])
                            self.assertTrue(all(edge["relation"] == "contained_by" for edge in reason["containment"]))
                        else:
                            self.assertEqual(reason["kind"], "consumer")
                            self.assertTrue(reason["relationship"]["field"].startswith("/consumes/"))
                for owner in participants | set(providers.values()):
                    self.assertTrue(set(projected["records"][owner]["data"]["design_limits"]) <= set(selected["limits"]))
                for edge in selected["relationships"]:
                    self.assertIn(edge, projected["relationships"])
                    self.assertTrue((root / edge["path"]).is_file())
                    self.assertTrue(edge["field"].startswith("/") or edge["field"] == "containment")
                self.assertTrue(any("not execution order" in limit for limit in selected["limits"]))
        # Retired text included these contracts' guarantees and failure behavior.
        # Browser detail must retain the authored operations and provenance whole.
        for identity in ("IF-003", "IF-004"):
            canonical = json.loads(self.entity_path(root, identity).read_text())
            self.assertEqual(projected["records"][identity]["data"], canonical)
            for operation in canonical["operations"]:
                self.assertTrue(operation["behavior"])
                self.assertTrue(operation["failure_behavior"])
            self.assertTrue(canonical["sources"])
        self.assertTrue({"preview_record_task", "execute_record_task"}
                        <= {item["name"] for item in projected["records"]["IF-003"]["data"]["operations"]})

    def test_all_cli_contribution_arguments_preserve_criteria_allocations_and_sources(self):
        root = self.fixture()
        projected = self.projected(root)
        expected = {(record["id"], index): source
                    for path in (root / "design/requirements").rglob("sr.json")
                    for record in [json.loads(path.read_text())]
                    for index, source in enumerate(record["sources"])
                    if source["source"] == "SRC-CLI-ALLOCATION"}
        contributions = projected["cli_contributions"]
        historical = {(record["id"], index): source
                      for path in (root / "design/requirements").rglob("sr.json")
                      for record in [json.loads(path.read_text())]
                      for index, source in enumerate(record["sources"])
                      if source["source"] == "SRC-CLI-ALLOCATION-BEFORE-LOCAL-STORE"}
        self.assertTrue(expected, "Fixture must exercise current contribution projection")
        self.assertTrue(historical, "Fixture must distinguish retained history from current coverage")
        self.assertEqual(len(contributions), len(expected))
        actual = {(item["requirement"], int(item["source_pointer"].split("/")[-1])): item for item in contributions}
        self.assertEqual(set(actual), set(expected))
        self.assertTrue(set(actual).isdisjoint(historical))
        for (identity, index), source in historical.items():
            self.assertEqual(projected["records"][identity]["data"]["sources"][index], source)
        for key, source in expected.items():
            item = actual[key]
            self.assertEqual((item["locator"], item["basis"]), (source["locator"], source["basis"]))
            requirement = projected["records"][key[0]]["data"]
            self.assertEqual(item["criterion_text"], requirement["acceptance_criteria"][item["criterion"] - 1])
            self.assertTrue(item["allocated_requirements"])
            self.assertEqual(set(item["allocated_requirements"]), set(re.findall(r"AR-\d+", source["locator"])))
            self.assertTrue(all(projected["records"][identity]["data"]["type"] == "allocated-requirement"
                                for identity in item["allocated_requirements"]))

    def test_process_participation_keeps_parent_contract_ownership_separate_from_execution(self):
        root = self.fixture()
        child_path, parent_path = self.entity_path(root, "MOD-011"), self.entity_path(root, "MOD-018")
        child, parent = json.loads(child_path.read_text()), json.loads(parent_path.read_text())
        child["provides"].remove("IF-003")
        parent["provides"].append("IF-003")
        self.write_record(child_path, child)
        self.write_record(parent_path, parent)
        model, helper = self.projection_model(root)
        sequence = model.facets[("IF-003", "interaction")].data["observed"]["sequences"][0]
        self.assertEqual(sequence["participants"], ["MOD-010", "MOD-011"])
        projected = helper.build_model(model)
        self.assertEqual(projected["interfaces"]["IF-003"]["provider"], "MOD-018")
        self.assertEqual(self.facet(projected, "IF-003", "interaction")["data"]["observed"]["sequences"][0], sequence)
        self.assertNotIn("#module/MOD-018", helper.diagram_sources(model)["process-publication"])

    def test_execution_and_physical_placement_preserve_exact_actors_and_qualifiers(self):
        root = self.fixture()
        model, helper = self.projection_model(root)
        projected = helper.build_model(model)
        execution = self.facet(projected, "MOD-010", "runtime")["data"]["observed"]["execution"]
        self.assertEqual(set(execution["modules"]), {"MOD-010", "MOD-011", "MOD-014"})
        self.assertIn({"caller": "MOD-010", "callee": "MOD-014", "interface": "IF-006"}, execution["calls"])
        self.assertEqual(projected["interfaces"]["IF-006"]["provider"], "MOD-019")
        self.assertEqual(projected["modules"]["MOD-014"]["provides"], [])
        selected = {(item["owner"], item["facet"]) for item in projected["views"]["physical"]["facet_refs"]}
        self.assertTrue({("MOD-010", "runtime"), ("IF-006", "interaction")} <= selected)
        binding = self.facet(projected, "MOD-010", "deployment")["data"]["observed"]["physical_bindings"][0]
        self.assertEqual({access["participant"] for access in binding["accesses"]}, {"MOD-010", "MOD-011", "MOD-014"})
        self.assertEqual(len(binding["accesses"]), 5)
        acquisition = self.facet(projected, "IF-006", "interaction")["data"]["observed"]["artifact_acquisition"]
        self.assertEqual([source["transport"] for source in acquisition["sources"]], ["HTTPS", "Local filesystem"])
        relations = {item["relation"] for facet in projected["facets"]
                     for item in facet["data"].get("observed", {}).get("location_constraints", [])}
        self.assertEqual(relations, {"same-filesystem", "disjoint"})
        for facet in projected["facets"]:
            canonical = model.facets[(facet["owner"], facet["facet"])]
            self.assertEqual(facet["data"], canonical.data)
            self.assertEqual(facet["path"], canonical.path.as_posix())

    def test_development_preserves_shared_software_responsibilities(self):
        root = self.fixture()
        projected = self.projected(root)
        shared = "packages/rigorloop/dist/lib/operational-contract.js"
        roles = {}
        for owner in ("MOD-010", "MOD-011"):
            canonical = json.loads((self.entity_path(root, owner).parent / "realization/software.json").read_text())
            expected = next(unit for unit in canonical["observed"]["software_units"] if unit["path"] == shared)
            observed = self.facet(projected, owner, "software")["data"]["observed"]["software_units"]
            self.assertIn(expected, observed)
            roles[owner] = expected["role"]
        self.assertNotEqual(roles["MOD-010"], roles["MOD-011"])

    def test_test_architecture_retains_subjects_and_sources_without_logical_allocation(self):
        root = self.fixture()
        model = Model(root)
        groups = model.architecture_views()["development"]["test_groups"]
        self.assertEqual({item["owner"] for item in groups}, {"MOD-010", "MOD-011", "MOD-013", "MOD-014"})
        self.assertEqual(len(groups), 9)
        for item in groups:
            source = json.loads((root / item["path"]).read_text())
            index = int(item["field"].split("/")[-1])
            self.assertEqual(item["group"], source["observed"]["test_groups"][index])
            self.assertEqual(item["group"]["execution"]["owner_contract"].split("#")[0],
                             "design/support/validation.md")
            self.assertTrue(source["observed"]["sources"])
        edges = model.edges
        for (owner, kind), facet in model.facets.items():
            if kind == "software" and "test_groups" in facet.data.get("observed", {}):
                changed = deepcopy(facet.data)
                del changed["observed"]["test_groups"]
                self.write_record(root / facet.path, changed)
        unannotated = Model(root)
        self.assertEqual(edges, unannotated.edges)
        self.assertEqual(model.records, unannotated.records)
        with self.assertRaisesRegex(ValueError, "unresolved source selection"):
            unannotated.architecture_views()
        # The canonical facet is optional; a reading profile explicitly selecting
        # its removed facts must be reconciled before views can be regenerated.
        profiles = deepcopy(scenario_profiles.OUTCOME_PROFILES)
        for outcomes in profiles.values():
            for item in outcomes.values():
                item["test_context"] = []
        with patch.object(scenario_profiles, "OUTCOME_PROFILES", profiles):
            self.assertEqual(unannotated.architecture_views()["development"]["test_groups"], [])

    def test_invalid_test_group_shapes_reject_before_path_consistency_without_writes(self):
        root = self.fixture()
        path = self.entity_path(root, "MOD-010").parent / "realization/software.json"
        original = json.loads(path.read_text())
        cases = [
            (lambda g: g.update(result="passed", contract="missing.md"), "unsupported test architecture shape"),
            (lambda g: g["execution"].update(module="MOD-007"), "unsupported test architecture shape"),
            (lambda g: g.update(name=" "), "nonblank test architecture text"),
            (lambda g: g.update(test_sources=[]), "nonempty test architecture array"),
            (lambda g: g.update(limits=[]), "nonempty test architecture array"),
            (lambda g: g["execution"].update(runners=[]), "nonempty test architecture array"),
            (lambda g: g["execution"].update(entrypoints=[]), "nonempty test architecture array"),
            (lambda g: g["test_sources"][0].update(role=""), "nonblank test architecture text"),
            (lambda g: g["test_sources"].append(deepcopy(g["test_sources"][0])), "duplicate test architecture path"),
            (lambda g: g.update(required_artifacts=[None]), "nonblank test architecture text"),
        ]
        for mutate, expected in cases:
            with self.subTest(expected=expected):
                changed = deepcopy(original)
                mutate(changed["observed"]["test_groups"][0])
                self.write_record(path, changed)
                self.assert_invalid_model(root, expected)
        changed = deepcopy(original)
        changed["observed"]["test_groups"].append(deepcopy(changed["observed"]["test_groups"][0]))
        self.write_record(path, changed)
        self.assert_invalid_model(root, "duplicate local test group name")
        changed = deepcopy(original)
        del changed["observed"]["sources"]
        self.write_record(path, changed)
        self.assert_invalid_model(root, "nonempty test architecture array")

    def test_test_dependencies_reject_missing_unsafe_or_nonfile_sources(self):
        root = self.fixture()
        path = self.entity_path(root, "MOD-010").parent / "realization/software.json"
        original = json.loads(path.read_text())
        cases = [
            (lambda g: g.update(contract="missing-contract.md")),
            (lambda g: g["execution"].update(owner_contract="missing-owner.md")),
            (lambda g: g["test_sources"][0].update(path="missing-test.py")),
            (lambda g: g.update(fixtures=[{"path": "../outside.py", "role": "Invalid escape."}])),
            (lambda g: g["execution"].update(selection=[{"path": "/tmp/catalog.py", "role": "Invalid absolute path."}])),
            (lambda g: g["execution"]["runners"][0].update(path="design")),
            (lambda g: g["execution"]["entrypoints"][0].update(path="test/*.py")),
        ]
        for mutate in cases:
            changed = deepcopy(original)
            mutate(changed["observed"]["test_groups"][0])
            self.write_record(path, changed)
            self.assert_invalid_model(root, "public entry path")

    def test_test_group_optional_dependencies_and_artifact_descriptions_remain_qualified(self):
        root = self.fixture()
        path = self.entity_path(root, "MOD-010").parent / "realization/software.json"
        original = json.loads(path.read_text())
        group = original["observed"]["test_groups"][0]
        group["fixtures"] = []
        group["execution"]["selection"] = []
        group["required_artifacts"] = ["A candidate supplied by the caller; no existing file or successful build is asserted."]
        self.write_record(path, original)
        projected = Model(root).architecture_views()["development"]["test_groups"]
        actual = next(item["group"] for item in projected if item["owner"] == "MOD-010")
        self.assertEqual(actual, group)
        group["required_artifacts"] = []
        self.write_record(path, original)
        Model(root)

    def test_shared_views_discover_new_realization_and_preserve_qualifications(self):
        root = self.fixture()
        directory = self.entity_path(root, "MOD-009").parent / "realization"
        directory.mkdir(exist_ok=True)
        origin = [{"source": "SRC-REM", "locator": "Private projection fixture",
                   "basis": "Attributed source inspection; no executed behavior."}]
        records = {
            "runtime": {"observed": {"runtime": ["A recorded learning-process boundary."], "sources": origin},
                        "deferred": ["Runtime execution remains unqualified."]},
            "software": {"observed": {"software_units": [{"path": "learning/author.py", "role": "Transform selected learning records."}],
                         "production_paths": [{"name": "Attributed learning export", "inputs": [{"path": "learning/input", "role": "Source input."}],
                                               "transformation": {"path": "learning/author.py", "description": "Describe a candidate layout."},
                                               "outputs": [{"path": "candidate/learning.json", "role": "Candidate-relative output; no generated bytes observed."}]}],
                         "sources": origin}},
            "deployment": {"observed": {"packaging": ["A recorded learning-package layout."], "sources": origin},
                           "deferred": ["No installed package was observed."]},
        }
        for facet, record in records.items():
            self.write_record(directory / f"{facet}.json", record)
        # Remove explicit references before removing their optional execution context.
        for identity, facet, field in (("MOD-010", "deployment", "physical_bindings"),
                                       ("IF-006", "interaction", "artifact_acquisition")):
            path = self.entity_path(root, identity).parent / f"realization/{facet}.json"
            record = json.loads(path.read_text())
            record["observed"].pop(field)
            self.write_record(path, record)
        (self.entity_path(root, "MOD-010").parent / "realization/runtime.json").unlink()
        model, helper = self.projection_model(root)
        with self.assertRaisesRegex(ValueError, "unresolved source selection"):
            helper.build_model(model)
        profiles = deepcopy(scenario_profiles.OUTCOME_PROFILES)
        for outcomes in profiles.values():
            for item in outcomes.values():
                item["realization"]["physical"] = [ref for ref in item["realization"]["physical"]
                                                    if (ref["owner"], ref["facet"]) != ("MOD-010", "deployment")]
        with patch.object(scenario_profiles, "OUTCOME_PROFILES", profiles):
            projected = helper.build_model(model)
            self.assertEqual(projected["views"], model.architecture_views())
        views = projected["views"]
        self.assertEqual(set(views), {"logical", "process", "development", "physical", "scenarios"})
        for view, facet in (("process", "runtime"), ("development", "software"), ("physical", "deployment")):
            with self.subTest(view=view):
                self.assertIn({"owner": "MOD-009", "facet": facet}, views[view]["facet_refs"])
                self.assertEqual(self.facet(projected, "MOD-009", facet)["data"], records[facet])
                self.assertTrue(views[view]["question"])
                self.assertTrue(views[view]["limits"])
                self.assertTrue(any("distinct qualifications" in value for value in views[view]["limits"]))
        self.assertNotIn({"owner": "MOD-010", "facet": "runtime"}, views["process"]["facet_refs"])
        self.assertIn("Runtime execution remains unqualified.", self.facet(projected, "MOD-009", "runtime")["data"]["deferred"])
        self.assertIn("No installed package was observed.", self.facet(projected, "MOD-009", "deployment")["data"]["deferred"])
        output = self.facet(projected, "MOD-009", "software")["data"]["observed"]["production_paths"][0]["outputs"][0]
        self.assertEqual(output, {"path": "candidate/learning.json", "role": "Candidate-relative output; no generated bytes observed."})

    def test_public_names_drive_browser_catalog_and_independent_inventory(self):
        root = self.fixture()
        path, facet = self.public_facet(root, "MOD-012")
        entry = facet["observed"]["public_entries"][0]
        original_name = entry["name"]
        entry.update(name="scoped-authoring-overview", group="Additional authoring navigation",
                     purpose="Locate one bounded authoring procedure and its responsibility.")
        mapping = next(item for item in self.public_mappings(facet) if item["entry"] == original_name)
        mapping["entry"] = entry["name"]
        self.write_record(path, facet)
        prefix, _, suffix = self.inventory_parts((root / INVENTORY).read_bytes())
        projected = self.projected(root)
        actual = self.catalog_entry(projected, "MOD-012", entry["name"])
        for key, value in entry.items():
            self.assertEqual(actual[key], value)
        self.assertEqual(actual["mapping"], mapping)
        self.assert_success(self.invoke_inventory(root))
        new_prefix, block, new_suffix = self.inventory_parts((root / INVENTORY).read_bytes())
        self.assertEqual((new_prefix, new_suffix), (prefix, suffix))
        self.assertIn(f"[{entry['name']}](../../{entry['source_path']})".encode(), block)
        self.assertIn(entry["purpose"].encode(), block)
        self.assertIn(entry["contract"].encode(), block)
        self.assertNotIn(f"[{original_name}](".encode(), block)
        self.assert_success(self.invoke_inventory(root, "--check"))

    def test_public_correspondence_derives_multiple_owners_and_features_without_allocating(self):
        root = self.fixture()
        before = self.projected(root)
        path, facet = self.public_facet(root, "MOD-012")
        mapping = self.public_mappings(facet)[0]
        mapping["functions"] = [
            {"function": "FUNC-032", "relation": "guides", "contribution": "Select applicable authoring guidance."},
            {"function": "FUNC-029", "relation": "guides", "contribution": "Assess the applicability of the supplied observations."},
        ]
        self.write_record(path, facet)
        projected = self.projected(root)
        entry = self.catalog_entry(projected, "MOD-012", mapping["entry"])
        self.assertEqual(set(entry["modules"]), {"MOD-007", "MOD-008"})
        self.assertEqual(set(entry["features"]), {"FEAT-009", "FEAT-010", "FEAT-011", "FEAT-016", "FEAT-017", "FEAT-018", "FEAT-020"})
        self.assertEqual(entry["mapping"]["functions"], mapping["functions"])
        self.assertNotIn("FUNC-029", projected["modules"]["MOD-012"]["functions"])
        self.assertNotIn("FUNC-032", projected["modules"]["MOD-012"]["functions"])
        self.assertEqual(projected["relationships"], before["relationships"])
        self.assertEqual(projected["views"]["scenarios"], before["views"]["scenarios"])
        self.assertEqual(projected["overview_collaborations"], before["overview_collaborations"])
        path = self.entity_path(root, "FUNC-032")
        function = json.loads(path.read_text())
        function["allocated_to"] = "MOD-003"
        self.write_record(path, function)
        path = self.entity_path(root, "FEAT-001")
        feature = json.loads(path.read_text())
        feature["realized_by"].append("FUNC-032")
        self.write_record(path, feature)
        changed = self.catalog_entry(self.projected(root), "MOD-012", mapping["entry"])
        self.assertEqual(set(changed["modules"]), {"MOD-007", "MOD-003"})
        self.assertIn("FEAT-001", changed["features"])

    def test_unmapped_entries_and_unallocated_functions_retain_explicit_limits(self):
        root = self.fixture()
        path, facet = self.public_facet(root, "MOD-012")
        mapping = self.public_mappings(facet)[0]
        mapping["functions"] = []
        limit = "Correspondence awaits review of the specialist output contract."
        mapping["limits"] = [limit]
        self.write_record(path, facet)
        entry = self.catalog_entry(self.projected(root), "MOD-012", mapping["entry"])
        self.assertEqual(entry["mapping"]["limits"], [limit])
        self.assertEqual(entry["mapping"]["functions"], [])
        self.assertEqual(entry["modules"], [])
        self.assertEqual(entry["features"], [])
        mapping["functions"] = [{"function": "FUNC-032", "relation": "guides", "contribution": "Explain the selected authoring scope."}]
        self.write_record(path, facet)
        path = self.entity_path(root, "FUNC-032")
        function = json.loads(path.read_text())
        del function["allocated_to"]
        function["unallocated_reason"] = "The accountable guidance boundary awaits review."
        self.write_record(path, function)
        projected = self.projected(root)
        entry = self.catalog_entry(projected, "MOD-012", mapping["entry"])
        self.assertEqual(entry["mapping"]["functions"][0]["function"], "FUNC-032")
        self.assertEqual(entry["modules"], [])
        self.assertEqual(projected["records"]["FUNC-032"]["data"]["unallocated_reason"], function["unallocated_reason"])

    def test_inventory_generation_is_repeatable_and_changes_only_marked_region(self):
        root = self.fixture()
        inventory = root / INVENTORY
        prefix, _, suffix = self.inventory_parts(inventory.read_bytes())
        inventory.write_bytes(prefix + b"<!-- skill-inventory:start -->\nStale catalog\n"
                              + b"<!-- skill-inventory:end -->" + suffix)
        before = snapshot(root)
        self.assert_success(self.invoke_inventory(root))
        after = snapshot(root)
        self.assertEqual(set(after), set(before))
        self.assertEqual({path: value for path, value in after.items() if path != INVENTORY},
                         {path: value for path, value in before.items() if path != INVENTORY})
        new_prefix, block, new_suffix = self.inventory_parts(inventory.read_bytes())
        self.assertEqual((new_prefix, new_suffix), (prefix, suffix))
        self.assertNotIn(b"Stale catalog", block)
        self.assert_success(self.invoke_inventory(root))
        self.assertEqual(snapshot(root), after)
        self.assert_success(self.invoke_inventory(root, "--check"))
        self.assertEqual(snapshot(root), after)

    def test_inventory_drift_is_read_only_and_preserves_surrounding_bytes(self):
        root = self.fixture()
        self.assert_success(self.invoke_inventory(root))
        inventory = root / INVENTORY
        prefix, block, suffix = self.inventory_parts(inventory.read_bytes())
        prefix = b"Maintained introduction.\r\n" + prefix
        suffix += b"\r\nRetained specialist evidence belongs here.\r\n"
        inventory.write_bytes(prefix + b"<!-- skill-inventory:start -->" + block
                              + b"<!-- skill-inventory:end -->" + suffix)
        self.assert_success(self.invoke_inventory(root, "--check"))
        inventory.write_bytes(prefix + b"<!-- skill-inventory:start -->\nOutdated public list.\n"
                              + b"<!-- skill-inventory:end -->" + suffix)
        before = snapshot(root)
        result = self.invoke_inventory(root, "--check")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(INVENTORY, result.stderr)
        self.assertEqual(snapshot(root), before)
        self.assert_success(self.invoke_inventory(root))
        new_prefix, new_block, new_suffix = self.inventory_parts(inventory.read_bytes())
        self.assertEqual((new_prefix, new_suffix), (prefix, suffix))
        self.assertNotIn(b"Outdated public list", new_block)
        self.assert_success(self.invoke_inventory(root, "--check"))

    def test_inventory_rejects_missing_document_and_invalid_markers_without_writes(self):
        for content in (None, b"No markers", b"<!-- skill-inventory:end --><!-- skill-inventory:start -->",
                        b"<!-- skill-inventory:start --><!-- skill-inventory:start --><!-- skill-inventory:end -->"):
            with self.subTest(content=content):
                root = self.fixture()
                path = root / INVENTORY
                if content is None:
                    path.unlink()
                else:
                    path.write_bytes(content)
                before = snapshot(root)
                for arguments in ((), ("--check",)):
                    result = self.invoke_inventory(root, *arguments)
                    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                    self.assertIn(INVENTORY, result.stderr)
                    self.assertEqual(snapshot(root), before)

    def test_inventory_rejects_missing_catalog_source_before_writing(self):
        root = self.fixture()
        self.assert_success(self.invoke_inventory(root))
        path, facet = self.public_facet(root, "MOD-012")
        facet["observed"]["public_entries"][0]["source_path"] = "skills/missing-entry/SKILL.md"
        self.write_record(path, facet)
        before = snapshot(root)
        for arguments in ((), ("--check",)):
            result = self.invoke_inventory(root, *arguments)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("missing or unsafe public entry path", result.stderr)
            self.assertEqual(snapshot(root), before)

    def test_catalog_generation_never_opens_skill_source_contents(self):
        root = self.fixture()
        guard = """import runpy, sys
def audit(event, arguments):
    if event == 'open' and str(arguments[0]).endswith('/SKILL.md'):
        raise AssertionError('Skill source content must not be opened')
sys.addaudithook(audit)
sys.argv = sys.argv[1:]
runpy.run_path(sys.argv[0], run_name='__main__')
"""
        result = subprocess.run([sys.executable, "-c", guard, str(INVENTORY_RENDERER), "--root", str(root)],
                                cwd=root, capture_output=True, text=True, check=False, timeout=30)
        self.assert_success(result)
        inventory = (root / INVENTORY).read_text()
        self.assertIn("Published skill", inventory)
        self.assertIn("skills/vision/SKILL.md", inventory)


if __name__ == "__main__":
    unittest.main()
