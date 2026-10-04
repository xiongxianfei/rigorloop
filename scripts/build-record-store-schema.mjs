// Bundle canonical recording schema and example templates. --check is read-only.
import { readFileSync, mkdirSync, writeFileSync } from "node:fs";
if (process.argv.slice(2).some(arg => arg !== "--check") || process.argv.slice(2).length > 1) throw new Error("Usage: node scripts/build-record-store-schema.mjs [--check]");
for (const relative of ["templates/shared/rigorloop-workflow.json", "schemas/rigorloop-records-v4.schema.json", "schemas/targeted-recording-v2.schema.json", "schemas/store-maintenance-v1.schema.json", "schemas/rigorloop-records-v3.schema.json"]) {
  const source = new URL(`../${relative}`, import.meta.url);
  const target = new URL(`../packages/rigorloop/dist/${relative}`, import.meta.url);
  const content = readFileSync(source);
  JSON.parse(content.toString("utf8"));
  if (process.argv.includes("--check")) {
    if (!content.equals(readFileSync(target))) throw new Error("record-store package data drift");
  } else {
    mkdirSync(new URL(".", target), {recursive:true});
    writeFileSync(target, content);
  }
}
