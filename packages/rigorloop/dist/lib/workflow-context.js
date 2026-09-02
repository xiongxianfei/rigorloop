import { existsSync, lstatSync, readFileSync } from "node:fs";
import { isAbsolute, join, relative, resolve, sep } from "node:path";

import {
  FINAL_VERIFICATION_ACTIVATION_MANIFEST_PATH,
  LIFECYCLE_ACTIVATION_MANIFEST_PATH,
  LIFECYCLE_CONTRACT_V3,
  PREACTIVATION_FINAL_VERIFICATION_MANIFEST,
  PREACTIVATION_LIFECYCLE_MANIFEST,
  classifyLifecycleContract,
  correctionStageOrder,
  parseLifecycleYaml,
} from "./lifecycle-contract.js";
import { discoverGovernedChanges, findRepositoryRoot, interpretGovernedChange, selectGovernedChange } from "./lifecycle-read.js";

export const WORKFLOW_CONTEXT_FORMATS = Object.freeze(["human", "json"]);
export const WORKFLOW_CONFIG_SCHEMA_VERSIONS = Object.freeze([1]);

const CONFIG_PATH = "rigorloop.workflow.yaml";
const SAFE_IDENTIFIER = /^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/;
const SAFE_CHANGE_ID = /^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/;
const TEMPLATE_VARIABLES = new Set(["change-id", "date", "slug", "review-round", "stage", "milestone-id"]);
const ENTRY_FIELDS = new Set(["path_template", "owner"]);
const MAX_PROJECTED_ITEMS = 32;

export const BUNDLED_WORKFLOW_DEFAULTS = Object.freeze({
  schema_version: 1,
  artifact_locations: Object.freeze({
    "change-record": Object.freeze({ path_template: "docs/changes/<change-id>/change.yaml", owner: "workflow" }),
    proposal: Object.freeze({ path_template: "docs/proposals/<change-id>.md", owner: "proposal" }),
    spec: Object.freeze({ path_template: "specs/<slug>.md", owner: "spec" }),
    architecture: Object.freeze({ path_template: "docs/architecture/<change-id>.md", owner: "architecture" }),
    adr: Object.freeze({ path_template: "docs/adr", owner: "architecture" }),
    plan: Object.freeze({ path_template: "docs/plans/<change-id>.md", owner: "plan" }),
    "proposal-review-record": Object.freeze({ path_template: "docs/changes/<change-id>/reviews/proposal-review-<review-round>.md", owner: "proposal-review" }),
    "design-review-record": Object.freeze({ path_template: "docs/changes/<change-id>/reviews/design-review-<review-round>.md", owner: "design-review" }),
    "delivery-review-record": Object.freeze({ path_template: "docs/changes/<change-id>/reviews/delivery-review-<review-round>.md", owner: "delivery-review" }),
    "code-review-record": Object.freeze({ path_template: "docs/changes/<change-id>/reviews/code-review-<review-round>.md", owner: "code-review" }),
    "review-resolution": Object.freeze({ path_template: "docs/changes/<change-id>/review-resolution.md", owner: "review-resolution" }),
    "implementation-evidence": Object.freeze({ path_template: "docs/changes/<change-id>/evidence", owner: "implement" }),
    "verification-report": Object.freeze({ path_template: "docs/changes/<change-id>/verify-report.md", owner: "verify" }),
  }),
});

const SUPPORTED_KINDS = new Set(Object.keys(BUNDLED_WORKFLOW_DEFAULTS.artifact_locations));
const EXPECTED_OWNERS = Object.fromEntries(Object.entries(BUNDLED_WORKFLOW_DEFAULTS.artifact_locations).map(([kind, value]) => [kind, value.owner]));

function diagnostic(code, invariant, source = null, artifactKind = null, identities = []) {
  return {
    code,
    blocking_invariant: invariant,
    ...(source ? { source } : {}),
    ...(artifactKind ? { artifact_kind: artifactKind } : {}),
    relevant_identities: identities.map(String).filter((value) => SAFE_IDENTIFIER.test(value)).slice(0, MAX_PROJECTED_ITEMS),
  };
}

