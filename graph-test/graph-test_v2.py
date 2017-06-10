import networkx as nx

g = nx.karate_club_graph()

cliques = nx.find_cliques(g)
cliques4 = [clq for clq in cliques if len(clq) >= 4]

nodes = [n for clq in cliques4 for n in clq]
h = g.subgraph(nodes)

deg = nx.degree(h)
nodes = [n for n in nodes if deg[n] >= 4]

k = h.subgraph(nodes)

nx.draw(k)
