# per ciascun nodo j-esimo della clique i-esima, aggiungiamo
# al label clique_number del nodo j, la clique a cui partecipa
#
# le clique sono calcolate su cosine similarity >= 0.6
#

from neo4jdbinfo import user_auth, pw_auth, uri_neo4j_db

from neo4j.v1 import GraphDatabase, basic_auth
import csv
import os

delimiter = ' '
file_name = 'clique/clique.6'
path_file = os.getcwd() + '/' + file_name


def run():
    # Neo4j session
    driver = GraphDatabase.driver(uri_neo4j_db, auth=(user_auth, pw_auth))
    session = driver.session()

    clique_number = 0

    print("Uploading clique 6 cosine similarity on neo4j")
    with open(path_file, 'r') as csvfile2:
        reader = csv.reader(csvfile2, dialect='excel', delimiter=delimiter)
        for usersId in reader:
            clique_number += 1
            #print(usersId)

            for id in usersId:
                
                q = 'MATCH (u:User {artistId: {id}})' \
                    'SET u += {cliques: {c_number}}' \
                    'RETURN u'
    
                result = session.run(q, {"id": id, "c_number": clique_number})
                for r in result:
                    #print("(%s, %s) [%s, %s]" % (r[0]["id"], r[1]["name"], r[2]["url"], r[3]["image_url"]))
                    print(r)

# EXECUTION
run()


