import networkx as nx
import matplotlib.pyplot as plt
import os

delimiter = '\t'
file_name = 'user_friends.dat'
path_file = os.getcwd() + '/' + file_name

clique_nodes_number = 7

def main():
    g = nx.read_edgelist(path_file, nodetype=int, delimiter=delimiter, )

    nodes = g.nodes()
    edges = g.edges()
    isolate_nodes = nx.isolates(g)
    selfloop_edges = g.selfloop_edges()

    print()
    print("File: " + str(file_name))
    print("Nodes: " + str(len(nodes)) + " Edges: " + str(len(edges)))
    print("Isolate nodes: " + str(len(isolate_nodes)) + " Self loop: " + str(len(selfloop_edges)))
    print()

    # nx.draw(g)
    # plt.show()

    #nx.draw(g, pos=nx.spring_layout(g))
    """""
    cliques = nx.enumerate_all_cliques(g)
    cliques = nx.find_cliques(g)
    """""
    cliques_nodes_set = set()

    cliques = nx.find_cliques_recursive(g)
    for e in cliques:
        length = len(e)
        # print(str(e) + ', ' + str(length))
        if length >= clique_nodes_number:
            for n in e:
                cliques_nodes_set.add(n)

    cliques_nodes_list = list(cliques_nodes_set)

    print("Nodes qliques with " + str(clique_nodes_number) + "cardinality : ")
    print(cliques_nodes_list)

    g2 = g.subgraph(cliques_nodes_list)

    nx.draw(g2)
    plt.show()


# EXECUTION
main()
