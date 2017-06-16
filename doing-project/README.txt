
• Neo4j on Docker

docker run \
--publish=7474:7474 --publish=7687:7687 \
--volume=$HOME/neo4j/data:/data \
--volume=$HOME/neo4j/logs:/logs \
neo4j:3.0

• Web interface: http://localhost:7474
