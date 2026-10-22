# Event loop phases

In what order do `nextTick`, promises, `setImmediate` and `setTimeout(0)` run?

## Run

```sh
make run
make test
```

Needs Node.js 20 or newer.

## What to notice

- Synchronous code finishes first, always. Then the microtask queues drain:
  `process.nextTick` before promise callbacks.
- After that it depends on **where you are in the loop**. The callbacks are scheduled
  from a `readFile` callback, which runs in the poll phase. The next phase is check,
  so `setImmediate` wins and `setTimeout(0)` waits for the timers phase of the next
  iteration.
- Schedule the same two from the main module instead and the winner depends on how
  long the process took to boot. The second test runs the experiment 50 times to show
  the I/O version does not flake.