function repositoryRoot(start) {
  const root = findRepositoryRoot(start);
  if (!existsSync(join(root, ".git")) && !existsSync(join(root, "docs", "changes"))) return null;
  return root;
}

function readProjectLifecycleContract(root) {
  try {
    const lifecyclePath = join(root, ...LIFECYCLE_ACTIVATION_MANIFEST_PATH.split("/"));
    const finalPath = join(root, ...FINAL_VERIFICATION_ACTIVATION_MANIFEST_PATH.split("/"));
    const lifecycleManifest = existsSync(lifecyclePath) ? parseLifecycleYaml(readFileSync(lifecyclePath, "utf8")) : PREACTIVATION_LIFECYCLE_MANIFEST;
    const finalManifest = existsSync(finalPath) ? parseLifecycleYaml(readFileSync(finalPath, "utf8")) : PREACTIVATION_FINAL_VERIFICATION_MANIFEST;
    return { lifecycle_contract: classifyLifecycleContract("workflow-context", { lifecycle_contract: LIFECYCLE_CONTRACT_V3 }, lifecycleManifest, finalManifest) };
  } catch {
    return { error: diagnostic("RL_CONTEXT_LIFECYCLE_INVALID", "workflow-context-lifecycle-contract") };
  }
}

function safeRepositoryPath(root, candidate) {
  if (typeof candidate !== "string" || !candidate || candidate.includes("\\") || isAbsolute(candidate) || /^[A-Za-z]:/.test(candidate)) return false;
  const parts = candidate.split("/");
  if (parts.some((part) => !part || part === "." || part === "..")) return false;
  const absolute = resolve(root, candidate);
  const rel = relative(root, absolute);
  if (rel === ".." || rel.startsWith(`..${sep}`) || rel.startsWith(sep)) return false;
  let cursor = root;
  for (const part of parts) {
    cursor = join(cursor, part);
    if (existsSync(cursor) && lstatSync(cursor).isSymbolicLink()) return false;
  }
  return true;
}

function validateTemplate(root, artifactKind, template) {
  if (!safeRepositoryPath(root, template)) return diagnostic("RL_CONTEXT_PATH_UNSAFE", "workflow-context-path", CONFIG_PATH, artifactKind, [artifactKind]);
  const variables = [...template.matchAll(/<([^>]+)>/g)].map((match) => match[1]);
  if (variables.some((value) => !TEMPLATE_VARIABLES.has(value)) || template.replace(/<[^>]+>/g, "").includes("<") || template.replace(/<[^>]+>/g, "").includes(">")) {
    return diagnostic("RL_CONTEXT_CONFIG_INVALID", "workflow-context-template-variable", CONFIG_PATH, artifactKind, [artifactKind]);
  }
  return null;
}

function invalidConfiguration(code, invariant, artifactKind = null) {
  return { error: diagnostic(code, invariant, CONFIG_PATH, artifactKind, artifactKind ? [artifactKind] : []) };
}

