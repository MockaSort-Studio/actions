import assert from "node:assert/strict";
import test from "node:test";
import { add } from "./index.mjs";

test("add adds", () => assert.equal(add(2, 3), 5));
