import community
import networkx as nx

for j in [3, 4, 5, 6, 7, 8, 9, 85, 95]:
    edge_dir = "graphs/"
    louvain_dir = "louvain/"
    cosim_dir = "cosim/"
    name = "rel.wedges.%s" % j
    input_file = edge_dir + cosim_dir + name
    output_file = edge_dir + louvain_dir + name
    G = nx.read_weighted_edgelist("%s.edges" % input_file, delimiter='\t')
    #first compute the best partition
    partition = community.best_partition(G)

    nx.set_node_attributes(G, name="louvain", values=partition)

    nx.write_gexf(G, path="%s-louvain.gexf" % output_file)