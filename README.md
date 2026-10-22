# sandbox

[![ci](https://github.com/napalm23zero/sandbox/actions/workflows/ci.yml/badge.svg)](https://github.com/napalm23zero/sandbox/actions/workflows/ci.yml)

My study lab, in public. One folder per technology, every folder shaped the same way,
every runnable piece tested in CI.

## How it's organized

```
<tech>/
├── README.md        what it is, roadmap, resources
├── 00-notes/        concepts in my own words, 00-cheatsheet.md first
├── 01-snippets/     how to do X: minimal, focused, runnable
├── 02-labs/         what happens if Y: hypothesis, measurement, conclusion
└── 03-challenges/   someone else's problem: katas, LeetCode, CTFs, certification tasks
```

- Numbers are two digits, start at `00`, and only grow: they are the order I learned
  things in. A new entry takes the next free number.
- Every snippet, lab and challenge is a folder with a `README.md` and a `Makefile`
  exposing `make run` and `make test`. CI runs `make test` in all of them.
- A category folder appears with its first entry.

## Index

Status goes `backlog`, `learning`, `practicing`, `comfortable`.

<!-- index:start -->
| Domain | Tech | Status | Notes | Snippets | Labs | Challenges |
|---|---|---|---|---|---|---|
| languages | [Java](java/) | learning | 0 | 0 | 0 | 0 |
| languages | [Python](python/) | learning | 0 | 0 | 0 | 0 |
| backend | [Node.js](nodejs/) | learning | 0 | 0 | 0 | 0 |
| data | [Apache Kafka](kafka/) | learning | 0 | 0 | 0 | 0 |
| devops | [Docker](docker/) | learning | 0 | 0 | 0 | 0 |
| devops | [Git](git/) | learning | 0 | 0 | 0 | 0 |
| devops | [Linux](linux/) | learning | 0 | 0 | 0 | 0 |
<!-- index:end -->
