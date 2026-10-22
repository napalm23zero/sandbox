#!/usr/bin/env bash
# Builds blobs and trees by hand with plumbing commands, in a throwaway repository.
set -euo pipefail

repo=$(mktemp -d)
trap 'rm -rf "$repo"' EXIT
# Pinned to SHA-1 so the hashes below match on any Git version, whatever its default.
git init --quiet --object-format=sha1 "$repo"
cd "$repo"

step() { printf '\n$ %s\n' "$*"; "$@"; }

blob=$(printf 'hello\n' | git hash-object -w --stdin)
step git cat-file -t "$blob"
step git cat-file -p "$blob"
echo "blob id: $blob   (same bytes, same id, on every machine)"

tree=$(printf '100644 blob %s\thello.txt\n' "$blob" | git mktree)
step git cat-file -p "$tree"
echo "tree id: $tree"

renamed=$(printf '100644 blob %s\tgreeting.txt\n' "$blob" | git mktree)
echo "renamed: $renamed   (new tree, same blob: names live in trees, not in blobs)"

twice=$(printf '100644 blob %s\ta.txt\n100644 blob %s\tb.txt\n' "$blob" "$blob" | git mktree)
step git cat-file -p "$twice"
step git count-objects -v
echo "4 objects: 1 blob and 3 trees. All four file entries point at the same blob."
