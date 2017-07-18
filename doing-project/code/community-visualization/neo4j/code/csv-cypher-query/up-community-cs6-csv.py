from neo4jdbinfo import user_auth, pw_auth, uri_neo4j_db

from neo4j.v1 import GraphDatabase, basic_auth
import csv
import os

delimiter = ' '
clique_file = "file:///files/clique/clique-num-filtered.6"
clique291_file = "file:///files/clique/clique-row-291.6"
kplex_file = "file:///files/kplex/cosim-sorted-num-filtered.6.2plexes"
kplex15_file = "file:///files/kplex/cosim-kplex-row-15.2plexes"
kplex291_file = "file:///files/kplex/cosim-kplex-row-291.2plexes"
louvain_file = "file:///files/louvain/louvain-num-filtered.6"


def run():
    # Neo4j session
    driver = GraphDatabase.driver(uri_neo4j_db, auth=(user_auth, pw_auth))
    session = driver.session()

    print("start..")

    q_clique = 'LOAD CSV FROM {file} AS line FIELDTERMINATOR ":" ' \
        'WITH SPLIT(line[1], " ") AS usersId, SPLIT(line[0], " ") AS row_num ' \
        'FOREACH ' \
        '( uId IN usersId | ' \
        'MERGE (u:User {userId: uId}) ' \
        'SET u.cs = coalesce(u.cs ,[]) + row_num ' \
        ')' \
        'RETURN usersId, row_num'

    q_kplex = 'LOAD CSV FROM {file} AS line FIELDTERMINATOR ":" ' \
               'WITH SPLIT(line[1], " ") AS usersId, SPLIT(line[0], " ") AS row_num ' \
               'FOREACH ' \
               '( uId IN usersId | ' \
               'MERGE (u:User {userId: uId}) ' \
               'SET u.ks = coalesce(u.ks ,[]) + row_num ' \
               ')' \
               'RETURN usersId, row_num'

    q_louvain = 'LOAD CSV FROM {file} AS line FIELDTERMINATOR ":" ' \
              'WITH SPLIT(line[1], " ") AS usersId, SPLIT(line[0], " ") AS row_num ' \
              'FOREACH ' \
              '( uId IN usersId | ' \
              'MERGE (u:User {userId: uId}) ' \
              'SET u.ls = coalesce(u.ls ,[]) + row_num ' \
              ')' \
              'RETURN usersId, row_num'


    q1 = 'LOAD CSV FROM {file} AS line FIELDTERMINATOR ":" ' \
        'WITH SPLIT(line[1], " ") AS usersId, SPLIT(line[0], " ") AS row_count ' \
        'FOREACH ' \
        '( uId IN usersId | ' \
        'MERGE (u:User {userId: uId}) ' \
        'SET u.ks = [] ' \
        ')' \
        'RETURN usersId, row_count'

    result_clique = session.run(q_clique, {"file": clique291_file})
    #result_kplex = session.run(q_kplex, {"file": kplex291_file})
    # result_louvain = session.run(q_louvain, {"file": louvain_file})
    for r in result_clique:
        # print("(%s, %s) [%s, %s]" % (r[0]["id"], r[1]["name"], r[2]["url"], r[3]["image_url"]))
        print(r)

# EXECUTE
run()
