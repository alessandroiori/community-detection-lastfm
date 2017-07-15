from neo4jdbinfo import user_auth, pw_auth, uri_neo4j_db

from neo4j.v1 import GraphDatabase, basic_auth
import csv
import os

delimiter = ' '
path_file = "file:///files/cosim-split/cosim-sorted-num-split.6.2plexesab"


def run():
    # Neo4j session
    driver = GraphDatabase.driver(uri_neo4j_db, auth=(user_auth, pw_auth))
    session = driver.session()

    print("start..")

    q = 'LOAD CSV FROM {file} AS line FIELDTERMINATOR ":" ' \
        'WITH SPLIT(line[1], " ") AS usersId, SPLIT(line[0], " ") AS row_count ' \
        'FOREACH ' \
        '( uId IN usersId | ' \
        'MERGE (u:User {userId: uId}) ' \
        'SET u.two_plexes = coalesce(u.two_plexes,[]) + row_count ' \
        ')' \
        'RETURN usersId, row_count'

    q1 = 'LOAD CSV FROM {file} AS line FIELDTERMINATOR ":" ' \
        'WITH SPLIT(line[1], " ") AS usersId, SPLIT(line[0], " ") AS row_count ' \
        'FOREACH ' \
        '( uId IN usersId | ' \
        'MERGE (u:User {userId: uId}) ' \
        'SET u.two_plexes = [] ' \
        ')' \
        'RETURN usersId, row_count'

    result = session.run(q, {"file": path_file})
    for r in result:
        # print("(%s, %s) [%s, %s]" % (r[0]["id"], r[1]["name"], r[2]["url"], r[3]["image_url"]))
        print(r)

# EXECUTE
run()
