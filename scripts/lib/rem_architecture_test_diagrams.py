"""Development diagrams for source-owned test assessment and dependencies.

Test groups remain subordinate realization observations. No generated edge adds
implementation ownership, execution chronology, or a requirement-satisfaction
claim to the engineering model.
"""

import json
import textwrap


def _quote(value):
    return json.dumps(str(value), ensure_ascii=False)


def _node(key, label, route, *, tooltip=None, children=None, columns=None,
          fill="#ECF3FF", dashed=False):
    wrapped = "\n".join("\n".join(textwrap.wrap(line, 29, break_long_words=False,
                                                 break_on_hyphens=False))
                        for line in label.split("\n"))
    lines = [f"{key}: {_quote(wrapped)} {{", f"  link: {_quote(route)}",
             f"  tooltip: {_quote(tooltip or label)}", f"  style.fill: {_quote(fill)}",
             '  style.stroke: "#7C8FA9"', '  style.font-color: "#23334A"',
             "  style.font-size: 17", "  style.border-radius: 6"]
    if dashed:
        lines.append("  style.stroke-dash: 3")
    if columns:
        lines.append(f"  grid-columns: {columns}")
    lines.extend("  " + line for line in children or [])
    return lines + ["}"]


def _edge(source, target, label, *, dependency=False):
    lines = [f"{source} -> {target}: {_quote(label)} {{",
             '  style.stroke: "#667A96"', '  style.fill: "#FFFFFF"',
             "  style.font-size: 13"]
    if dependency:
        lines.append("  style.stroke-dash: 3")
    return lines + ["}"]


def _header(model, caption):
    return ["# Generated from canonical REM records; do not edit.",
            f"# Source identity: {model.digest}", "# " + caption,
            "vars: {d2-config: {layout-engine: elk}}", "direction: down"]


def test_diagrams(model):
    """Project assessed Modules separately from retained execution ownership."""
    groups = model.test_groups
    if not groups:
        return {}, {}
    caption = ("Test groups assess the named responsibility; they do not implement it. "
               "Dashed dependencies describe recorded test inputs and execution tooling, "
               "not an execution sequence. These static mappings are not passing results "
               "or complete coverage claims. Shared execution retains its existing contract "
               "owner; its REM responsibility allocation remains unresolved.")
    legend = [{"label": "Assesses", "description": "The test group observes the named Module's responsibility."},
              {"label": "Static dependency", "description": "Test sources, fixtures, artifacts and execution references; no ordering is implied."},
              {"label": "Execution ownership", "description": "Retained validation contract, separate from the assessed Module and unresolved in REM."}]
    sources, descriptors, overview_nodes, overview_sources = {}, {}, [], []
    owners = sorted({item["owner"] for item in groups})
    for owner in owners:
        selected = [item for item in groups if item["owner"] == owner]
        title = model.records[owner].data["title"]
        route = "#development/testing-" + owner
        refs = [{"owner": owner, "facet": "software", "path": item["path"],
                 "field": item["field"]} for item in selected]
        overview_sources.extend(refs)
        lines = _header(model, caption)
        expanded = []
        for index, item in enumerate(selected):
            group = item["group"]
            route_group = route
            execution = group["execution"]
            execution_count = sum(len(execution[field])
                                  for field in ("selection", "runners", "entrypoints"))
            dependency_label = "\n".join([
                "Static dependencies",
                f"Test sources: {len(group['test_sources'])}",
                f"Fixtures: {len(group['fixtures'])}",
                f"Execution references: {execution_count}",
                f"Required artifacts: {len(group['required_artifacts'])}",
            ])
            members = _node("group", group["name"], route_group,
                            tooltip=group["observation_boundary"], fill="#E9F4EE")
            members.extend(_node("subject", title, "#module/" + owner,
                                 tooltip=title + " (" + owner + ")"))
            members.extend(_node("dependencies", dependency_label, route_group,
                                 tooltip="Recorded dependencies; execution tooling retains its existing contract owner.",
                                 fill="#FFF5DB", dashed=True))
            members.extend(_edge("group", "subject", "assesses"))
            members.extend(_edge("group", "dependencies", "requires", dependency=True))
            expanded.extend(_node("g" + str(index), "Assessment and dependencies", route,
                                  children=members, fill="#FFFFFF"))
        lines.extend(_node("groups", "Recorded test groups", route,
                           children=expanded, columns=1, fill="#FFFFFF"))
        compact = _node("population", f"{len(selected)} recorded test groups", route,
                        tooltip="\n".join(item["group"]["name"] for item in selected), fill="#E9F4EE")
        compact.extend(_node("subject", title, "#module/" + owner,
                             tooltip=title + " (" + owner + ")"))
        compact.extend(_edge("population", "subject", "assesses"))
        overview_nodes.extend(_node("owner" + owner.replace("-", ""), "Test assessment", route,
                                    children=compact, fill="#FFFFFF"))
        key = "development-testing-" + owner
        sources[key] = "\n".join(lines) + "\n"
        descriptors[key] = {"key": key, "view": "development", "perspective": "testing",
                            "owner": owner, "route": route, "initial_view": "readable",
                            "title": title + " — test architecture", "caption": caption,
                            "legend": legend, "sources": refs}
    overview = _header(model, caption)
    overview.extend(_node("tests", "Recorded test assessment groups", "#development/testing",
                          children=overview_nodes, columns=2, fill="#FFFFFF"))
    key = "development-testing"
    sources[key] = "\n".join(overview) + "\n"
    descriptors[key] = {"key": key, "view": "development", "perspective": "testing",
                        "route": "#development/testing", "title": "Test assessment map",
                        "caption": caption, "legend": legend, "sources": overview_sources}
    return sources, descriptors
