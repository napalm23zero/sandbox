import { readFile } from "node:fs";
import { fileURLToPath } from "node:url";

// Schedules one callback of each kind from inside an I/O callback and records the order
// they run in. From the poll phase, setImmediate (check phase) always beats
// setTimeout(0) (timers phase, next loop iteration). From the main module that race is
// not deterministic, which is why the experiment starts inside readFile.
export function eventLoopOrder() {
  return new Promise((resolve) => {
    const order = [];
    readFile(fileURLToPath(import.meta.url), () => {
      setTimeout(() => {
        order.push("setTimeout");
        resolve(order);
      }, 0);
      setImmediate(() => order.push("setImmediate"));
      Promise.resolve().then(() => order.push("promise"));
      process.nextTick(() => order.push("nextTick"));
      order.push("sync");
    });
  });
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  console.log((await eventLoopOrder()).join(" -> "));
}
