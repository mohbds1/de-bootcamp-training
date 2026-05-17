#!/bin/bash

docker exec -it kafka1 kafka-topics \
--create \
--topic logistics-clean \
--bootstrap-server kafka1:19092 \
--partitions 3 \
--replication-factor 3

docker exec -it kafka1 kafka-topics \
--describe \
--topic logistics-clean \
--bootstrap-server kafka1:19092