function loadConfiguration(root) {
  const configAbsolute = join(root, CONFIG_PATH);
  const effective = Object.fromEntries(Object.entries(BUNDLED_WORKFLOW_DEFAULTS.artifact_locations).map(([kind, value]) => [kind, { ...value, provenance: "bundled-default" }]));
  if (!existsSync(configAbsolute)) return { configuration: { schema_version: 1, source: "bundled-default", path: null }, effective };
  if (!lstatSync(configAbsolute).isFile() || lstatSync(configAbsolute).isSymbolicLink()) return invalidConfiguration("RL_CONTEXT_PATH_UNSAFE", "workflow-context-config-source");
  let parsed;
  try { parsed = parseLifecycleYaml(readFileSync(configAbsolute, "utf8")); }
  catch { return invalidConfiguration("RL_CONTEXT_CONFIG_INVALID", "workflow-context-config-syntax"); }
  if (!WORKFLOW_CONFIG_SCHEMA_VERSIONS.includes(parsed.schema_version)) return invalidConfiguration("RL_CONTEXT_CONFIG_UNSUPPORTED", "workflow-context-config-version");
  if (Object.keys(parsed).some((key) => !["schema_version", "artifact_locations"].includes(key)) || !parsed.artifact_locations || Array.isArray(parsed.artifact_locations) || typeof parsed.artifact_locations !== "object") {
    return invalidConfiguration("RL_CONTEXT_CONFIG_INVALID", "workflow-context-config-fields");
  }
  for (const [kind, entry] of Object.entries(parsed.artifact_locations)) {
    if (!SUPPORTED_KINDS.has(kind)) return invalidConfiguration("RL_CONTEXT_CONFIG_INVALID", "workflow-context-artifact-kind", kind);
    if (!entry || Array.isArray(entry) || typeof entry !== "object" || Object.keys(entry).some((key) => !ENTRY_FIELDS.has(key)) || typeof entry.path_template !== "string") {
      return invalidConfiguration("RL_CONTEXT_CONFIG_INVALID", "workflow-context-location-shape", kind);
    }
    if (entry.owner !== undefined && entry.owner !== EXPECTED_OWNERS[kind]) return invalidConfiguration("RL_CONTEXT_CONFIG_INVALID", "workflow-context-owner", kind);
    const templateError = validateTemplate(root, kind, entry.path_template);
    if (templateError) return { error: templateError };
    effective[kind] = { path_template: entry.path_template, owner: EXPECTED_OWNERS[kind], provenance: "repository-override" };
  }
  return { configuration: { schema_version: 1, source: CONFIG_PATH, path: CONFIG_PATH }, effective };
}

function variablesForChange(changeId) {
  const dated = /^(\d{4}-\d{2}-\d{2})-(.+)$/.exec(changeId);
  return {
    "change-id": changeId,
    date: dated?.[1],
    slug: dated?.[2] ?? changeId,
  };
}

function resolveLocations(root, effective, changeId = null) {
  const variables = changeId ? variablesForChange(changeId) : {};
  const locations = [];
  const paths = new Map();
  for (const [artifactKind, entry] of Object.entries(effective).sort(([left], [right]) => left.localeCompare(right))) {
    let path = entry.path_template;
    if (changeId) {
      path = path.replace(/<([^>]+)>/g, (match, name) => variables[name] ?? match);
      if (/<[^>]+>/.test(path)) {
        if (/<review-round>/.test(path) && artifactKind.endsWith("-review-record")) {
          locations.push({ artifact_kind: artifactKind, owner: entry.owner, path_template: entry.path_template, path: null, requires: ["review-round"], provenance: entry.provenance });
          continue;
        }
        return { error: diagnostic("RL_CONTEXT_LOCATION_UNRESOLVED", "workflow-context-template-resolution", entry.provenance === "repository-override" ? CONFIG_PATH : "bundled-default", artifactKind, [artifactKind]) };
      }
      if (!safeRepositoryPath(root, path)) return { error: diagnostic("RL_CONTEXT_PATH_UNSAFE", "workflow-context-path", entry.provenance === "repository-override" ? CONFIG_PATH : "bundled-default", artifactKind, [artifactKind]) };
      const prior = paths.get(path);
      if (prior) return { error: diagnostic("RL_CONTEXT_LOCATION_CONFLICT", "workflow-context-location-ownership", entry.provenance === "repository-override" ? CONFIG_PATH : "bundled-default", artifactKind, [prior, artifactKind]) };
      paths.set(path, artifactKind);
    }
    locations.push({ artifact_kind: artifactKind, owner: entry.owner, path_template: entry.path_template, ...(changeId ? { path } : {}), provenance: entry.provenance });
  }
  return { locations };
}

