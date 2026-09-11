import {readFileSync} from "node:fs";
import {createRecordFormat} from "./record-format-core.js";
export const RECORDS_V2_SCHEMA=JSON.parse(readFileSync(new URL("../schemas/rigorloop-records-v2.schema.json",import.meta.url),"utf8"));
const format=createRecordFormat(RECORDS_V2_SCHEMA,{version:2,contract:"rigorloop-records-v2"});
export const {parseRecord:parseV2Record,validateRecord:validateV2Record,validateSet:validateV2Set,preserve:validateV2Preservation,creation:validateV2Creation,pathKind:v2PathKind,validateRequest:validateV2Request,parseRequestJSON}=format;
