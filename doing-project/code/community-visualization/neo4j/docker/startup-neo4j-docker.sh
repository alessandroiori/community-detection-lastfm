#!/bin/bash

docker run  --publish=7474:7474 --publish=7687:7687  \
--volume=$HOME/neo4j/data:/data    \
--volume=$HOME/neo4j/logs:/logs  \
--volume=$HOME/neo4j/files:/var/lib/neo4j/import/files \
neo4j:3.0