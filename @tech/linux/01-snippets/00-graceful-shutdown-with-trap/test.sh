#!/usr/bin/env bash
set -euo pipefail

fail() { echo "FAIL: $1"; cat "$out"; exit 1; }

out=$(mktemp)
bash worker.sh > "$out" &
pid=$!

for _ in $(seq 50); do
  grep -q '^ready' "$out" && break
  sleep 0.1
done
workdir=$(awk '/^ready/ {print $2}' "$out")
[ -d "$workdir" ] || fail "worker never became ready"

start=$SECONDS
kill -TERM "$pid"
status=0
wait "$pid" || status=$?

(( status == 143 )) || fail "exit code $status, expected 143"
(( SECONDS - start < 5 )) || fail "shutdown took $((SECONDS - start)) s"
[ ! -e "$workdir" ] || fail "$workdir was left behind"
grep -q '^received TERM' "$out" || fail "trap did not run"

cat "$out"
rm -f "$out"
echo ok
