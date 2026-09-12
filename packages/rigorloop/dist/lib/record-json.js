import { parseDocument } from "yaml";

// Format-neutral strict JSON decoding; transport versions remain independent.
export const MIB = 1024 * 1024;
export const fail = (message) => {
  const code = /limit/.test(message) ? "limit-exceeded" : /unsafe-path|cross-change|unsupported record path/.test(message) ? "unsafe-path"
    : message === "unsupported-contract" ? "unsupported-contract" : message === "broken-reference" ? "broken-reference" : "invalid-input";
  throw Object.assign(new Error(`record-store: ${message}`), {recordStoreCode:code});
};
export const plain = v => v !== null && typeof v === "object" && !Array.isArray(v) && [Object.prototype, null].includes(Object.getPrototypeOf(v));

export function unicode(text) {
  for (let i = 0; i < text.length; i++) {
    const c = text.charCodeAt(i);
    if (c >= 0xd800 && c <= 0xdbff) {
      const next = text.charCodeAt(++i);
      if (!(next >= 0xdc00 && next <= 0xdfff)) fail("invalid Unicode");
    } else if (c >= 0xdc00 && c <= 0xdfff) fail("invalid Unicode");
  }
}

export function jsonDomain(value, depth = 0, ancestors = new Set()) {
  if (value === null || typeof value === "boolean") return;
  if (typeof value === "string") return unicode(value);
  if (typeof value === "number") { if (!Number.isFinite(value)) fail("nonfinite number"); return; }
  if ((!plain(value) && !Array.isArray(value)) || ancestors.has(value)) fail("invalid JSON value");
  if (depth >= 32) fail("nesting limit exceeded");
  ancestors.add(value);
  for (const [key, child] of Object.entries(value)) { unicode(key); jsonDomain(child, depth + 1, ancestors); }
  ancestors.delete(value);
}

export function decode(input, limit) {
  if (!(typeof input === "string" || Buffer.isBuffer(input))) fail("expected UTF-8 text");
  if (Buffer.byteLength(input) > limit) fail("byte limit exceeded");
  let text;
  try { text = typeof input === "string" ? input : new TextDecoder("utf-8", {fatal:true, ignoreBOM:true}).decode(input); }
  catch { fail("invalid UTF-8"); }
  unicode(text);
  if (text.startsWith("\ufeff") || text.includes("\r") || !text.endsWith("\n")) fail("invalid record encoding");
  return text;
}

export function strictJSON(text) {
  // Bound nesting before either parser sees the payload, ignoring quoted delimiters.
  let depth=0, quoted=false, escaped=false;
  for (const c of text) {
    if (quoted) { if (escaped) escaped=false; else if (c === "\\") escaped=true; else if (c === '"') quoted=false; }
    else if (c === '"') quoted=true;
    else if (c === "{" || c === "[") { if (++depth > 32) fail("nesting limit exceeded"); }
    else if (c === "}" || c === "]") depth--;
  }
  let value;
  try {
    value = JSON.parse(text); // YAML extensions are never admitted.
    const document = parseDocument(text, {uniqueKeys:true, strict:true, prettyErrors:false});
    if (document.errors.length) fail("duplicate or invalid JSON keys");
  } catch { fail("invalid JSON or duplicate keys"); }
  jsonDomain(value);
  return value;
}

// Shared strict, bounded decoding before advanced request version dispatch.
export function parseRequestJSON(input) {
  return strictJSON(decode(input,8*MIB));
}

