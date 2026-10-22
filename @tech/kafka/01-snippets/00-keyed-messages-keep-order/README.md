# Keyed messages keep their order

How do I guarantee that the events of one entity are consumed in the order they were
produced, on a topic with several partitions?

## Run

```sh
make run
make test
```

Needs Docker. Starts a single Kafka 4.1 node in KRaft mode, and stops and removes it
when done.

## What to notice

- Kafka orders messages **per partition**, never across a topic. The producer picks the
  partition by hashing the key, so every event of `order-1` goes to the same partition
  and is read back in the order it was written.
- Events of different keys interleave freely. That is fine: nobody cares whether
  `order-2:paid` came before `order-3:created`.
- Here two keys hash to partition 0, one to partition 1, and partition 2 stays empty.
  Hashing spreads keys, not load: with few keys, partitions are not balanced.
- The guarantee holds while the partition count stays the same. Add partitions and the
  hash sends a key somewhere new, so its old and new events sit in different partitions.
