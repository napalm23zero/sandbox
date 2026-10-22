#!/usr/bin/env bash
set -euo pipefail

out=$(bash objects.sh)
expect() { grep -qF "$1" <<<"$out" || { echo "FAIL: missing '$1'"; echo "$out"; exit 1; }; }

expect "blob id: ce013625030ba8dba906f756967f9e9ca394464a"
expect "tree id: aaa96ced2d9a1c8e72c56b253a0e2fe78393feb7"
expect "renamed: 57e9529754dc514a3ec10db2ff882018fbe1fcbf"
expect "count: 4"
echo ok
