"""Focused contracts for the generated offline architecture browser.

Run with REM_D2, REM_PUPPETEER and REM_CHROMIUM for composed generation and
offline reader checks. The generator itself requires D2 0.9.0 only; Puppeteer
and Chromium are test dependencies. Semantic and rejection checks run without them.
Private fixtures stat placeholder source references without reading skill files.
"""

import hashlib
from copy import deepcopy
from html.parser import HTMLParser
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[3]
RENDERER = ROOT / "scripts/render-rem-architecture-browser.py"
OUTPUT = Path("design/architecture/views/browser")
D2 = os.environ.get("REM_D2") or shutil.which("d2")
PUPPETEER = os.environ.get("REM_PUPPETEER")
CHROMIUM = os.environ.get("REM_CHROMIUM")
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("rem_browser_under_test", RENDERER)
browser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(browser)
from lib.rem_architecture_realization_diagrams import realization_diagrams
from lib.rem_architecture_test_diagrams import test_diagrams


def snapshot(root):
    return {path.relative_to(root).as_posix():
            (hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_mtime_ns)
            for path in root.rglob("*") if path.is_file()}


class PageContents(HTMLParser):
    def __init__(self, content):
        super().__init__()
        self.scripts = []
        self.current_script = None
        self.resources = []
        self.feed(content)

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        if tag == "script":
            self.current_script = {"attributes": attributes, "text": ""}
            self.scripts.append(self.current_script)
        if tag in ("script", "link", "img", "iframe"):
            self.resources.extend(attributes[key] for key in ("src", "href")
                                  if key in attributes)

    def handle_data(self, content):
        if self.current_script is not None:
            self.current_script["text"] += content

    def handle_endtag(self, tag):
        if tag == "script":
            self.current_script = None


