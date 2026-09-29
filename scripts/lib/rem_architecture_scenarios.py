"""Bounded Scenario outcome reading profiles, resolved from canonical records.

Selections help readers inspect relevant obligations and existing realization;
they add no engineering relationship, execution ordering, coverage or evidence.
All substantive outcome, criterion and realization content remains source-owned.
"""

import re


def _source(owner, facet, *selection):
    return {"owner": owner, "facet": facet, "selection": selection}


def _named(field, value):
    return (field, value)


def _publication(*selection):
    return _source("IF-003", "interaction", "observed", "sequences",
                   _named("/operation", "publish_record_candidate"), *selection)


def _recovery(*selection):
    return _source("IF-003", "interaction", "observed", "sequences",
                   _named("/operation", "recover_record_transaction"), *selection)


def _coordination(*selection):
    return _source("MOD-011", "runtime", "observed", "lifecycles",
                   _named("/name", "Record journal coordination"), *selection)


def _software(owner, filename):
    return _source(owner, "software", "observed", "software_units",
                   _named("/path", "packages/rigorloop/dist/lib/" + filename))


def _test(owner, name):
    return _source(owner, "software", "observed", "test_groups", _named("/name", name))


_STORAGE = [
    _source("MOD-010", "deployment", "observed", "physical_bindings",
            _named("/name", "Consumer CLI package and selected storage"), "accesses",
            _named("/placement/name", "Registered operational records")),
    _source("MOD-010", "deployment", "observed", "physical_bindings",
            _named("/name", "Consumer CLI package and selected storage"), "accesses",
            _named("/placement/name", "Record transaction metadata")),
    _source("MOD-011", "persistence", "observed", "location_constraints",
            _named("/name", "Authoritative records and private transaction state remain separate")),
]
_STORE_IMPLEMENTATION = [_software("MOD-011", "record-store.js"),
                         _software("MOD-011", "record-store-files.js")]
_RECOVERY_IMPLEMENTATION = [_software("MOD-010", "record-store-cli.js"), *_STORE_IMPLEMENTATION]
_PUBLICATION_TESTS = [_test("MOD-010", "Public recording interaction composition"),
                      _test("MOD-011", "Guarded publication and exact recovery")]
_RECOVERY_TESTS = [_test("MOD-011", "Guarded publication and exact recovery")]


def _profile(title, obligations, process, development, tests, gaps=(), limit_sources=()):
    return {"title": title, "obligations": obligations,
            "realization": {"process": process, "development": development, "physical": _STORAGE},
            "test_context": tests, "gaps": list(gaps), "limit_sources": list(limit_sources)}


