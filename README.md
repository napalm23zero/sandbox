# sandbox

[![ci](https://github.com/napalm23zero/sandbox/actions/workflows/ci.yml/badge.svg)](https://github.com/napalm23zero/sandbox/actions/workflows/ci.yml)

My study lab, in public. Every subject has its own folder, every folder is shaped the
same way, and every runnable piece is tested in CI.

## How it's organized

```
@tech/                   one area per field of study, @ keeps areas apart from repo machinery
└── <subject>/
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
### @tech

| Domain | Subject | Status | Notes | Snippets | Labs | Challenges |
|---|---|---|---|---|---|---|
| languages | [Java](@tech/java/) | learning | 1 | 1 | 0 | 0 |
| languages | [Python](@tech/python/) | learning | 1 | 1 | 0 | 0 |
| backend | [Node.js](@tech/nodejs/) | learning | 1 | 1 | 0 | 0 |
| data | [Apache Kafka](@tech/kafka/) | learning | 1 | 1 | 0 | 0 |
| devops | [Docker](@tech/docker/) | learning | 1 | 1 | 0 | 0 |
| devops | [Git](@tech/git/) | learning | 1 | 1 | 0 | 0 |
| devops | [Linux](@tech/linux/) | learning | 1 | 1 | 0 | 0 |
<!-- index:end -->
