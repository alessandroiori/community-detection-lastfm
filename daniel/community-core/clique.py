import networkx as nx

k = 4
for j in [3, 4, 5, 6, 7, 8, 9, 85, 95]:
    edge_dir = "graphs/"
    clique_dir = "clique/"
    cosim_dir = "cosim/"
    raw = "raw/"
    name = "rel.wedges.%s" % j
    raw_name = "clique.%s" % j
    input_file = edge_dir + cosim_dir + name
    output_file = edge_dir + clique_dir + name
    cliques_file = edge_dir + clique_dir + raw + raw_name
    G = nx.read_weighted_edgelist("%s.edges" % input_file, delimiter='\t')

    kliques = nx.find_cliques(G)
    cliques = sorted(list(filter(lambda x: len(x) >= k, kliques)), key=len, reverse=True)

    with open(cliques_file, "w") as fh:
        for c in cliques:
            length = len(c)
            for i, k in zip(c, range(1,length+1)):
                if k == length:
                    fh.write("%s\n" % i)
                fh.write("%s " % i)
    i = 1
    dic = {}
    node = set()
    for clique in cliques:
        for el in clique:
            if el not in node:
                node.add(el)
                dic[el] = i
        i += 1

    gi = nx.subgraph(G, list(node))
    nx.set_node_attributes(gi, name="clique", values=dic)

    nx.write_gexf(gi, path="%s.%s-clique.gexf" % (output_file, k))
