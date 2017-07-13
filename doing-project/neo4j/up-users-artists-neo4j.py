from neo4jdbinfo import user_auth, pw_auth, uri_neo4j_db

from neo4j.v1 import GraphDatabase, basic_auth
import csv
import os

delimiter = '\t'
file_name = 'data/dataset/user_artists.dat'
path_file = os.getcwd() + '/' + file_name


def run():
    # Neo4j session
    driver = GraphDatabase.driver(uri_neo4j_db, auth=(user_auth, pw_auth))
    session = driver.session()

    print("Uploading users-artist edges with weight (# of listen) on neo4j")
    with open(path_file, 'r') as csvfile2:
        reader = csv.reader(csvfile2, dialect='excel', delimiter=delimiter)
        for row in reader:
            user_id = row[0].encode('utf-8')
            artist_id = row[1].encode('utf-8')
            weight = row[2].encode('utf-8')

            print(str(user_id)+str(artist_id)+str(weight))
            # MERGE create if a node or relation does not exist else match it
            q = "MERGE (u:User {userId: {user_id}}) \
                MERGE (a:Artist {artistId: {artist_id}}) \
                MERGE (u)-[r:listen {weight: {weight}}]->(a) \
                RETURN u, a, r"

            result = session.run(q, {"user_id": user_id, "artist_id": artist_id, "weight": weight})
            for r in result:
                print(r)

# EXECUTION
run()
