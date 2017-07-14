import networkx as nx
import community as cm
import os


def main():

    #  path_file = os.getcwd() + '/data.edges'
    #  G = nx.read_edgelist(path_file, nodetype=int, delimiter=' ',)
    path_file = os.getcwd() + '/user_friends.dat'
    G = nx.read_edgelist(path_file, nodetype=int, delimiter='\t',)
    #  G.add_node(7)

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

    """
    print("\nLouvain dendrogram (partions tree):")
    dendrogram = cm.generate_dendrogram(G)
    print("(level\tpartition)")
    count = 0
    for d in dendrogram:
        print(str(count) + '\t' + str(d))
        count += 1

    print("\nLouvain best partition:")
    partition = cm.best_partition(G)
    print("(partion\tnode)")
    for node, part in partition.items():
        print(str(part) + '\t' + str(node))

    print("\nLouvain graph modularity:")
    modularity = cm.modularity(partition, G)
    print(modularity)
    """

    """""
    g = nx.erdos_renyi_graph(1000, 0.01)
    dendo = cm.generate_dendrogram(g)
    for level in range(len(dendo) - 1):
        print("partition at level", level,
              "is", cm.partition_at_level(dendo, level))
    """""

# EXECUTION
main()