class ArchitectureBrowserTests(unittest.TestCase):
    def fixture(self):
        temporary = tempfile.TemporaryDirectory(prefix="rem-browser-test-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        # The browser is derived output, not required fixture input.
        shutil.copytree(ROOT / "design", root / "design", ignore=lambda directory, names:
                        ["browser"] if Path(directory).name == "views" else [])
        for path in (root / "design/architecture").rglob("*.json"):
            record = json.loads(path.read_text())
            for entry in record.get("observed", {}).get("public_entries", []):
                for field in ("source_path", "contract"):
                    target = root / entry[field].split("#", 1)[0]
                    if not target.exists():
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_text("Source-navigation fixture only.\n")
            for group in record.get("observed", {}).get("test_groups", []):
                references = [group["contract"], group["execution"]["owner_contract"]]
                references += [item["path"] for key in ("test_sources", "fixtures")
                               for item in group[key]]
                references += [item["path"] for key in ("selection", "runners", "entrypoints")
                               for item in group["execution"][key]]
                for reference in references:
                    target = root / reference.split("#", 1)[0]
                    if not target.exists():
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_text("Static test architecture source-navigation fixture only.\n")
        return root

    def entity_path(self, root, identity):
        matches = [path for path in (root / "design").rglob("*.json")
                   if json.loads(path.read_text()).get("id") == identity]
        self.assertEqual(len(matches), 1, identity)
        return matches[0]

    def update_entity(self, root, identity, **changes):
        path = self.entity_path(root, identity)
        record = json.loads(path.read_text())
        record.update(changes)
        path.write_text(json.dumps(record, indent=2) + "\n")
        return path

    def invoke(self, root, d2, *arguments):
        return subprocess.run([sys.executable, str(RENDERER), "--root", str(root),
                               "--d2", str(d2), *arguments], cwd=root,
                              capture_output=True, text=True, timeout=180)

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_parent_contracts_and_overview_preserve_exact_child_responsibility(self):
        root = self.fixture()
        model = browser.Model(root)
        data = browser.build_model(model)
        self.assertEqual(data["roots"], ["MOD-016", "MOD-017", "MOD-018", "MOD-019"])
        self.assertEqual(data["interfaces"]["IF-004"]["provider"], "MOD-018")
        self.assertEqual(data["interfaces"]["IF-006"]["provider"], "MOD-019")
        self.assertEqual(data["modules"]["MOD-018"]["functions"], [])
        self.assertIn("FUNC-040", data["modules"]["MOD-010"]["functions"])
        self.assertIn("FUNC-040", data["modules"]["MOD-018"]["subtree_functions"])
        self.assertEqual(data["modules"]["MOD-016"]["children"],
                         ["MOD-001", "MOD-002", "MOD-003", "MOD-004"])
        expected = {
            ("IF-006", "MOD-010", "MOD-019", "MOD-018", "MOD-019"),
            ("IF-007", "MOD-005", "MOD-016", "MOD-017", "MOD-016"),
            ("IF-008", "MOD-012", "MOD-017", "MOD-018", "MOD-017"),
            ("IF-009", "MOD-015", "MOD-017", "MOD-019", "MOD-017"),
            ("IF-010", "MOD-015", "MOD-017", "MOD-019", "MOD-017"),
            ("IF-009", "MOD-012", "MOD-017", "MOD-018", "MOD-017"),
            ("IF-010", "MOD-012", "MOD-017", "MOD-018", "MOD-017"),
            ("IF-011", "MOD-012", "MOD-017", "MOD-018", "MOD-017"),
            ("IF-012", "MOD-010", "MOD-016", "MOD-018", "MOD-016"),
        }
        actual = {(item["interface"], item["consumer"], item["provider"],
                   item["consumer_boundary"], item["provider_boundary"])
                  for item in data["overview_collaborations"]}
        self.assertEqual(actual, expected)
        self.assertTrue(data["cli_contributions"])
        self.assertTrue(all(
            data["records"][item["requirement"]]["data"]["sources"][
                int(item["source_pointer"].rsplit("/", 1)[1])]["source"] == "SRC-CLI-ALLOCATION"
            for item in data["cli_contributions"]))
        self.assertEqual(data["records"]["MOD-017"]["data"]["design_limits"],
                         json.loads(self.entity_path(root, "MOD-017").read_text())["design_limits"])

    def test_exposed_child_contract_keeps_ownership_and_catalog_host_on_child(self):
        root = self.fixture()
        self.update_entity(root, "MOD-018", provides=[])
        self.update_entity(root, "MOD-010", provides=["IF-004"])
        self.update_entity(root, "IF-004", exposed_through=["MOD-018"])
        # A separately governed consumer makes the explicit exposure visible.
        path = self.entity_path(root, "MOD-015")
        module = json.loads(path.read_text())
        self.update_entity(root, "MOD-015", consumes=module["consumes"] + ["IF-004"])
        data = browser.build_model(browser.Model(root))
        self.assertEqual(data["interfaces"]["IF-004"]["provider"], "MOD-010")
        self.assertEqual(data["interfaces"]["IF-004"]["exposed_through"], ["MOD-018"])
        command_catalog = next(catalog for catalog in data["catalogs"] if catalog["owner"] == "IF-004")
        self.assertEqual(command_catalog["host"], "MOD-010")
        collaboration = next(item for item in data["overview_collaborations"] if item["interface"] == "IF-004")
        self.assertEqual(collaboration, {"interface": "IF-004", "consumer": "MOD-015",
                                        "provider": "MOD-010", "consumer_boundary": "MOD-019",
                                        "provider_boundary": "MOD-018"})
        self.assertNotIn("IF-004", data["modules"]["MOD-018"]["provides"])

    def test_cli_reading_scopes_preserve_selected_obligations_and_canonical_sources(self):
        model = browser.Model(self.fixture())
        data = browser.build_model(model)
        cooperation = data["cli_cooperation"]
        expected = {
            "SCN-041": ["AR-013", "AR-014"],
            "SCN-042": ["AR-013", "AR-014", "AR-024"],
            "SCN-043": ["AR-015"],
            "SCN-044": ["AR-017", "AR-019", "AR-020"],
            "SCN-045": ["AR-016", "AR-017"],
            "SCN-046": ["AR-020", "AR-021", "AR-025", "AR-026"],
            "SCN-047": ["AR-022", "AR-023"],
            "SCN-048": ["AR-011", "AR-012"],
            "SCN-049": ["AR-027", "AR-028"],
        }
        self.assertEqual({item["scenario"]: item["allocated_requirements"]
                          for item in cooperation["walkthroughs"]}, expected)
        self.assertEqual(len(cooperation["topics"]), 8)
        for item in cooperation["walkthroughs"]:
            owners = {data["records"][identity]["data"]["allocated_to"]
                      for identity in expected[item["scenario"]]}
            self.assertEqual(set(item["modules"]), owners)
            self.assertFalse(owners & set(item["context_modules"]))
            self.assertEqual(item["interfaces"], ["IF-004"] if item["scenario"] == "SCN-049"
                             else ["IF-003", "IF-004"])
        for item in cooperation["topics"] + cooperation["walkthroughs"]:
            self.assertTrue(item["sources"])
            for source in item["sources"]:
                record = data["records"][source["owner"]]
                self.assertEqual(source["path"], record["path"])
                value = record["data"]
                for token in source["field"].lstrip("/").split("/"):
                    token = token.replace("~1", "/").replace("~0", "~")
                    value = value[int(token)] if isinstance(value, list) else value[token]
                self.assertIsNotNone(value)
        self.assertTrue(data["cli_contributions"])
        self.assertTrue(all(
            data["records"][item["requirement"]]["data"]["sources"][
                int(item["source_pointer"].rsplit("/", 1)[1])]["source"] == "SRC-CLI-ALLOCATION"
            for item in data["cli_contributions"]))
        for item in data["cli_contributions"]:
            sr = data["records"][item["requirement"]]
            self.assertEqual(item["path"], sr["path"])
            self.assertEqual(item["criterion_text"], sr["data"]["acceptance_criteria"][item["criterion"] - 1])
            self.assertEqual(item["basis"], sr["data"]["sources"][int(item["source_pointer"].rsplit("/", 1)[1])]["basis"])

    def test_stale_cli_reading_selection_rejects_before_compiler_or_output_writes(self):
        root = self.fixture()
        self.update_entity(root, "SCN-049", informs=["SR-040"])
        output = root / OUTPUT / "index.html"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("Keep this existing browser.\n")
        before = snapshot(root)
        result = self.invoke(root, root / "compiler-must-not-run")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("does not inform parent of AR-027", result.stderr)
        self.assertNotIn("compiler-must-not-run", result.stderr)
        self.assertEqual(snapshot(root), before)

    def test_public_correspondence_preserves_roles_limits_and_exact_owners(self):
        root = self.fixture()
        original = browser.build_model(browser.Model(root))
        catalogs = {catalog["owner"]: catalog for catalog in original["catalogs"]}
        self.assertEqual(len(catalogs["IF-004"]["entries"]), 17)
        self.assertEqual(len(catalogs["MOD-012"]["entries"]), 20)
        installation = next(item for item in catalogs["IF-004"]["entries"] if item["name"] == "init")
        self.assertEqual(installation["modules"], ["MOD-014"])
        self.assertEqual({item["relation"] for item in installation["mapping"]["functions"]}, {"invokes"})
        route = next(item for item in catalogs["MOD-012"]["entries"] if item["name"] == "route")
        self.assertEqual(route["modules"], ["MOD-006", "MOD-012"])
        self.assertTrue(route["mapping"]["limits"])
        facet = self.entity_path(root, "MOD-012").parent / "realization/software.json"
        record = json.loads(facet.read_text())
        designed = {catalog["owner"]: catalog for catalog in original["designed_catalogs"]}
        skills = {entry["name"]: entry for entry in designed["MOD-012"]["entries"]}
        self.assertTrue({"requirement-analysis", "requirement-review", "system-design", "architecture-design"} <= skills.keys())
        self.assertFalse({"proposal", "proposal-review", "design"} & skills.keys())
        analysis = skills["requirement-analysis"]
        self.assertNotIn("source_path", analysis)
        self.assertEqual(analysis["modules"], ["MOD-008", "MOD-012"])
        self.assertEqual(analysis["entry_pointer"], "/proposed/1/public_capabilities/0")
        commands = {entry["name"] for entry in designed["IF-004"]["entries"]}
        self.assertEqual(commands, {
            "store backup", "store restore", "store migrate", "init", "change create", "change context", "change update", "change complete",
            "review prepare", "review show", "review record", "verification show", "verification record",
            "browser generate", "browser check", "browser recover",
            "--help", "version", "capabilities", "logs",
        })
        # New names and text come from design sources, with no corresponding source file.
        capability = record["proposed"][1]["public_capabilities"][0]
        capability["name"] = "renamed-analysis"
        capability["purpose"] = "Changed design meaning."
        facet.write_text(json.dumps(record, indent=2) + "\n")
        updated = browser.build_model(browser.Model(root))
        projected = next(c for c in updated["designed_catalogs"] if c["owner"] == "MOD-012")["entries"][0]
        self.assertEqual(projected["name"], "renamed-analysis")
        self.assertEqual(projected["purpose"], "Changed design meaning.")
        # Invalid design relationships reject before unresolved references are followed.
        capability["functions"][0].update(relation="unknown", function="FUNC-999999")
        facet.write_text(json.dumps(record, indent=2) + "\n")
        with self.assertRaisesRegex(ValueError, "unsupported public entry relation"):
            browser.Model(root)
        mapping = next(item for proposal in record["proposed"]
                       for item in proposal.get("public_entry_mappings", []) if item["entry"] == "route")
        mapping["functions"] = []
        mapping["limits"] = ["Specialist correspondence requires separate analysis."]
        record["proposed"] = [choice for choice in record["proposed"] if "public_entry_mappings" in choice]
        facet.write_text(json.dumps(record, indent=2) + "\n")
        changed = browser.build_model(browser.Model(root))
        changed_catalog = next(item for item in changed["catalogs"] if item["owner"] == "MOD-012")
        self.assertNotIn("MOD-012", {c["owner"] for c in changed["designed_catalogs"]})
        self.assertEqual(len(changed_catalog["entries"]), 20)
        route = next(item for catalog in changed["catalogs"] if catalog["owner"] == "MOD-012"
                     for item in catalog["entries"] if item["name"] == "route")
        self.assertEqual(route["modules"], [])
        self.assertEqual(route["features"], [])
        self.assertEqual(route["mapping"]["limits"], mapping["limits"])
        self.assertEqual(changed["relationships"], original["relationships"])
        self.assertEqual(changed["overview_collaborations"], original["overview_collaborations"])
        self.assertEqual(changed["modules"], original["modules"])

    def test_new_graphs_preserve_recorded_calls_placements_and_static_source_mappings(self):
        model = browser.Model(self.fixture())
        data = browser.build_model(model)
        sources = browser.diagram_sources(model)
        metadata = data["view_diagrams"]
        self.assertTrue({"process", "development", "physical", "scenarios"} <= metadata.keys())
        self.assertEqual(set(metadata), set(sources) - {"overview"} -
                         {"module-" + identity for identity in data["modules"]})
        execution_edges = re.findall(r"^\s*(\w+) -> (\w+):", sources["process"], re.MULTILINE)
        expected_edges = [("MOD-010", "MOD-011"), ("MOD-010", "MOD-014")]
        self.assertEqual(execution_edges, [("n_" + source.encode().hex(), "n_" + target.encode().hex())
                                          for source, target in expected_edges])
        self.assertIn('#interface/IF-006', sources["process"])
        self.assertIn('#interface/IF-004', sources["process"])
        self.assertNotIn('#module/MOD-019', sources["process"])
        self.assertEqual(data["interfaces"]["IF-006"]["provider"], "MOD-019")
        self.assertIn("behavioral implementation", metadata["process"]["caption"])
        self.assertEqual([(item["owner"], item["facet"], item["field"])
                          for item in metadata["process"]["sources"]],
                         [("MOD-010", "runtime", "/observed/execution")])
        placements = {(item["owner"], item["facet"], item["field"])
                      for key, descriptor in metadata.items() if re.fullmatch(r"physical-MOD-[0-9]+", key)
                      for item in descriptor["sources"]}
        self.assertEqual(placements, {
            ("MOD-010", "deployment", "/observed/placements/0"),
            ("MOD-010", "persistence", "/observed/placements/0"),
            ("MOD-011", "persistence", "/observed/placements/0"),
            ("MOD-011", "persistence", "/observed/placements/1"),
            ("MOD-013", "deployment", "/observed/placements/0"),
            ("MOD-013", "deployment", "/observed/placements/1"),
            ("MOD-013", "deployment", "/observed/placements/2"),
            ("MOD-014", "deployment", "/observed/placements/0"),
            ("MOD-014", "deployment", "/observed/placements/1"),
        })
        for key, source in sources.items():
            if re.fullmatch(r"physical-MOD-[0-9]+", key):
                self.assertNotIn(" -> ", source, key)
                self.assertTrue(all(route.startswith("#physical/")
                                    for route in re.findall(r'link: "([^"]+)"', source)))
        production = sources["development-MOD-013"]
        for name in ("Skill archive production", "CLI candidate composition", "scripts/build-adapters.py",
                     "rigorloop-adapter-codex-{release}.zip", "adapter-artifacts-{release}.json"):
            self.assertIn(name, production)
        self.assertEqual(production.count('"candidate outputs"'), 2)
        self.assertTrue(all(route == "#development/MOD-013"
                            for route in re.findall(r'link: "([^"]+)"', production)))
        skill_sources = sources["development-MOD-012"]
        for name in ("skills/vision/SKILL.md", "skills/route/SKILL.md", "Published procedure sources"):
            self.assertIn(name, skill_sources.replace("\\n", " "))
        self.assertNotIn("#entity/FUNC-", skill_sources, "Published filenames do not establish Function realization")
        self.assertEqual([(item["facet"], item["field"]) for item in metadata["development-IF-006"]["sources"]],
                         [("interaction", "/observed/bindings")])
        # Removing optional typed facts must not cause prose or software paths
        # to be guessed into replacement execution/placement relationships.
        for record in model.facets.values():
            for field in ("execution", "placements", "physical_bindings", "production_placement",
                          "location_constraints", "artifact_acquisition"):
                record.data.get("observed", {}).pop(field, None)
        # The outcome reading profile now requires some of these facts. Its
        # dangling selectors reject the complete browser, while this projection
        # must still preserve absence instead of guessing replacements.
        with self.assertRaisesRegex(ValueError, "Scenario profile: unresolved source selection"):
            browser.build_model(model)
        reduced = realization_diagrams(model)[1]
        self.assertNotIn("process", reduced)
        self.assertNotIn("physical", reduced)

    def test_test_architecture_keeps_assessment_and_execution_ownership_separate(self):
        model = browser.Model(self.fixture())
        data = browser.build_model(model)
        sources = browser.diagram_sources(model)
        groups = data["views"]["development"]["test_groups"]
        self.assertEqual({item["owner"] for item in groups},
                         {"MOD-010", "MOD-011", "MOD-013", "MOD-014"})
        self.assertEqual(len(groups), 9)
        for owner in sorted({item["owner"] for item in groups}):
            selected = [item for item in groups if item["owner"] == owner]
            descriptor = data["view_diagrams"]["development-testing-" + owner]
            self.assertEqual(descriptor["route"], "#development/testing-" + owner)
            self.assertEqual(descriptor["perspective"], "testing")
            self.assertEqual(descriptor["sources"], [
                {"owner": owner, "facet": "software", "path": item["path"], "field": item["field"]}
                for item in selected])
            source = sources["development-testing-" + owner]
            self.assertEqual(source.count('"assesses"'), len(selected))
            self.assertEqual(source.count('"requires"'), len(selected))
            self.assertIn("Static dependencies", source)
            self.assertNotIn("source mapping", source)
            self.assertIn("REM responsibility allocation remains unresolved", descriptor["caption"])
            self.assertIn("#module/" + owner, source)
            for item in selected:
                group = item["group"]
                self.assertIn(group["name"], source.replace("\\n", " "))
                record = model.facets[owner, "software"]
                self.assertEqual(item["path"], record.path.as_posix())
                index = int(item["field"].rsplit("/", 1)[1])
                self.assertEqual(group, record.data["observed"]["test_groups"][index])
                self.assertEqual(group["execution"]["owner_contract"],
                                 "design/support/validation.md")
                self.assertNotIn("allocated_to", group["execution"])
                # A test assessment is not a software implementation binding.
                self.assertNotIn(group["name"], sources["development-" + owner].replace("\\n", " "))
        self.assertFalse(any("test" in edge["relation"] for edge in data["relationships"]))

    def test_missing_test_observations_do_not_infer_groups_from_implementation_files(self):
        root = self.fixture()
        for path in (root / "design/architecture/modules").rglob("software.json"):
            record = json.loads(path.read_text())
            record.get("observed", {}).pop("test_groups", None)
            path.write_text(json.dumps(record, indent=2) + "\n")
        model = browser.Model(root)
        self.assertEqual(model.test_groups, [])
        self.assertEqual(test_diagrams(model), ({}, {}))
        self.assertTrue(model.facets["MOD-010", "software"].data["observed"]["software_units"])
        # Retained implementation paths do not create test groups. The whole
        # browser additionally rejects the now-dangling outcome reading profile.
        with self.assertRaisesRegex(ValueError, "Scenario profile: unresolved source selection"):
            browser.build_model(model)

    def test_missing_test_source_rejects_before_compilation_or_output_writes(self):
        root = self.fixture()
        facet = self.entity_path(root, "MOD-010").parent / "realization/software.json"
        record = json.loads(facet.read_text())
        record["observed"]["test_groups"][0]["test_sources"][0]["path"] = "missing-test-source.py"
        facet.write_text(json.dumps(record, indent=2) + "\n")
        output = root / OUTPUT
        output.mkdir(parents=True)
        (output / "index.html").write_text("Preserve existing browser.\n")
        before = snapshot(root)
        result = self.invoke(root, root / "compiler-must-not-be-called")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("/observed/test_groups/0/test_sources/0/path", result.stderr)
        self.assertIn("missing-test-source.py", result.stderr)
        self.assertNotIn("compiler-must-not-be-called", result.stderr)
        self.assertEqual(snapshot(root), before)

    def test_physical_topics_keep_access_actors_acquisition_alternatives_and_production_roles(self):
        model = browser.Model(self.fixture())
        sources = browser.diagram_sources(model)
        metadata = browser.build_model(model)["view_diagrams"]
        for topic in ("consumer", "storage", "production"):
            descriptor = metadata["physical-" + topic]
            self.assertEqual(descriptor["route"], "#physical/" + topic)
            self.assertTrue(descriptor["sources"])
        # Resolve independently readable generated endpoint handles. Runtime
        # participants retain distinct access even when in one process.
        def local(handle):
            return ".".join(bytes.fromhex(part[2:]).decode() for part in handle.split("."))
        storage = sources["physical-storage"].replace("\\n", " ")
        accesses = [(local(a), local(b), label) for a, b, label in
                    re.findall(r'^\s*([\w.]+) -> ([\w.]+): "([^"]+)"', storage, re.MULTILINE)
                    if label in ("reads", "writes", "reads and writes")]
        self.assertEqual(len(accesses), 5)
        expected = {
            "MOD-010": {"Local invocation diagnostics"},
            "MOD-011": {"Registered operational records", "Record transaction metadata"},
            "MOD-014": {"Selected target skill units", "Retained installation originals"},
        }
        for participant, names in expected.items():
            self.assertEqual({target.rsplit(":", 1)[-1] for actor, target, _ in accesses
                              if actor.endswith("." + participant)}, names)
        self.assertEqual(len(re.findall(r"^\s*\w+ -- \w+:", storage, re.MULTILINE)), 3)
        self.assertIn("same filesystem", storage.replace("\\n", " "))
        self.assertIn("disjoint locations", storage.replace("\\n", " "))
        consumer = sources["physical-consumer"].replace("\\n", " ")
        self.assertIn("Official release archive", consumer)
        self.assertIn("Explicit local archive", consumer)
        self.assertEqual(consumer.count('"alternative input"'), 2)
        self.assertFalse(any(href.startswith("http") for href in re.findall(r'link: "([^"]+)"', consumer)))
        producer = sources["physical-production"].replace("\\n", " ")
        roles = re.findall(r'^\s*(\w+) -> (\w+): "(source|workspace|output) location"', producer, re.MULTILINE)
        self.assertEqual({role for _, _, role in roles}, {"source", "workspace", "output"})
        self.assertTrue(all(local(start) == "producer:MOD-013" for start, _, _ in roles))
        self.assertEqual(len(re.findall(r"^\s*\w+ -> \w+:", producer, re.MULTILINE)), 3)
        # No path inventory or hypothetical transfer links become overview text.
        for topic in ("consumer", "storage", "production"):
            visible = [json.loads(label) for label in re.findall(r'^\s*\w+: ("(?:[^"\\]|\\.)*") \{', sources["physical-" + topic], re.MULTILINE)]
            self.assertFalse(any("docs/changes/" in label or "dist/bin/" in label for label in visible))

    def test_physical_bindings_do_not_infer_connections_from_matching_location_labels(self):
        model = browser.Model(self.fixture())
        # Equal location prose is not a physical identity or a connection.
        for record in model.facets.values():
            observed = record.data.get("observed", {})
            for placement in observed.get("placements", []):
                placement["location"] = "Selected filesystem"
        sources = browser.diagram_sources(model)
        self.assertEqual(sources["physical-storage"].replace("\\n", " ").count('"reads and writes"'), 5)
        # Remove all optional binding facts while retaining named placements:
        # the old inventory remains, with no replacement topology inferred.
        for record in model.facets.values():
            observed = record.data.get("observed", {})
            for field in ("physical_bindings", "production_placement", "location_constraints", "artifact_acquisition"):
                observed.pop(field, None)
        with self.assertRaisesRegex(ValueError, "Scenario profile: unresolved source selection"):
            browser.diagram_sources(model)
        reduced = realization_diagrams(model)[0]
        self.assertIn("physical", reduced)
        self.assertNotIn(" -> ", reduced["physical"])
        for topic in ("consumer", "storage", "production"):
            self.assertNotIn("physical-" + topic, reduced)

    def test_process_topics_preserve_explicit_order_terminal_paths_and_journal_guards(self):
        model = browser.Model(self.fixture())
        sources = browser.diagram_sources(model)
        metadata = browser.build_model(model)["view_diagrams"]
        selected = {
            "process-publication": ("#process/interaction/publication", "IF-003", "interaction", "/observed/sequences/0"),
            "process-recovery": ("#process/interaction/recovery", "IF-003", "interaction", "/observed/sequences/1"),
            "process-coordination": ("#process/lifecycle/coordination", "MOD-011", "runtime", "/observed/lifecycles/0"),
        }
        for key, (route, owner, facet, field) in selected.items():
            self.assertEqual(metadata[key]["route"], route)
            self.assertEqual([(item["owner"], item["facet"], item["field"])
                              for item in metadata[key]["sources"]], [(owner, facet, field)])
            self.assertTrue(all(link == route for link in re.findall(r'link: "([^"]+)"', sources[key])))
        publication = sources["process-publication"].replace("\\n", " ")
        self.assertLess(publication.index("Prepare bounded receipt"), publication.index("Publish complete candidate"))
        self.assertLess(publication.index("Publish complete candidate"), publication.index("Commit durable transaction"))
        self.assertIn("Inspect preview snapshot", publication)
        self.assertIn("Release unchanged writer", publication)
        self.assertIn("terminal alternative", publication)
        recovery = sources["process-recovery"].replace("\\n", " ")
        self.assertIn("Establish coherent storage state", recovery)
        self.assertIn("Read current account", recovery)
        # Alternative outcomes and unlocated failures cannot secretly rejoin
        # the main path through a generated outgoing edge.
        for key in ("process-publication", "process-recovery"):
            for start in re.findall(r"^\s*(n_[a-f0-9]+|failures) ->", sources[key], re.MULTILINE):
                if start == "failures":
                    self.fail("Unlocated failure acquired a triggering path")
                local = bytes.fromhex(start[2:]).decode()
                self.assertFalse(local.endswith(":outcome"), local)
        lifecycle = sources["process-coordination"]
        state_edges = [(bytes.fromhex(a[2:]).decode(), bytes.fromhex(b[2:]).decode())
                       for a, b in re.findall(r"^\s*(n_[a-f0-9]+) -> (n_[a-f0-9]+):", lifecycle, re.MULTILINE)]
        self.assertEqual(state_edges, [("Available", "Fenced preparation"),
                                      ("Fenced preparation", "Activated replacement"),
                                      ("Fenced preparation", "Available"),
                                      ("Activated replacement", "Available")])
        self.assertIn("Guards:", lifecycle)
        self.assertIn("Effects:", lifecycle)
        # Omitted observations remain omitted; prose/Scenario paths do not
        # manufacture replacement diagrams.
        model.facets[("IF-003", "interaction")].data["observed"].pop("sequences")
        model.facets[("MOD-011", "runtime")].data["observed"].pop("lifecycles")
        with self.assertRaisesRegex(ValueError, "Scenario profile: unresolved source selection"):
            browser.diagram_sources(model)
        reduced = realization_diagrams(model)[0]
        self.assertFalse(set(selected) & set(reduced))
        self.assertIn("process", reduced)

    def test_scenario_graphs_keep_exact_allocations_separate_from_provider_context(self):
        data = browser.build_model(browser.Model(self.fixture()))
        metadata = data["view_diagrams"]
        scenarios = {key for key in metadata if key.startswith("scenario-")}
        self.assertEqual(scenarios, {"scenario-SCN-019", "scenario-SCN-046", "scenario-SCN-047",
                                    "scenario-SCN-053", "scenario-SCN-066"})
        publication = metadata["scenario-SCN-046"]
        groups = {(item["kind"], item["module"]): item["members"] for item in publication["groups"]}
        self.assertEqual(groups, {
            ("functions", "MOD-010"): ["FUNC-042", "FUNC-048"],
            ("functions", "MOD-011"): ["FUNC-044", "FUNC-045", "FUNC-046"],
            ("allocated_requirements", "MOD-010"): ["AR-018", "AR-024", "AR-025"],
            ("allocated_requirements", "MOD-011"): ["AR-016", "AR-017", "AR-019", "AR-020", "AR-021", "AR-026"],
        })
        release = metadata["scenario-SCN-066"]
        self.assertEqual({group["module"] for group in release["groups"]}, {"MOD-006", "MOD-015"})
        self.assertNotIn("allocated_requirements", {group["kind"] for group in release["groups"]})
        provider_basis = {(source["owner"], source["field"]) for source in release["sources"]}
        self.assertIn(("MOD-013", "/provides/0"), provider_basis)
        self.assertIn(("MOD-017", "/provides/1"), provider_basis)
        self.assertIn("not execution order", release["caption"])

    def test_scenario_outcomes_preserve_exact_results_and_bounded_accountability(self):
        model = browser.Model(self.fixture())
        data = browser.build_model(model)
        sources = browser.diagram_sources(model)
        profiled_count = 0
        for slice in data["views"]["scenarios"]["scenarios"]:
            identity = slice["scenario"]
            scenario = model.records[identity].data
            expected = [("expected", "expected", "/expected_outcome", "", scenario["expected_outcome"])]
            expected += [(f"alternative-{index}", "alternative", f"/alternatives/{index}", item["condition"], item["outcome"])
                         for index, item in enumerate(scenario["alternatives"])]
            expected += [(f"failure-{index}", "failure", f"/failures/{index}", item["condition"], item["outcome"])
                         for index, item in enumerate(scenario["failures"])]
            self.assertEqual([(item["key"], item["kind"], item["source"]["field"], item["condition"], item["outcome"])
                              for item in slice["outcomes"]], expected)
            pilot = identity in {"SCN-046", "SCN-047"}
            descriptor = data["view_diagrams"]["scenario-" + identity]
            for outcome in slice["outcomes"]:
                self.assertEqual(outcome["profiled"], pilot)
                self.assertEqual(outcome["source"]["owner"], identity)
                self.assertEqual(outcome["source"]["path"], model.records[identity].path.as_posix())
                self.assertTrue(outcome["gaps"])
                if not pilot:
                    for key in ("obligations", "requirements", "allocated_requirements", "modules", "interfaces", "test_context"):
                        self.assertEqual(outcome[key], [], (identity, outcome["key"], key))
                    continue
                profiled_count += 1
                accountable = {model.records[allocation].data["allocated_to"]
                               for allocation in outcome["allocated_requirements"]}
                self.assertEqual(set(outcome["modules"]), accountable)
                drawn = next(item for item in descriptor["outcomes"] if item["key"] == outcome["key"])
                self.assertEqual(set(drawn["modules"]), accountable)
                self.assertEqual(drawn["allocated_requirements"], outcome["allocated_requirements"])
                self.assertIn(f'#scenario/{identity}/outcome/{outcome["key"]}', sources["scenario-" + identity])
                for obligation in outcome["obligations"]:
                    record = model.records[obligation["owner"]]
                    index = int(obligation["field"].rsplit("/", 1)[1])
                    self.assertEqual(obligation["text"], record.data["acceptance_criteria"][index])
                    self.assertIn({"owner": record.id, "facet": "record", "path": record.path.as_posix(),
                                   "field": obligation["field"]}, descriptor["sources"])
                for allocation in outcome["allocated_requirements"]:
                    self.assertIn({"owner": allocation, "facet": "record",
                                   "path": model.records[allocation].path.as_posix(), "field": "/allocated_to"},
                                  descriptor["sources"])
                self.assertTrue(outcome["test_context"])
                self.assertTrue(all("/observed/test_groups/" in ref["field"] for ref in outcome["test_context"]))
                self.assertNotIn("coverage", outcome)
                self.assertNotIn("evidence", outcome)
            if pilot:
                self.assertIn("not execution order", descriptor["caption"])
                self.assertIn("complete coverage or satisfaction", descriptor["caption"])
            else:
                self.assertNotIn("outcomes", descriptor)
        self.assertEqual(profiled_count, 11)
        self.assertEqual(len(sources), 55)

    def test_removed_scenario_outcome_rejects_before_compilation_or_output_writes(self):
        root = self.fixture()
        path = self.entity_path(root, "SCN-046")
        scenario = json.loads(path.read_text())
        scenario["alternatives"].pop()
        path.write_text(json.dumps(scenario, indent=2) + "\n")
        output = root / OUTPUT
        output.mkdir(parents=True)
        (output / "index.html").write_text("Preserve the current outcome browser.\n")
        before = snapshot(root)
        result = self.invoke(root, root / "compiler-must-not-be-called")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("outcome selectors must exactly match canonical outcomes", result.stderr)
        self.assertNotIn("compiler-must-not-be-called", result.stderr)
        self.assertEqual(snapshot(root), before)

    def test_changed_process_selection_rejects_before_compilation_or_output_writes(self):
        root = self.fixture()
        data = browser.build_model(browser.Model(root))
        outcome = next(slice for slice in data["views"]["scenarios"]["scenarios"]
                       if slice["scenario"] == "SCN-046")["outcomes"][0]
        selected = next(ref for ref in outcome["realization"]["process"] if "/steps/" in ref["field"])
        path = root / selected["path"]
        record = json.loads(path.read_text())
        value = record
        for part in selected["field"].lstrip("/").split("/"):
            part = part.replace("~1", "/").replace("~0", "~")
            value = value[int(part)] if isinstance(value, list) else value[part]
        self.assertIn("name", value)
        value["name"] = "Changed process boundary outside the reading profile"
        path.write_text(json.dumps(record, indent=2) + "\n")
        output = root / OUTPUT
        output.mkdir(parents=True)
        (output / "index.html").write_text("Preserve the current outcome browser.\n")
        before = snapshot(root)
        result = self.invoke(root, root / "compiler-must-not-be-called")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing or ambiguous named detail", result.stderr)
        self.assertNotIn("compiler-must-not-be-called", result.stderr)
        self.assertEqual(snapshot(root), before)

    def test_invalid_model_fails_before_compilation_or_output_writes(self):
        root = self.fixture()
        output = root / OUTPUT
        output.mkdir(parents=True)
        (output / "index.html").write_text("Existing reviewed browser.\n")
        self.update_entity(root, "FUNC-040", allocated_to="MOD-999999")
        before = snapshot(root)
        result = self.invoke(root, root / "compiler-must-not-be-invoked")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing reference 'MOD-999999'", result.stderr)
        self.assertEqual(snapshot(root), before)

    def test_authored_topic_sources_and_qualifications_remain_exact(self):
        root = self.fixture()
        topics = browser.read_authored_topics(browser.Model(root))
        self.assertEqual(len(topics), 24)
        self.assertEqual({t["kind"] for t in topics}, {"topology", "sequence", "state", "flowchart"})
        release_topics = {t["id"]: (t["view"], t["kind"], t["qualification"]) for t in topics if t["owner"] == "MOD-015"}
        self.assertEqual(release_topics, {
            "publication-flow": ("process", "sequence", "observed"),
            "publication-recovery": ("process", "flowchart", "observed"),
            "release-code": ("development", "topology", "observed"),
            "release-placement": ("physical", "topology", "observed"),
        })
        technical = next(t for t in topics if t["id"] == "browser-technical-structure")
        self.assertEqual(technical["route"], "#logical/MOD-004/proposed/topology/browser-technical-structure")
        self.assertIn('adapter -> engine: "Browser operation contract"', technical["source"])
        self.assertIn('Rust · MOD-001 / MOD-003 / MOD-004', technical["source"])
        build_topic = next(t for t in topics if t["id"] == "browser-build-packaging")
        self.assertEqual(build_topic["route"], "#development/MOD-004/proposed/topology/browser-build-packaging")
        self.assertIn('tool: "Reusable tool package — MOD-013"', build_topic["source"])
        self.assertIn('tool.assembly -> tool.candidate: "Produces"', build_topic["source"])
        self.assertIn('website.assembly -> website.output: "Produces"', build_topic["source"])
        self.assertEqual(build_topic["source"].count(': "Included in"'), 4)
        files = next(t for t in topics if t["id"] == "browser-file-organization")
        self.assertIn('packages/rigorloop/browser/', files["source"])
        self.assertIn('packages/rigorloop/dist/browser/', files["source"])
        self.assertIn('index.html — platform and embedded project data', files["source"])
        self.assertNotIn(' -> ', files["source"])
        software = next(t for t in topics if t["id"] == "browser-software-organization")
        self.assertIn('template -> data: "Reads for presentation"', software["source"])
        self.assertIn('generator.projection -> contract: "Conforms to"', software["source"])

        for topic in topics:
            self.assertIn(topic["owner"], {"MOD-004", "MOD-006", "MOD-011", "MOD-015", "MOD-017", "MOD-018"})
            qualification = "observed" if topic["owner"] == "MOD-015" else "proposed"
            self.assertEqual(topic["qualification"], qualification)
            self.assertIn(topic["source"], (root / topic["path"]).read_text())
            self.assertEqual(topic["source_digest"], hashlib.sha256(topic["source"].encode()).hexdigest())
            self.assertIn("/" + qualification + "/", topic["route"])

        mappings = browser.build_model(browser.Model(root))["development_implementations"]
        self.assertEqual(set(mappings), {"MOD-004"})
        mapping = mappings["MOD-004"]
        self.assertEqual(mapping["headers"], ["Software responsibility", "Current source", "Scope and limitation"])
        self.assertEqual(len(mapping["rows"]), 5)
        self.assertEqual(mapping["rows"][0][0], [{"text": "Model reading and interpretation"}])
        self.assertEqual(mapping["rows"][0][1][1], {"text": "rem_architecture_model.py", "path": "scripts/lib/rem_architecture_model.py"})
        self.assertIn("do not establish clean-customer package qualification", mapping["explanation"])
        self.assertEqual(mapping["source_digest"], hashlib.sha256((root / mapping["source"]).read_bytes()).hexdigest())
        document = root / mapping["source"]
        document.write_text(document.read_text().replace('Model reading and interpretation |', 'Changed source responsibility |', 1))
        refreshed = browser.build_model(browser.Model(root))["development_implementations"]["MOD-004"]
        self.assertEqual(refreshed["rows"][0][0], [{"text": "Changed source responsibility"}])
        self.assertNotEqual(refreshed["source_digest"], mapping["source_digest"])

        builds = browser.build_model(browser.Model(root))["development_build_resources"]
        self.assertEqual(set(builds), {"MOD-004"})
        build = builds["MOD-004"]
        self.assertEqual(build["headers"], ["Software or resource", "Role in browser design", "Build/package relationship"])
        self.assertEqual(len(build["rows"]), 6)
        self.assertEqual(build["rows"][0][0], [{"text": "Rust browser engine and Node adapter"}])
        self.assertEqual(build["rows"][-1][2][1]["text"], "Package production (MOD-013)")
        self.assertEqual(build["rows"][-1][2][1]["path"], "design/architecture/modules/MOD-019-product-delivery/modules/MOD-013-product-package-production/README.md#browser-candidate-contract")
        self.assertIn("Customer snapshot generation is runtime product behavior", build["explanation"])
        self.assertEqual(build["source_digest"], hashlib.sha256(document.read_bytes()).hexdigest())
        content = document.read_text()
        document.write_text(re.sub(r'<!-- development-implementation -->.*?<!-- /development-implementation -->', '', content, flags=re.S))
        design_only = browser.build_model(browser.Model(root))
        self.assertFalse(design_only["development_implementations"])
        self.assertEqual(design_only["development_build_resources"]["MOD-004"]["rows"], build["rows"])
        document.write_text(re.sub(r'<!-- development-build-resources -->.*?<!-- /development-build-resources -->', '', content, flags=re.S))
        implementation_only = browser.build_model(browser.Model(root))
        self.assertFalse(implementation_only["development_build_resources"])
        self.assertIn("MOD-004", implementation_only["development_implementations"])

    def test_authored_admission_rejects_unknown_vocabulary_before_source_access(self):
        root = self.fixture()
        owner = self.entity_path(root, "MOD-004").parent
        registry = owner / "browser-views.toml"
        original = registry.read_text()
        for old, new in [('version = 1', 'version = 99'), ('view = "process"', 'view = "unknown"'),
                         ('kind = "sequence"', 'kind = "unknown"'),
                         ('qualification = "proposed"', 'qualification = "unknown"'),
                         ('kind = "sequence"', 'kind = "flowchart"\nprevious_kind = "unknown"')]:
            with self.subTest(new=new):
                registry.write_text(original.replace(old, new).replace('source = "README.md"', 'source = "missing.md"'))
                before = snapshot(root)
                with self.assertRaisesRegex(ValueError, "unsupported"):
                    browser.read_authored_topics(browser.Model(root))
                self.assertEqual(snapshot(root), before)
        registry.write_text(original)

    def test_authored_svg_rejects_executable_and_external_content(self):
        from lib.rem_authored_views import validate_svg
        wrap = lambda body: ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 50">' + body + '</svg>').encode()
        self.assertEqual(validate_svg(wrap('<path fill="url(#local)"/>')), [100, 50])
        for body in ['<script>alert(1)</script>', '<g onload="alert(1)"/>',
                     '<image href="https://example.invalid/image"/>',
                     '<path fill="url(https://example.invalid/image)"/>',
                     '<style>@IMPORT "https://example.invalid/style";</style>',
                     '<set attributeName="href" to="javascript:alert(1)"/>']:
            with self.subTest(body=body), self.assertRaises(ValueError):
                validate_svg(wrap(body))

    def test_authored_source_rejection_preserves_existing_output(self):
        root = self.fixture()
        owner = self.entity_path(root, "MOD-004").parent
        registry = owner / "browser-views.toml"
        document = owner / "README.md"
        original, content = registry.read_text(), document.read_text()
        output = root / OUTPUT
        output.mkdir(parents=True)
        (output / "index.html").write_text("Prior complete output")
        cases = [(original.replace('source = "README.md"', 'source = "../README.md"'), content),
                 (original, content.replace('shape: sequence_diagram', 'shape: sequence_diagram\nicon: "https://example.invalid"')),
                 (original, content.replace('shape: sequence_diagram', 'shape: sequence_diagram\n...@private-file')),
                 (original, content.replace('shape: sequence_diagram', 'shape: sequence_diagram\nvars: {d2-config: {theme-id: 1}}')),
                 (original, content.replace('shape: sequence_diagram', 'shape: sequence_diagram\nshape: image')),
                 (original, content.replace('architecture-diagram: generation-sequence', 'architecture-diagram: absent'))]
        for registration, source in cases:
            registry.write_text(registration)
            document.write_text(source)
            before = snapshot(root)
            result = self.invoke(root, root / "compiler-must-not-run")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Authored view", result.stderr)
            self.assertEqual(snapshot(root), before)

        registry.write_text(original)
        for old, new in [
                ('<!-- /development-implementation -->', ''),
                ('<!-- development-implementation -->', '<!-- development-implementation --><!-- development-implementation -->'),
                ('| --- | --- | --- |', '| --- | --- |'),
                ('(../../../../../../scripts/lib/rem_architecture_model.py)', '(javascript:alert)'),
                ('(../../../../../../scripts/lib/rem_architecture_model.py)', '(../../../../../../../outside.py)')]:
            with self.subTest(replacement=new):
                changed = content.replace(old, new)
                self.assertNotEqual(changed, content)
                document.write_text(changed)
                before = snapshot(root)
                result = self.invoke(root, root / "compiler-must-not-run")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Development implementation", result.stderr)
                self.assertEqual(snapshot(root), before)

        for old, new in [
                ('<!-- /development-build-resources -->', ''),
                ('<!-- development-build-resources -->', '<!-- development-build-resources --><!-- development-build-resources -->'),
                ('(../../../MOD-019-product-delivery/modules/MOD-013-product-package-production/README.md#browser-candidate-contract)', '(javascript:invalid)')]:
            with self.subTest(build_replacement=new):
                changed = content.replace(old, new)
                self.assertNotEqual(changed, content)
                document.write_text(changed)
                before = snapshot(root)
                result = self.invoke(root, root / "compiler-must-not-run")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Development build resources", result.stderr)
                self.assertEqual(snapshot(root), before)

    def test_compiler_failures_leave_every_existing_output_untouched(self):
        root = self.fixture()
        output = root / OUTPUT
        output.mkdir(parents=True)
        (output / "index.html").write_text("Existing reviewed browser.\n")
        compiler = root / "controlled-compiler-failure"
        cases = {
            "wrong version": ("print('v0.8.0')", "print('unused')", "v0.9.0 is required"),
            "failed compilation": ("print('v0.9.0')", "sys.stderr.write('Controlled diagram failure'); sys.exit(7)", "Controlled diagram failure"),
            "malformed SVG": ("print('v0.9.0')", "print('<svg')", "unclosed token"),
        }
        for name, (version, compile_action, diagnostic) in cases.items():
            with self.subTest(name=name):
                compiler.write_text("#!/usr/bin/env python3\nimport sys\nif '--version' in sys.argv:\n    "
                                    + version + "\nelse:\n    " + compile_action + "\n")
                compiler.chmod(0o755)
                before = snapshot(root)
                result = self.invoke(root, compiler)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(diagnostic, result.stderr)
                self.assertEqual(snapshot(root), before)

    @unittest.skipUnless(D2 and PUPPETEER and CHROMIUM, "Set REM_D2, REM_PUPPETEER and REM_CHROMIUM for generation and offline reader checks")
    def test_real_generation_escapes_model_text_and_checks_drift_without_writes(self):
        root = self.fixture()
        payload = '</script><script>globalThis.untrustedTextExecuted=true</script> & {{DIAGRAMS}}'
        self.update_entity(root, "MOD-016", description=payload)
        before = snapshot(root)
        self.assert_success(self.invoke(root, D2))
        output = root / OUTPUT
        after = snapshot(root)
        self.assertEqual({path: after[path] for path in before}, before)
        self.assertTrue(set(after) - set(before))
        self.assertTrue(all(path.startswith(OUTPUT.as_posix() + "/") for path in set(after) - set(before)))
        original_page = (output / "index.html").read_bytes()
        # Copy just the page: successful navigation/diagrams cannot rely on source or sibling files.
        copied = root / "copied-browser.html"
        copied.write_bytes(original_page)
        ui = subprocess.run(["node", str(ROOT / "tests/engineering/validation/architecture_browser_ui_checks.cjs"), str(copied)],
                            capture_output=True, text=True, timeout=90)
        self.assert_success(ui)
        copied.unlink()

        page = PageContents(original_page.decode())
        self.assertEqual(len(page.scripts), 2)
        self.assertFalse(page.resources)
        embedded = next(script["text"] for script in page.scripts
                        if script["attributes"].get("id") == "architecture-model")
        self.assertNotIn("</script>", embedded.lower())
        data = json.loads(embedded)
        self.assertEqual(data["records"]["MOD-016"]["data"]["description"], payload)
        self.assertEqual(set(data["views"]), {"logical", "process", "development", "physical", "scenarios"})
        for view, expected in (("process", ("MOD-010", "runtime")),
                               ("development", ("MOD-012", "software")),
                               ("physical", ("MOD-010", "deployment"))):
            facets = {(item["owner"], item["facet"]) for item in data["views"][view]["facet_refs"]}
            self.assertIn(expected, facets, view)
        self.assertEqual({item["scenario"] for item in data["views"]["scenarios"]["scenarios"]},
                         {"SCN-019", "SCN-046", "SCN-047", "SCN-053", "SCN-066"})
        manifest = (output / "manifest.sha256").read_text()
        self.assertIn(data["source_digest"], manifest)
        self.assertIn("D2 v0.9.0; ELK layout", manifest)
        self.assertEqual(len(data["authored_topics"]), 24)
        for topic in data["authored_topics"]:
            self.assertTrue(topic["image"].startswith("data:image/svg+xml;base64,"))
            self.assertEqual((output / "diagrams" / (topic["key"] + ".d2")).read_text(), topic["source"] + "\n")
            self.assertIn(topic["source"], (root / topic["path"]).read_text())
        members = {line.split("  ", 1)[1]: line.split("  ", 1)[0]
                   for line in manifest.splitlines() if line and not line.startswith("#")}
        self.assertEqual(set(members), {path.relative_to(output).as_posix()
                                       for path in output.rglob("*")
                                       if path.is_file() and path.name != "manifest.sha256"})
        self.assertFalse(list(output.rglob("*.json")), "Generated artifacts must not enter canonical JSON discovery")
        for name, expected_hash in members.items():
            self.assertEqual(hashlib.sha256((output / name).read_bytes()).hexdigest(), expected_hash, name)
        diagrams = list((output / "diagrams").glob("*.svg"))
        self.assertEqual(len(diagrams), 79)
        self.assertEqual({path.stem for path in diagrams},
                         {"overview", *["module-" + identity for identity in data["modules"]],
                          *data["view_diagrams"], *[t["key"] for t in data["authored_topics"]]})
        # Names lead navigation. Identity remains on the link and in metadata,
        # while visible text retains meaningful names without routine ID labels.
        shortened_names = {"IF-008": "Engineering authoring guidance",
                           "IF-009": "Governed-action authority"}
        for diagram in diagrams:
            for anchor in ET.parse(diagram).iter("{http://www.w3.org/2000/svg}a"):
                href = anchor.attrib.get("href") or anchor.attrib.get("{http://www.w3.org/1999/xlink}href", "")
                if "#interface/" not in href and "#module/" not in href:
                    continue
                identity = href.rsplit("/", 1)[1]
                visible = " ".join(" ".join(text.itertext())
                                   for text in anchor.iter("{http://www.w3.org/2000/svg}text"))
                visible = " ".join(visible.split())
                if not visible:  # A separate link icon has no text label.
                    continue
                title = data["records"][identity]["data"]["title"]
                expected_label = shortened_names.get(identity, title)
                if diagram.stem.startswith("process") and identity == "IF-004":
                    expected_label = "Entry contract " + title
                self.assertEqual(visible, expected_label, diagram.name)
                self.assertNotRegex(visible, r"\b(?:IF|MOD)-\d+\b", diagram.name)
                metadata = [" ".join(" ".join(item.itertext()).split())
                            for item in anchor.iter("{http://www.w3.org/2000/svg}title")]
                self.assertIn(f"{title} ({identity})", metadata, f"{diagram.name}: {identity}")
        overview_links = {element.attrib.get("href") or element.attrib.get("{http://www.w3.org/1999/xlink}href")
                          for element in ET.parse(output / "diagrams/overview.svg").iter()
                          if element.tag == "{http://www.w3.org/2000/svg}a"}
        self.assertTrue({f"../index.html#module/MOD-{value:03}" for value in range(16, 20)} <= overview_links)
        self.assertTrue({f"../index.html#interface/IF-{value:03}" for value in range(6, 11)} <= overview_links)
        for key in data["view_diagrams"]:
            svg = ET.parse(output / f"diagrams/{key}.svg")
            routes = [element.attrib.get("href") or element.attrib.get("{http://www.w3.org/1999/xlink}href", "")
                      for element in svg.iter("{http://www.w3.org/2000/svg}a")]
            self.assertTrue(routes, key)
            self.assertTrue(all(route.startswith("../index.html#") for route in routes), (key, routes))
            if key.startswith("development-MOD-013"):
                self.assertTrue(all(route == "../index.html#development/MOD-013" for route in routes))
        stable = snapshot(root)
        self.assert_success(self.invoke(root, D2, "--check"))
        self.assertEqual(snapshot(root), stable)
        (output / "index.html").write_text("Locally changed browser.\n")
        (output / "diagrams/module-MOD-001.svg").unlink()
        obsolete = output / "diagrams/module-MOD-999.svg"
        obsolete.write_text("Retired generated diagram.\n")
        retired_scenario = output / "diagrams/scenario-SCN-999.svg"
        retired_scenario.write_text("Retired Scenario projection.\n")
        retired_development = output / "diagrams/development-MOD-999.d2"
        retired_development.write_text("Retired implementation projection.\n")
        unrelated = output / "diagrams/reader-notes.txt"
        unrelated.write_text("Preserve my diagram notes.\n")
        before_drift_check = snapshot(root)
        result = self.invoke(root, D2, "--check")
        self.assertEqual(result.returncode, 1, result.stderr)
        for name in ("index.html", "module-MOD-001.svg", "module-MOD-999.svg",
                     "scenario-SCN-999.svg", "development-MOD-999.d2"):
            self.assertIn(name, result.stderr)
        self.assertEqual(snapshot(root), before_drift_check)
        self.assert_success(self.invoke(root, D2))
        self.assertFalse(obsolete.exists())
        self.assertFalse(retired_scenario.exists())
        self.assertFalse(retired_development.exists())
        self.assertEqual(unrelated.read_text(), "Preserve my diagram notes.\n")
        self.assertEqual((output / "index.html").read_bytes(), original_page)

    @unittest.skipUnless(D2, "Set REM_D2 to D2 0.9.0 for actual SVG label checks")
    def test_real_diagram_names_follow_renames_and_disambiguate_collisions(self):
        original = browser.Model(self.fixture())
        cases = {
            "renamed title is not a stale alias": (
                {"IF-008": "Applicable project authoring guidance"},
                {"IF-008": "Applicable project authoring guidance",
                 "IF-009": "Governed-action authority"}),
            "shortened name conflicts with another contract": (
                {"IF-010": "Engineering authoring guidance"},
                {"IF-008": "Applicable engineering authoring guidance",
                 "IF-010": "Engineering authoring guidance"}),
            "identical canonical names need secondary identity": (
                {"IF-010": "Applicable governed-action authority"},
                {"IF-009": "Applicable governed-action authority (IF-009)",
                 "IF-010": "Applicable governed-action authority (IF-010)"}),
        }
        for name, (changes, expected) in cases.items():
            with self.subTest(name=name):
                model = deepcopy(original)
                # This exercises presentation on an already loaded model, not
                # the separately owned directory/title validation boundary.
                for identity, title in changes.items():
                    model.records[identity].data["title"] = title
                source = browser.diagram_sources(model)["overview"]
                svg = ET.fromstring(browser.compile_svg(D2, "overview", source))
                labels = {}
                for anchor in svg.iter("{http://www.w3.org/2000/svg}a"):
                    href = anchor.attrib.get("href") or anchor.attrib.get("{http://www.w3.org/1999/xlink}href", "")
                    if not href.startswith("#interface/"):
                        continue
                    text = " ".join(" ".join(item.itertext())
                                    for item in anchor.iter("{http://www.w3.org/2000/svg}text"))
                    if text.strip():
                        labels[href.rsplit("/", 1)[1]] = " ".join(text.split())
                self.assertEqual({identity: labels[identity] for identity in expected}, expected)
                self.assertEqual(len(set(labels.values())), len(labels))


if __name__ == "__main__":
    unittest.main()
