#NetworkX Test

import networkx as nx
import matplotlib.pyplot as plt
import sys

graphFile = sys.argv[1] 
g = nx.read_edgelist(graphFile, create_using=nx.Graph(), nodetype=int)
print nx.info(g)
#nx.draw(g)
#plt.show()
clique = nx.find_cliques(g)

print clique