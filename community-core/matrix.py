import numpy as np
import matplotlib.pyplot as plt
import os

j = 6
edge_dir = "graphs/"
louvain_dir = "louvain/"
clique_dir = "clique/"
kplex_dir = "kplex/"
mat_dir = "matrix/"

raw = "raw/"
louvain_raw_name = "louvain.%s" % j
clique_raw_name = "clique.%s" % j
kplex_raw_name = "2plex.%s" % j
mat_name = "matrix.%s.npy" % j

louvain_file = edge_dir + louvain_dir + raw + louvain_raw_name
clique_file = edge_dir + clique_dir + raw + clique_raw_name
kplex_file = edge_dir + kplex_dir + kplex_raw_name
mat_file = edge_dir + mat_dir + mat_name

CLIQUE_POS = 0
KPLEX_POS = 1
LOU_POS = 2


def load_matrix():
    global j, matrix
    with open(louvain_file, "r") as fh:
        louvains = [sorted(list(map(int, line.split()))) for line in fh]
    with open(clique_file, "r") as fh:
        cliques = [sorted(list(map(int, line.split()))) for line in fh]
    with open(kplex_file, "r") as fh:
        kplexes = [sorted(list(map(int, line.split()))) for line in fh]
    mx = max([val for sublist in cliques for val in sublist])
    nx = max([val for sublist in louvains for val in sublist])
    rx = max([val for sublist in kplexes for val in sublist])
    mx = max(mx, nx, rx) + 1
    mat = [[[0, 0, 0] for x in range(mx)] for y in range(mx)]
    for clique in cliques:
        n = len(clique)
        for i in range(n):
            for j in range(i + 1, n):
                u = clique[i]
                v = clique[j]
                mat[u][v][CLIQUE_POS] += 1
    for lou in louvains:
        n = len(lou)
        for i in range(n):
            for j in range(i + 1, n):
                u = lou[i]
                v = lou[j]
                mat[u][v][LOU_POS] += 1
    for plex in kplexes:
        n = len(plex)
        for i in range(n):
            for j in range(i + 1, n):
                u = plex[i]
                v = plex[j]
                mat[i][j][LOU_POS] += 1

    matrix = np.array(mat).astype(float)
    np.save(mat_file, mat)

if not os.path.exists(mat_file):
    load_matrix()
else:
    matrix = np.load(mat_file).astype(float)




#plt.imshow(matrix)
#plt.show()
