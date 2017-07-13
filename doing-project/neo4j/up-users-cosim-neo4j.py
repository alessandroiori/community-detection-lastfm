from neo4jdbinfo import user_auth, pw_auth, uri_neo4j_db

from neo4j.v1 import GraphDatabase, basic_auth
import csv
import os

delimiter = '\t'
file_name = 'data/dataset/cosim/rel.wedges.6.edges'
path_file = os.getcwd() + '/' + file_name


def run():
    # Neo4j session
    driver = GraphDatabase.driver(uri_neo4j_db, auth=(user_auth, pw_auth))
    session = driver.session()

    print("Uploading cosine similarity between users on neo4j")
    with open(path_file, 'r') as csvfile2:
        reader = csv.reader(csvfile2, dialect='excel', delimiter=delimiter)
        for row in reader:
            u1 = row[0].encode('utf-8')
            u2 = row[1].encode('utf-8')
            weight = float(row[2].encode('utf-8'))

            q = "MATCH (u1:User {userId: {id1}}) \
                MATCH (u2:User {userId: {id2}}) \
                MERGE (u1)-[r:cosim {weight: {weight}}]-(u2) \
                RETURN u1, u2, r"

            result = session.run(q, {"id1": u1, "id2": u2, "weight": weight})
            for r in result:
                #print("(%s, %s) [%s, %s]" % (r[0]["id"], r[1]["name"], r[2]["url"], r[3]["image_url"]))
                print(r)


# EXECUTION
run()


