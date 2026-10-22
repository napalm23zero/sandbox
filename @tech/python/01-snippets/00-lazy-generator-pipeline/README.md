# Lazy generator pipeline

How do I chain processing stages without building an intermediate list at each step?

## Run

```sh
make run
make test
```

Needs Python 3.9 or newer. Standard library only.

## What to notice

- Each stage takes an iterable and yields values. Chaining them builds the pipeline,
  and nothing executes until `islice` starts pulling.
- Values flow one at a time through every stage. Asking for two squares reads three
  lines and stops: the log in `make run` shows the rest of the source never being
  touched.
- Because of that, the source can be infinite (`itertools.count`) and memory stays
  constant whatever its size.
- The price: a generator is single use. Once consumed it yields nothing, and it raises
  no error to tell you.
