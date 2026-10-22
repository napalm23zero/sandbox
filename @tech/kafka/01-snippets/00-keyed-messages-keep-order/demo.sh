#!/usr/bin/env bash
# Produces keyed events to a 3-partition topic and prints, per partition, what landed there.
set -euo pipefail

kafka() { docker compose exec -T kafka "/opt/kafka/bin/$1" "${@:2}"; }
BOOTSTRAP=localhost:9092
TOPIC=orders

kafka kafka-topics.sh --bootstrap-server $BOOTSTRAP --create --if-not-exists \
  --topic $TOPIC --partitions 3 --replication-factor 1 >/dev/null

printf '%s\n' \
  order-1:created order-2:created order-1:paid order-3:created \
  order-2:paid order-1:shipped order-3:paid order-2:shipped order-3:shipped |
  kafka kafka-console-producer.sh --bootstrap-server $BOOTSTRAP --topic $TOPIC \
    --property parse.key=true --property key.separator=:

for partition in 0 1 2; do
  kafka kafka-console-consumer.sh --bootstrap-server $BOOTSTRAP --topic $TOPIC \
    --partition $partition --offset earliest --timeout-ms 5000 \
    --property print.key=true --property key.separator=: 2>/dev/null |
    sed "s/^/p$partition /"
done
