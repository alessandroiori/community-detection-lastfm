Prerequisite


> Python3
# pip3 install neo4j-driver
# pip3 install networkx


> Docker

•Install Docker
# Linux: https://docs.docker.com/engine/installation/linux/ubuntu/#install-using-the-repository
# OS X: https://docs.docker.com/docker-for-mac/install/#download-docker-for-mac

• Neo4j on Docker:
docker run \
--publish=7474:7474 --publish=7687:7687 \
--volume=$HOME/neo4j/data:/data \
--volume=$HOME/neo4j/logs:/logs \
neo4j:3.0

• Neo4j web interface: http://localhost:7474
