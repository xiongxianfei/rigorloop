"""Resolve and validate scoped physical facts; do not infer hosts or logical edges."""


def resolve_placement(model, reference, location):
    model.resolve(reference["owner"], ("module",), location)
    facet = model.facets.get((reference["owner"], reference["facet"]))
    values = facet.data.get("observed", {}).get("placements", []) if facet else []
    matches = [(index, value) for index, value in enumerate(values) if value["name"] == reference["name"]]
    if len(matches) != 1:
        raise ValueError(f"{location}: expected one scoped placement reference")
    index, value = matches[0]
    return facet, index, value


def resolve_execution(model, reference, location):
    model.resolve(reference["owner"], ("module",), location)
    facet = model.facets.get((reference["owner"], "runtime"))
    execution = facet.data.get("observed", {}).get("execution") if facet else None
    if not execution or execution["name"] != reference["name"]:
        raise ValueError(f"{location}: missing scoped execution reference")
    return facet, execution


def validate_physical_facts(model):
    def shape(value, fields, location):
        if not isinstance(value, dict) or set(value) != set(fields):
            raise ValueError(f"{location}: unsupported Physical structure shape")

    def text(value, location):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{location}: expected nonblank Physical text")

    def array(value, location, empty=False):
        if not isinstance(value, list) or (not empty and not value):
            raise ValueError(f"{location}: expected {'an' if empty else 'nonempty'} Physical array")

    def texts(value, location):
        array(value, location)
        for item in value:
            text(item, location)

    def reference(value, location, execution=False):
        shape(value, ("owner", "name") if execution else ("owner", "facet", "name"), location)
        for key, item in value.items():
            text(item, location + "/" + key)
        if not execution and value["facet"] not in ("deployment", "persistence"):
            raise ValueError(f"{location}: unknown placement reference facet")

    def names(values, location):
        values = [value["name"] for value in values]
        if len(set(values)) != len(values):
            raise ValueError(f"{location}: duplicate local Physical name")

    def signature(value):
        return value["owner"], value["facet"], value["name"]

    fields = {"physical_bindings": {"deployment"}, "production_placement": {"deployment"},
              "location_constraints": {"deployment", "persistence"}, "artifact_acquisition": {"interaction"}}
    pending = []
    # Admit every new closed shape/vocabulary before checking its references.
    for (owner, kind), facet in sorted(model.facets.items()):
        observed = facet.data.get("observed", {})
        if "placements" in observed:
            names(observed["placements"], str(facet.path) + " /observed/placements")
        for field, allowed in fields.items():
            if field not in observed:
                continue
            location = f"{facet.path} /observed/{field}"
            if kind not in allowed:
                raise ValueError(f"{location}: Physical field belongs to {' or '.join(sorted(allowed))}")
            if not observed.get("sources"):
                raise ValueError(f"{location}: Physical observations require sources")
            values = observed[field]
            if field in ("physical_bindings", "location_constraints"):
                array(values, location)
            else:
                values = [values]
            for index, value in enumerate(values):
                at = f"{location}/{index}" if isinstance(observed[field], list) else location
                if field == "physical_bindings":
                    shape(value, ("name", "execution", "package", "accesses", "constraints"), at)
                    text(value["name"], at + "/name")
                    reference(value["execution"], at + "/execution", execution=True)
                    reference(value["package"], at + "/package")
                    array(value["accesses"], at + "/accesses", empty=True)
                    texts(value["constraints"], at + "/constraints")
                    for i, access in enumerate(value["accesses"]):
                        path = f"{at}/accesses/{i}"
                        shape(access, ("participant", "placement", "mode", "purpose", "conditions"), path)
                        for name in ("participant", "mode", "purpose"):
                            text(access[name], path + "/" + name)
                        if access["mode"] not in ("read", "write", "read-write"):
                            raise ValueError(f"{path}: unknown Physical access mode")
                        reference(access["placement"], path + "/placement")
                        texts(access["conditions"], path + "/conditions")
                elif field == "production_placement":
                    shape(value, ("source", "workspace", "output", "constraints"), at)
                    for role in ("source", "workspace", "output"):
                        reference(value[role], at + "/" + role)
                    texts(value["constraints"], at + "/constraints")
                elif field == "location_constraints":
                    shape(value, ("name", "relation", "placements", "conditions", "rationale"), at)
                    for name in ("name", "relation", "rationale"):
                        text(value[name], at + "/" + name)
                    if value["relation"] not in ("disjoint", "same-filesystem"):
                        raise ValueError(f"{at}: unknown Physical location relation")
                    array(value["placements"], at + "/placements")
                    if len(value["placements"]) != 2:
                        raise ValueError(f"{at}: location relation requires two placements")
                    for i, item in enumerate(value["placements"]):
                        reference(item, f"{at}/placements/{i}")
                    texts(value["conditions"], at + "/conditions")
                else:
                    shape(value, ("name", "execution", "participant", "artifact", "sources", "constraints"), at)
                    for name in ("name", "participant", "artifact"):
                        text(value[name], at + "/" + name)
                    reference(value["execution"], at + "/execution", execution=True)
                    array(value["sources"], at + "/sources")
                    for i, source in enumerate(value["sources"]):
                        path = f"{at}/sources/{i}"
                        shape(source, ("name", "transport", "address", "conditions"), path)
                        for name in ("name", "transport", "address"):
                            text(source[name], path + "/" + name)
                        texts(source["conditions"], path + "/conditions")
                    names(value["sources"], at + "/sources")
                    texts(value["constraints"], at + "/constraints")
                pending.append((owner, field, at, value))
            if field in ("physical_bindings", "location_constraints"):
                names(values, location)

    for owner, field, at, value in pending:
        if field == "physical_bindings":
            _, execution = resolve_execution(model, value["execution"], at)
            _, _, package = resolve_placement(model, value["package"], at)
            if owner not in execution["modules"]:
                raise ValueError(f"{at}: physical binding owner must participate in the execution")
            if value["package"]["facet"] != "deployment":
                raise ValueError(f"{at}: execution package must reference a deployment placement")
            if not set(execution["modules"]) <= set(package["modules"]):
                raise ValueError(f"{at}: execution participants are outside the package mapping")
            for access in value["accesses"]:
                model.resolve(access["participant"], ("module",), at)
                if access["participant"] not in execution["modules"]:
                    raise ValueError(f"{at}: access participant is outside the referenced execution")
                resolve_placement(model, access["placement"], at)
        elif field == "production_placement":
            references = [value[role] for role in ("source", "workspace", "output")]
            if len({signature(ref) for ref in references}) != 3:
                raise ValueError(f"{at}: production roles require distinct scoped placements")
            for ref in references:
                _, _, placement = resolve_placement(model, ref, at)
                if owner not in placement["modules"]:
                    raise ValueError(f"{at}: production placement must include the accountable producer")
        elif field == "location_constraints":
            if len({signature(ref) for ref in value["placements"]}) != 2:
                raise ValueError(f"{at}: location relation requires distinct scoped placements")
            placements = [resolve_placement(model, ref, at)[2] for ref in value["placements"]]
            if not any(owner in placement["modules"] for placement in placements):
                raise ValueError(f"{at}: location constraint owner has no referenced responsibility")
        else:
            _, execution = resolve_execution(model, value["execution"], at)
            model.resolve(value["participant"], ("module",), at)
            if value["participant"] not in execution["modules"]:
                raise ValueError(f"{at}: acquisition participant is outside the referenced execution")
            provider = model.incoming(owner, "provides")[0].source
            if provider not in {value["participant"], *model.ancestors(value["participant"])}:
                raise ValueError(f"{at}: acquisition participant is outside the Interface provider boundary")
            if owner not in execution["entry_interfaces"] and not any(
                    call["interface"] == owner and call["callee"] == value["participant"] for call in execution["calls"]):
                raise ValueError(f"{at}: acquisition Interface has no declared execution binding")
