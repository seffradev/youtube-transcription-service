#!/usr/bin/env bash
container=$1
partitions=$2
docker exec $container kafka-topics.sh --create --topic email --bootstrap-server localhost:9092 --partitions $partitions --replication-factor 1
