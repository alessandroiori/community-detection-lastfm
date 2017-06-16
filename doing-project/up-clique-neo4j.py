#
# up-clique-neo4j.py allow to add for each nodes in the neo4j graph,
# the number of cardinality of the cliques in witch it participates.
#
# es. clique1 = [3,4,2,6,11] (cardinality 5), clique2 = [5,4,9,7,2,10] (cardinality 6).
# The node v=4 participates in both then v.clique_n=[5,6] while v=5 v.clique_n[6], ecc..
#
# Cypher query example: MATCH r=(n:User)<-[]->(m:User) WHERE 10 IN n.clique_n AND 10 IN m.clique_n RETURN r
#

from neo4j.v1 import GraphDatabase, basic_auth
import networkx as nx
import os

from neo4jdbinfo import user_auth, pw_auth, uri_neo4j_db

delimiter = '\t'
file_name = 'user_friends.dat'
path_file = os.getcwd() + '/' + file_name

clique_nodes_number_min = 3
clique_nodes_number_max = 10


def printGraphInfo(g):
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
    printGraphInfo(g)

    print("Cliques with cardinality from minimum " + str(clique_nodes_number_min) + " to minimum " + str(clique_nodes_number_max))
    for i in range(clique_nodes_number_min, clique_nodes_number_max+1):

        k_cliques = list(nx.k_clique_communities(g, i))
        cliques_nodes_set = set()  # delete duplicates

        print("\nCliques with cardinality >= " + str(i) + " :")
        for c in k_cliques:
            nodes = list(c)
            for n in nodes:
                cliques_nodes_set.add(n)
            print(nodes)

        q = 'MATCH (u:User) \
             WHERE u.id= {id} AND NOT {number} IN u.clique_n \
             SET u.clique_n = u.clique_n + {number} \
             RETURN u'

        # clean clique_n field
        q2 = 'MATCH (u:User) \
                 WHERE u.id= {id} \
                 SET u.clique_n = [] \
                 RETURN u'

        print("Nodes on neo4j: ")
        for n in cliques_nodes_set:
            result = session.run(q, {"id": n, "number": i})
            for r in result:
                print(r[0].properties)

    session.close()


# EXECUTION
run()
