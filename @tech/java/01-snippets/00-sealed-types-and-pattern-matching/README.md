# Sealed types and pattern matching

How do I model a closed set of types and handle every case without a `default` branch?

## Run

```sh
make run
make test
```

Needs Java 21 or newer.

## What to notice

- `sealed interface Shape permits ...` closes the hierarchy. The `switch` in `area` has
  no `default`, and it does not need one: add a fourth shape and the compiler points at
  every switch that forgot it.
- `case Circle(double radius)` deconstructs the record in place. No cast, no getter.
- Guards (`when`) refine a case. Order matters: the guarded `Circle` sits above the
  general one, otherwise the compiler rejects it as dominated.
- Records give `equals`, `hashCode` and `toString` from the components, which is what
  makes them good values for this kind of modeling.
