# Java cheatsheet

Targets Java 21 and newer.

## Modern types

```java
record Point(int x, int y) {}                       // equals, hashCode, toString, accessors
record Range(int from, int to) {
    Range {                                         // compact constructor: validation only
        if (from > to) throw new IllegalArgumentException("from > to");
    }
}

sealed interface Shape permits Circle, Square {}    // closed hierarchy
enum Status { ACTIVE, SUSPENDED }
```

## Pattern matching

```java
if (obj instanceof String s && !s.isBlank()) { ... }

String label = switch (shape) {                     // exhaustive over a sealed type
    case Circle(double r) when r == 0 -> "point";
    case Circle c -> "circle";
    case Square s -> "square";
};
```

See [`01-snippets/00-sealed-types-and-pattern-matching`](../01-snippets/00-sealed-types-and-pattern-matching/).

## Collections

```java
List.of(1, 2, 3);  Set.of("a");  Map.of("k", 1);   // immutable, reject nulls
new ArrayList<>(list);                              // mutable copy
list.getFirst();  list.reversed();                  // SequencedCollection, Java 21
map.computeIfAbsent(key, k -> new ArrayList<>()).add(value);
map.merge(word, 1, Integer::sum);                   // counting
```

## Streams

```java
orders.stream()
      .filter(o -> o.total() > 100)
      .map(Order::customer)
      .distinct()
      .toList();                                    // unmodifiable, Java 16

Map<Status, List<User>> byStatus = users.stream().collect(Collectors.groupingBy(User::status));
Map<Status, Long> counts = users.stream().collect(Collectors.groupingBy(User::status, Collectors.counting()));
IntStream.rangeClosed(1, 10).sum();
```

## Optional

```java
repository.findById(id)
          .map(User::email)
          .orElseThrow(() -> new NotFoundException(id));
```

Return it, do not take it as a parameter or store it in a field.

## Concurrency

```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {   // Java 21
    var futures = urls.stream().map(u -> executor.submit(() -> fetch(u))).toList();
}                                                                    // close() waits for all

CompletableFuture.supplyAsync(this::load)
                 .thenApply(this::transform)
                 .exceptionally(error -> fallback);
```

Virtual threads are cheap enough to create one per task. Pool them and you lose the
point; cap concurrency with a `Semaphore` instead.

## Text and time

```java
String json = """
    {"name": "%s"}
    """.formatted(name);                            // text block
Instant.now();                                      // a point on the timeline, UTC
LocalDate.of(2026, 10, 22);                         // a calendar date, no time zone
Duration.ofSeconds(90).toMinutes();
```

## Tooling

```sh
java Main.java                      # run a source file without compiling first
jshell                              # REPL
jcmd <pid> Thread.print             # thread dump of a running JVM
jcmd <pid> GC.heap_info
jcmd <pid> JFR.start duration=60s filename=rec.jfr   # flight recorder, low overhead profiling
```
