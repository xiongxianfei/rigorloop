import assert from "node:assert/strict";
import { greeting } from "../src/app.js";

assert.equal(greeting("customer"), "hello customer");
