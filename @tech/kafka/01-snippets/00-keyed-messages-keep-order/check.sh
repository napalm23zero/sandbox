#!/usr/bin/env bash
# Reads "p<partition> <key>:<event>" lines from demo.sh and fails unless every key
# landed in exactly one partition with its events in the order they were produced.
set -euo pipefail

input=$(cat)
echo "$input"

[ "$(grep -c . <<<"$input")" -eq 9 ] || { echo "expected 9 messages"; exit 1; }
for key in order-1 order-2 order-3; do
  lines=$(grep " $key:" <<<"$input")
  partitions=$(cut -d' ' -f1 <<<"$lines" | sort -u | wc -l)
  events=$(cut -d: -f2 <<<"$lines" | paste -sd, -)
  (( partitions == 1 )) || { echo "$key spread over $partitions partitions"; exit 1; }
  [ "$events" = "created,paid,shipped" ] || { echo "$key out of order: $events"; exit 1; }
done
echo ok
