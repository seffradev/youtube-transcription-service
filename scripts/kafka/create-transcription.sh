#!/usr/bin/env bash
container=$1
partitions=$2
docker exec $container kafka-topics.sh --create --topic transcription --bootstrap-server localhost:9092 --partitions $partitions --replication-factor 1
docker exec $container kafka-configs.sh --bootstrap-server localhost:9092 --alter --topic transcription --add-config cleanup.policy=compact
