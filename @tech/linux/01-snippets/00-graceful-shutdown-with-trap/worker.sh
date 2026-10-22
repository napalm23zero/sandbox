#!/usr/bin/env bash
# A long-running worker that cleans up after itself on SIGTERM or SIGINT.
set -euo pipefail

workdir=$(mktemp -d)
sleeper=

shutdown() {
  local signal=$1 code=$2
  echo "received $signal, removing $workdir"
  [ -n "$sleeper" ] && kill "$sleeper" 2>/dev/null
  rm -rf "$workdir"
  exit "$code"
}
# 128 + signal number is the convention supervisors read: 143 for TERM, 130 for INT.
trap 'shutdown TERM 143' TERM
trap 'shutdown INT 130' INT

echo "ready $workdir"
while true; do
  # bash only runs a trap between commands. A foreground `sleep 30` would delay the
  # shutdown by up to 30 s; `wait` is interrupted by the signal immediately.
  sleep 30 &
  sleeper=$!
  wait "$sleeper"
done
