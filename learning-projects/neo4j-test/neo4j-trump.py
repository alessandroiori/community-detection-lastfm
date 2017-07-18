# pip install neo4j-driver

from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver(
    "bolt://107.22.143.35:33328",
    auth=basic_auth("neo4j", "railways-keys-movement"))
session = driver.session()

# What are all the Organizations in Trumpworld?
cypher_query = '''
MATCH (o:Organization)
RETURN o.name AS name LIMIT $limit
'''

results = session.run(cypher_query, parameters={"limit": 10})

for record in results:
  print(record['name'])
