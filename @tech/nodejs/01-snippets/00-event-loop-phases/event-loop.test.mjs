import { test } from "node:test";
import assert from "node:assert/strict";
import { eventLoopOrder } from "./event-loop.mjs";

test("inside an I/O callback: sync, microtasks, check phase, then timers", async () => {
  assert.deepEqual(await eventLoopOrder(), ["sync", "nextTick", "promise", "setImmediate", "setTimeout"]);
});

test("the order holds on every run, not just once", async () => {
  const runs = await Promise.all(Array.from({ length: 50 }, eventLoopOrder));
  assert.ok(runs.every((order) => order.join() === runs[0].join()));
});