function boundedDiagnostic(item) {
  return {
    code: item.code,
    blocking_invariant: item.blocking_invariant,
    relevant_identities: (item.relevant_identities ?? []).map(String).filter((value) => SAFE_IDENTIFIER.test(value)).slice(0, MAX_PROJECTED_ITEMS),
    corrective_operation: SAFE_IDENTIFIER.test(String(item.corrective_operation ?? "")) ? item.corrective_operation : null,
  };
}

function boundedDiagnostics(items) {
  const projected = items.map(boundedDiagnostic);
  return {
    items: projected.slice(0, MAX_PROJECTED_ITEMS),
    total_count: projected.length,
    truncated: projected.length > MAX_PROJECTED_ITEMS,
  };
}

function boundedAutomation(automation) {
  if (!automation || typeof automation !== "object" || Array.isArray(automation)) return null;
  const result = {};
  for (const field of ["status", "target", "occurrence", "current_stage", "authorization_id", "pause_reason", "stop_reason"]) {
    if (typeof automation[field] === "string" && SAFE_IDENTIFIER.test(automation[field])) result[field] = automation[field];
  }
  if (automation.budgets && typeof automation.budgets === "object" && !Array.isArray(automation.budgets)) {
    const budgets = Object.entries(automation.budgets).filter(([key, value]) => SAFE_IDENTIFIER.test(key) && Number.isSafeInteger(value) && value >= 0).sort(([left], [right]) => left.localeCompare(right));
    result.budgets = Object.fromEntries(budgets.slice(0, MAX_PROJECTED_ITEMS));
    result.budget_total_count = budgets.length;
    result.budgets_truncated = budgets.length > MAX_PROJECTED_ITEMS;
  }
  if (Array.isArray(automation.receipts)) {
    const receipts = automation.receipts.filter((value) => typeof value === "string" && SAFE_IDENTIFIER.test(value));
    result.receipts = receipts.slice(0, MAX_PROJECTED_ITEMS);
    result.receipt_total_count = receipts.length;
    result.receipts_truncated = receipts.length > MAX_PROJECTED_ITEMS;
  }
  return Object.keys(result).length ? result : null;
}

function projectPackages(root, reviewPackages) {
  return Object.fromEntries(Object.entries(reviewPackages).filter(([kind]) => SAFE_IDENTIFIER.test(kind)).sort(([left], [right]) => left.localeCompare(right)).slice(0, MAX_PROJECTED_ITEMS).map(([kind, value]) => {
    const members = Object.entries(value.members ?? {}).filter(([id]) => SAFE_IDENTIFIER.test(id)).sort(([left], [right]) => left.localeCompare(right));
    return [kind, {
    members: Object.fromEntries(members.slice(0, MAX_PROJECTED_ITEMS).map(([id, path]) => [id, safeRepositoryPath(root, path) ? path : null])),
    member_total_count: members.length,
    members_truncated: members.length > MAX_PROJECTED_ITEMS,
    upstream_review_id: SAFE_IDENTIFIER.test(String(value.upstream_review_id ?? "")) ? value.upstream_review_id : null,
    status: SAFE_IDENTIFIER.test(String(value.status ?? "")) ? value.status : null,
    authority: SAFE_IDENTIFIER.test(String(value.authority ?? "")) ? value.authority : null,
    blockers: boundedDiagnostics(value.blockers ?? []).items,
    errors: boundedDiagnostics(value.errors ?? []).items,
    next_permitted_operation: SAFE_IDENTIFIER.test(String(value.next_permitted_operation ?? "")) ? value.next_permitted_operation : null,
  }]; }));
}

