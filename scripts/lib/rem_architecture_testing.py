"""Validate static test observations without assigning tooling or proof ownership."""


def validate_test_groups(model):
    def shape(value, fields, location):
        if not isinstance(value, dict) or set(value) != set(fields):
            raise ValueError(f"{location}: unsupported test architecture shape")

    def text(value, location):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{location}: expected nonblank test architecture text")

    def array(value, location, empty=False):
        if not isinstance(value, list) or (not empty and not value):
            raise ValueError(f"{location}: expected {'an' if empty else 'nonempty'} test architecture array")

    def paths(values, location, empty=False):
        array(values, location, empty)
        for index, value in enumerate(values):
            at = f"{location}/{index}"
            shape(value, ("path", "role"), at)
            text(value["path"], at + "/path")
            text(value["role"], at + "/role")
        if len({value["path"] for value in values}) != len(values):
            raise ValueError(f"{location}: duplicate test architecture path")

    groups = []
    # Admit the complete closed shape before resolving any of its paths.
    for (owner, kind), facet in sorted(model.facets.items()):
        observed = facet.data.get("observed", {})
        if "test_groups" not in observed:
            continue
        at = f"{facet.path} /observed/test_groups"
        if kind != "software" or model.records[owner].data["type"] != "module":
            raise ValueError(f"{at}: test groups belong to Module software realization")
        values = observed["test_groups"]
        array(values, at)
        sources = observed.get("sources")
        array(sources, str(facet.path) + " /observed/sources")
        for source in sources:
            shape(source, ("source", "locator", "basis"), at + "/sources")
            for key, value in source.items():
                text(value, at + "/sources/" + key)
        names = set()
        for index, group in enumerate(values):
            pointer = f"/observed/test_groups/{index}"
            location = f"{facet.path} {pointer}"
            shape(group, ("name", "contract", "test_sources", "observation_boundary", "fixtures",
                          "execution", "required_artifacts", "limits"), location)
            for key in ("name", "contract", "observation_boundary"):
                text(group[key], location + "/" + key)
            if group["name"] in names:
                raise ValueError(f"{location}: duplicate local test group name")
            names.add(group["name"])
            paths(group["test_sources"], location + "/test_sources")
            paths(group["fixtures"], location + "/fixtures", empty=True)
            execution = group["execution"]
            shape(execution, ("owner_contract", "selection", "runners", "entrypoints"), location + "/execution")
            text(execution["owner_contract"], location + "/execution/owner_contract")
            for key in ("selection", "runners", "entrypoints"):
                paths(execution[key], location + "/execution/" + key, empty=key == "selection")
            for key in ("required_artifacts", "limits"):
                array(group[key], location + "/" + key, empty=key == "required_artifacts")
                for value in group[key]:
                    text(value, location + "/" + key)
            groups.append({"owner": owner, "path": facet.path.as_posix(), "field": pointer, "group": group})

    for item in groups:
        group = item["group"]
        at = item["path"] + " " + item["field"]
        model.public_path(group["contract"], at + "/contract", contract=True)
        model.public_path(group["execution"]["owner_contract"], at + "/execution/owner_contract", contract=True)
        collections = [(key, group[key]) for key in ("test_sources", "fixtures")]
        collections += [("execution/" + key, group["execution"][key])
                        for key in ("selection", "runners", "entrypoints")]
        for key, values in collections:
            for index, value in enumerate(values):
                model.public_path(value["path"], f"{at}/{key}/{index}/path")
    return groups
