import time

import networkx as nx

from graphpartitioning import SpectralBisection, KernighanLin

g = nx.powerlaw_cluster_graph(100, 2, 0.6)
for i in range(100, 10000, 100):
    start = time.perf_counter()
    SpectralBisection(g).partition(2)
    finish = time.perf_counter()
    print(finish - start)
