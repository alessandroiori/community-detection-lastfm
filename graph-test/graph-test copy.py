#NetworkX Test

import networkx as nx

# G = nx.Graph()

# elist=[('a','b',5.0),('b','c',3.0),('a','c',1.0),('c','d',7.3)]
# G.add_weighted_edges_from(elist)

# dijkstra = nx.dijkstra_path(G,'a','d')

# nx.draw(G)
graphFile = args[1] 

G = nx.read_edgelist('%s' % graphFileName, comments='Source', delimiter='\t', nodetype = int, data=(('type',unicode),))

print(G.adj)
