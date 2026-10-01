/* Offline presentation only. Canonical records and derived indexes are embedded by the renderer. */
(() => {
  "use strict";
  const main = document.getElementById("main");
  let model;
  try {
    model = JSON.parse(document.getElementById("architecture-model").textContent);
  } catch (_) {
    main.replaceChildren(Object.assign(document.createElement("p"), {
      textContent: "The architecture model could not be loaded. Regenerate this page from the repository sources."
    }));
    return;
  }
  const records = model.records || {};
  const modules = model.modules || {};
  const interfaces = model.interfaces || {};
  const catalogs = model.catalogs || [];
  const webCapabilities = model.web_capabilities || [];
  const views = model.views || {};
  const cooperation = model.cli_cooperation || {};
  const contributions = model.cli_contributions || [];
  const viewKinds = ["logical", "process", "development", "physical", "scenarios"];
  const moduleViewQuestions = {
    logical: "What responsibilities, contracts and technical structure does this Module have?",
    process: "How does its behavior run and interact over time?",
    development: "How is its software organized and built?",
    physical: "Where does it run and keep its data?",
    scenarios: "Which stakeholder situations involve or constrain it?"
  };
  const viewRoute = kind => kind === "logical" ? "#overview" : `#${kind}`;
  const roots = model.roots || Object.keys(modules).filter(id => !modules[id].parent);
  const list = value => Array.isArray(value) ? value : [];
  const authoredTopics = list(model.authored_topics);
  let initializeDiagrams = [];
  const data = id => records[id]?.data || {};
  const title = id => data(id).title || id;
  const nice = key => key.replace(/_/g, " ").replace(/^./, letter => letter.toUpperCase());
  const qualificationLabel = value => value === "proposed" ? "Design" : nice(value);
  const entityRoute = id => `#${modules[id] ? "module" : interfaces[id] ? "interface" : "entity"}/${encodeURIComponent(id)}`;
  const entryRoute = (catalog, entry) => `#entry/${encodeURIComponent(catalog.owner)}/${encodeURIComponent(entry.name)}`;
  const isCommand = catalog => data(catalog.owner).type === "interface";
  const catalogKind = catalog => isCommand(catalog) ? "commands" : "skills";
  function node(tag, className, text) {
    const result = document.createElement(tag);
    if (className) result.className = className;
    if (text !== undefined && text !== null) result.textContent = String(text);
    return result;
  }
  function link(text, href, className) {
    const result = node("a", className, text);
    result.href = href;
    return result;
  }
  function sourceHref(path) {
    if (typeof path !== "string" || /^(?:[a-z][a-z\d+.-]*:|\/|\\)/i.test(path) || path.split(/[\\/]/).includes("..")) return null;
    const [file, ...fragment] = path.split("#");
    return "../../../../" + file.split("/").map(encodeURIComponent).join("/") + (fragment.length ? "#" + encodeURIComponent(fragment.join("#")) : "");
  }
  function sourceLink(path, label) {
    const href = sourceHref(path);
    return href ? link(label || path, href, "source-link") : node("span", "muted", label || path || "Source unavailable");
  }
  function entityLink(id, compact = false) {
    const result = link("", entityRoute(id), "entity-pill");
    if (!compact) result.append(node("span", "", title(id)));
    result.append(node("code", "", id));
    return result;
  }
  function entityList(ids, empty = "None declared.") {
    if (!list(ids).length) return node("p", "muted small", empty);
    const result = node("div", "pill-list");
    ids.forEach(id => result.append(entityLink(id)));
    return result;
  }
  function detail(label, content, open = false) {
    const result = node("details", "detail-section");
    result.open = open;
    const body = node("div", "detail-body");
    if (content) body.append(content);
    result.append(node("summary", "", label), body);
    return result;
  }
  function section(heading, content) {
    const result = node("section", "section");
    result.append(node("h2", "", heading));
    if (content) result.append(content);
    return result;
  }
  function valueView(value) {
    if (value === null) return node("span", "muted", "Not specified.");
    if (Array.isArray(value)) {
      if (!value.length) return node("span", "muted", "None declared.");
      const result = node("ul", "field-list");
      value.forEach(item => { const li = node("li"); li.append(valueView(item)); result.append(li); });
      return result;
    }
    if (typeof value === "object") {
      const result = node("dl", "definition");
      Object.entries(value).forEach(([key, item]) => {
        const row = node("div");
        const dd = node("dd");
        dd.append(valueView(item));
        row.append(node("dt", "", nice(key)), dd);
        result.append(row);
      });
      return result;
    }
    return records[value] ? entityLink(value) : node("span", "", value);
  }
  function recordFields(record, fields) {
    const result = node("dl", "definition");
    fields.forEach(key => {
      if (!(key in record)) return;
      const dd = node("dd"); dd.append(valueView(record[key]));
      const row = node("div"); row.append(node("dt", "", nice(key)), dd); result.append(row);
    });
    return result;
  }
  function breadcrumb(items) {
    const nav = node("nav", "breadcrumb"); nav.setAttribute("aria-label", "Breadcrumb");
    [{text:"Architecture", href:"#home"}, ...items].forEach((item, index) => {
      if (index) nav.append(node("span", "separator", "/"));
      if (item.href) nav.append(link(item.text, item.href));
      else { const current = node("span", "", item.text); current.setAttribute("aria-current", "page"); nav.append(current); }
    });
    main.append(nav);
  }
  function header(eyebrow, heading, description, status) {
    const result = node("header", "page-header");
    result.append(node("p", "eyebrow", eyebrow));
    const row = node("div", "heading-row"); row.append(node("h1", "", heading));
    if (status) row.append(node("span", "badge", status));
    result.append(row);
    if (description) result.append(node("p", "page-description", description));
    main.append(result);
    document.title = `${heading} · RigorLoop Architecture`;
  }
  function diagramInterfaces(collaborations) {
    const grouped = new Map();
    list(collaborations).forEach(item => {
      if (!grouped.has(item.interface)) grouped.set(item.interface, {provider:item.provider, consumers:new Set()});
      grouped.get(item.interface).consumers.add(item.consumer);
    });
    if (!grouped.size) return null;
    const result = node("section", "diagram-interfaces");
    result.append(node("h2", "", "Interfaces shown"));
    const items = node("ul", "diagram-interface-list");
    grouped.forEach((owners, id) => {
      const item = node("li");
      const contract = link("", entityRoute(id), "diagram-interface-name");
      contract.append(node("span", "", title(id)));
      const provider = node("p");
      provider.append(document.createTextNode("Provided by "), link(title(owners.provider), entityRoute(owners.provider)));
      const consumers = node("p");
      consumers.append(document.createTextNode(owners.consumers.size === 1 ? "Consumer shown: " : "Consumers shown: "));
      [...owners.consumers].forEach((consumer, index) => {
        if (index) consumers.append(document.createTextNode("; "));
        consumers.append(link(title(consumer), entityRoute(consumer)));
      });
      item.append(contract, provider, consumers); items.append(item);
    });
    result.append(items);
    return result;
  }
  function diagramAnnotations(metadata) {
    const result = node("div", "diagram-annotations");
    const legend = list(metadata.legend);
    if (legend.length) {
      const items = node("ul", "diagram-legend");
      items.setAttribute("aria-label", "Diagram legend");
      legend.forEach(item => {
        const row = node("li");
        if (typeof item === "string") row.append(node("span", "", item));
        else {
          if (item.label) row.append(node("strong", "", item.label));
          if (item.description) row.append(node("span", "", item.description));
        }
        items.append(row);
      });
      result.append(items);
    }
    const sources = list(metadata.sources);
    if (sources.length) {
      const rows = node("ul", "record-list");
      sources.forEach(source => {
        const row = node("li");
        if (source.owner && records[source.owner]) {
          const heading = node("p", "diagram-source-owner");
          heading.append(entityLink(source.owner)); row.append(heading);
        }
        if (source.path) row.append(sourceLink(source.path, source.facet ? `${nice(source.facet)} record ↗` : source.path));
        if (source.field) row.append(node("p", "small muted", source.field));
        if (source.description) row.append(node("p", "small muted", source.description));
        rows.append(row);
      });
      result.append(detail("Diagram sources and scope", rows));
    }
    return result.childElementCount ? result : null;
  }
  function diagram(key, heading, caption, collaborations, metadata) {
    const template = Array.from(document.querySelectorAll("template[data-diagram]")).find(item => item.dataset.diagram === key);
    if (!template) return node("p", "notice", "No diagram is available for this scope. Use the linked Modules and Interfaces below.");
    const panel = node("section", "diagram-panel");
    panel.dataset.diagramView = metadata?.view || "logical";
    const toolbar = node("div", "diagram-toolbar"); toolbar.append(node("h2", "", heading));
    const controls = node("div", "diagram-tools");
    const out = node("output", "", "100%"); out.setAttribute("aria-live", "polite");
    const minus = node("button", "", "−"); minus.type="button"; minus.setAttribute("aria-label", "Zoom out");
    const plus = node("button", "", "+"); plus.type="button"; plus.setAttribute("aria-label", "Zoom in");
    const fit = node("button", "", "Fit"); fit.type="button"; fit.setAttribute("aria-label", "Fit diagram");
    controls.append(minus, out, plus, fit); toolbar.append(controls);
    const viewport = node("div", metadata ? "diagram-viewport view-graph-viewport" : key === "overview" ? "diagram-viewport overview-viewport" : "diagram-viewport");
    const canvas = node("div", "diagram-canvas");
    canvas.append(template.content.cloneNode(true));
    const svg = canvas.querySelector("svg");
    if (svg) {
      svg.setAttribute("role", "group"); svg.setAttribute("aria-label", heading);
      svg.querySelectorAll("a").forEach(anchor => {
        anchor.removeAttribute("target");
        const href = anchor.getAttribute("href") || anchor.getAttribute("xlink:href") || "";
        const identity = /^#(?:module|interface)\/([^/]+)$/.exec(href)?.[1];
        const label = records[identity] ? `${title(identity)} (${identity})` : anchor.textContent.trim();
        if (label) anchor.setAttribute("aria-label", label);
      });
    }
    viewport.append(canvas);
    const dimensions = (svg?.getAttribute("viewBox") || "0 0 800 450").trim().split(/[\s,]+/).map(Number);
    const naturalWidth = dimensions[2] || 800, naturalHeight = dimensions[3] || 450;
    const minimumZoom = metadata ? 1 : 25;
    let zoom = 100;
    function updateZoom(next) {
      zoom = Math.max(minimumZoom, Math.min(250, metadata ? Math.floor(next) : Math.round(next)));
      canvas.style.width = `${naturalWidth * zoom / 100}px`;
      out.textContent = `${zoom}%`; minus.disabled = zoom === minimumZoom; plus.disabled = zoom === 250;
    }
    function fitZoom() {
      const availableWidth = Math.max(1, viewport.clientWidth - 36);
      const availableHeight = metadata ? Math.max(1, Math.min(innerHeight * 0.8, 850) - 36)
        : Math.max(1, parseFloat(getComputedStyle(viewport).maxHeight) - 36 || 530);
      updateZoom(Math.min(availableWidth / naturalWidth, availableHeight / naturalHeight) * 100);
      viewport.scrollLeft = 0; viewport.scrollTop = 0;
    }
    minus.addEventListener("click", () => updateZoom(zoom - 25));
    plus.addEventListener("click", () => updateZoom(zoom + 25));
    fit.addEventListener("click", fitZoom);
    requestAnimationFrame(() => {
      if (!panel.isConnected) return;
      if (metadata?.initial_view === "readable") {
        updateZoom(Math.max(75, Math.min(100, (viewport.clientWidth - 36) / naturalWidth * 100)));
        const firstLabel = svg?.querySelector("text");
        if (firstLabel && canvas.clientWidth > viewport.clientWidth) {
          const labelBounds = firstLabel.getBoundingClientRect(), viewportBounds = viewport.getBoundingClientRect();
          viewport.scrollLeft += labelBounds.left + labelBounds.width / 2 - viewportBounds.left - viewportBounds.width / 2;
        }
      }
      else if (metadata) fitZoom();
      else updateZoom(Math.max(85, Math.min(100, (viewport.clientWidth - 36) / naturalWidth * 100)));
    });
    panel.append(toolbar, viewport, node("p", "diagram-caption", caption));
    const namedInterfaces = diagramInterfaces(collaborations);
    if (namedInterfaces) panel.append(namedInterfaces);
    if (metadata) {
      const annotations = diagramAnnotations(metadata);
      if (annotations) panel.append(annotations);
    }
    return panel;
  }
  function projectedDiagram(kind, owner) {
    const key = owner ? `${kind}-${owner}` : kind;
    const metadata = model.view_diagrams?.[key];
    if (!metadata) return null;
    return diagram(metadata.key || key, metadata.title || `${nice(kind)} relationships`, metadata.caption || "", undefined, metadata);
  }
  function processTopics() {
    return Object.values(model.view_diagrams || {}).filter(item => item.view === "process" && /^#process\/(?:interaction|lifecycle)\/[^/]+$/.test(item.route || ""));
  }
  function processTopicApplies(topic, owner) {
    return !owner || topic.owner === owner || list(topic.sources).some(source =>
      source.owner === owner || list(resolveSourceField(source)?.participants).includes(owner));
  }
  function processTopicsContent(owner, inline = false, overview = null) {
    const topics = processTopics().filter(topic => processTopicApplies(topic, owner)).map(topic => ({
        ...topic, route:owner ? topic.route.replace("#process/", `#process/${owner}/`) : topic.route, group:topic.interaction ? "Interactions" : "State and coordination", qualification:"observed"
      }));
    authoredTopics.filter(topic => topic.view === "process" && (!owner || topic.owner === owner)).forEach(topic => {
      topics.push({...topic, summary:topic.description, group:topic.kind === "topology" ? "Runtime topology" : ["sequence", "flowchart"].includes(topic.kind) ? "Interactions" : "State and coordination"});
    });
    if (!topics.length) return null;
    if (inline) {
      const groups = ["Runtime topology", "Interactions", "State and coordination"];
      return viewDiagramSections(groups.flatMap(group => topics.filter(topic => topic.group === group)), true, overview);
    }
    const result=node("div","process-details");
    ["Runtime topology", "Interactions", "State and coordination"].forEach(group=>{
      const selected=topics.filter(topic=>topic.group===group);
      if(!selected.length)return;
      const cards=node("div","card-grid process-topic-grid");
      selected.forEach(topic=>{
        const card=link("",topic.route,"module-card");
        card.append(node("span",`qualification ${topic.qualification}`,qualificationLabel(topic.qualification)),node("h3","",topic.title));
        if(topic.summary)card.append(node("p","",topic.summary));
        card.append(node("p","small muted",title(topic.owner)));
        cards.append(card);
      });
      result.append(section(group,cards));
    });
    return result;
  }
  function processTopicsForField(facet, key) {
    return processTopics().filter(topic => list(topic.sources).some(source => source.owner === facet.owner && source.facet === facet.facet && (source.field === `/observed/${key}` || source.field?.startsWith(`/observed/${key}/`)))).map(topic => modules[facet.owner] ? {...topic, route:topic.route.replace("#process/", `#process/${facet.owner}/`)} : topic);
  }
  function parentProcessTopics(owner) {
    const parent = modules[owner]?.parent;
    const topics = authoredTopics.filter(topic => parent && topic.owner === parent && topic.view === "process");
    if (!topics.length) return null;
    const body = node("div", "parent-process-topics");
    body.append(node("p", "section-note", "Parent-owned interactions provide composition context. These links do not establish this Module's participation or realization."));
    const cards = node("div", "card-grid");
    topics.forEach(topic => {
      const card = link("", topic.route, "module-card");
      card.append(node("span", `qualification ${topic.qualification}`, qualificationLabel(topic.qualification)), node("h3", "", topic.title),
        node("p", "", topic.description), node("p", "small muted", title(parent)));
      cards.append(card);
    });
    body.append(cards);
    return section("Parent composition", body);
  }
  function physicalTopics() {
    return Object.values(model.view_diagrams || {}).filter(item => item.view === "physical" && /^#physical\/(?:consumer|storage|production)$/.test(item.route || ""));
  }
  function physicalNavigation(activeRoute) {
    const nav = node("nav", "physical-navigation");
    nav.setAttribute("aria-label", "Physical scopes");
    const overview = link("Overview", "#physical");
    if (activeRoute === "#physical") overview.setAttribute("aria-current", "page");
    else if (!physicalTopics().some(topic => topic.route === activeRoute)) overview.setAttribute("aria-current", "location");
    nav.append(overview);
    physicalTopics().forEach(topic => {
      const item = link(topic.navigation_label || topic.title, topic.route);
      if (activeRoute === topic.route) item.setAttribute("aria-current", "page");
      nav.append(item);
    });
    return nav;
  }
  function relatedPhysicalTopics(owner) {
    return physicalTopics().filter(topic => !owner || topic.owner === owner || list(topic.owners).includes(owner) || list(topic.sources).some(source =>
      source.owner === owner || list(resolveSourceField(source)?.modules).includes(owner)));
  }
  function physicalTopicCards(owner) {
    const topics = relatedPhysicalTopics(owner);
    if (!topics.length) return null;
    const cards = node("div", "card-grid physical-topic-grid");
    topics.forEach(topic => {
      const card = link("", topic.route, "module-card");
      card.append(node("h3", "", topic.title));
      if (topic.summary) card.append(node("p", "", topic.summary));
      cards.append(card);
    });
    return section("Explore physical scope", cards);
  }
  function physicalTopicsForField(facet, key) {
    return physicalTopics().filter(topic => list(topic.sources).some(source => source.owner === facet.owner && source.facet === facet.facet && (source.field === `/observed/${key}` || source.field?.startsWith(`/observed/${key}/`))));
  }
  function resolveSourceField(source) {
    const facet = list(model.facets).find(item => item.owner === source.owner && item.facet === source.facet && item.path === source.path);
    if (!facet || typeof source.field !== "string" || !source.field.startsWith("/")) return undefined;
    let value = facet.data;
    for (const part of source.field.slice(1).split("/")) {
      const key = part.replace(/~1/g, "/").replace(/~0/g, "~");
      if (value === null || typeof value !== "object" || !Object.hasOwn(value, key)) return undefined;
      value = value[key];
    }
    return value;
  }
  function processStep(step, includeBranches = true) {
    const item = node("li");
    item.append(node("h3", "", step.name));
    if (step.participant) item.append(entityLink(step.participant));
    item.append(node("p", "", step.action));
    if (includeBranches && list(step.branches).length) {
      const branches = node("div");
      step.branches.forEach(branch => {
        const alternative = node("section", "process-branch");
        alternative.append(node("h4", "", branch.condition));
        const steps = node("ol", "scenario-steps");
        list(branch.steps).forEach(child => steps.append(processStep(child, false)));
        alternative.append(steps, node("p", "process-branch-outcome", branch.outcome));
        branches.append(alternative);
      });
      item.append(detail("Terminal alternatives", branches));
    }
    return item;
  }
  function processSequence(sequence) {
    const body = node("div");
    body.append(node("h3", "", "Participants"), entityList(sequence.participants));
    if (sequence.operation) body.append(node("p", "small muted", `Interface operation: ${sequence.operation}`));
    if (list(sequence.preconditions).length) body.append(detail("Preconditions", valueView(sequence.preconditions)));
    const steps = node("ol", "scenario-steps");
    list(sequence.steps).forEach(step => steps.append(processStep(step)));
    body.append(section("Source-defined order", steps));
    if (sequence.outcome) body.append(section("Main outcome", node("p", "expected-outcome", sequence.outcome)));
    if (list(sequence.failures).length) body.append(detail("Failures and retained effects", valueView(sequence.failures)));
    if (list(sequence.constraints).length) body.append(detail("Interaction constraints", valueView(sequence.constraints)));
    return body;
  }
  function processLifecycle(lifecycle) {
    const body = node("div");
    const states = node("ul", "record-list");
    list(lifecycle.states).forEach(state => {
      const item = node("li"); item.append(node("h3", "", state.name), node("p", "", state.meaning)); states.append(item);
    });
    body.append(section("Recorded states", states));
    const transitions = node("ul", "record-list");
    list(lifecycle.transitions).forEach(transition => {
      const item = node("li");
      item.append(node("h3", "", `${transition.from} → ${transition.to}`), node("p", "", transition.trigger));
      item.append(detail("Guards and effects", recordFields(transition, ["guards", "effects"])));
      transitions.append(item);
    });
    body.append(section("Guarded transitions", transitions));
    if (list(lifecycle.constraints).length) body.append(detail("Coordination constraints", valueView(lifecycle.constraints)));
    return body;
  }
  function renderProcessTopic(kind, name, owner) {
    const route = `#process/${kind}/${encodeURIComponent(name)}`;
    const topic = processTopics().find(item => item.route === route);
    if (!topic || !processTopicApplies(topic, owner)) return notFound("Process diagram", name);
    breadcrumb([...(owner ? [{text:title(owner),href:entityRoute(owner)}] : []), {text:"Process", href:scopeRoute(owner,"process")}, {text:topic.title}]);
    header(kind === "interaction" ? "Process view · Selected interaction" : "Process view · Coordination and lifecycle", topic.title, topic.summary);
    main.append(link("← Process overview", scopeRoute(owner,"process"), "topic-return"));
    main.append(node("p", "section-note", "This view preserves the selected source-defined steps, guards, and outcomes. It does not establish observed execution or add ordering between independent paths."));
    main.append(diagram(topic.key, topic.title, topic.caption || "", undefined, topic));
    const seen = new Set();
    list(topic.sources).forEach(source => {
      const identity = `${source.path}#${source.field}`;
      const value = resolveSourceField(source);
      if (value === undefined || value === null || typeof value !== "object" || seen.has(identity)) return;
      seen.add(identity);
      const body = node("div");
      body.append(kind === "interaction" && list(value.steps).length ? processSequence(value)
        : kind === "lifecycle" && list(value.states).length ? processLifecycle(value) : valueView(value));
      if (source.path) body.append(sourceLink(source.path, "Read canonical realization record ↗"));
      main.append(detail(value.name || `${title(source.owner)} · ${nice(source.facet)} source detail`, body));
    });
    main.append(viewScope("process"));
  }
  function physicalFact(value) {
    if (value === null || typeof value !== "object" || Array.isArray(value)) return valueView(value);
    const body = node("div");
    Object.entries(value).forEach(([key, item]) => {
      if (key === "name") return;
      if (key === "constraints") { body.append(detail("Constraints", valueView(item))); return; }
      if (["execution", "package", "source", "workspace", "output", "placement"].includes(key) && item?.owner && item?.name) {
        body.append(section(nice(key), physicalReference(item, key === "execution" ? "runtime" : item.facet))); return;
      }
      if (key === "placements" && Array.isArray(item) && item.every(reference => reference?.owner && reference?.name)) {
        const references = node("div", "physical-reference-grid"); item.forEach(reference => references.append(physicalReference(reference, reference.facet)));
        body.append(section("Related placements", references)); return;
      }
      if (key === "accesses" && Array.isArray(item)) {
        const accesses = node("div");
        item.forEach(access => {
          const card = node("article", "physical-access");
          const mode = {read:"Read", write:"Write", "read-write":"Read and write"}[access.mode] || access.mode;
          card.append(node("h3", "", `${mode} · ${access.placement?.name || "Recorded placement"}`));
          if (access.participant) card.append(node("p", "small muted", "Participating responsibility"), entityLink(access.participant));
          if (access.purpose) card.append(node("p", "", access.purpose));
          if (access.placement) card.append(physicalReference(access.placement, access.placement.facet));
          if (access.conditions) card.append(section("Applicable conditions", valueView(access.conditions)));
          const remaining = Object.keys(access).filter(field => !["mode","participant","purpose","placement","conditions"].includes(field));
          if (remaining.length) card.append(recordFields(access, remaining));
          accesses.append(card);
        });
        body.append(section("Recorded access", item.length ? accesses : node("p", "muted small", "No access declared."))); return;
      }
      if (key === "sources" && value.artifact && Array.isArray(item)) {
        const alternatives = node("div");
        item.forEach(source => {
          const card = node("article", "physical-access");
          card.append(node("h3", "", source.name));
          if (source.transport) card.append(node("p", "", source.transport));
          if (source.address) card.append(node("code", "physical-address", source.address));
          if (source.conditions) card.append(section("Applicable conditions", valueView(source.conditions)));
          const remaining = Object.keys(source).filter(field => !["name","transport","address","conditions"].includes(field));
          if (remaining.length) card.append(recordFields(source, remaining));
          alternatives.append(card);
        });
        body.append(section("Artifact source alternatives", alternatives)); return;
      }
      if (key === "participant") { body.append(section("Participating responsibility", entityLink(item))); return; }
      if (key === "modules") { body.append(section("Related Modules", entityList(item))); return; }
      if (key === "paths" && Array.isArray(item)) {
        const paths = node("ul", "physical-paths");
        item.forEach(path => { const row = node("li"); row.append(node("code", "", path)); paths.append(row); });
        body.append(section("Recorded relative paths and templates", paths));
      } else body.append(recordFields(value, [key]));
    });
    return body;
  }
  function physicalReference(reference, facetName) {
    const card = node("div", "physical-reference");
    card.append(node("strong", "", reference.name));
    if (reference.owner) card.append(entityLink(reference.owner));
    const facet = list(model.facets).find(item => item.owner === reference.owner && item.facet === facetName);
    if (facet) card.append(sourceLink(facet.path, `Read ${facetName} record ↗`));
    return card;
  }
  function renderPhysicalTopic(name) {
    const route = `#physical/${encodeURIComponent(name)}`;
    const topic = physicalTopics().find(item => item.route === route);
    if (!topic) return notFound("Physical scope", name);
    breadcrumb([{text:"Physical", href:"#physical"}, {text:topic.title}]);
    header("Physical view", topic.title, topic.summary);
    main.append(physicalNavigation(route));
    main.append(diagram(topic.key, topic.title, topic.caption || "", undefined, topic));
    const seen = new Set();
    list(topic.sources).forEach(source => {
      const identity = `${source.path}#${source.field}`;
      const value = resolveSourceField(source);
      if (value === undefined || seen.has(identity)) return;
      seen.add(identity);
      const facts = Array.isArray(value) && value.every(item => item && typeof item === "object") ? value : [value];
      facts.forEach(fact => {
        const body = node("div", "physical-fact");
        body.append(physicalFact(fact));
        if (source.path) body.append(sourceLink(source.path, "Read canonical realization record ↗"));
        if (source.field) body.append(node("p", "small muted", `Source field: ${source.field}`));
        main.append(detail(fact?.name || `${title(source.owner)} · ${nice(source.facet)} source detail`, body));
      });
    });
    main.append(viewScope("physical"));
  }
  function moduleCard(id) {
    const card = link("", entityRoute(id), "module-card");
    card.append(node("h3", "", title(id)), node("p", "", data(id).description));
    const info = modules[id] || {};
    const childCount = list(info.children).length;
    const pieces = childCount ? [`${childCount} child Modules`] : [`${list(info.functions).length} allocated Functions`];
    if (list(info.provides).length) pieces.push(`${info.provides.length} provided ${info.provides.length === 1 ? "Interface" : "Interfaces"}`);
    card.append(node("div", "card-meta", pieces.join(" · ")));
    return card;
  }
  function moduleCards(ids) {
    const result = node("div", "card-grid"); ids.forEach(id => result.append(moduleCard(id))); return result;
  }
  function sourceDetails(id) {
    const body = node("div");
    if (records[id]?.path) body.append(sourceLink(records[id].path, "Open canonical JSON ↗"));
    if (data(id).sources?.length) body.append(node("h3", "", "Provenance"), valueView(data(id).sources));
    const facets = list(model.facets).filter(item => item.owner === id);
    if (facets.length) {
      body.append(node("h3", "", "Realization records"));
      const links = node("ul", "field-list");
      facets.forEach(item => { const li = node("li"); li.append(sourceLink(item.path, `${nice(item.facet)} ↗`)); links.append(li); });
      body.append(links);
    }
    return detail("Sources and realization", body);
  }
  function facetsFor(kind, owner) {
    return list(views[kind]?.facet_refs).filter(ref => !owner || ref.owner === owner).map(ref =>
      list(model.facets).find(facet => facet.owner === ref.owner && facet.facet === ref.facet)
    ).filter(Boolean);
  }
  function relatedViews(owners, currentKind) {
    const result = node("div", "cross-view-links");
    const links = node("div", "link-row");
    ["process", "development", "physical"].forEach(kind => {
      const related = [...new Set(owners)].filter(owner => facetsFor(kind, owner).length);
      related.forEach(owner => {
        if (currentKind === kind && owners.length === 1) return;
        links.append(link(`${nice(kind)} · ${title(owner)} →`, `#${kind}/${encodeURIComponent(owner)}`));
      });
    });
    if (!links.childElementCount) return null;
    result.append(node("p", "eyebrow", "Related architecture views"), links);
    return result;
  }
  function viewScope(kind) {
    const view = views[kind] || {};
    const body = node("div");
    if (view.scope) body.append(valueView(view.scope));
    if (["process", "development", "physical"].includes(kind)) body.append(node("p", "", "Design describes the current intended behavior and structure; observed facts describe inspected implementation sources. Deferred items remain unresolved. These labels describe the basis, not an approval stage."));
    if (list(view.limits).length) body.append(node("h3", "", "Limits"), valueView(view.limits));
    body.append(node("h3", "", "Generated source"));
    body.append(node("p", "small muted", "The diagrams and details are derived from canonical records. Their source links remain available beside each definition and projection."));
    if (model.source_digest) {
      body.append(node("p", "small muted", "Source identity for this generated model:"), node("code", "source-digest", model.source_digest));
    }
    return detail("View scope, limits, and source", body);
  }
  function facetSummary(facet) {
    const observed = facet.data.observed || {};
    const facts = Object.entries(observed).filter(([key]) => !["sources", "public_entries", "software_units", "bindings", "production_paths"].includes(key));
    for (const [, value] of facts) {
      if (typeof value === "string") return value;
      const first = list(value).find(item => typeof item === "string");
      if (first) return first;
    }
    const production = list(observed.production_paths);
    if (production.length) return production.map(item => item.name).join(" · ");
    const units = list(observed.software_units).concat(list(observed.bindings));
    if (units.length) return units[0].role || units[0].path;
    if (list(observed.public_entries).length) return "Named public capabilities and their proposed architectural correspondence.";
    return list(facet.data.proposed)[0]?.choice || list(facet.data.deferred)[0] || "Recorded realization details and their applicable limits.";
  }
  function productionPaths(paths) {
    const result = node("div", "production-paths");
    list(paths).forEach(path => {
      const card = node("article", "production-path");
      card.append(node("h3", "", path.name));
      const steps = node("div", "production-steps");
      const inputs = node("section", "production-step"); inputs.append(node("h4", "", "Source inputs"));
      list(path.inputs).forEach(input => {
        const item = node("div", "production-file");
        item.append(sourceLink(input.path), node("p", "", input.role)); inputs.append(item);
      });
      const transformation = node("section", "production-step"); transformation.append(node("h4", "", "Transformation"));
      if (path.transformation?.path) transformation.append(sourceLink(path.transformation.path));
      if (path.transformation?.description) transformation.append(node("p", "", path.transformation.description));
      const outputs = node("section", "production-step"); outputs.append(node("h4", "", "Candidate outputs"));
      list(path.outputs).forEach(output => {
        const item = node("div", "production-file");
        item.append(node("code", "", output.path), node("p", "", output.role)); outputs.append(item);
      });
      steps.append(inputs, transformation, outputs); card.append(steps);
      result.append(card);
    });
    result.append(node("p", "section-note", "Output paths describe candidate locations. They do not establish that an artifact was generated, qualified, or published."));
    return result;
  }
  function observationField(key, value) {
    if (["software_units", "bindings"].includes(key)) {
      const items = node("ul", "record-list");
      list(value).forEach(unit => {
        const item = node("li");
        if (unit.path) item.append(sourceLink(unit.path));
        if (unit.role) item.append(node("p", "", unit.role));
        items.append(item);
      });
      return detail(nice(key), items);
    }
    if (key === "production_paths") return section("Product generation", productionPaths(value));
    const body = node("div", "observation-field");
    body.append(node("h3", "", nice(key)));
    if (Array.isArray(value) && value.length > 2) {
      body.append(valueView(value.slice(0, 2)), detail(`More ${key.replace(/_/g, " ")}`, valueView(value.slice(2))));
    } else body.append(valueView(value));
    return body;
  }
  function facetPanel(facet) {
    const result = node("article", "facet-panel");
    const heading = node("div", "section-head");
    heading.append(node("h2", "", nice(facet.facet)), sourceLink(facet.path, "Canonical record ↗"));
    result.append(heading);
    const observed = facet.data.observed || {};
    const observationKeys = Object.keys(observed).filter(key => !["sources", "public_entries"].includes(key));
    if (observationKeys.length || list(observed.public_entries).length) {
      result.append(node("p", "qualification observed", "Observed in repository sources"));
      observationKeys.forEach(key => {
        if (key === "test_groups") {
          const reading = testPerspectiveLink(facet.owner); if (reading) result.append(reading);
          list(observed[key]).forEach(group => result.append(detail(group.name, testGroupBody(facet.owner, group))));
          return;
        }
        const topics = processTopicsForField(facet, key).concat(physicalTopicsForField(facet, key));
        if (!topics.length) { result.append(observationField(key, observed[key])); return; }
        const links = node("div", "link-row");
        topics.forEach(topic => links.append(link(`${topic.title} →`, topic.route)));
        result.append(section(nice(key), links));
        // A diagram replaces only the exact array entries its sources select.
        // Neighboring observations remain readable even without a projection.
        if (Array.isArray(observed[key])) {
          const prefix = `/observed/${key}/`;
          const covered = new Set(topics.flatMap(topic => list(topic.sources)).filter(source =>
            source.owner === facet.owner && source.facet === facet.facet && source.field?.startsWith(prefix)
          ).map(source => source.field.slice(prefix.length)).filter(index => /^(0|[1-9]\d*)$/.test(index)).map(Number));
          observed[key].forEach((value, index) => {
            if (covered.has(index)) return;
            const content = key === "sequences" && list(value?.steps).length ? processSequence(value)
              : key === "lifecycles" && list(value?.states).length ? processLifecycle(value)
              : topics.some(topic => topic.view === "physical") ? physicalFact(value) : valueView(value);
            result.append(detail(value?.name || `Additional ${key.replace(/_/g, " ")}`, content));
          });
        } else if (!topics.some(topic => topic.view === "physical" && list(topic.sources).some(source =>
          source.owner === facet.owner && source.facet === facet.facet && source.field === `/observed/${key}`
        ))) result.append(observationField(key, observed[key]));
      });
      if (list(observed.public_entries).length) {
        const matches = catalogs.filter(catalog => catalog.owner === facet.owner);
        const links = node("div", "link-row");
        matches.forEach(catalog => links.append(link(`Explore ${catalogKind(catalog)} →`, `#${catalogKind(catalog)}`)));
        result.append(node("p", "small muted", "Public names, purposes, and mappings are available in the capability catalog."), links);
      }
    }
    if (list(facet.data.proposed).length) {
      const proposals = node("div");
      facet.data.proposed.forEach(proposal => {
        const body = recordFields(proposal, ["choice", "rationale", "alternatives", "consequences", "revisit_when"]);
        if (list(proposal.public_entry_mappings).length) {
          const matches = catalogs.filter(catalog => catalog.owner === facet.owner);
          matches.forEach(catalog => body.append(link(`Read individual ${catalogKind(catalog)} mappings →`, `#${catalogKind(catalog)}`, "source-link")));
        }
        proposals.append(detail(proposal.choice || "Design decision", body));
      });
      result.append(node("h3", "qualification proposed", "Design decisions"), proposals);
    }
    if (list(facet.data.deferred).length) result.append(detail("Deferred decisions and qualification", valueView(facet.data.deferred)));
    if (list(observed.sources).length) result.append(detail("Observation sources and limits", valueView(observed.sources)));
    return result;
  }
  function testGroups(owner) {
    return list(views.development?.test_groups).filter(item => !owner || item.owner === owner);
  }
  function testRoute(owner) {
    return owner ? `#development/testing-${encodeURIComponent(owner)}` : "#development/testing";
  }
  function developmentNavigation(activeRoute) {
    const nav = node("nav", "development-navigation"); nav.setAttribute("aria-label", "Development perspectives");
    [["Implementation map", "#development"], ["Test architecture", testRoute()]].forEach(([label, route]) => {
      const item = link(label, route);
      if (activeRoute === route) item.setAttribute("aria-current", "page");
      else if (activeRoute.startsWith("#development/testing-") && route === testRoute()) item.setAttribute("aria-current", "location");
      else if (!activeRoute.startsWith("#development/testing") && route === "#development") item.setAttribute("aria-current", "location");
      nav.append(item);
    });
    return nav;
  }
  function testPerspectiveLink(owner) {
    if (!testGroups(owner).length) return null;
    const result = node("div", "link-row");
    result.append(link(owner ? "Explore this responsibility's test architecture →" : "Explore test architecture →", testRoute(owner)));
    return result;
  }
  function testReferences(values) {
    if (!list(values).length) return node("p", "muted", "No references recorded in this group.");
    const items = node("ul", "record-list test-reference-list");
    values.forEach(reference => {
      const item = node("li");
      item.append(node("p", "", reference.role), sourceLink(reference.path));
      items.append(item);
    });
    return items;
  }
  function testGroupBody(owner, group) {
    const result = node("div", "test-group-body");
    const assessed = node("p", "test-assessed");
    assessed.append(document.createTextNode("Assesses "), entityLink(owner));
    result.append(assessed, node("h3", "", "Observation boundary"), node("p", "test-observation-boundary", group.observation_boundary));
    const contract = node("p", "small"); contract.append(sourceLink(group.contract, "Read the governing test and coverage contract ↗")); result.append(contract);
    result.append(detail("Test sources", testReferences(group.test_sources)), detail("Fixtures and resource support", testReferences(group.fixtures)));
    const execution = node("div"), ownership = node("p");
    ownership.append(document.createTextNode("Execution owner: "), sourceLink(group.execution.owner_contract, "Retained Validation contract ↗"));
    execution.append(ownership, node("p", "section-note", "The assessed Module is not assigned ownership of shared execution tooling by this mapping. That REM responsibility allocation remains unresolved."));
    [["selection", "Suite selection"], ["runners", "Runners"], ["entrypoints", "Entrypoints"]].forEach(([key, label]) => {
      execution.append(node("h3", "", label), testReferences(group.execution[key]));
    });
    result.append(detail("Execution dependencies and ownership", execution));
    result.append(detail("Required artifacts", valueView(group.required_artifacts)), detail("Coverage and execution limits", valueView(group.limits), true));
    return result;
  }
  function sharedTestExecution(groups) {
    const body = node("div");
    body.append(node("p", "section-note", "References are grouped by their recorded role in execution. Each group's detail retains its specific role and limits; these references do not establish a run sequence."));
    [["selection", "Suite selection"], ["runners", "Runners"], ["entrypoints", "Entrypoints"]].forEach(([field, label]) => {
      const references = new Map();
      groups.forEach(item => list(item.group.execution[field]).forEach(reference => {
        if (!references.has(reference.path)) references.set(reference.path, []);
        references.get(reference.path).push(item);
      }));
      if (!references.size) return;
      body.append(node("h3", "", label));
      const items = node("ul", "record-list test-reference-list");
      references.forEach((users, path) => {
        const item = node("li"); item.append(sourceLink(path));
        const related = node("div", "link-row");
        users.forEach(user => related.append(link(user.group.name, testRoute(user.owner))));
        item.append(node("p", "small muted", "Referenced by:"), related); items.append(item);
      });
      body.append(items);
    });
    return detail("Shared execution support", body);
  }
  function renderTestArchitecture(owner) {
    const groups = testGroups(owner);
    if (owner && (!records[owner] || !groups.length)) return notFound("Test architecture scope", owner);
    breadcrumb([{text:"Development", href:"#development"}, ...(owner ? [{text:"Test architecture", href:testRoute()}, {text:title(owner)}] : [{text:"Test architecture"}])]);
    header("Development view · test architecture", owner ? `${title(owner)} — tests` : "Test architecture", "Follow test groups to the responsibilities they assess and the sources, fixtures, execution tooling, and artifacts they require.");
    main.append(developmentNavigation(testRoute(owner)), node("p", "notice", "This perspective records static test organization. Assessment links do not mean implementation ownership; dependency links do not establish execution order, passing tests, or complete coverage."));
    const graphic = projectedDiagram("development-testing", owner); if (graphic) main.append(graphic);
    const ownership = node("section", "panel test-execution-ownership"); ownership.append(node("h2", "", "Shared execution responsibility"));
    ownership.append(node("p", "", "The retained Validation contract owns the shared execution machinery. Its REM allocation remains unresolved; it is not assigned to the Modules assessed by these groups."));
    [...new Set(groups.map(item => item.group.execution.owner_contract))].forEach(path => ownership.append(sourceLink(path, "Execution owner contract ↗")));
    main.append(ownership);
    if (!owner && groups.length) main.append(sharedTestExecution(groups));
    if (!groups.length) main.append(empty("No test groups recorded", "The current Development scope has no typed test architecture observations."));
    if (!owner) {
      const cards = node("div", "card-grid test-group-grid");
      groups.forEach(item => {
        const card = link("", testRoute(item.owner), "module-card"); card.dataset.testGroup = item.group.name;
        card.append(node("h3", "", item.group.name), node("p", "", item.group.observation_boundary), node("div", "card-meta", `Assesses ${title(item.owner)}`)); cards.append(card);
      });
      main.append(section("Explore a test group", cards));
    } else {
      const links = node("div", "link-row"); links.append(link("Logical responsibility →", entityRoute(owner)), link("Implementation mapping →", `#development/${owner}`)); main.append(links);
      groups.forEach(item => {
        const article = node("article", "test-group"); article.dataset.testGroup = item.group.name;
        article.append(node("h2", "", item.group.name), testGroupBody(item.owner, item.group));
        const provenance = node("div");
        provenance.append(sourceLink(item.path, "Canonical software realization ↗"), node("p", "small muted", item.field));
        const facet = list(model.facets).find(value => value.owner === owner && value.facet === "software" && value.path === item.path);
        if (facet) {
          if (list(facet.data.observed?.sources).length) provenance.append(node("h3", "", "Observation sources"), valueView(facet.data.observed.sources));
          if (list(facet.data.deferred).length) provenance.append(node("h3", "", "Deferred realization decisions"), valueView(facet.data.deferred));
        }
        article.append(detail("Source attribution and qualification", provenance)); main.append(article);
      });
    }
    main.append(viewScope("development"));
  }
  function scopeRoute(owner, view) {
    if (!owner) return view === "summary" ? "#home" : viewRoute(view);
    return view === "summary" ? entityRoute(owner) : `#${view}/${owner}`;
  }
  function architectureContext(route) {
    const [kind, id] = route;
    if (kind === "module" && modules[id]) return {owner:id, view:"summary"};
    if (kind === "home") return {owner:null, view:"summary"};
    if (kind === "overview") return {owner:null, view:"logical"};
    if (viewKinds.includes(kind)) return {owner:modules[id] ? id : null, view:kind};
    if (kind === "scenario") return {owner:null, view:"scenarios"};
    if (["cooperation", "contributions"].includes(kind)) return {owner:null, view:"logical"};
    return null;
  }
  function architectureViewNavigation(context) {
    const nav = node("nav", "architecture-view-navigation"); nav.setAttribute("aria-label", "Architecture views");
    ["summary", ...viewKinds].forEach(kind => {
      const item = link(nice(kind), scopeRoute(context.owner, kind));
      if (kind === context.view) item.setAttribute("aria-current", "page");
      nav.append(item);
    }); return nav;
  }
  function authoredDiagram(topic, inline = false) {
    const panel = node("section", "diagram-panel authored-diagram");
    const toolbar = node("div", "diagram-toolbar"), controls = node("div", "diagram-tools");
    toolbar.append(node(inline ? "h3" : "h2", "", topic.title));
    if (inline) controls.append(link("Open expanded →", topic.route, "diagram-expanded-link"));
    const viewport = node("div", "diagram-viewport authored-viewport"); viewport.tabIndex=0; viewport.setAttribute("aria-label", `${topic.title}: scrollable diagram`);
    const img = node("img"); img.src=topic.image; img.alt=`${topic.title}. Authored description and source text follow.`;
    let width;
    const available = () => Math.max(100, viewport.clientWidth-36);
    const resize = n => { width=Math.max(120,Math.min(4000,n));img.style.width=width+"px"; };
    [["−","Zoom out",()=>resize(width*.8)],["+","Zoom in",()=>resize(width*1.25)],["Fit","Fit diagram",()=>resize(available())]].forEach(([label,aria,action])=>{
      const button=node("button","",label);button.type="button";button.setAttribute("aria-label",aria);button.onclick=action;controls.append(button);
    }); toolbar.append(controls);viewport.append(img);panel.append(toolbar);
    if (inline) panel.append(node("p", `qualification diagram-qualification ${topic.qualification}`, `${qualificationLabel(topic.qualification)} · ${title(topic.owner)} · ${nice(topic.kind)}`), node("p", "diagram-introduction", topic.description));
    panel.append(viewport,node("p","diagram-caption","Scroll within the diagram or use Fit. Rendering does not establish implementation or approval."));
    initializeDiagrams.push(() => resize(Math.max(Math.min(available(),topic.width),Math.min(topic.width,800))));
    return panel;
  }
  function viewDiagramSections(topics, grouped, overview) {
    const result = node("div", grouped ? "inline-view-diagrams process-details" : "inline-view-diagrams");
    const targets = [];
    const addTarget = (element, label, id) => {
      element.id = id; element.tabIndex = -1;
      targets.push({element, label});
    };
    const toc = node("nav", "diagram-section-navigation"); toc.setAttribute("aria-label", "On this page");
    if (topics.length + (overview ? 1 : 0) > 1) result.append(toc);
    if (overview) {
      addTarget(overview, overview.querySelector("h2")?.textContent || "Overview", "diagram-overview");
      result.append(overview);
    }
    let currentGroup, body = result;
    const sources = node("div");
    topics.forEach(topic => {
      if (grouped && currentGroup !== topic.group) {
        currentGroup = topic.group; body = node("div", "diagram-group-body");
        result.append(section(currentGroup, body));
      }
      let panel;
      if (topic.image) {
        panel = authoredDiagram(topic, true);
        const source = node("div");
        source.append(sourceLink(topic.path, "Owning design ↗"), node("p", "small muted", `Anchor: ${topic.anchor}`), node("code", "source-digest", topic.source_digest), sourceLink(topic.registration, "View registration ↗"), node("pre", "authored-source", topic.source));
        sources.append(detail(topic.title, source));
      } else {
        panel = diagram(topic.key, topic.title, topic.caption || "", undefined, topic);
        panel.querySelector(".diagram-toolbar").append(link("Open expanded →", topic.route, "diagram-expanded-link"));
        panel.querySelector(".diagram-toolbar").after(node("p", `qualification diagram-qualification ${topic.qualification}`, `${qualificationLabel(topic.qualification)} · ${title(topic.owner)}`));
      }
      panel.dataset.topicRoute = topic.route;
      addTarget(panel, topic.title, `diagram-${topic.key}`);
      body.append(panel);
    });
    if (toc.parentNode) {
      toc.append(node("strong", "", "On this page"));
      const entries = node("ul");
      targets.forEach(({element, label}) => {
        const button = node("button", "section-jump", label); button.type = "button";
        button.setAttribute("aria-controls", element.id);
        button.onclick = () => { element.focus({preventScroll:true}); element.scrollIntoView({block:"start"}); };
        const entry = node("li"); entry.append(button); entries.append(entry);
      });
      toc.append(entries);
    }
    if (sources.childElementCount) result.append(detail("Diagram sources and attribution", sources));
    return result;
  }
  function authoredTopicsContent(kind, owner, inline = false, overview = null) {
    const selected = authoredTopics.filter(t => t.view === kind && (!owner || t.owner === owner));
    if (!selected.length) return null;
    if (inline) return viewDiagramSections(selected, false, overview);
    const cards = node("div", "card-grid");
    selected.forEach(t => {
      const a = link("", t.route, "module-card");
      a.append(node("span", `qualification ${t.qualification}`, qualificationLabel(t.qualification)), node("h3", "", t.title),
        node("p", "", t.description), node("p", "small muted", `${title(t.owner)} · ${nice(t.kind)}`)); cards.append(a);
    }); return section("Design details", cards);
  }
  function renderAuthoredTopic(kind, owner, qualification, diagramKind, identity) {
    const requestedRoute = `#${kind}/${owner}/${qualification}/${diagramKind}/${identity}`;
    const topic = authoredTopics.find(t => t.route === requestedRoute || list(t.previous_routes).includes(requestedRoute));
    if (!topic) return notFound("Design topic", identity);
    breadcrumb([{text:title(owner),href:entityRoute(owner)},{text:nice(kind),href:`#${kind}/${owner}`},{text:topic.title}]);
    header(`${nice(kind)} · ${owner}`, topic.title, topic.description);
    main.append(link(`← ${nice(kind)} overview`, scopeRoute(owner, kind), "topic-return"));
    main.append(node("p", `qualification ${qualification}`, `${qualificationLabel(qualification)} · ${nice(topic.kind)}`));
    main.append(authoredDiagram(topic));
    const source=node("div");source.append(node("p","",topic.description),node("pre","authored-source",topic.source));
    main.append(detail("Text explanation and exact diagram source",source));
    const attribution=node("div");attribution.append(sourceLink(topic.path,"Owning design ↗"),node("p","small muted",`Anchor: ${topic.anchor}`),node("code","source-digest",topic.source_digest),sourceLink(topic.registration,"View registration ↗"));
    main.append(detail("Source identity and qualification",attribution));
    main.append(section("Accountable design owner",entityList([owner])),section("Direct Function allocations",entityList(modules[owner].functions)),section("Direct allocated requirements",entityList(modules[owner].allocated_requirements)));
    const topics=kind === "process" ? processTopicsContent(owner) : authoredTopicsContent(kind,owner);if(topics)main.append(topics);
    if (kind === "process") { const context = parentProcessTopics(owner); if (context) main.append(context); }
  }
  function renderHome() {
    header("System overview", "RigorLoop architecture", "Explore the selected engineering model, its responsibilities and their architectural views.");
    main.append(section("Top-level Modules",moduleCards(roots)));
    main.append(node("p","notice","Views show selected relationships and source-owned explanations. Missing details and recorded design limits remain visible on their owning Module pages."));
    const source = node("div");
    source.append(node("p", "", "Model status and realization qualification are distinct; neither implies approval or satisfaction."), node("p", "", "Source identity for this generated model:"), node("code", "source-digest", model.source_digest));
    main.append(detail("Snapshot and sources", source));
  }
  function renderModuleScenarios(owner) {
    if(!modules[owner])return notFound("Module",owner);
    breadcrumb([{text:title(owner),href:entityRoute(owner)},{text:"Scenarios"}]);header("Module Scenario view",title(owner),moduleViewQuestions.scenarios);
    const selected=list(views.scenarios?.scenarios).filter(t=>list(t.modules).includes(owner));
    if(selected.length)main.append(section("Participation walkthroughs",entityList(selected.map(t=>t.scenario))),node("p","section-note","Declared participation does not establish execution or satisfaction."));
    const obligations=new Set(list(model.relationships).filter(r=>r.relation==="parent" && modules[owner].allocated_requirements.includes(r.source)).map(r=>r.target));
    const related=Object.keys(records).filter(id=>data(id).type==="scenario" && list(data(id).informs).some(sr=>obligations.has(sr)));
    if(related.length){main.append(section("Related stakeholder Scenarios",entityList(related)),node("p","section-note","Derived through this Module's directly allocated obligations and their SRs. These links preserve black-box intent; they do not assert declared execution participation or coverage."));}
    const authored = authoredTopicsContent("scenarios", owner); if (authored) main.append(authored);
    if (!selected.length) {
      const explanation = "No selected walkthrough declares this Module's participation. Related Scenarios do not establish execution or coverage.";
      main.append(related.length || authored
        ? node("p", "section-note", `No participation walkthrough recorded. ${explanation}`)
        : empty("No participation walkthrough recorded", explanation));
    }
    main.append(sourceDetails(owner));
  }
  function developmentTable(mapping, label, qualification) {
    const body = node("div", "development-table");
    body.append(node("p", `qualification ${qualification}`, `${qualificationLabel(qualification)} · ${label}`));
    body.append(node("p", "small muted development-scroll-hint", "Scroll horizontally to read all columns."));
    const scroll = node("div", "development-table-scroll"); scroll.tabIndex = 0;
    scroll.setAttribute("role", "region"); scroll.setAttribute("aria-label", `${label} table`);
    const table = node("table"), head = node("thead"), labels = node("tr"), rows = node("tbody");
    mapping.headers.forEach(label => { const cell = node("th", "", label); cell.scope = "col"; labels.append(cell); });
    head.append(labels);
    mapping.rows.forEach(row => {
      const entry = node("tr");
      row.forEach(segments => {
        const cell = node("td");
        segments.forEach(segment => cell.append(segment.path ? sourceLink(segment.path, segment.text) : document.createTextNode(segment.text)));
        entry.append(cell);
      });
      rows.append(entry);
    });
    table.append(head, rows); scroll.append(table); body.append(scroll);
    if (mapping.explanation) body.append(node("p", "section-note", mapping.explanation));
    const attribution = node("div");
    attribution.append(sourceLink(mapping.source, "Owning design source ↗"), node("code", "source-digest", mapping.source_digest));
    body.append(detail(`${label} source`, attribution));
    return body;
  }
  function developmentBuildResources(owner) {
    const mapping = model.development_build_resources?.[owner];
    if (!mapping) return null;
    const body = developmentTable(mapping, "Build and resources", "proposed");
    body.classList.add("development-build-resources");
    return section("Build and resources", body);
  }
  function developmentImplementationReferences(owner) {
    const mapping = model.development_implementations?.[owner];
    if (!mapping) return null;
    const body = developmentTable(mapping, "Current implementation", "observed");
    body.classList.add("development-implementation");
    const references = detail("Implementation references", body);
    references.classList.add("implementation-references");
    return references;
  }
  function renderFacetView(kind, owner) {
    const view = views[kind];
    if (!view) return notFound("Architecture view", kind);
    const facets = facetsFor(kind, owner);
    if (owner && !records[owner]) return notFound(`${nice(kind)} scope`, owner);
    breadcrumb(owner ? [{text:nice(kind), href:viewRoute(kind)}, {text:title(owner)}] : [{text:nice(kind)}]);
    header(`${nice(kind)} view`, owner ? title(owner) : view.title, modules[owner] ? moduleViewQuestions[kind] : owner ? data(owner).description : view.question);
    if (!owner && kind === "physical") main.append(physicalNavigation(owner ? `#physical/${owner}` : "#physical"));
    if (!owner && kind === "development") main.append(developmentNavigation(owner ? `#development/${owner}` : "#development"));
    let graphic = projectedDiagram(kind, owner);
    if (!graphic && kind === "physical" && owner) {
      const contexts = relatedPhysicalTopics(owner);
      if (contexts.length === 1) {
        const context = contexts[0];
        graphic = diagram(context.key, `${context.title} · context`, context.caption || "", undefined, context);
      }
    }
    const inline = Boolean(modules[owner]);
    const authored = kind === "process" ? null : authoredTopicsContent(kind, owner, inline, graphic);
    const topics = kind === "process" ? processTopicsContent(owner, inline, graphic) : kind === "physical" ? physicalTopicCards(owner) : null;
    // A composed inline section already includes the scope's overview graph.
    if (graphic && !(inline && (authored || (kind === "process" && topics)))) main.append(graphic);
    if (authored) main.append(authored);
    if (topics) main.append(topics);
    const buildResources = kind === "development" ? developmentBuildResources(owner) : null;
    if (buildResources) main.append(buildResources);
    const implementation = kind === "development" ? developmentImplementationReferences(owner) : null;
    if (kind === "development") { const reading = testPerspectiveLink(owner); if (reading) main.append(reading); }
    if (owner && !facets.length && !graphic && !authored && !topics && !buildResources) main.append(empty(`No ${nice(kind).toLowerCase()} realization detail recorded`, "The selected owner and source limits remain unchanged. Missing detail is not inferred from another view."));
    if (kind === "process" && owner) { const context = parentProcessTopics(owner); if (context) main.append(context); }
    if (!owner) {
      const owners = [...new Set(facets.map(facet => facet.owner))];
      const cards = node("div", "card-grid realization-grid");
      owners.forEach(id => {
        const owned = facets.filter(facet => facet.owner === id);
        const card = link("", `#${kind}/${encodeURIComponent(id)}`, "module-card realization-card");
        card.append(node("h3", "", title(id)), node("p", "", facetSummary(owned[0])));
        const tags = node("div", "facet-tags"); owned.forEach(facet => tags.append(node("span", "tag", nice(facet.facet))));
        card.append(tags); cards.append(card);
      });
      if (cards.childElementCount) main.append(section("Explore by responsibility", cards));
      else if (!graphic && !authored && !topics) main.append(empty("No realization facets recorded", "The view's scope and limits identify the remaining design work."));
    } else {
      if (!modules[owner]) {
        const links = node("div", "link-row"); links.append(link("Definition →", entityRoute(owner))); main.append(links);
        const related = relatedViews([owner], kind); if (related) main.append(related);
      }
      facets.forEach(facet => main.append(facetPanel(facet)));
      if (list(data(owner).design_limits).length) main.append(detail("Responsibility design limits", valueView(data(owner).design_limits)));
    }
    if (implementation) main.append(implementation);
    main.append(viewScope(kind));
  }
  function renderScenarios() {
    const view = views.scenarios;
    if (!view) return notFound("Architecture view", "scenarios");
    breadcrumb([{text:"Scenarios"}]); header("Scenario view", view.title, view.question);
    if (view.scope) main.append(node("p", "section-note", Array.isArray(view.scope) ? view.scope.join(" ") : view.scope));
    main.append(node("p", "notice", "Each walkthrough connects a stakeholder situation to selected behavior, contracts, and recorded limits. Participation does not establish execution order or successful verification."));
    const graphic = projectedDiagram("scenarios"); if (graphic) main.append(graphic);
    const cards = node("div", "card-grid realization-grid");
    list(view.scenarios).forEach(slice => {
      const scenario = data(slice.scenario);
      const card = link("", `#scenario/${encodeURIComponent(slice.scenario)}`, "module-card");
      card.append(node("h3", "", scenario.title), node("p", "", scenario.goal));
      card.append(node("div", "card-meta", `${list(slice.outcomes).length} recorded outcomes · ${list(slice.outcomes).some(item => item.profiled) ? "selected architecture readings" : "broader traceability; outcome detail unselected"}`));
      cards.append(card);
    });
    main.append(cards);
    const authored = authoredTopicsContent("scenarios"); if (authored) main.append(authored);
    main.append(viewScope("scenarios"));
  }
  function scenarioSlice(id) {
    return list(views.scenarios?.scenarios).find(item => item.scenario === id);
  }
  function outcomeRoute(id, key) {
    return `#scenario/${encodeURIComponent(id)}/outcome/${encodeURIComponent(key)}`;
  }
  function outcomeCards(slice) {
    const result = node("div", "outcome-groups");
    [["expected", "Expected outcome"], ["alternative", "Alternative outcomes"], ["failure", "Failure outcomes"]].forEach(([kind, heading]) => {
      const selected = list(slice.outcomes).filter(item => item.kind === kind);
      if (!selected.length) return;
      const cards = node("div", "card-grid outcome-card-grid");
      selected.forEach(item => {
        const card = link("", outcomeRoute(slice.scenario, item.key), "module-card outcome-card"); card.dataset.outcomeKey = item.key;
        card.append(node("h3", "", item.title));
        if (item.condition && item.condition !== item.title) card.append(node("p", "outcome-condition", item.condition));
        card.append(node("p", "outcome-result", item.outcome));
        card.append(node("div", "card-meta", item.profiled ? "Explore selected obligations and architecture context →" : "Read the outcome and its analysis gaps →"));
        cards.append(card);
      });
      result.append(section(heading, cards));
    });
    return result;
  }
  function scenarioTraceability(slice) {
    const body = node("div");
    body.append(node("p", "section-note", "This broader Scenario context retains every selected requirement and behavior allocation. It is separate from the narrower obligations selected for an individual outcome and does not establish execution order or complete coverage."));
    body.append(node("h3", "", "Participating responsibilities"), entityList(slice.modules));
    if (list(slice.context_modules).length) body.append(node("h3", "", "Contract and ancestor context"), entityList(slice.context_modules));
    body.append(node("h3", "", "Selected Interfaces"), entityList(slice.interfaces), node("h3", "", "System Requirements"), entityList(slice.requirements), node("h3", "", "Features"), entityList(data(slice.scenario).exercises), node("h3", "", "Functions"), entityList(slice.functions), node("h3", "", "Allocated Requirements"), entityList(slice.allocated_requirements));
    if (list(slice.owner_limits).length) body.append(detail("Responsibility limits", valueView(slice.owner_limits)));
    if (list(slice.allocation_gaps).length) body.append(detail("Allocation gaps", valueView(slice.allocation_gaps)));
    if (list(slice.limits).length) body.append(detail("Broader walkthrough limits", valueView(slice.limits)));
    const relationships = list(slice.relationships).concat(list(slice.feature_relationships), list(slice.contract_context).map(item => item.relationship).filter(Boolean));
    if (relationships.length) {
      const sources = node("ul", "record-list");
      [...new Map(relationships.map(item => [[item.source, item.relation, item.target, item.path, item.field].join("|"), item])).values()].forEach(item => {
        const row = node("li"); row.append(entityLink(item.source), node("span", "small muted", ` ${nice(item.relation)} `), entityLink(item.target));
        const provenance = node("p", "small muted"); provenance.append(sourceLink(item.path, "Owning relationship ↗"), document.createTextNode(` · ${item.field}`)); row.append(provenance); sources.append(row);
      });
      body.append(detail("Relationship provenance", sources));
    }
    return detail("Broader Scenario traceability and limits", body);
  }
  function outcomeSourceRoutes(source, kind) {
    const prefix = (parent, child) => parent === child || child.startsWith(parent + "/");
    const matches = Object.values(model.view_diagrams || {}).filter(descriptor => descriptor.view === kind && descriptor.perspective !== "testing").flatMap(descriptor => {
      const route = descriptor.route || (descriptor.owner ? `#${kind}/${descriptor.owner}` : null);
      if (!route) return [];
      const sources = list(descriptor.sources).filter(ref => ref.owner === source.owner && ref.facet === source.facet && ref.path === source.path && typeof ref.field === "string" && (prefix(ref.field, source.field) || prefix(source.field, ref.field)));
      if (!sources.length) return [];
      return [{route, title:descriptor.title, specificity:Math.max(...sources.map(ref => Math.min(ref.field.length, source.field.length)))}];
    });
    if (!matches.length) return facetsFor(kind, source.owner).some(facet => facet.path === source.path) ? [{route:`#${kind}/${source.owner}`, title:`${nice(kind)} · ${title(source.owner)}`}] : [];
    const best = Math.max(...matches.map(item => item.specificity));
    return [...new Map(matches.filter(item => item.specificity === best).map(item => [item.route, item])).values()];
  }
  function outcomeReference(source, kind, context = false) {
    const value = resolveSourceField(source), result = node("article", "outcome-reference");
    result.dataset.sourceOwner = source.owner; result.dataset.sourceField = source.field;
    const heading = node("h3"); heading.append(entityLink(source.owner)); result.append(heading);
    const label = value?.name || nice(source.field.split("/").filter(token => token && !/^\d+$/.test(token)).slice(-1)[0] || source.facet);
    result.append(node("p", "contract-purpose", label));
    const links = node("div", "link-row");
    const routes = context ? [{route:testRoute(source.owner), title:"Related test organization"}] : outcomeSourceRoutes(source, kind);
    routes.forEach(route => links.append(link(`${route.title} →`, route.route)));
    if (links.childElementCount) result.append(links);
    let content;
    if (context && value?.execution && value?.test_sources) content = testGroupBody(source.owner, value);
    else if (kind === "physical") content = physicalFact(value);
    else if (kind === "development" && value?.path && value?.role) {
      content = node("div"); content.append(node("p", "", value.role), sourceLink(value.path));
      const remaining = Object.keys(value).filter(key => !["path", "role"].includes(key));
      if (remaining.length) content.append(recordFields(value, remaining));
    }
    else if (value?.steps && value?.preconditions) content = processSequence(value);
    else if (value?.states && value?.transitions) content = processLifecycle(value);
    else content = valueView(value === undefined ? "The selected reference is unavailable; regenerate this browser." : value);
    result.append(detail(context ? "Contextual test organization and limits" : "Exact selected source detail", content));
    const parents = node("div"), segments = source.field.split("/").filter(Boolean);
    for (let length = 1; length < segments.length; length++) {
      const pointer = "/" + segments.slice(0, length).join("/");
      const parent = resolveSourceField({...source, field:pointer});
      if (!parent || Array.isArray(parent) || typeof parent !== "object") continue;
      const fields = ["preconditions", "condition", "constraints", "limits"].filter(key => key in parent);
      if (!fields.length) continue;
      parents.append(node("h3", "", parent.name || parent.operation || "Containing source context"), recordFields(parent, fields), node("p", "small muted", pointer));
    }
    if (parents.childElementCount) result.append(detail("Enclosing conditions and constraints", parents));
    const provenance = node("p", "small muted"); provenance.append(sourceLink(source.path, "Canonical realization record ↗"), document.createTextNode(` · ${source.field}`)); result.append(provenance);
    const facet = list(model.facets).find(item => item.owner === source.owner && item.facet === source.facet && item.path === source.path);
    if (facet) {
      const limits = node("div");
      if (list(facet.data.observed?.sources).length) limits.append(node("h3", "", "Observation sources"), valueView(facet.data.observed.sources));
      if (list(facet.data.deferred).length) limits.append(node("h3", "", "Deferred decisions and limitations"), valueView(facet.data.deferred));
      if (limits.childElementCount) result.append(detail("Source attribution and retained limitations", limits));
    }
    return result;
  }
  function renderScenarioOutcome(id, key) {
    const slice = scenarioSlice(id), selected = list(slice?.outcomes).find(item => item.key === key);
    if (!slice || !selected) return notFound("Scenario outcome", `${id}/${key}`);
    breadcrumb([{text:"Scenarios", href:"#scenarios"}, {text:title(id), href:`#scenario/${id}`}, {text:selected.title}]);
    header(`${nice(selected.kind)} outcome · ${id}`, selected.title, data(id).goal);
    const navigation = node("nav", "outcome-navigation"); navigation.setAttribute("aria-label", "Scenario outcomes");
    navigation.append(link("All outcomes", `#scenario/${id}`));
    const chooser = node("details", "outcome-chooser"), choices = node("div", "outcome-choice-list");
    chooser.append(node("summary", "", "Choose an outcome"));
    list(slice.outcomes).forEach(item => { const anchor = link(item.title, outcomeRoute(id, item.key)); if (item.key === key) anchor.setAttribute("aria-current", "page"); choices.append(anchor); });
    chooser.append(choices); navigation.append(chooser);
    main.append(navigation);
    const result = node("section", "panel outcome-statement");
    if (selected.condition) result.append(node("h2", "", "Condition"), node("p", "outcome-condition", selected.condition));
    result.append(node("h2", "", "Required outcome"), node("p", "outcome-result", selected.outcome));
    const source = node("p", "small muted"); source.append(sourceLink(selected.source.path, "Owning Scenario ↗"), document.createTextNode(` · ${selected.source.field}`)); result.append(source); main.append(result);
    main.append(node("p", "notice", selected.profiled ? "This is a bounded reading selection of existing obligations and architecture facts. It does not establish complete outcome coverage, execution order, or requirement satisfaction." : "A detailed architecture selection is not recorded for this outcome. The Scenario meaning and broader traceability remain available; the gaps below retain the unfinished analysis."));
    if (list(selected.gaps).length || list(selected.limit_sources).length) {
      const gaps = node("div"); gaps.append(valueView(selected.gaps));
      list(selected.limit_sources).forEach(source => {
        const record = node("article", "outcome-limit-source"); record.dataset.limitOwner = source.owner; record.dataset.limitField = source.field;
        record.append(node("h3", "", "Source of unresolved wording"), entityLink(source.owner), node("p", "", source.text));
        const provenance = node("p", "small muted"); provenance.append(sourceLink(source.path, "Owning requirement ↗"), document.createTextNode(` · ${source.field}`)); record.append(provenance); gaps.append(record);
      });
      main.append(detail("Reading and analysis gaps", gaps, !selected.profiled || list(selected.limit_sources).length > 0));
    }
    if (list(selected.obligations).length) {
      const obligations = node("div", "outcome-obligations");
      selected.obligations.forEach(obligation => {
        const card = node("article", "panel outcome-obligation"); card.dataset.obligationOwner = obligation.owner; card.dataset.obligationField = obligation.field;
        const heading = node("h3"); heading.append(entityLink(obligation.owner)); card.append(heading, node("p", "", obligation.text));
        if (data(obligation.owner).allocated_to) {
          const owner = node("p", "small"); owner.append(document.createTextNode("Accountable Module: "), entityLink(data(obligation.owner).allocated_to)); card.append(owner);
        }
        const ref = node("p", "small muted"); ref.append(sourceLink(obligation.path, "Owning requirement ↗"), document.createTextNode(` · ${obligation.field}`)); card.append(ref); obligations.append(card);
      });
      main.append(section("Selected obligations", obligations));
    }
    if (list(selected.modules).length) main.append(section("Accountable responsibilities", entityList(selected.modules)));
    if (list(selected.interfaces).length) {
      const contracts = node("div", "contract-grid");
      selected.interfaces.forEach(identity => {
        const card = node("section", "panel"), heading = node("h3"); heading.append(entityLink(identity));
        const provider = node("p", "small"); provider.append(document.createTextNode("Contract provider: "), entityLink(interfaces[identity].provider));
        card.append(heading, node("p", "", data(identity).description), provider); contracts.append(card);
      });
      main.append(section("Selected Interface context", contracts), node("p", "section-note", "The Interface provider retains contract accountability. A parent provider does not acquire the selected child obligations through this reading."));
    }
    ["process", "development", "physical"].forEach(kind => {
      const references = list(selected.realization?.[kind]); if (!references.length) return;
      const content = node("div", "outcome-reference-list"); references.forEach(reference => content.append(outcomeReference(reference, kind)));
      main.append(section(`${nice(kind)} context`, content));
    });
    if (list(selected.test_context).length) {
      const context = node("div");
      context.append(node("p", "notice", "These test groups provide organizational context only. Their selection asserts no outcome-to-test coverage relationship, adequate assertions, passing execution, or verification evidence."));
      selected.test_context.forEach(reference => context.append(outcomeReference(reference, "development", true)));
      main.append(section("Contextual test organization", context));
    }
    main.append(scenarioTraceability(slice), sourceDetails(id));
  }
  function renderScenario(id) {
    const slice = scenarioSlice(id);
    if (!slice || !records[id]) return notFound("Selected Scenario", id);
    const scenario = data(id);
    breadcrumb([{text:"Scenarios", href:"#scenarios"}, {text:scenario.title}]);
    header(`Scenario · ${id}`, scenario.title, scenario.goal);
    main.append(node("p", "section-note", "Start with a stakeholder outcome. Each reading preserves its required result and distinguishes selected obligations, architecture context, and remaining analysis gaps."));
    main.append(outcomeCards(slice));
    const graphic = projectedDiagram("scenario", id); if (graphic) main.append(section("Selected architecture context", graphic));
    const situation = node("div");
    situation.append(recordFields(scenario, ["actor", "context", "trigger", "preconditions"]));
    const steps = node("ol", "scenario-steps");
    list(scenario.interaction).forEach(step => {
      const item = node("li"); item.append(node("strong", "", step.actor), node("p", "", step.action || step.response)); steps.append(item);
    });
    situation.append(node("h3", "", "Recorded stakeholder interaction"), steps);
    main.append(detail("Stakeholder situation and interaction", situation), scenarioTraceability(slice));
    const related = relatedViews(list(slice.modules).concat(list(slice.context_modules))); if (related) main.append(related);
    main.append(sourceDetails(id));
  }
  function cliReadingLinks() {
    const result = node("div", "link-row");
    result.append(link("CLI cooperation and walkthroughs →", "#cooperation"), link("CLI acceptance contributions →", "#contributions"));
    return result;
  }
  function resolveRecordField(source) {
    let value = data(source.owner);
    for (const encoded of source.field.replace(/^\//, "").split("/")) {
      const key = encoded.replace(/~1/g, "/").replace(/~0/g, "~");
      if (value === null || value === undefined || !Object.prototype.hasOwnProperty.call(value, key)) return undefined;
      value = value[key];
    }
    return value;
  }
  function cooperationSource(source) {
    const result = node("article", "cooperation-source");
    result.dataset.sourceOwner = source.owner;
    result.dataset.sourceField = source.field;
    const value = resolveRecordField(source);
    const heading = node("h3"); heading.append(entityLink(source.owner)); result.append(heading);
    if (value && typeof value === "object" && !Array.isArray(value) && value.name && value.purpose) {
      result.append(node("p", "contract-purpose", value.purpose), node("code", "small muted", value.name));
      result.append(recordFields(value, ["inputs", "preconditions", "outputs", "behavior", "failure_behavior"]));
    } else if (value !== undefined) result.append(valueView(value));
    else result.append(node("p", "notice", "The selected source field is unavailable. Regenerate this browser from the current canonical records."));
    const provenance = node("p", "small muted");
    provenance.append(sourceLink(source.path, "Canonical contract ↗"), document.createTextNode(` · ${source.field}`));
    result.append(provenance);
    return result;
  }
  function cooperationCards() {
    const result = node("div", "card-grid realization-grid");
    list(cooperation.walkthroughs).forEach(slice => {
      const scenario = data(slice.scenario);
      const card = link("", `#cooperation/${slice.scenario}`, "module-card");
      card.append(node("h3", "", scenario.title), node("p", "", scenario.goal));
      card.append(node("div", "card-meta", `${list(slice.allocated_requirements).length} selected allocated obligations`));
      result.append(card);
    });
    return result;
  }
  function cooperationNavigation(id) {
    const result = node("nav", "view-subnav"); result.setAttribute("aria-label", "CLI cooperation");
    const overview = link("Cooperation overview", "#cooperation");
    if (!id) overview.setAttribute("aria-current", "page");
    result.append(overview, link("Acceptance contributions", "#contributions"));
    if (id) result.append(link("All CLI commands", "#commands"));
    return result;
  }
  function renderCooperation(id) {
    if (id) return renderCooperationScenario(id);
    breadcrumb([{text:"CLI cooperation"}]);
    header("Logical architecture", "CLI cooperation", "Read the public command and record contracts together, then follow a selected stakeholder situation to its accountable obligations.");
    main.append(cooperationNavigation(), node("p", "notice", "These are logical contract responsibilities, not an observed execution sequence. The walkthroughs select review scope; they do not add obligations or establish satisfaction."));
    const ownership = node("div", "contract-grid");
    list(cooperation.interfaces).forEach(contract => {
      const card = node("section", "panel");
      const heading = node("h2"); heading.append(entityLink(contract)); card.append(heading, node("p", "", data(contract).description));
      card.append(node("h3", "", "Accountable provider"), entityList([interfaces[contract]?.provider].filter(Boolean)));
      card.append(node("h3", "", "Declared consumers"), entityList(interfaces[contract]?.consumers));
      ownership.append(card);
    });
    main.append(ownership, node("p", "section-note", "Public Interface ownership remains with its declared provider. The selected Function and Allocated Requirement records identify contributing child responsibilities; this reading creates no additional provider or consumption relationship."));
    const topics = node("div", "cooperation-topics");
    list(cooperation.topics).forEach(topic => {
      const body = node("div"); list(topic.sources).forEach(source => body.append(cooperationSource(source)));
      const item = detail(topic.title, body); item.dataset.cooperationTopic = topic.key; topics.append(item);
    });
    main.append(section("Read a contract responsibility", topics));
    const observed = node("div", "link-row");
    observed.append(link("Observed publication and recovery interactions →", "#process"));
    main.append(observed, section("CLI Scenario walkthroughs", cooperationCards()));
    const rules = node("div");
    list(cooperation.interfaces).forEach(contract => {
      const heading = node("h3"); heading.append(entityLink(contract));
      rules.append(heading, recordFields(data(contract), ["consistency_rules", "compatibility_rules"]));
      rules.append(sourceLink(records[contract]?.path, "Canonical contract and provenance ↗"));
    });
    main.append(detail("Contract consistency and retained boundaries", rules), viewScope("logical"));
  }
  function contributionCard(item) {
    const card = node("article", "contribution-card");
    card.dataset.contribution = `${item.requirement}-AC${item.criterion}`;
    card.append(node("h3", "", `Acceptance criterion ${item.criterion}`), node("p", "criterion-text", item.criterion_text));
    card.append(node("h4", "", "Contribution argument"), node("p", "contribution-basis", item.basis));
    const allocation = node("div", "contribution-allocation");
    list(item.allocated_requirements).forEach(id => {
      const row = node("div", "mapping-item"); row.append(entityLink(id));
      const accountable = data(id).allocated_to;
      if (accountable) {
        const ownership = node("p", "small"); ownership.append(document.createTextNode("Accountable responsibility: "), entityLink(accountable)); row.append(ownership);
      }
      allocation.append(row);
    });
    card.append(detail("Allocated contributors and source", allocation));
    allocation.append(node("p", "small muted", item.locator));
    const source = node("p", "small muted");
    source.append(sourceLink(item.path, "Owning System Requirement ↗"), document.createTextNode(` · ${item.source_pointer}`));
    allocation.append(source);
    return card;
  }
  function renderContributions(scope) {
    if (scope && !contributions.some(item => item.requirement === scope || list(item.allocated_requirements).includes(scope))) return notFound("CLI contribution scope", scope);
    breadcrumb([{text:"CLI cooperation", href:"#cooperation"}, {text:"Acceptance contributions"}]);
    header("Requirement allocation", "CLI acceptance contributions", "Read each system acceptance criterion with its source-owned allocation argument and accountable responsibilities.");
    main.append(cliReadingLinks(), node("p", "notice", "These arguments explain how allocated obligations contribute to a system criterion. They are design rationale, not verification evidence or a claim that the criterion is satisfied."));
    if (scope) {
      const selection = node("p", "section-note"); selection.append(document.createTextNode("Selected scope: "), entityLink(scope), document.createTextNode(" · "), link("Show all contributions", "#contributions")); main.append(selection);
    }
    const selected = contributions.filter(item => !scope || item.requirement === scope || list(item.allocated_requirements).includes(scope));
    const controls = node("div", "catalog-controls");
    const field = node("div", "filter-field"), label = node("label", "", "Find a criterion or contribution"); label.htmlFor = "contribution-filter";
    const filter = node("input"); filter.type = "search"; filter.id = "contribution-filter"; filter.placeholder = "Criterion, argument, requirement, or responsibility"; field.append(label, filter);
    const group = node("div", "filter-field"), groupLabel = node("label", "", "System Requirement"); groupLabel.htmlFor = "contribution-requirement";
    const select = node("select"); select.id = "contribution-requirement";
    const all = node("option", "", "All System Requirements"); all.value = ""; select.append(all);
    [...new Set(selected.map(item => item.requirement))].forEach(id => { const option = node("option", "", title(id)); option.value = id; select.append(option); });
    group.append(groupLabel, select); controls.append(field, group); main.append(controls);
    const count = node("p", "results-count"); count.setAttribute("role", "status");
    const results = node("div"); main.append(count, results);
    function refresh() {
      const query = filter.value.trim().toLocaleLowerCase();
      const matches = selected.filter(item => {
        const ids = [item.requirement, ...list(item.allocated_requirements)];
        const owners = ids.map(id => data(id).allocated_to).filter(Boolean);
        const text = [item.criterion_text, item.basis, item.locator, ...ids.concat(owners).map(id => `${id} ${title(id)}`)].join(" ").toLocaleLowerCase();
        return (!select.value || item.requirement === select.value) && text.includes(query);
      });
      count.textContent = `${matches.length} of ${selected.length} contribution arguments${scope ? " in the selected scope" : ""}`;
      results.replaceChildren();
      if (!matches.length) { results.append(empty("No matching contributions", "Try another criterion, argument, or responsibility, or clear the filters.")); return; }
      [...new Set(matches.map(item => item.requirement))].forEach(id => {
        const group = node("section", "section contribution-group");
        const heading = node("h2"); heading.append(entityLink(id)); group.append(heading, node("p", "section-note", data(id).statement));
        matches.filter(item => item.requirement === id).forEach(item => group.append(contributionCard(item))); results.append(group);
      });
      annotateEntityLinks();
    }
    filter.addEventListener("input", refresh); select.addEventListener("change", refresh); refresh();
  }
  function renderCooperationScenario(id) {
    const slice = list(cooperation.walkthroughs).find(item => item.scenario === id);
    if (!slice || !records[id]) return notFound("CLI Scenario walkthrough", id);
    const scenario = data(id);
    breadcrumb([{text:"CLI cooperation", href:"#cooperation"}, {text:scenario.title}]);
    header(`CLI Scenario · ${id}`, scenario.title, scenario.goal);
    main.append(cooperationNavigation(id), node("p", "section-note", "This walkthrough connects the recorded stakeholder situation to a selected set of allocated obligations. It preserves logical contract composition without claiming implementation order, complete coverage, or executed verification."));
    const situation = node("div", "panel"); situation.append(recordFields(scenario, ["actor", "context", "trigger"]));
    if (list(scenario.preconditions).length) situation.append(detail("Preconditions", valueView(scenario.preconditions)));
    main.append(situation);
    const steps = node("ol", "scenario-steps");
    list(scenario.interaction).forEach(step => { const item = node("li"); item.append(node("strong", "", step.actor), node("p", "", step.action || step.response)); steps.append(item); });
    main.append(section("Recorded stakeholder interaction", steps));
    if (scenario.expected_outcome) main.append(section("Required outcome", node("p", "expected-outcome", scenario.expected_outcome)));
    main.append(detail("Alternatives and failure boundaries", recordFields(scenario, ["alternatives", "failures"]), true));
    const composition = node("div");
    list(slice.modules).forEach(owner => {
      const group = node("section", "panel cooperation-responsibility"), heading = node("h3"); heading.append(entityLink(owner)); group.append(heading);
      list(slice.allocated_requirements).filter(allocation => data(allocation).allocated_to === owner).forEach(allocation => {
        const record = data(allocation), article = node("article", "selected-obligation"); article.dataset.selectedAllocation = allocation;
        const heading = node("h4"); heading.append(entityLink(allocation)); article.append(heading, node("p", "", record.statement));
        article.append(detail("Required observations and acceptance boundaries", valueView(record.acceptance_criteria)));
        const links = node("div", "link-row"); links.append(link("Related system contribution arguments →", `#contributions/${allocation}`), sourceLink(records[allocation].path, "Owning obligation ↗")); article.append(links);
        group.append(article);
      });
      composition.append(group);
    });
    main.append(section("Responsibility composition", composition));
    const contracts = node("div");
    list(slice.interfaces).forEach(contract => {
      const row = node("section", "panel"), heading = node("h3"); heading.append(entityLink(contract));
      const provider = node("p", "small"); provider.append(document.createTextNode("Contract provider: "), entityLink(interfaces[contract].provider));
      row.append(heading, node("p", "", data(contract).description), provider); contracts.append(row);
    });
    main.append(section("Selected contract context", contracts));
    main.append(node("p", "section-note", "Contract providers and parent responsibilities supply context; they do not acquire the selected child allocations. Other contracts of the same Module are outside this walkthrough's selection."));
    const trace = node("div");
    trace.append(node("h3", "", "System Requirements containing the selected obligations"), entityList(slice.requirements), node("h3", "", "Functions constrained by the selected obligations"), entityList(slice.functions), node("h3", "", "Scenario Features"), entityList(scenario.exercises));
    main.append(detail("Selected requirement and behavior traceability", trace));
    const argumentsForScope = contributions.filter(item => list(item.allocated_requirements).some(allocation => list(slice.allocated_requirements).includes(allocation)));
    const argumentsBody = node("div");
    argumentsBody.append(node("p", "section-note", "These complete source arguments mention at least one selected obligation. They may include additional contributors or broader criteria; their inclusion does not assert complete coverage by this Scenario."));
    argumentsForScope.forEach(item => {
      const heading = node("h3"); heading.append(entityLink(item.requirement)); argumentsBody.append(heading, contributionCard(item));
    });
    main.append(detail(`Related system contribution arguments (${argumentsForScope.length})`, argumentsBody));
    const related = relatedViews(list(slice.modules).concat(list(slice.context_modules))); if (related) main.append(related);
    const limits = node("div");
    [...new Set(list(slice.modules).concat(list(slice.context_modules)))].forEach(owner => {
      if (!list(data(owner).design_limits).length) return;
      const heading = node("h3"); heading.append(entityLink(owner)); limits.append(heading, valueView(data(owner).design_limits));
    });
    if (limits.childElementCount) main.append(detail("Responsibility limits", limits));
    const siblings = node("div", "link-row"), position = list(cooperation.walkthroughs).indexOf(slice);
    const previous = cooperation.walkthroughs[position - 1], next = cooperation.walkthroughs[position + 1];
    if (previous) siblings.append(link(`← ${title(previous.scenario)}`, `#cooperation/${previous.scenario}`));
    if (next) siblings.append(link(`${title(next.scenario)} →`, `#cooperation/${next.scenario}`));
    main.append(siblings, sourceDetails(id));
  }
  function renderOverview() {
    const states = [...new Set(roots.map(id => data(id).status).filter(Boolean))];
    header("Logical architecture", "Explore the architecture", "Start with a responsibility, follow its collaborations, then explore the behavior it owns.", states.length === 1 ? states[0] : undefined);
    main.append(node("p", "section-note", "This view shows selected collaborations. Missing connections do not establish that the architecture is complete; recorded design limits remain part of each responsibility."));
    main.append(diagram("overview", "System responsibilities", "Select a Module to explore its children. Named Interfaces explain the collaboration contracts. Arrows run from consumer to provider; the list below identifies the exact owners.", model.overview_collaborations));
    const limits = node("div");
    roots.forEach(id => {
      if (!list(data(id).design_limits).length) return;
      const group = node("section");
      const heading = node("h3"); heading.append(link(title(id), entityRoute(id)));
      group.append(heading, valueView(data(id).design_limits));
      if (records[id]?.path) group.append(sourceLink(records[id].path, "Canonical Module definition ↗"));
      limits.append(group);
    });
    if (limits.childElementCount) main.append(detail("Recorded architecture limits by responsibility", limits));
    main.append(section("Choose a responsibility", moduleCards(roots)));
    const authored = authoredTopicsContent("logical"); if (authored) main.append(authored);
    if (views.logical) main.append(viewScope("logical"));
  }
  function renderModule(id, logical = false) {
    if (!modules[id]) return notFound("Module", id);
    const record = data(id), info = modules[id];
    const ancestors = [...list(info.ancestors)].reverse().map(parent => ({text:title(parent),href:entityRoute(parent)}));
    breadcrumb([...ancestors, {text:record.title}]);
    header(logical ? `Logical view · ${id}` : `Module · ${id}`, record.title, logical ? moduleViewQuestions.logical : record.description, record.status);
    if (!logical) main.append(section("Responsibilities", valueView(record.responsibilities)));
    const testing = testPerspectiveLink(id); if (testing) main.append(testing);
    if (list(cooperation.walkthroughs).some(slice => list(slice.modules).concat(list(slice.context_modules)).includes(id))) main.append(cliReadingLinks());
    const hosted = catalogs.filter(catalog => catalog.host === id || catalog.owner === id);
    if (hosted.length) {
      const row = node("div", "link-row");
      hosted.forEach(catalog => row.append(link(`Explore ${catalogKind(catalog)} →`, `#${catalogKind(catalog)}`)));
      main.append(row);
    }
    if (logical) {
      const overview = diagram(`module-${id}`, list(info.children).length ? "Responsibilities and collaboration" : "Collaboration context", "This diagram focuses on the selected Module, its immediate children, and relevant neighbors. Arrows run from consumer to provider. Dashed Modules provide surrounding context. Scroll or use Fit to see the complete diagram.", info.collaborations);
      main.append(authoredTopicsContent("logical", id, true, overview) || overview);
    }
    if (list(info.children).length) main.append(section("Child responsibilities", moduleCards(info.children)));
    const contracts = node("div", "contract-grid");
    [["Provides", info.provides], ["Consumes", info.consumes]].forEach(([label, ids]) => {
      const group = node("div"); group.append(node("h2", "", label));
      if (!list(ids).length) group.append(node("p", "muted small", "No direct Interface declared."));
      list(ids).forEach(interfaceId => {
        const contract = link("", entityRoute(interfaceId), "contract-card");
        contract.append(node("strong", "", title(interfaceId)));
        const meta = interfaces[interfaceId] || {};
        const context = label === "Provides" ? `Consumed by ${list(meta.consumers).map(title).join(", ") || "no declared consumer"}` : `Provided by ${title(meta.provider)}`;
        contract.append(node("small", "", context)); group.append(contract);
      });
      contracts.append(group);
    });
    main.append(section("Direct Interfaces", contracts));
    if (list(info.children).length) main.append(node("p", "section-note", "Child-owned contracts and allocations remain on the child pages."));
    if (list(info.exposed_interfaces).length) main.append(section("Child contracts exposed at this boundary", entityList(info.exposed_interfaces)));
    const details = node("div", "details-stack");
    details.append(detail("State authority and scope", recordFields(record, ["owned_state", "scope"])));
    const allocations = node("div");
    allocations.append(node("h3", "", "Direct Function allocations"), entityList(info.functions), node("h3", "", "Direct Allocated Requirements"), entityList(info.allocated_requirements));
    const descendantFunctions = list(info.subtree_functions).filter(item => !list(info.functions).includes(item));
    const descendantRequirements = list(info.subtree_allocated_requirements).filter(item => !list(info.allocated_requirements).includes(item));
    if (descendantFunctions.length || descendantRequirements.length) {
      allocations.append(node("p", "notice", "The following descendant allocations are rolled up for navigation. Their accountable owners remain the child Modules."));
      allocations.append(node("h3", "", "Descendant Functions"), entityList(descendantFunctions), node("h3", "", "Descendant Allocated Requirements"), entityList(descendantRequirements));
    }
    details.append(detail("Functions and requirement allocations", allocations, !logical));
    if (record.design_limits?.length) details.append(detail("Design limits", valueView(record.design_limits)));
    details.append(sourceDetails(id)); main.append(details);
  }
  function renderInterface(id) {
    if (!interfaces[id]) return notFound("Interface", id);
    const record = data(id), info = interfaces[id];
    breadcrumb([{text:"Interfaces",href:"#search/IF-"},{text:record.title}]);
    header(`Interface · ${id}`, record.title, record.description, record.status);
    if (list(cooperation.interfaces).includes(id)) main.append(cliReadingLinks());
    const ownership = node("div", "split");
    const provider = node("section", "panel"); provider.append(node("h2", "", "Provider"), entityList(info.provider ? [info.provider] : []));
    const consumers = node("section", "panel"); consumers.append(node("h2", "", "Consumers"), entityList(info.consumers));
    ownership.append(provider, consumers); main.append(ownership);
    if (list(info.exposed_through).length) main.append(section("Exposed through", entityList(info.exposed_through)));
    const hosted = catalogs.filter(catalog => catalog.owner === id);
    hosted.forEach(catalog => { const row = node("div", "link-row"); row.append(link(`Explore public ${catalogKind(catalog)} →`, `#${catalogKind(catalog)}`)); main.append(row); });
    const related = relatedViews([id]); if (related) main.append(related);
    const operations = node("div");
    list(record.operations).forEach(operation => {
      const block = node("article", "operation");
      block.append(node("h3", "", operation.name), node("p", "", operation.purpose));
      block.append(detail("Inputs and outputs", recordFields(operation, ["inputs", "preconditions", "outputs"])));
      block.append(detail("Behavior and failure outcomes", recordFields(operation, ["behavior", "failure_behavior"])));
      operations.append(block);
    });
    main.append(section("Operations", operations));
    main.append(detail("Consistency and compatibility", recordFields(record, ["consistency_rules", "compatibility_rules"])));
    main.append(sourceDetails(id));
  }
  function catalogItems(kind) {
    return catalogs.filter(catalog => catalogKind(catalog) === kind).flatMap(catalog => list(catalog.entries).map(entry => ({catalog,entry})));
  }
  function renderWebCapability(id) {
    const capability = webCapabilities.find(item => item.id === id);
    if (!capability) return notFound("Public capability", id);
    breadcrumb([{text:"Public capabilities"},{text:capability.title}]);
    header("Public capability · Web", capability.title, capability.content.purpose);
    const paragraphs = text => {
      const body = node("div");
      text.split(/\n\s*\n/).forEach(part => body.append(node("p", "", part)));
      return body;
    };
    const access = paragraphs(capability.content.access), actions = node("div", "link-row");
    actions.append(link("Open architecture →", "#home"), link("Find a definition →", "#search/"),
      link("Explore the responsible Module →", entityRoute(capability.owner)),
      link("Technical design →", `#logical/${encodeURIComponent(capability.owner)}`),
      link("Development design →", `#development/${encodeURIComponent(capability.owner)}`));
    access.append(actions); main.append(section("Open and use", access));
    const interactions = node("div", "card-grid");
    capability.interactions.forEach(item => {
      const card = node("article", "panel");
      card.append(node("h3", "", item.title), node("p", "", item.description)); interactions.append(card);
    });
    main.append(section("Available interactions", interactions),
      section("Current limits and proposed work", paragraphs(capability.content.limits)),
      section("Related engineering basis", entityList([capability.feature, ...capability.related, capability.owner])));
    const allocations = node("div");
    allocations.append(node("p", "section-note", "These allocations describe the broader Feature, including proposed work. Each Function retains its accountable Module; links do not establish delivered support."));
    list(data(capability.feature).realized_by).forEach(id => {
      const row = node("p"); row.append(entityLink(id));
      const owner = data(id).allocated_to;
      if (owner) row.append(document.createTextNode(" → "), entityLink(owner));
      else row.append(document.createTextNode(" · No accountable Module recorded"));
      allocations.append(row);
    });
    main.append(detail("Functions and accountable Modules", allocations));
    const sources = node("div");
    sources.append(node("p", "", "Descriptions are included in this snapshot. These optional repository links may be unavailable in a copied file."),
      sourceLink(capability.source, "Owning description ↗"), node("code", "source-digest", capability.source_digest),
      sourceLink(capability.binding, "Presentation binding ↗"), node("code", "source-digest", capability.binding_digest),
      recordFields(capability, ["selectors"]));
    main.append(detail("Sources and snapshot identity", sources));
  }
  function renderCatalog(kind) {
    const items = catalogItems(kind);
    breadcrumb([{text:nice(kind)}]);
    header("Public capabilities", nice(kind), kind === "commands" ? "Executable entry points, their purposes, and the architectural responsibilities they reach." : "Engineering procedures, the behavior they guide, and the responsibilities that remain with specialist owners.");
    if (kind === "commands") main.append(cliReadingLinks());
    main.append(node("p", "section-note", "Public names are observed in the repository. Their architectural mappings are proposed; each entry retains its detailed contract and mapping limits."));
    const controls = node("div", "catalog-controls");
    const field = node("div", "filter-field");
    const label = node("label", "", `Find ${kind}`); label.htmlFor = "catalog-filter";
    const filter = node("input"); filter.type="search"; filter.id="catalog-filter"; filter.placeholder="Search name, purpose, or responsibility";
    field.append(label, filter);
    const groupField = node("div", "filter-field");
    const groupLabel = node("label", "", "Purpose group"); groupLabel.htmlFor="catalog-group";
    const select = node("select"); select.id="catalog-group";
    const all = node("option", "", "All groups"); all.value=""; select.append(all);
    [...new Set(items.map(({entry}) => entry.group))].forEach(group => { const option = node("option", "", group); option.value=group; select.append(option); });
    groupField.append(groupLabel, select); controls.append(field, groupField); main.append(controls);
    const count = node("p", "results-count"); count.setAttribute("role", "status");
    const results = node("div"); main.append(count, results);
    function refresh() {
      const query = filter.value.trim().toLocaleLowerCase();
      const matches = items.filter(({entry}) => (!select.value || entry.group === select.value) && `${entry.name} ${entry.purpose} ${list(entry.modules).map(id => `${id} ${title(id)}`).join(" ")}`.toLocaleLowerCase().includes(query));
      count.textContent = `${matches.length} of ${items.length} ${kind}`;
      results.replaceChildren();
      if (!matches.length) { results.append(empty("No matching entries", "Try another name or clear the group filter.")); return; }
      [...new Set(matches.map(({entry}) => entry.group))].forEach(group => {
        const sectionNode = node("section", "catalog-group"); sectionNode.append(node("h2", "", group));
        matches.filter(({entry}) => entry.group === group).forEach(({catalog,entry}) => {
          const row = link("", entryRoute(catalog,entry), "catalog-entry");
          row.append(node("strong", "", entry.name), node("p", "", entry.purpose), node("span", "entry-owner", list(entry.modules).map(title).join(" · ") || "Mapping not established"));
          sectionNode.append(row);
        });
        results.append(sectionNode);
      });
    }
    filter.addEventListener("input",refresh); select.addEventListener("change",refresh); refresh();
  }
  function renderEntry(owner, name) {
    const catalog = catalogs.find(item => item.owner === owner && list(item.entries).some(entry => entry.name === name));
    const entry = catalog?.entries.find(item => item.name === name);
    if (!entry) return notFound("Public entry", name);
    const kind = catalogKind(catalog), mapping = entry.mapping || {};
    breadcrumb([{text:nice(kind),href:`#${kind}`},{text:entry.name}]);
    header(entry.group, entry.name, entry.purpose);
    const entryLinks = node("div", "link-row");
    if (entry.contract) entryLinks.append(sourceLink(entry.contract,"Read detailed contract ↗"));
    if (entry.source_path) entryLinks.append(sourceLink(entry.source_path,"Open implementation or procedure ↗"));
    main.append(entryLinks);
    const related = relatedViews([catalog.owner, catalog.host, ...list(entry.modules)].filter(Boolean)); if (related) main.append(related);
    const boundary = node("section", "panel"); boundary.append(node("h2", "", isCommand(catalog) ? "Public contract" : "Published guidance responsibility"), entityList([catalog.owner]));
    if (entry.operation) boundary.append(node("p", "small muted", `Operation: ${entry.operation}`));
    main.append(boundary);
    const mappings = node("div", "panel");
    if (!list(mapping.functions).length) mappings.append(node("p", "muted", "No Function correspondence is established."));
    list(mapping.functions).forEach(contribution => {
      const row = node("article", "mapping-item");
      row.append(node("span", "mapping-relation", contribution.relation), entityLink(contribution.function), node("p", "", contribution.contribution));
      const allocated = data(contribution.function).allocated_to;
      if (allocated) { const ownerRow = node("div", "pill-list"); ownerRow.append(node("span", "small muted", "Accountable Module"), entityLink(allocated)); row.append(ownerRow); }
      mappings.append(row);
    });
    main.append(section("Proposed architectural correspondence", mappings));
    if (list(mapping.limits).length) main.append(detail("Mapping limits", valueView(mapping.limits), true));
    if (list(entry.features).length) main.append(detail("Related Features", entityList(entry.features)));
    const sources = node("div");
    sources.append(sourceLink(catalog.path,"Open canonical public-entry mappings ↗"));
    if (entry.entry_pointer) sources.append(node("p", "small muted", `Entry: ${entry.entry_pointer}`));
    if (entry.mapping_pointer) sources.append(node("p", "small muted", `Mapping: ${entry.mapping_pointer}`));
    main.append(detail("Mapping source", sources));
  }
  function renderEntity(id) {
    if (!records[id]) return notFound("Entity", id);
    const record = data(id);
    breadcrumb([{text:id}]);
    header(`${nice(record.type || "Entity")} · ${id}`, record.title, record.description || record.statement, record.status);
    if (contributions.some(item => item.requirement === id || list(item.allocated_requirements).includes(id))) {
      const row = node("div", "link-row"); row.append(link("Read related CLI contribution arguments →", `#contributions/${id}`)); main.append(row);
    }
    if (list(cooperation.walkthroughs).some(slice => slice.scenario === id)) {
      const row = node("div", "link-row"); row.append(link("Read the CLI architecture walkthrough →", `#cooperation/${id}`)); main.append(row);
    }
    if (record.allocated_to) main.append(section("Accountable Module",entityList([record.allocated_to])));
    if (list(record.realized_by).length) main.append(section("Realized by",entityList(record.realized_by)));
    const hidden = new Set(["id","type","title","status","description","statement","sources","allocated_to","realized_by"]);
    const fields = Object.keys(record).filter(key=>!hidden.has(key));
    if (fields.length) main.append(detail("Definition and behavior",recordFields(record,fields),true));
    const relationships = list(model.relationships).filter(relation=>relation.source === id || relation.target === id);
    if (relationships.length) {
      const items = node("ul","record-list");
      relationships.forEach(relation=>{const row=node("li");row.append(entityLink(relation.source),node("span","small muted",` ${relation.relation} `),entityLink(relation.target));items.append(row);});
      main.append(detail("Engineering relationships",items));
    }
    main.append(sourceDetails(id));
  }
  function empty(heading, message) {
    const result = node("div", "empty-state"); result.append(node("h2", "", heading), node("p", "", message)); return result;
  }
  function notFound(kind, id) {
    breadcrumb([{text:"Page unavailable"}]); header("Architecture explorer", `${kind} not found`, `“${id}” is not in this generated model.`);
    main.append(link("Return to the architecture overview →", "#overview"));
  }
  function renderSearch(query) {
    const normalized = query.trim().toLocaleLowerCase();
    breadcrumb([{text:"Search"}]); header("Find architecture context", "Search", normalized ? `Results for “${query}”` : "Search by a public name, an entity identifier, or a responsibility.");
    document.getElementById("global-search").value=query;
    if (!normalized) { main.append(empty("Enter a name or identifier", "Use the search field to find a Module, Interface, command, skill, or other engineering entity.")); return; }
    const matches = Object.entries(records).filter(([id,record])=>`${id} ${record.data.title}`.toLocaleLowerCase().includes(normalized)).map(([id,record])=>({name:record.data.title,kind:`${nice(record.data.type || "Entity")} · ${id}`,purpose:record.data.description || record.data.statement || "",href:entityRoute(id)}));
    catalogs.forEach(catalog=>list(catalog.entries).forEach(entry=>{
      if (`${entry.name} ${entry.purpose}`.toLocaleLowerCase().includes(normalized)) matches.push({name:entry.name,kind:isCommand(catalog)?"Command":"Skill",purpose:entry.purpose,href:entryRoute(catalog,entry)});
    }));
    main.append(node("p","results-count",`${matches.length} ${matches.length === 1 ? "result" : "results"}`));
    if (!matches.length) { main.append(empty("No matches", "Try a shorter name or an identifier such as MOD-016.")); return; }
    const rows=node("ul","search-results");
    matches.forEach(match=>{const row=node("li"),a=link("",match.href);a.append(node("small","",match.kind),node("strong","",match.name),node("p","",match.purpose));row.append(a);rows.append(row);});
    main.append(rows);
  }
  function renderNavigation(activeRoute) {
    const nav=document.getElementById("navigation");nav.replaceChildren();
    const route=activeRoute.slice(1).split("/");
    const context=architectureContext(route);
    const selectedOwner=context?.owner;
    const view=context?.view || "summary";
    nav.append(node("p","nav-label","Architecture"));
    const root=link("RigorLoop",scopeRoute(null,view),"nav-link system-nav");
    if(context && !selectedOwner)root.setAttribute("aria-current","location");
    nav.append(root);
    function tree(id) {
      const children=list(modules[id].children);
      const a=link(`${title(id)} (${id})`,scopeRoute(id,view),"nav-link module-nav");
      a.dataset.scope=id;
      if(id===selectedOwner)a.setAttribute("aria-current","location");
      if(!children.length)return a;
      const branch=node("details","module-tree"),summary=node("summary");summary.append(a);branch.append(summary);
      branch.open=id===selectedOwner || list(modules[selectedOwner]?.ancestors).includes(id);
      const nested=node("div","module-tree-children");children.forEach(child=>nested.append(tree(child)));branch.append(nested);return branch;
    }
    const scopes=node("div","system-tree-children");
    roots.forEach(id=>scopes.append(tree(id)));nav.append(scopes);
    const kinds=[...new Set(catalogs.map(catalogKind))];
    const activeCatalog=route[0]==="entry" ? catalogs.find(c=>c.owner===route[1]) : null;
    if(kinds.length || webCapabilities.length){
      nav.append(node("p","nav-label","Public capabilities"));
      kinds.forEach(kind=>{
        const a=link(nice(kind),`#${kind}`,"nav-link");
        if(route[0]===kind || (activeCatalog && catalogKind(activeCatalog)===kind))a.setAttribute("aria-current",route[0]===kind ? "page" : "location");
        nav.append(a);
      });
      webCapabilities.forEach(capability => {
        const a = link(capability.title, capability.route, "nav-link");
        if (activeRoute === capability.route) a.setAttribute("aria-current", "page");
        nav.append(a);
      });
    }
  }
  const identityTooltip = node("div", "identity-tooltip");
  identityTooltip.id = "entity-identity-tooltip";
  identityTooltip.setAttribute("role", "tooltip");
  identityTooltip.hidden = true;
  document.body.append(identityTooltip);
  let hoveredEntity = null, focusedEntity = null, describedEntity = null;
  function hideIdentity() {
    if (describedEntity) describedEntity.removeAttribute("aria-describedby");
    describedEntity = null;
    identityTooltip.hidden = true;
  }
  function showIdentity(anchor) {
    hideIdentity();
    if (!anchor?.isConnected) return;
    const id = anchor.dataset.entityId;
    identityTooltip.textContent = anchor.dataset.entityLabel || `${anchor.dataset.viewLabel || ""}${title(id)} (${id})`;
    identityTooltip.hidden = false;
    const bounds = anchor.getBoundingClientRect();
    const tip = identityTooltip.getBoundingClientRect();
    const left = Math.max(8, Math.min(bounds.left, innerWidth - tip.width - 8));
    const below = bounds.bottom + 8;
    const top = Math.max(8, Math.min(innerHeight - tip.height - 8,
      below + tip.height < innerHeight - 8 ? below : bounds.top - tip.height - 8));
    identityTooltip.style.left = `${left}px`;
    identityTooltip.style.top = `${top}px`;
    anchor.setAttribute("aria-describedby", identityTooltip.id);
    describedEntity = anchor;
  }
  function graphNodeDescription(anchor) {
    if (anchor.namespaceURI !== "http://www.w3.org/2000/svg" || anchor.closest(".diagram-panel")?.dataset.diagramView === "logical") return "";
    // D2 owns the label on the anchor's immediate shape group. Descendant
    // shapes and nested links have separate labels and must not name a container.
    const group = Array.from(anchor.children).find(child => child.localName === "g") || anchor;
    const normalize = value => value.replace(/\s+/g, " ").trim();
    const ownText = Array.from(group.children).filter(child => child.localName === "text").map(text => {
      const spans = Array.from(text.querySelectorAll("tspan"));
      return normalize(spans.length ? spans.map(span => span.textContent).join(" ") : text.textContent);
    }).filter(Boolean).join("; ");
    const ownTitle = Array.from(group.children).find(child => child.localName === "title");
    return [...new Set([ownText, ownTitle ? normalize(ownTitle.textContent) : ""].filter(Boolean))].join("; ");
  }
  function annotateEntityLinks() {
    document.querySelectorAll("#main a, #navigation a").forEach(anchor => {
      const href = anchor.getAttribute("href") || anchor.getAttribute("xlink:href") || "";
      if (anchor.dataset.identityAnnotated) return;
      const route = /^#(module|interface|entity|scenario|process|development|physical|cooperation|contributions)\/([^/]+)$/.exec(href);
      const outcomeMatch = /^#scenario\/([^/]+)\/outcome\/([^/]+)$/.exec(href);
      const outcome = outcomeMatch && list(scenarioSlice(outcomeMatch[1])?.outcomes).find(item => item.key === outcomeMatch[2]);
      const topic = processTopics().concat(physicalTopics(), Object.values(model.view_diagrams || {}).filter(item => item.perspective === "testing")).find(item => item.route === href);
      const id = route?.[2];
      if (!records[id] && !topic && !outcome) return;
      anchor.dataset.identityAnnotated = "true";
      if (records[id]) anchor.dataset.entityId = id;
      const viewLabel = outcome ? "Scenario outcome: " : topic ? `${nice(topic.view)} view: ` : route[1] === "cooperation" ? "CLI walkthrough: " : route[1] === "contributions" ? "CLI contributions: " : ["process", "development", "physical"].includes(route[1]) ? `${nice(route[1])} view: ` : "";
      if (viewLabel) anchor.dataset.viewLabel = viewLabel;
      const destination = outcome ? `${viewLabel}${outcome.title} (${outcomeMatch[1]})` : topic ? `${viewLabel}${topic.title}` : `${viewLabel}${title(id)} (${id})`;
      const localMeaning = graphNodeDescription(anchor) || (topic?.perspective === "testing" && anchor.namespaceURI !== "http://www.w3.org/2000/svg"
        ? (anchor.querySelector("h3")?.textContent || anchor.textContent).replace(/\s+/g, " ").trim() : "");
      const label = localMeaning ? `${localMeaning}. Opens ${destination}` : destination;
      anchor.dataset.entityLabel = label;
      anchor.setAttribute("aria-label", label);
      anchor.addEventListener("pointerenter", () => { hoveredEntity = anchor; showIdentity(anchor); });
      anchor.addEventListener("pointerleave", () => {
        hoveredEntity = null;
        if (describedEntity === anchor) showIdentity(focusedEntity);
      });
      anchor.addEventListener("focus", () => { focusedEntity = anchor; showIdentity(anchor); });
      anchor.addEventListener("blur", () => {
        focusedEntity = null;
        if (describedEntity === anchor) showIdentity(hoveredEntity);
      });
    });
  }
  document.addEventListener("keydown", event => { if (event.key === "Escape") hideIdentity(); });
  const repositionIdentity = () => { if (!identityTooltip.hidden) showIdentity(describedEntity); };
  window.addEventListener("resize", repositionIdentity);
  document.addEventListener("scroll", repositionIdentity, true);
  function render() {
    if(location.hash==="#main") {
      if(main.querySelector("h1")) { main.focus();return; }
    }
    const raw=(location.hash === "#main" ? "#home" : location.hash || "#home").slice(1);
    let route;
    try { route=raw.split("/").map(decodeURIComponent); }
    catch (_) { route=["invalid",raw]; }
    hoveredEntity = null;focusedEntity = null;hideIdentity();
    initializeDiagrams = [];
    main.replaceChildren();renderNavigation(`#${raw}`);
    const [kind,id,name]=route;
    if(kind==="home" && route.length===1)renderHome();
    else if(viewKinds.includes(kind) && modules[id] && route.length===5)renderAuthoredTopic(kind,id,route[2],route[3],route[4]);
    else if(kind==="process" && modules[id] && ["interaction","lifecycle"].includes(name) && route.length===4)renderProcessTopic(name,route[3],id);
    else if(kind==="logical" && route.length===2)renderModule(id,true);
    else if(kind==="scenarios" && route.length===2)renderModuleScenarios(id);
    else if(["overview","logical"].includes(kind) && route.length===1)renderOverview();
    else if(kind==="cooperation" && route.length<=2)renderCooperation(id);
    else if(kind==="contributions" && route.length<=2)renderContributions(id);
    else if(kind==="process" && ["interaction","lifecycle"].includes(id) && route.length===3)renderProcessTopic(id,name);
    else if(kind==="physical" && ["consumer","storage","production"].includes(id) && route.length===2)renderPhysicalTopic(id);
    else if(kind==="development" && id === "testing" && route.length===2)renderTestArchitecture();
    else if(kind==="development" && id?.startsWith("testing-") && route.length===2)renderTestArchitecture(id.slice("testing-".length));
    else if(["process","development","physical"].includes(kind) && route.length<=2)renderFacetView(kind,id);
    else if(kind==="scenarios" && route.length===1)renderScenarios();
    else if(kind==="scenario" && name==="outcome" && route.length===4)renderScenarioOutcome(id,route[3]);
    else if(kind==="scenario" && route.length===2)renderScenario(id);
    else if(kind==="module" && route.length===2)renderModule(id);
    else if(kind==="interface" && route.length===2)renderInterface(id);
    else if(kind==="entity" && route.length===2)renderEntity(id);
    else if(kind==="capability" && route.length===2)renderWebCapability(id);
    else if(["commands","skills"].includes(kind) && route.length===1)renderCatalog(kind);
    else if(kind==="entry" && route.length===3)renderEntry(id,name);
    else if(kind==="search" && route.length<=2)renderSearch(id || "");
    else notFound("Page",raw);
    const context=architectureContext(route);
    if(context) {
      const scope=node("p","architecture-scope",context.owner ? `${context.owner} · ${title(context.owner)}` : "RigorLoop · System");
      const tabs=architectureViewNavigation(context);
      const heading=main.querySelector(".page-header");
      if(heading)heading.after(scope,tabs);
    }
    initializeDiagrams.forEach(initialize => initialize());
    annotateEntityLinks();
    document.getElementById("navigation").classList.remove("mobile-open");
    document.getElementById("navigation-toggle").setAttribute("aria-expanded","false");
    window.scrollTo(0,0);main.focus({preventScroll:true});
  }
  document.getElementById("search-form").addEventListener("submit",event=>{
    event.preventDefault();const query=document.getElementById("global-search").value.trim();const hash=`#search/${encodeURIComponent(query)}`;
    if(location.hash===hash)render();else location.hash=hash;
  });
  const navigationToggle=document.getElementById("navigation-toggle");
  navigationToggle.onclick=()=>{const open=document.getElementById("navigation").classList.toggle("mobile-open");navigationToggle.setAttribute("aria-expanded",String(open));};
  document.addEventListener("keydown",event=>{if(event.key==="Escape" && document.getElementById("navigation").classList.contains("mobile-open")){document.getElementById("navigation").classList.remove("mobile-open");navigationToggle.setAttribute("aria-expanded","false");navigationToggle.focus();}});
  window.addEventListener("hashchange",render);render();
})();