# Acceptance criteria use their authored zero-based JSON pointers. Named facet
# selectors are resolved afresh, rejecting missing or ambiguous matches. Short
# labels are presentation only; actual outcome/condition text is never copied.
OUTCOME_PROFILES = {
    "SCN-046": {
        "expected": _profile(
            "Coherent durable publication",
            [("SR-042", 1), ("SR-043", 2), ("SR-044", 1), ("SR-046", 0),
             ("AR-016", 3), ("AR-019", 2), ("AR-021", 1), ("AR-021", 2), ("AR-024", 0)],
            [_publication("steps", _named("/name", "Construct and recheck candidate")),
             _publication("steps", _named("/name", "Publish exact candidate bytes")),
             _publication("steps", _named("/name", "Persist committed phase")),
             _publication("steps", _named("/name", "Clean up and return receipt"))],
            [_software("MOD-010", "recording-mutation-cli.js"),
             _software("MOD-011", "recording-construction.js"), *_STORE_IMPLEMENTATION],
            _PUBLICATION_TESTS,
            ["The selected Process account describes changed targeted publication. Its advanced supplied-byte variant remains qualified context, not the same construction path.",
             "AR-018 /acceptance_criteria/2 uses broad creation-in-batch wording alongside this Scenario's supporting-record context. This criterion is a source of reading uncertainty, not a supporting obligation here; reconciliation remains with the requirement owner."],
            limit_sources=[("AR-018", 2)]),
        "alternative-0": _profile(
            "Fresh identical candidate remains unchanged",
            [("SR-044", 3), ("AR-020", 4), ("AR-026", 3)],
            [_publication("steps", _named("/name", "Prepare bounded receipt"), "branches", 0),
             _coordination("constraints", 3)],
            [_software("MOD-010", "recording-result.js"), *_STORE_IMPLEMENTATION],
            _PUBLICATION_TESTS,
            ["Unchanged authoritative records do not imply zero private effects: the recorded non-preview path may already update lock/epoch coordination."]),
        "alternative-1": _profile(
            "Fitting receipt with explicit omitted detail",
            [("SR-046", 2), ("SR-046", 3), ("AR-024", 4), ("AR-025", 1),
             ("AR-025", 2), ("AR-025", 4), ("AR-026", 2), ("AR-026", 4)],
            [_publication("steps", _named("/name", "Prepare bounded receipt"))],
            [_software("MOD-010", "recording-result.js"),
             _software("MOD-010", "recording-query-cli.js"),
             _software("MOD-011", "record-store.js"),
             _software("MOD-011", "recording-observations.js")],
            [_test("MOD-010", "Command admission and selected reading"), *_PUBLICATION_TESTS],
            ["The selected Process step records bounded receipt preparation, not a separate diagnostic-detail retrieval interaction or observed transport delivery."]),
        "failure-0": _profile(
            "Lost-response retry conflicts on stale revision",
            [("SR-044", 3), ("SR-046", 0), ("AR-020", 4), ("AR-024", 0), ("AR-026", 4)],
            [_publication("steps", _named("/name", "Construct and recheck candidate")),
             _publication("failures", 2)],
            [_software("MOD-010", "recording-mutation-cli.js"), *_STORE_IMPLEMENTATION],
            _PUBLICATION_TESTS,
            ["A lost output response is not proof that storage failed. The selected source failure context also contains other interruption cases; only the canonical retry outcome is being discussed."]),
        "failure-1": _profile(
            "Competing writer or changed basis stops publication",
            [("SR-044", 0), ("SR-044", 1), ("SR-044", 4),
             ("AR-020", 0), ("AR-020", 1), ("AR-020", 5), ("AR-021", 3)],
            [_publication("steps", _named("/name", "Acquire writer exclusion")),
             _publication("steps", _named("/name", "Construct and recheck candidate")),
             _publication("failures", 0), _publication("failures", 1)],
            _STORE_IMPLEMENTATION, _PUBLICATION_TESTS,
            ["Supported CLI writers coordinate; arbitrary outside edits are detected only at the recorded checks. This context establishes no universal external-writer exclusion."]),
        "failure-2": _profile(
            "Interrupted publication requires explicit recovery",
            [("SR-044", 5), ("SR-046", 0), ("AR-021", 0), ("AR-021", 1),
             ("AR-021", 4), ("AR-024", 0), ("AR-026", 3)],
            [_publication("failures", 2),
             _coordination("states", _named("/name", "Prepared journal")),
             _coordination("constraints", 1)],
            _STORE_IMPLEMENTATION, _PUBLICATION_TESTS,
            ["A terminated caller may receive no response. The source reports recovery-required when control returns with transaction attention; an unconditional delivered error receipt is not established.",
             "The separate recovery request is inspected under SCN-047; this publication outcome does not choose or automatically execute it."]),
    },
    "SCN-047": {
        "expected": _profile(
            "Exact selected recovery without semantic replay",
            [("SR-045", 1), ("SR-045", 2), ("SR-046", 0),
             ("AR-022", 2), ("AR-022", 3), ("AR-023", 2), ("AR-023", 3)],
            [_recovery("steps", _named("/name", "Recheck recovery admissibility")),
             _recovery("steps", _named("/name", "Complete exact retained candidate")),
             _recovery("steps", _named("/name", "Finish verified completion"))],
            _RECOVERY_IMPLEMENTATION, _RECOVERY_TESTS,
            ["The main recorded path completes the candidate; its restore branch terminates separately and must not rejoin completion.",
             "The inspected advanced recovery path prepares its retained-state result inside Store.prepareResult. It does not establish invocation of the primary MOD-010 receipt callback."]),
        "alternative-0": _profile(
            "Restore only transaction-created initial content",
            [("SR-045", 2), ("AR-022", 2), ("AR-022", 3)],
            [_recovery("steps", _named("/name", "Recheck recovery admissibility"), "branches", 0)],
            _RECOVERY_IMPLEMENTATION, _RECOVERY_TESTS,
            ["The selected terminal restore branch includes initial-creation cleanup; it does not describe blanket project rollback or removal of externally added content."]),
        "alternative-1": _profile(
            "Committed transaction permits completion and cleanup only",
            [("SR-045", 2), ("AR-022", 3), ("AR-026", 4)],
            [_recovery("steps", _named("/name", "Recheck recovery admissibility")),
             _coordination("states", _named("/name", "Committed journal")),
             _coordination("transitions", _named("/from", "Committed journal"))],
            _RECOVERY_IMPLEMENTATION, _RECOVERY_TESTS,
            ["The committed journal controls restore admissibility even when the caller did not receive the success response; acknowledgement must not be interpreted as confirmed stdout delivery."]),
        "failure-0": _profile(
            "Untrusted recovery information or foreign target stops repair",
            [("SR-040", 3), ("SR-045", 0), ("AR-022", 0), ("AR-022", 1), ("AR-023", 2)],
            [_recovery("steps", _named("/name", "Validate retained journal")),
             _recovery("steps", _named("/name", "Recheck recovery admissibility")),
             _recovery("failures", 0)],
            _RECOVERY_IMPLEMENTATION, _RECOVERY_TESTS,
            ["A failure before exclusion has no recovery writes; a later safe stop may follow private lock/epoch effects. Unavailable identities remain unavailable."]),
        "failure-1": _profile(
            "Changed completion basis or repeated interruption requires reinspection",
            [("SR-045", 1), ("SR-045", 3), ("AR-022", 2), ("AR-022", 4),
             ("AR-022", 5), ("AR-023", 4)],
            [_recovery("steps", _named("/name", "Prepare candidate recovery receipt")),
             _recovery("steps", _named("/name", "Recheck basis and commit recovery")),
             _recovery("failures", 1)],
            _RECOVERY_IMPLEMENTATION, _RECOVERY_TESTS,
            ["The existing failure record combines changed reads, interrupted filesystem work and cleanup. The profile retains that combined source instead of inventing one triggering step or guaranteed restoration."]),
    },
}


