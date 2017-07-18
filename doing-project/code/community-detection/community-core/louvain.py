import community
import networkx as nx

for j in [3, 4, 5, 6, 7, 8, 9, 85, 95]:
    edge_dir = "graphs/"
    louvain_dir = "louvain/"
    cosim_dir = "cosim/"
    raw = "raw/"
    name = "rel.wedges.%s" % j
    raw_name = "louvain.%s" % j
    input_file = edge_dir + cosim_dir + name
    output_file = edge_dir + louvain_dir + name
    louvain_file = edge_dir + louvain_dir + raw + raw_name

    G = nx.read_weighted_edgelist("%s.edges" % input_file, delimiter='\t')
    #first compute the best partition
    partition = community.best_partition(G)
    dict = {}
    for k, v in partition.items():
        if dict.get(v):
            dict[v].append(k)
        else:
            dict[v] = [k]

    with open(louvain_file, "w") as fh:
        for o in dict.items():
            length = len(o[1])
            for i, k in zip(o[1], range(1, length+1)):
                if k == length:
                    fh.write("%s\n" % i)
                else:
                    fh.write("%s " % i)


    nx.set_node_attributes(G, name="louvain", values=partition)

    nx.write_gexf(G, path="%s-louvain.gexf" % output_file)