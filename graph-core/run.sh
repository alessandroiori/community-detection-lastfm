#!/bin/bash

spark-submit  --packages datastax:spark-cassandra-connector:2.0.0-M2-s_2.11 --class com.bigdata.main.Main --jars target/spark-sql_2.10-1.0.0.jar target/graph-core-0.0.1-SNAPSHOT.jar  $1 $2 $3 $4
