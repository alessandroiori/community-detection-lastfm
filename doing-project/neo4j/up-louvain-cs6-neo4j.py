# per ciascun nodo j-esimo del louvain i-esimo, aggiungiamo
# al label "louvains" del nodo j, il louvain a cui partecipa
#
# louvain methond calcolato su cosine similarity >= 0.6
# e numerate da 1 a N da quella con cardinalita maggiore a minore
#
# MATCH p=(u1:User)-[r1:cosim]-(u2:User)
# MATCH q=(u1:User)-[r2:listen]->(a:Artist)
# MATCH f=(u2:User)-[r3:listen]->(a:Artist)
# WHERE 1 IN u1.cliques AND 1 IN u2.cliques AND toFloat(r1.weight) >= 0.8
# AND toInt(r2.weight) >= 5000 AND toInt(r3.weight) >= 5000
# return p, q, f
#

from neo4jdbinfo import user_auth, pw_auth, uri_neo4j_db

from neo4j.v1 import GraphDatabase, basic_auth
import csv
import os

delimiter = ' '
file_name = 'data/dataset/louvain/louvain.6'
path_file = os.getcwd() + '/' + file_name


def run():
    # Neo4j session
    driver = GraphDatabase.driver(uri_neo4j_db, auth=(user_auth, pw_auth))
    session = driver.session()

    louvain_number = 0

    print("Uploading clique 6 cosine similarity on neo4j")
    with open(path_file, 'r') as csvfile2:
        reader = csv.reader(csvfile2, dialect='excel', delimiter=delimiter)
        for usersId in reader:
            louvain_number += 1
            # print(usersId)

            for id in usersId:

                q = 'MATCH (u:User {userId: {id}}) \
                    SET u.louvains = u.louvains + {l_number} \
                    RETURN u'

                # clean louvains field
                q2 = 'MATCH (u:User {userId: {id}}) \
                    SET u.louvains = [] \
                    RETURN u'

                q3 = 'MATCH (u:User {userId: {id}}) \
                    REMOVE u.louvains \
                    RETURN u'

                id = id.encode('utf-8')
                result = session.run(q, {"id": id, "l_number": louvain_number})
                for r in result:
                    # print("(%s, %s) [%s, %s]" % (r[0]["id"], r[1]["name"], r[2]["url"], r[3]["image_url"]))
                    print(r)


# EXECUTION
run()


