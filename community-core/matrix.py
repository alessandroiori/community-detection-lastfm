from pyparsing import CaselessLiteral

j = 6
edge_dir = "graphs/"
louvain_dir = "louvain/"
clique_dir = "clique/"
kplex_dir = "kplex/"
raw = "raw/"
louvain_raw_name = "louvain.%s" % j
clique_raw_name = "clique.%s" % j
kplex_raw_name = "2plex.%s" % j

louvain_file = edge_dir + louvain_dir + raw + louvain_raw_name
clique_file = edge_dir + clique_dir + raw + clique_raw_name
kplex_file = edge_dir + kplex_dir + kplex_raw_name
CLIQUE_POS = 0
KPLEX_POS = 1
LOU_POS = 2
with open(louvain_file, "r") as fh:
    louvains = [sorted(list(map(int, line.split()))) for line in fh]

with open(clique_file, "r") as fh:
    cliques = [sorted(list(map(int, line.split()))) for line in fh]

with open(kplex_file, "r") as fh:
    kplexes = [sorted(list(map(int, line.split()))) for line in fh]


mx = max([val for sublist in cliques for val in sublist])
nx = max([val for sublist in louvains for val in sublist])
rx = max([val for sublist in kplex for val in sublist])
mx = max(mx, nx, rx)

mat = [[[0, 0, 0] for x in range(mx)] for y in range(mx)]


for clique in cliques:
    n = len(clique)
    for i in range(n):
        for j in range(i+1, n):
            mat[i][j][CLIQUE_POS]+=1

for lou in louvains:
    n = len(lou)
    for i in range(n):
        for j in range(i+1, n):
            mat[i][j][LOU_POS]+=1

for plex in :
    n = len(lou)
    for i in range(n):
        for j in range(i+1, n):
            mat[i][j][LOU_POS]+=1



