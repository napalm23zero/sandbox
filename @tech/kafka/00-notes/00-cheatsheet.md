# Apache Kafka cheatsheet

## Model

- **Topic**: a named stream, split into **partitions**.
- **Partition**: an append-only log. Each message gets an increasing **offset**.
  Order is guaranteed inside a partition, never across partitions.
- **Key**: decides the partition (hash of the key, modulo partition count). Same key,
  same partition, so per-key order. See [`01-snippets/00-keyed-messages-keep-order`](../01-snippets/00-keyed-messages-keep-order/).
- **Consumer group**: consumers sharing the work. Each partition is read by exactly
  one consumer of the group, so parallelism is capped by the partition count.
- **Replication**: each partition has a leader and followers. The **ISR** (in-sync
  replicas) are the followers caught up with the leader.
- **KRaft**: the metadata quorum built into Kafka. ZooKeeper is gone since 4.0.

## Producer settings that matter

| Setting | Meaning |
|---|---|
| `acks=all` | Wait for every in-sync replica. The default since 3.0 |
| `enable.idempotence=true` | No duplicates from retries. The default since 3.0 |
| `linger.ms`, `batch.size` | Wait a little to send bigger batches: throughput over latency |
| `compression.type` | `lz4` or `zstd` cut network and disk at little CPU cost |

## Consumer settings that matter

| Setting | Meaning |
|---|---|
| `auto.offset.reset` | Where a new group starts: `earliest` or `latest` |
| `enable.auto.commit` | Off when you need to commit only after processing succeeds |
| `max.poll.interval.ms` | Process slower than this and the consumer is kicked from the group |
| `isolation.level=read_committed` | Skip messages from aborted transactions |

## Delivery semantics

- **At most once**: commit the offset before processing. A crash loses messages.
- **At least once**: process, then commit. A crash reprocesses messages, so make the
  processing idempotent. The usual choice.
- **Exactly once**: transactions, for read-process-write loops that stay inside Kafka.

## CLI

```sh
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic t --partitions 3 --replication-factor 1
kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic t
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic t --property parse.key=true --property key.separator=:
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic t --from-beginning --property print.key=true
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group g   # lag per partition
```
