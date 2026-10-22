# Graceful shutdown with trap

How do I make a shell script clean up after itself when it is stopped?

## Run

```sh
make run    # then Ctrl-C
make test
```

Needs bash 3.2 or newer, so it runs on macOS and any Linux.

## What to notice

- `trap '...' TERM` runs a handler instead of dying on the spot. `docker stop`,
  `kubectl delete pod` and `systemctl stop` all send SIGTERM first, and only send the
  unblockable SIGKILL after a grace period.
- bash runs traps **between** commands. With a plain `sleep 30` in the loop the
  handler waits up to 30 seconds. Sleeping in the background and calling `wait` lets
  the signal interrupt immediately; the test fails if shutdown takes 5 seconds or more.
- The exit code is `128 + signal number` (143 for TERM, 130 for INT). Exiting 0 would
  tell the supervisor the job finished, when it was actually stopped.
- The handler also kills the background `sleep`, or it would outlive its parent.
