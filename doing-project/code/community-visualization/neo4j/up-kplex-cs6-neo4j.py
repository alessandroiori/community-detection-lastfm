# per ciascun nodo j-esimo del louvain i-esimo, aggiungiamo
# al label "kplexes" del nodo j, il louvain a cui partecipa
#
# k-plex calcolato su cosine similarity >= 0.6
# e numerate da 1 a N da quella con cardinalita maggiore a minore
#
# MATCH (n:User) WHERE n.kplexes IS NULL RETURN COUNT(*)
#

from neo4jdbinfo import user_auth, pw_auth, uri_neo4j_db

from neo4j.v1 import GraphDatabase, basic_auth
import csv
import os

delimiter = ' '
file_name = 'data/dataset/kplex/cosim-sorted-4k.6.2plexes'
path_file = os.getcwd() + '/' + file_name


def run():
    # Neo4j session
    driver = GraphDatabase.driver(uri_neo4j_db, auth=(user_auth, pw_auth))
    session = driver.session()

    kplex_number = 0

    print("Uploading clique 6 cosine similarity on neo4j")
    with open(path_file, 'r') as csvfile2:
        reader = csv.reader(csvfile2, dialect='excel', delimiter=delimiter)
        for usersId in reader:
            kplex_number += 1
            # print(usersId)

            for id in usersId:

                q = 'MATCH (u:User {userId: {id}}) \
                    WHERE NOT {kp_number} IN u.kplexes \
                    SET u.kplexes = u.kplexes + {kp_number} \
                    RETURN u'

                # clean louvains field
                q2 = 'MATCH (u:User {userId: {id}}) \
                    SET u.kplexes = [] \
                    RETURN u'

                q3 = 'MATCH (u:User) \
                    SET u.kplexes = [] \
                    RETURN u'

                q4 = 'MATCH (u:User {userId: {id}}) \
                    REMOVE u.kplexes \
                    RETURN u'

                id = id.encode('utf-8')
                result = session.run(q, {"id": id, "kp_number": kplex_number})
                for r in result:
                    # print("(%s, %s) [%s, %s]" % (r[0]["id"], r[1]["name"], r[2]["url"], r[3]["image_url"]))
                    print(r)


# EXECUTION
run()


