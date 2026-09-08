// Local configuration parsing and root lookup; no lifecycle interpretation.
import {existsSync} from 'node:fs';
import {dirname,join,resolve} from 'node:path';
import {isAlias,isMap,isScalar,isSeq,parseAllDocuments} from 'yaml';
const STANDARD_TAGS = new Set([
  "tag:yaml.org,2002:map",
  "tag:yaml.org,2002:seq",
  "tag:yaml.org,2002:str",
  "tag:yaml.org,2002:null",
  "tag:yaml.org,2002:bool",
  "tag:yaml.org,2002:int",
  "tag:yaml.org,2002:float",
]);

function invalid(message) {
  const error = new Error(`RL_INVALID_REQUEST: ${message}`);
  error.code = "RL_INVALID_REQUEST";
  return error;
}

function inspectNode(node) {
  if (!node) return;
  if (isAlias(node)) throw invalid("YAML aliases are not supported");
  if (node.anchor) throw invalid("YAML anchors are not supported");
  if (node.tag && !STANDARD_TAGS.has(node.tag)) throw invalid("custom YAML tags are not supported");
  if (isMap(node)) {
    for (const pair of node.items) {
      if (!isScalar(pair.key) || typeof pair.key.value !== "string") {
        throw invalid("YAML mapping keys must be strings");
      }
      if (pair.key.value === "<<") throw invalid("YAML merge keys are not supported");
      inspectNode(pair.value);
    }
  } else if (isSeq(node)) {
    for (const item of node.items) inspectNode(item);
  } else if (isScalar(node)) {
    if (typeof node.value === "number" && !Number.isFinite(node.value)) {
      throw invalid("non-finite YAML numbers are not supported");
    }
  } else {
    throw invalid("unsupported YAML node kind");
  }
}

export function parseProjectYaml(text) {
  if (typeof text !== "string") throw invalid("YAML input must be UTF-8 text");
  let documents;
  try {
    documents = parseAllDocuments(text, { uniqueKeys: true, merge: false, maxAliasCount: 0 });
  } catch (error) {
    throw invalid(error.message);
  }
  if (documents.length !== 1) throw invalid("exactly one YAML document is required");
  const [document] = documents;
  if (document.errors.length > 0) throw invalid(document.errors[0].message);
  inspectNode(document.contents);
  const value = document.toJS({ maxAliasCount: 0, mapAsMap: false });
  if (!value || Array.isArray(value) || typeof value !== "object") {
    throw invalid("lifecycle YAML root must be a mapping");
  }
  return value;
}


export function findRepositoryRoot(start) {
  let cursor = resolve(start);
  while (true) {
    if (existsSync(join(cursor, ".git")) || existsSync(join(cursor, "docs", "changes"))) return cursor;
    const parent = dirname(cursor);
    if (parent === cursor) return resolve(start);
    cursor = parent;
  }
}

