"""Validate owner-contained Process facts without adding logical relationships."""


def validate_process_facts(model):
    def shape(value, required, location, optional=()):
        if (not isinstance(value, dict) or not set(required) <= set(value)
                or set(value) - set(required) - set(optional)):
            raise ValueError(f"{location}: unsupported Process structure shape")

    def text(value, location):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{location}: expected nonblank Process text")

    def array(value, location):
        if not isinstance(value, list) or not value:
            raise ValueError(f"{location}: expected nonempty Process array")

    def texts(value, location, unique=False):
        array(value, location)
        for item in value:
            text(item, location)
        if unique and len(set(value)) != len(value):
            raise ValueError(f"{location}: duplicate Process reference")

    def names(values, location):
        values = [value["name"] for value in values]
        if len(set(values)) != len(values):
            raise ValueError(f"{location}: duplicate local Process name")

    def step(value, location, branches=False):
        shape(value, ("name", "participant", "action"), location,
              ("branches",) if branches else ())
        for field in ("name", "participant", "action"):
            text(value[field], location + "/" + field)
        if "branches" in value:
            array(value["branches"], location + "/branches")
            for index, branch in enumerate(value["branches"]):
                place = f"{location}/branches/{index}"
                shape(branch, ("condition", "steps", "outcome"), place)
                text(branch["condition"], place + "/condition")
                text(branch["outcome"], place + "/outcome")
                array(branch["steps"], place + "/steps")
                for index, item in enumerate(branch["steps"]):
                    step(item, f"{place}/steps/{index}")
                names(branch["steps"], place + "/steps")

    sequences, lifecycles = [], []
    # Complete shape admission before resolving any new Process references.
    for (owner, kind), facet in sorted(model.facets.items()):
        observed = facet.data.get("observed", {})
        for field, required_kind in (("sequences", "interaction"), ("lifecycles", "runtime")):
            if field not in observed:
                continue
            location = f"{facet.path} /observed/{field}"
            if kind != required_kind:
                raise ValueError(f"{location}: {field} belongs to {required_kind}")
            if not observed.get("sources"):
                raise ValueError(f"{location}: Process observations require sources")
            array(observed[field], location)
            for index, value in enumerate(observed[field]):
                place = f"{location}/{index}"
                if field == "sequences":
                    shape(value, ("name", "operation", "participants", "preconditions", "steps",
                                  "outcome", "failures", "constraints"), place)
                    for name in ("name", "operation", "outcome"):
                        text(value[name], place + "/" + name)
                    for name in ("participants", "preconditions", "constraints"):
                        texts(value[name], place + "/" + name, unique=name == "participants")
                    array(value["steps"], place + "/steps")
                    for i, item in enumerate(value["steps"]):
                        step(item, f"{place}/steps/{i}", branches=True)
                    names(value["steps"], place + "/steps")
                    array(value["failures"], place + "/failures")
                    for i, failure in enumerate(value["failures"]):
                        at = f"{place}/failures/{i}"
                        shape(failure, ("condition", "outcome", "effects"), at)
                        text(failure["condition"], at + "/condition")
                        text(failure["outcome"], at + "/outcome")
                        texts(failure["effects"], at + "/effects")
                    sequences.append((owner, place, value))
                else:
                    shape(value, ("name", "states", "transitions", "constraints"), place)
                    text(value["name"], place + "/name")
                    texts(value["constraints"], place + "/constraints")
                    array(value["states"], place + "/states")
                    for i, state in enumerate(value["states"]):
                        at = f"{place}/states/{i}"
                        shape(state, ("name", "meaning"), at)
                        text(state["name"], at + "/name")
                        text(state["meaning"], at + "/meaning")
                    names(value["states"], place + "/states")
                    array(value["transitions"], place + "/transitions")
                    for i, transition in enumerate(value["transitions"]):
                        at = f"{place}/transitions/{i}"
                        shape(transition, ("from", "to", "trigger", "guards", "effects"), at)
                        for name in ("from", "to", "trigger"):
                            text(transition[name], at + "/" + name)
                        for name in ("guards", "effects"):
                            texts(transition[name], at + "/" + name)
                    lifecycles.append((owner, place, value))
            names(observed[field], location)

    for owner, place, sequence in sequences:
        contract = model.resolve(owner, ("interface",), place)
        operations = {item["name"] for item in contract.data["operations"]}
        if sequence["operation"] not in operations:
            raise ValueError(f"{place}: unknown Process operation for owning Interface")
        provider = model.incoming(owner, "provides")[0].source
        consumers = {edge.source for edge in model.incoming(owner, "consumes")}
        participants = set(sequence["participants"])
        for participant in participants:
            model.resolve(participant, ("module",), place + "/participants")
            boundary = {participant, *model.ancestors(participant)}
            if not ({provider, *consumers} & boundary):
                raise ValueError(f"{place}: Process participant is outside the Interface provider/consumer boundaries")
        if not any(provider in {p, *model.ancestors(p)} for p in participants):
            raise ValueError(f"{place}: Process sequence has no provider participant")
        for item in sequence["steps"]:
            steps = [item, *(step for branch in item.get("branches", []) for step in branch["steps"])]
            for value in steps:
                if value["participant"] not in participants:
                    raise ValueError(f"{place}: Process step participant is not declared")
    for owner, place, lifecycle in lifecycles:
        model.resolve(owner, ("module",), place)
        states = {value["name"] for value in lifecycle["states"]}
        seen = set()
        for transition in lifecycle["transitions"]:
            if transition["from"] not in states or transition["to"] not in states:
                raise ValueError(f"{place}: Process transition references an unknown state")
            signature = (transition["from"], transition["to"], transition["trigger"])
            if signature in seen:
                raise ValueError(f"{place}: duplicate Process transition")
            seen.add(signature)