_CONCERN_FIELDS = {
    "process": {"runtime": {"runtime", "execution", "lifecycles"}, "interaction": {"sequences"}},
    "development": {"software": {"software_units", "production_paths"}, "interaction": {"bindings"}},
    "physical": {"deployment": {"placements", "physical_bindings", "production_placement", "location_constraints"},
                 "persistence": {"placements", "location_constraints"}},
    "test_context": {"software": {"test_groups"}},
}

_PROFILE_SCENARIOS = {"SCN-046", "SCN-047"}


def _admit_criteria(selectors, *, allow_empty=False):
    if not isinstance(selectors, list) or (not selectors and not allow_empty):
        raise ValueError("Scenario profile: supporting criterion selectors must be nonempty")
    for selector in selectors:
        if (not isinstance(selector, tuple) or len(selector) != 2
                or not isinstance(selector[0], str) or not selector[0].strip()
                or type(selector[1]) is not int or selector[1] < 0):
            raise ValueError("Scenario profile: unsupported criterion selector")


def _admit_source(concern, selector):
    if not isinstance(selector, dict) or set(selector) != {"owner", "facet", "selection"}:
        raise ValueError("Scenario profile: unsupported source selector shape")
    owner, facet, selection = selector["owner"], selector["facet"], selector["selection"]
    if not isinstance(owner, str) or not owner.strip() or not isinstance(facet, str) or not facet.strip():
        raise ValueError("Scenario profile: source owner and facet must be nonblank strings")
    if concern not in _CONCERN_FIELDS or facet not in _CONCERN_FIELDS[concern]:
        raise ValueError("Scenario profile: incompatible realization concern")
    if (not isinstance(selection, (list, tuple)) or len(selection) < 2
            or selection[0] != "observed" or not isinstance(selection[1], str)
            or selection[1] not in _CONCERN_FIELDS[concern][facet]):
        raise ValueError("Scenario profile: unsupported realization field selection")
    for token in selection:
        if isinstance(token, tuple):
            if (len(token) != 2 or not isinstance(token[0], str)
                    or not token[0].startswith("/") or token[0] == "/"
                    or not isinstance(token[1], str) or not token[1].strip()):
                raise ValueError("Scenario profile: unsupported named selector")
        elif not ((isinstance(token, str) and token) or (type(token) is int and token >= 0)):
            raise ValueError("Scenario profile: unsupported source selection token")
    if concern == "test_context" and (len(selection) != 3 or not isinstance(selection[2], tuple)
                                     or selection[2][0] != "/name"):
        raise ValueError("Scenario profile: test context must select one whole named test group")


