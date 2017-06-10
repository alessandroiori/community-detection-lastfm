import networkx as nx
import community as cm
import os


def main():
    path_file = os.getcwd() + '/data.edges'
    G = nx.read_edgelist(path_file, nodetype=int, delimiter=' ',)
    G.add_node(7)

    print("\nNodes:")
    for n in G.nodes():
        print(n)

    print("\nEdges:")
    for e in G.edges():
        print(str(e[0]) + ' ' + str(e[1]))

    print("\nIsolate nodes:")
    isolate_nodes = nx.isolates(G)
    for i in isolate_nodes:
        print(i)

    print("\nSelfloop edges:")
    selfloop_edges = G.selfloop_edges()
    for sle in selfloop_edges:
        print(sle)

    #  G.remove_nodes_from(G.selfloop_edges()), G.remove_nodes_from(nx.isolates(G))

    print("\nMaximal cliques:")
    max_cliques = nx.find_cliques(G)
    for c in max_cliques:
        print(c)

    print("\nLouvain heuristices graph partitions:")
    partition = cm.best_partition(G)
    #  for (n, p) in partition:
    print(partition)

# EXECUTION
main()
