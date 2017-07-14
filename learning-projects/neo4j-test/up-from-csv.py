from neo4jdbinfo import user_auth, pw_auth, uri_neo4j_db

from neo4j.v1 import GraphDatabase, basic_auth
import csv
import os

delimiter = ' '
path_file = "file:///files/test-new.csv"


def run():
    # Neo4j session
    driver = GraphDatabase.driver(uri_neo4j_db, auth=(user_auth, pw_auth))
    session = driver.session()

    q = 'LOAD CSV FROM {file} AS line FIELDTERMINATOR ":" ' \
        'WITH SPLIT(line[1], " ") AS usersId, SPLIT(line[0], " ") AS count ' \
        'FOREACH ' \
        '( uId IN usersId | ' \
        'MERGE (u:Test {userId: uId}) ' \
        'SET u.test = coalesce(u.test,[]) + count' \
        ')' \
        'RETURN usersId, count'

    result = session.run(q, {"file": path_file})
    for r in result:
        # print("(%s, %s) [%s, %s]" % (r[0]["id"], r[1]["name"], r[2]["url"], r[3]["image_url"]))
        print(r)

# EXECUTE
run()
