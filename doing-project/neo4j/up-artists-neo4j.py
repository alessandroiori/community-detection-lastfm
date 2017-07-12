from neo4jdbinfo import user_auth, pw_auth, uri_neo4j_db

from neo4j.v1 import GraphDatabase, basic_auth
# import networkx as nx
import csv
import os

delimiter = '\t'
file_name = 'artists.dat'
path_file = os.getcwd() + '/' + file_name


def run():
    # Neo4j session
    driver = GraphDatabase.driver(uri_neo4j_db, auth=(user_auth, pw_auth))
    session = driver.session()

    print("Uploading artist on neo4j")
    with open(path_file, 'r') as csvfile2:
        reader = csv.reader(csvfile2, dialect='excel', delimiter=delimiter)
        for row in reader:
            id = row[0].encode('utf-8')
            name = row[1].encode('utf-8')
            url = row[2].encode('utf-8')
            image_url = row[3].encode('utf-8')
            #writer.writerow([col1, col2, graphType])

            q = 'MATCH (a:Artist {artistId: {id}})' \
                'SET a += {name: {name}, url: {url}}' \
                'RETURN a'

            result = session.run(q, {"id": id, "name": name, "url": url})
            for r in result:
                #print("(%s, %s) [%s, %s]" % (r[0]["id"], r[1]["name"], r[2]["url"], r[3]["image_url"]))
                print(r)


# EXECUTION
run()