def _admit_profiles():
    """Reject shape and vocabulary errors before resolving any source or obligation."""
    if not isinstance(OUTCOME_PROFILES, dict) or set(OUTCOME_PROFILES) - _PROFILE_SCENARIOS:
        raise ValueError("Scenario profile: unsupported profiled Scenario")
    for profiles in OUTCOME_PROFILES.values():
        if not isinstance(profiles, dict):
            raise ValueError("Scenario profile: unsupported outcome profile collection")
        for key, profile in profiles.items():
            if not isinstance(key, str) or not re.fullmatch(r"expected|(?:alternative|failure)-(?:0|[1-9][0-9]*)", key):
                raise ValueError("Scenario profile: unsupported outcome selector vocabulary")
            if (not isinstance(profile, dict)
                    or set(profile) != {"title", "obligations", "realization", "test_context", "gaps", "limit_sources"}
                    or not isinstance(profile["title"], str) or not profile["title"].strip()
                    or not isinstance(profile["realization"], dict)
                    or set(profile["realization"]) != {"process", "development", "physical"}):
                raise ValueError("Scenario profile: unsupported outcome profile shape")
            _admit_criteria(profile["obligations"])
            _admit_criteria(profile["limit_sources"], allow_empty=True)
            for concern in (*profile["realization"], "test_context"):
                selectors = profile[concern] if concern == "test_context" else profile["realization"][concern]
                if not isinstance(selectors, list):
                    raise ValueError("Scenario profile: source selectors must be an array")
                for selector in selectors:
                    _admit_source(concern, selector)
            if not isinstance(profile["gaps"], list) or any(not isinstance(gap, str) or not gap.strip() for gap in profile["gaps"]):
                raise ValueError("Scenario profile: reading limits must be nonblank strings")


def _named_value(value, pointer):
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ValueError("Scenario profile: invalid named selector field")
    for token in pointer[1:].split("/"):
        if not isinstance(value, dict) or token not in value:
            return None
        value = value[token]
    return value


def _resolve_source(model, scenario_slice, concern, selector):
    _admit_source(concern, selector)
    owner, facet, selection = selector["owner"], selector["facet"], selector["selection"]
    allowed_owners = set(scenario_slice["modules"] + scenario_slice["context_modules"] + scenario_slice["interfaces"])
    if owner not in allowed_owners:
        raise ValueError(f"Scenario profile: source owner outside selected scope: {owner}")
    record = model.facets.get((owner, facet))
    if record is None:
        raise ValueError(f"Scenario profile: missing realization facet {owner}/{facet}")
    value, tokens = record.data, []
    for token in selection:
        if isinstance(token, tuple):
            if (len(token) != 2 or not isinstance(token[1], str) or not token[1].strip()
                    or not isinstance(value, list)):
                raise ValueError("Scenario profile: unsupported named selector")
            matches = [index for index, item in enumerate(value) if _named_value(item, token[0]) == token[1]]
            if len(matches) != 1:
                raise ValueError(f"Scenario profile: missing or ambiguous named detail {owner}/{facet}: {token!r}")
            token = matches[0]
        if isinstance(value, dict) and isinstance(token, str) and token in value:
            value = value[token]
        elif isinstance(value, list) and type(token) is int and 0 <= token < len(value):
            value = value[token]
        else:
            raise ValueError(f"Scenario profile: unresolved source selection {owner}/{facet}: {selection!r}")
        tokens.append(str(token).replace("~", "~0").replace("/", "~1"))
    if value is None or value == "" or value == [] or value == {}:
        raise ValueError("Scenario profile: selected source detail is empty")
    if concern == "test_context" and not isinstance(value, dict):
        raise ValueError("Scenario profile: test context must select one whole named test group")
    return {"owner": owner, "facet": facet, "path": record.path.as_posix(), "field": "/" + "/".join(tokens)}


