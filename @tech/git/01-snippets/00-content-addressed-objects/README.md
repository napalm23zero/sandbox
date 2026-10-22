# Content-addressed objects

How does Git actually store files, and why are its ids the same on every machine?

## Run

```sh
make run
make test
```

Needs Git. Works in a temporary repository that is deleted on exit.

## What to notice

- A blob id is the SHA-1 of `blob <size>\0<content>`. `hello\n` is
  `ce013625...` here, on your laptop and on the CI runner. The test asserts the exact
  hashes, which only works because the id is a function of the content and nothing else.
- A blob holds bytes only: no name, no permissions. Those live in the tree that points
  at it. Renaming the file produces a new tree around the same blob.
- Identical content is stored once. Four file entries across three trees all point at
  the same blob, so `count-objects` says 4: one blob, three trees.
- The repository is created with `--object-format=sha1` on purpose. SHA-256
  repositories exist, and a Git version that defaults to them would produce different
  ids for the same content.
