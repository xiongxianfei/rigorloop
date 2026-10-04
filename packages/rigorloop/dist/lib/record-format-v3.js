import {readFileSync} from "node:fs";
import {createRecordFormat} from "./record-format-core.js";
export const RECORDS_V3_SCHEMA=JSON.parse(readFileSync(new URL("../schemas/rigorloop-records-v3.schema.json",import.meta.url),"utf8"));
const format=createRecordFormat(RECORDS_V3_SCHEMA,{version:3,contract:"rigorloop-records-v3"});
export const {parseRecord:parseV3Record,validateRecord:validateV3Record,validateSet:validateV3Set,pathKind:v3PathKind}=format;
