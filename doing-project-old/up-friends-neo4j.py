# Python3
# pip3 install neo4j-driver
# pip3 install networkx

from neo4j.v1 import GraphDatabase, basic_auth
import networkx as nx
import os

from neo4jdbinfo import user_auth, pw_auth, uri_neo4j_db

# graph
delimiter = '\t'
file_name = 'user_friends.dat'
path_file = os.getcwd() + '/' + file_name


def print_graph_info(g):
    nodes = g.nodes()
    edges = g.edges()
    isolate_nodes = nx.isolates(g)
    selfloop_edges = g.selfloop_edges()

    print()
    print("File: " + str(file_name))
    print("Nodes: " + str(len(nodes)) + " Edges: " + str(len(edges)))
    print("Isolate nodes: " + str(len(isolate_nodes)) + " Self loop: " + str(len(selfloop_edges)))
    print()


def run():

    # Neo4j session
    driver = GraphDatabase.driver(uri_neo4j_db, auth=(user_auth, pw_auth))
    session = driver.session()

    g = nx.read_edgelist(path_file, nodetype=int, delimiter=delimiter, )
    print_graph_info(g)

    nodes = g.nodes()
    edges = g.edges()

    print("Uploading graph on neo4j")
    for e in edges:
        s = e[0]
        d = e[1]

        # MERGE create if a node or relation does not exist else match it
        q = "MERGE (u1:User {id: {id1}}) \
            MERGE (u2:User {id: {id2}}) \
            MERGE (u1)-[r:follow]->(u2) \
            RETURN u1, u2, r"

        result = session.run(q, {"id1": s, "id2": d})
        for r in result:
            print("(%s)-[%s]->(%s)" % (r[0]["id"], r[2].type, r[1]["id"]))

    session.close()

# EXECUTION
run()
