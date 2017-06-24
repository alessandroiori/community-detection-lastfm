#!/bin/bash

spark-submit --class com.bigdata.main.Main target/graph-core-0.0.1-SNAPSHOT-jar-with-dependencies.jar $1 $2
