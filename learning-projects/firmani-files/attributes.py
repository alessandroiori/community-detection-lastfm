import networkx as nx
from collections import defaultdict
import os

name = 'dolphins'
k = 2
knum=100000
G = nx.read_edgelist('%s.edges' % name, comments='Source', delimiter=' ', nodetype = int, data=(('type',unicode),))
G.remove_edges_from(G.selfloop_edges())
G.remove_nodes_from(nx.isolates(G)) 

print 'reading done'

with open('%s.berlowitz' % name,'w') as f:
    for (u,v) in G.edges():
        f.write('%d\t%d\n' % (u, v))

os.system(u'python kplex_without_improvments/kplex.py --file="%s.berlowitz" --k=%d --num_of_kplex=%d' % (name,k,knum))

Kplexes = []

with open('output_file_connected','r') as f:
    lines = f.readlines()
    for l in lines:
        Kplexes += [l.strip().split(',')]
        
Kplexes = sorted(Kplexes, key=lambda x: len(x), reverse=True) 

with open('%s.%dplexes' % (name,k),'w') as f:
    for kplex in Kplexes:
        f.write(" ".join([str(e) for e in sorted(kplex)]))
        f.write("\n")

print 'found %d %dplexes' % (len(Kplexes),k)

coreness = nx.core_number(G)

with open('%s.coreness' % name,'w') as f:
    f.write('%s %s\n' % ('Id', 'Coreness'))
    for u in coreness:
        f.write('%d %d\n' % (u, coreness[u]))

print 'coreness done'

Kliques = sorted(list(nx.find_cliques(G)), key=lambda x: len(x), reverse=True)

with open('%s.cliques' % name,'w') as f:
    for klique in Kliques:
        f.write(" ".join([str(e) for e in sorted(klique)]))
        f.write("\n")

print 'cliques done'

cliqueness = defaultdict(int)

for klique in Kliques:
    for u in klique:
        cliqueness[u] = max(cliqueness[u], len(klique))

with open('%s.cliquenesss' % name,'w') as f:
    f.write('%s %s\n' % ('Id', 'Cliqueness'))
    for u in cliqueness:
        f.write('%d %d\n' % (u, cliqueness[u]))

print 'cliqueness done'

coreness = nx.core_number(G)