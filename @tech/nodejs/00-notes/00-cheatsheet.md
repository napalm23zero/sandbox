# Node.js cheatsheet

Targets Node.js 22 and newer.

## Event loop order

1. Synchronous code.
2. `process.nextTick` queue, then the promise microtask queue. Both drain completely
   between every macrotask.
3. Loop phases: **timers** (`setTimeout`, `setInterval`), **poll** (I/O callbacks),
   **check** (`setImmediate`), **close** callbacks.

From inside an I/O callback, `setImmediate` always runs before `setTimeout(0)`.
See [`01-snippets/00-event-loop-phases`](../01-snippets/00-event-loop-phases/).

## Modules

```js
// ES modules: "type": "module" in package.json, or the .mjs extension
import { readFile } from "node:fs/promises";
export function parse() {}
const config = await import("./config.mjs");        // dynamic import, top-level await is fine

// CommonJS: .cjs, or no "type" field
const { readFile } = require("node:fs/promises");
module.exports = { parse };
```

Prefer the `node:` prefix for built-ins: it cannot be shadowed by an npm package.

## Async

```js
const [user, orders] = await Promise.all([getUser(id), getOrders(id)]);   // fail fast
const results = await Promise.allSettled(tasks);                          // never rejects
const first = await Promise.any(mirrors.map(fetch));                      // first success

const controller = new AbortController();
setTimeout(() => controller.abort(), 5000);
await fetch(url, { signal: controller.signal });                          // cancellable

await fetch(url, { signal: AbortSignal.timeout(5000) });                  // same, shorter
```

## Streams

```js
import { pipeline } from "node:stream/promises";
import { createReadStream, createWriteStream } from "node:fs";
import { createGzip } from "node:zlib";

await pipeline(createReadStream("in.log"), createGzip(), createWriteStream("in.log.gz"));
```

`pipeline` handles backpressure and destroys every stream when one fails. Chaining
`.pipe()` does neither.

## Built-ins that replace dependencies

```js
fetch(url)                                          // HTTP client
import { test } from "node:test";                   // test runner: node --test
import assert from "node:assert/strict";
import { parseArgs } from "node:util";              // CLI flags
crypto.randomUUID();
structuredClone(obj);                               // deep copy
```

```sh
node --watch app.js                 # restart on change
node --env-file=.env app.js         # load environment variables
node --inspect app.js               # debugger, open chrome://inspect
node --cpu-prof app.js              # CPU profile to a .cpuprofile file
```

## CPU-bound work

The event loop is one thread. Heavy computation blocks every request; move it to
`node:worker_threads`.