def _obligations(model, scenario_slice, selectors):
    _admit_criteria(selectors)
    informed = set(model.records[scenario_slice["scenario"]].data["informs"])
    obligations, requirements, allocations, modules, seen = [], set(), set(), set(), set()
    for selector in selectors:
        if (not isinstance(selector, tuple) or len(selector) != 2
                or not isinstance(selector[0], str) or type(selector[1]) is not int or selector[1] < 0):
            raise ValueError("Scenario profile: unsupported criterion selector")
        identity, index = selector
        if selector in seen:
            raise ValueError("Scenario profile: duplicate criterion selector")
        seen.add(selector)
        record = model.records.get(identity)
        if record is None or record.data.get("type") not in ("system-requirement", "allocated-requirement"):
            raise ValueError(f"Scenario profile: incompatible or missing obligation {identity}")
        if record.data["type"] == "system-requirement":
            parent = identity
        else:
            parents = model.outgoing(identity, "parent")
            if len(parents) != 1:
                raise ValueError(f"Scenario profile: ambiguous requirement parent {identity}")
            parent = parents[0].target
            owner = record.data.get("allocated_to")
            if owner not in scenario_slice["modules"]:
                raise ValueError(f"Scenario profile: allocation outside selected responsibility scope {identity}")
            allocations.add(identity)
            modules.add(owner)
        if parent not in informed or parent not in scenario_slice["requirements"]:
            raise ValueError(f"Scenario profile: obligation outside informed requirement scope {identity}")
        requirements.add(parent)
        criteria = record.data.get("acceptance_criteria")
        if (not isinstance(criteria, list) or index >= len(criteria)
                or not isinstance(criteria[index], str) or not criteria[index].strip()):
            raise ValueError(f"Scenario profile: missing criterion {identity} /acceptance_criteria/{index}")
        obligations.append({"owner": identity, "path": record.path.as_posix(),
                            "field": f"/acceptance_criteria/{index}", "text": criteria[index]})
    return obligations, sorted(requirements), sorted(allocations), sorted(modules)


def scenario_outcomes(model, scenario_slice):
    """Keep each canonical outcome once; add only the bounded reading selections."""
    _admit_profiles()
    identity = scenario_slice["scenario"]
    record = model.records[identity]
    canonical = [("expected", "expected", "/expected_outcome", "", record.data["expected_outcome"])]
    for field, kind in (("alternatives", "alternative"), ("failures", "failure")):
        canonical += [(f"{kind}-{index}", kind, f"/{field}/{index}", item["condition"], item["outcome"])
                      for index, item in enumerate(record.data[field])]
    profiles = OUTCOME_PROFILES.get(identity, {})
    if identity in OUTCOME_PROFILES and set(profiles) != {item[0] for item in canonical}:
        raise ValueError(f"Scenario profile: outcome selectors must exactly match canonical outcomes for {identity}")
    result = []
    for key, kind, field, condition, outcome in canonical:
        item = {"key": key, "kind": kind, "title": {"expected": "Expected outcome", "alternative": "Alternative outcome", "failure": "Failure outcome"}[kind],
                "source": {"owner": identity, "facet": "scenario", "path": record.path.as_posix(), "field": field},
                "condition": condition, "outcome": outcome, "profiled": key in profiles,
                "obligations": [], "limit_sources": [], "requirements": [], "allocated_requirements": [], "modules": [], "interfaces": [],
                "realization": {"process": [], "development": [], "physical": []}, "test_context": [], "gaps": []}
        if key not in profiles:
            if kind != "expected":
                item["title"] = condition
            item["gaps"] = ["No detailed outcome reading selection is recorded here. This does not establish missing architecture or test coverage."]
            result.append(item)
            continue
        profile = profiles[key]
        item["title"] = profile["title"]
        (item["obligations"], item["requirements"], item["allocated_requirements"], item["modules"]) = _obligations(model, scenario_slice, profile["obligations"])
        if profile["limit_sources"]:
            item["limit_sources"] = _obligations(model, scenario_slice, profile["limit_sources"])[0]
        for concern in (*item["realization"], "test_context"):
            selectors = profile[concern] if concern == "test_context" else profile["realization"][concern]
            if not isinstance(selectors, list):
                raise ValueError("Scenario profile: source selectors must be an array")
            refs = [_resolve_source(model, scenario_slice, concern, selector) for selector in selectors]
            if len({(ref["owner"], ref["facet"], ref["field"]) for ref in refs}) != len(refs):
                raise ValueError("Scenario profile: duplicate source selector")
            if concern == "test_context":
                item["test_context"] = refs
            else:
                item["realization"][concern] = refs
        item["gaps"] = list(profile["gaps"]) + ["This reading profile selects no outcome-specific Verification or Evidence. Related test groups are contextual source organization, not coverage or passing results."]
        for concern in (*item["realization"], "test_context"):
            selected = item[concern] if concern == "test_context" else item["realization"][concern]
            if not selected:
                label = {"test_context": "contextual test group", "process": "Process", "development": "Development", "physical": "Physical"}[concern]
                item["gaps"].append(f"No {label} detail is selected by this reading profile; this does not establish absent architecture or test coverage.")
        item["interfaces"] = sorted({ref["owner"] for refs in item["realization"].values() for ref in refs
                                     if model.records[ref["owner"]].data["type"] == "interface"})
        result.append(item)
    return result