function projectMilestones(change) {
  const planned = change.workflow_state?.planned_work;
  if (!planned) return { current_milestone: null, remaining_implementation_milestones: [], milestones: {} };
  const milestones = Object.entries(planned.milestones ?? {}).filter(([id]) => SAFE_IDENTIFIER.test(id)).sort(([left], [right]) => left.localeCompare(right));
  const remaining = (planned.remaining_implementation_milestones ?? []).filter((id) => typeof id === "string" && SAFE_IDENTIFIER.test(id));
  return {
    current_milestone: SAFE_IDENTIFIER.test(String(planned.current_milestone ?? "")) ? planned.current_milestone : null,
    remaining_implementation_milestones: remaining.slice(0, MAX_PROJECTED_ITEMS),
    remaining_total_count: remaining.length,
    remaining_truncated: remaining.length > MAX_PROJECTED_ITEMS,
    milestones: Object.fromEntries(milestones.slice(0, MAX_PROJECTED_ITEMS).map(([id, value]) => [id, { kind: SAFE_IDENTIFIER.test(String(value.kind ?? "")) ? value.kind : null, state: SAFE_IDENTIFIER.test(String(value.state ?? "")) ? value.state : null }])),
    total_count: milestones.length,
    truncated: milestones.length > MAX_PROJECTED_ITEMS,
  };
}

function baseResult(phase, overrides = {}) {
  return {
    schema_version: 1,
    command: "workflow-context",
    phase,
    status: "success",
    configuration: null,
    lifecycle_contract: null,
    selection: { state: "none", selected_change: null },
    candidates: [],
    blockers: [],
    warnings: [],
    errors: [],
    ...overrides,
  };
}

function errorResult(phase, error, configuration = null, exitCode = 2) {
  const result = baseResult(phase, { status: exitCode === 2 ? "blocked" : "error", configuration, blockers: [error], errors: [error] });
  return { result, exitCode };
}

function parseArgs(args) {
  let change = null;
  let format = "human";
  let changeSeen = false;
  let formatSeen = false;
  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];
    if (arg === "--change" && !changeSeen && args[index + 1] && !args[index + 1].startsWith("--")) { changeSeen = true; change = args[++index]; }
    else if (arg === "--format" && !formatSeen && args[index + 1]) { formatSeen = true; format = args[++index]; }
    else if (arg === "--json" && !formatSeen) { formatSeen = true; format = "json"; }
    else return { error: diagnostic("RL_CONTEXT_INVALID_REQUEST", "workflow-context-command-input"), format };
  }
  if (!WORKFLOW_CONTEXT_FORMATS.includes(format) || (change !== null && !SAFE_CHANGE_ID.test(change))) return { error: diagnostic("RL_CONTEXT_INVALID_REQUEST", "workflow-context-command-input"), format: "human" };
  return { change, format };
}

export function workflowContextHuman(result) {
  const lines = [`Workflow context: ${result.status}`, `Phase: ${result.phase}`];
  if (result.configuration) lines.push(`Configuration: ${result.configuration.source}`);
  if (result.lifecycle_contract) lines.push(`Lifecycle contract: ${result.lifecycle_contract.contract_class}; ${result.lifecycle_contract.activation_state}`);
  lines.push(`Selection: ${result.selection.state}`);
  if (result.change_id) lines.push(`Change: ${result.change_id}`);
  if (result.lifecycle_revision) lines.push(`Lifecycle revision: ${result.lifecycle_revision}`);
  if (result.current_stage) lines.push(`Current stage: ${result.current_stage}`);
  if (result.candidates.length) lines.push(`Candidates: ${result.candidates.map((item) => `${item.change_id} (${item.current_stage})`).join(", ")}`);
  for (const location of result.locations ?? []) lines.push(`Location ${location.artifact_kind}: ${location.path ?? location.path_template} [${location.provenance}]`);
  for (const blocker of result.blockers) lines.push(`Blocker: ${blocker.code} (${blocker.blocking_invariant})`);
  if (result.permitted_operations?.length) lines.push(`Permitted operations: ${result.permitted_operations.join(", ")}`);
  return `${lines.join("\n")}\n`;
}

