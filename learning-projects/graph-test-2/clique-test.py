import networkx as nx
import matplotlib.pyplot as plt
import os

delimiter = '\t'
file_name = 'user_friends.dat'
path_file = os.getcwd() + '/' + file_name

clique_nodes_number = 4


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


def main():
    g = nx.read_edgelist(path_file, nodetype=int, delimiter=delimiter, )
    printGraphInfo(g)

    k_cliques = list(nx.k_clique_communities(g, clique_nodes_number))
    cliques_nodes_set = set()  # delete duplicates

    print("Cliques with cardinality >= " + str(clique_nodes_number) + " :")
    for c in k_cliques:
        nodes = list(c)
        for n in nodes:
            cliques_nodes_set.add(n)
        print(nodes)

    cliques_nodes_list = list(cliques_nodes_set)

    g2 = g.subgraph(cliques_nodes_list)
    printGraphInfo(g2)

    nx.draw(g2)
    plt.show()

# EXECUTION
main()
