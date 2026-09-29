"""Outcome reading diagrams without inferred control flow or satisfaction edges."""

import json
import textwrap


def _quote(value):
    return json.dumps(str(value), ensure_ascii=False)


def _node(key, label, route, *, tooltip=None, children=None, columns=None, fill="#ECF3FF"):
    label = "\n".join("\n".join(textwrap.wrap(line, 31, break_long_words=False,
                                                 break_on_hyphens=False))
                      for line in label.split("\n"))
    lines = [f"{key}: {_quote(label)} {{", f"  link: {_quote(route)}",
             f"  tooltip: {_quote(tooltip or label)}", f"  style.fill: {_quote(fill)}",
             '  style.stroke: "#7C8FA9"', '  style.font-color: "#23334A"',
             "  style.font-size: 17", "  style.border-radius: 6"]
    if columns:
        lines.append(f"  grid-columns: {columns}")
    lines.extend("  " + line for line in children or [])
    return lines + ["}"]


def outcome_diagram(model, slice):
    """A presentation selection leads to its exact AR-accountable Module set."""
    outcomes = [item for item in slice.get("outcomes", []) if item["profiled"]]
    if not outcomes:
        return None
    scenario = slice["scenario"]
    title = model.records[scenario].data["title"]
    caption = ("Each outcome opens its exact selected obligations and accountable responsibilities. "
               "The arrows summarize this reading selection, not execution order, causal flow, "
               "complete coverage or satisfaction. Broader Scenario traceability remains in the detail.")
    cards, sources, selections = [], [], []
    for index, item in enumerate(outcomes):
        route = "#scenario/" + scenario + "/outcome/" + item["key"]
        names = [model.records[owner].data["title"] for owner in item["modules"]]
        members = _node("outcome", item["title"], route, tooltip=item["outcome"],
                        fill={"expected": "#E9F4EE", "alternative": "#FFF5DB", "failure": "#F7EDEE"}[item["kind"]])
        members.extend(_node("accountability", "\n".join(names) or "Accountability not selected", route,
                             tooltip="Selected allocated-obligation owners: " + ", ".join(item["modules"])))
        members += ['outcome -> accountability: "selected accountability" {',
                    '  style.stroke: "#667A96"', '  style.fill: "#FFFFFF"',
                    "  style.font-size: 13", "}"]
        cards.extend(_node("o" + str(index), item["kind"].capitalize() + " outcome", route,
                           children=members, fill="#FFFFFF"))
        sources.append(item["source"])
        for obligation in item["obligations"]:
            source = {"owner": obligation["owner"], "facet": "record", "path": obligation["path"],
                      "field": obligation["field"]}
            if source not in sources:
                sources.append(source)
        for identity in item["allocated_requirements"]:
            source = {"owner": identity, "facet": "record", "path": model.records[identity].path.as_posix(),
                      "field": "/allocated_to"}
            if source not in sources:
                sources.append(source)
        selections.append({"key": item["key"], "kind": item["kind"],
                           "allocated_requirements": item["allocated_requirements"],
                           "modules": item["modules"]})
    lines = ["# Generated from canonical REM records; do not edit.",
             f"# Source identity: {model.digest}", "# " + caption,
             "vars: {d2-config: {layout-engine: elk}}", "direction: down"]
    lines.extend(_node("outcomes", "Selected outcome accountability", "#scenario/" + scenario,
                       children=cards, columns=2, fill="#FFFFFF"))
    key = "scenario-" + scenario
    descriptor = {"key": key, "view": "scenarios", "scenario": scenario,
                  "title": title + " — selected outcomes", "caption": caption,
                  "initial_view": "readable", "outcomes": selections,
                  "legend": [{"label": "Selected accountability", "description": "Exact Module owners of the selected allocated obligations; open an outcome for its source criteria and limits."}],
                  "sources": sources}
    return "\n".join(lines) + "\n", descriptor