function executeWorkflowContextUnsafe(args, options = {}) {
  const parsed = parseArgs(args);
  if (parsed.error) {
    const execution = errorResult("project", parsed.error, null, 4);
    return { ...execution, format: parsed.format, human: workflowContextHuman(execution.result) };
  }
  const root = repositoryRoot(options.cwd ?? process.cwd());
  if (!root) {
    const execution = errorResult(parsed.change ? "change" : "project", diagnostic("RL_CONTEXT_REPOSITORY_NOT_FOUND", "workflow-context-repository"));
    return { ...execution, format: parsed.format, human: workflowContextHuman(execution.result) };
  }
  const loaded = loadConfiguration(root);
  if (loaded.error) {
    const execution = errorResult(parsed.change ? "change" : "project", loaded.error, { schema_version: null, source: CONFIG_PATH, path: CONFIG_PATH });
    return { ...execution, format: parsed.format, human: workflowContextHuman(execution.result) };
  }
  const projectContract = readProjectLifecycleContract(root);
  if (projectContract.error) {
    const execution = errorResult(parsed.change ? "change" : "project", projectContract.error, loaded.configuration);
    return { ...execution, format: parsed.format, human: workflowContextHuman(execution.result) };
  }
  const resolved = resolveLocations(root, loaded.effective, parsed.change);
  if (resolved.error) {
    const execution = errorResult(parsed.change ? "change" : "project", resolved.error, loaded.configuration);
    return { ...execution, format: parsed.format, human: workflowContextHuman(execution.result) };
  }
  if (!parsed.change) {
    const discovered = discoverGovernedChanges(root);
    const malformed = discovered.find((candidate) => candidate.error || !SAFE_CHANGE_ID.test(candidate.id));
    if (malformed) {
      const execution = errorResult("project", diagnostic("RL_CONTEXT_CHANGE_INVALID", "workflow-context-change-input", null, null, [malformed.id]), loaded.configuration);
      return { ...execution, format: parsed.format, human: workflowContextHuman(execution.result) };
    }
    const active = discovered.filter((candidate) => candidate.change?.workflow_state?.lifecycle_state === "active");
    const interpreted = active.map((candidate) => interpretGovernedChange(root, candidate));
    const allCandidates = interpreted.map((item) => ({ change_id: item.change_id, current_stage: SAFE_IDENTIFIER.test(String(item.effective_state.current_stage ?? "")) ? item.effective_state.current_stage : null, lifecycle_state: SAFE_IDENTIFIER.test(String(item.change.workflow_state.lifecycle_state ?? "")) ? item.change.workflow_state.lifecycle_state : null, effective_state: SAFE_IDENTIFIER.test(String(item.effective_state.effective_state ?? "")) ? item.effective_state.effective_state : null, blocker_codes: [...new Set([...item.blockers, ...item.errors].map((entry) => entry.code).filter((value) => SAFE_IDENTIFIER.test(String(value))))].slice(0, MAX_PROJECTED_ITEMS) })).sort((left, right) => left.change_id.localeCompare(right.change_id));
    const candidates = allCandidates.slice(0, MAX_PROJECTED_ITEMS);
    const lifecycleContract = projectContract.lifecycle_contract;
    const selection = { state: allCandidates.length === 0 ? "none" : allCandidates.length === 1 ? "single-candidate" : "ambiguous", selected_change: null };
    const projectBlockers = [];
    if (allCandidates.length > 1) projectBlockers.push(diagnostic("RL_CONTEXT_SELECTION_AMBIGUOUS", "workflow-context-selection", null, null, allCandidates.map((item) => item.change_id)));
    if (interpreted.some((item) => item.errors.length)) projectBlockers.push(diagnostic("RL_CONTEXT_CHANGE_INVALID", "workflow-context-change-input", null, null, interpreted.filter((item) => item.errors.length).map((item) => item.change_id)));
    const result = baseResult("project", { status: projectBlockers.length ? "blocked" : "success", configuration: loaded.configuration, lifecycle_contract: lifecycleContract, selection, candidates, candidate_total_count: allCandidates.length, candidates_truncated: allCandidates.length > MAX_PROJECTED_ITEMS, locations: resolved.locations, blockers: projectBlockers, errors: projectBlockers });
    const exitCode = projectBlockers.length ? 2 : 0;
    return { result, exitCode, format: parsed.format, human: workflowContextHuman(result) };
  }
  const selected = selectGovernedChange(root, parsed.change);
  if (selected.error) {
    const execution = errorResult("change", diagnostic(selected.error.code === "RL_CHANGE_NOT_FOUND" ? "RL_CONTEXT_CHANGE_NOT_FOUND" : "RL_CONTEXT_CHANGE_INVALID", "workflow-context-change-selection", null, null, [parsed.change]), loaded.configuration);
    return { ...execution, format: parsed.format, human: workflowContextHuman(execution.result) };
  }
  const interpreted = interpretGovernedChange(root, selected);
  const currentStage = interpreted.effective_state.current_stage;
  const projectionErrors = correctionStageOrder(interpreted.change).includes(currentStage) ? [] : [diagnostic("RL_CONTEXT_PROJECTION_INVALID", "workflow-context-closed-identifier")];
  const errorProjection = boundedDiagnostics([...interpreted.errors, ...projectionErrors]);
  const blockerProjection = boundedDiagnostics(interpreted.blockers);
  const warningProjection = boundedDiagnostics(interpreted.warnings);
  const errors = errorProjection.items;
  const blockers = blockerProjection.items;
  const result = baseResult("change", {
    status: errors.length ? "error" : "success",
    configuration: loaded.configuration,
    lifecycle_contract: interpreted.effective_state.lifecycle_contract,
    selection: { state: "exact", selected_change: interpreted.change_id },
    candidates: [],
    change_id: interpreted.change_id,
    lifecycle_revision: interpreted.lifecycle_revision,
    current_stage: projectionErrors.length ? null : currentStage,
    artifacts: interpreted.artifacts.filter((item) => SAFE_IDENTIFIER.test(String(item.artifact_id))).slice(0, MAX_PROJECTED_ITEMS).map((item) => ({ artifact_id: item.artifact_id, path: safeRepositoryPath(root, item.path) ? item.path : null, sha256: /^([0-9a-f]{64}|sha256:[0-9a-f]{64})$/.test(String(item.sha256 ?? "")) ? item.sha256 : null, recorded_state: SAFE_IDENTIFIER.test(String(item.recorded_state ?? "")) ? item.recorded_state : null, evidence_state: SAFE_IDENTIFIER.test(String(item.evidence_state ?? "")) ? item.evidence_state : null })),
    artifact_total_count: interpreted.artifacts.length,
    artifacts_truncated: interpreted.artifacts.length > MAX_PROJECTED_ITEMS,
    locations: resolved.locations,
    packages: projectPackages(root, interpreted.review_packages),
    milestones: projectMilestones(interpreted.change),
    blockers,
    blocker_total_count: blockerProjection.total_count,
    blockers_truncated: blockerProjection.truncated,
    permitted_operations: interpreted.permitted_operations.filter((value) => SAFE_IDENTIFIER.test(String(value))).slice(0, MAX_PROJECTED_ITEMS),
    automation: boundedAutomation(interpreted.change.workflow?.automation),
    warnings: warningProjection.items,
    warning_total_count: warningProjection.total_count,
    warnings_truncated: warningProjection.truncated,
    errors,
    error_total_count: errorProjection.total_count,
    errors_truncated: errorProjection.truncated,
  });
  const exitCode = errors.length ? 3 : 0;
  return { result, exitCode, format: parsed.format, human: workflowContextHuman(result) };
}

export function executeWorkflowContext(args, options = {}) {
  try {
    return executeWorkflowContextUnsafe(args, options);
  } catch {
    const parsed = parseArgs(args);
    const execution = errorResult(parsed.change ? "change" : "project", diagnostic("RL_CONTEXT_READ_FAILED", "workflow-context-filesystem"));
    return { ...execution, format: parsed.format, human: workflowContextHuman(execution.result) };
  }
}
