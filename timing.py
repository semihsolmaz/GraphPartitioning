import time
from memory_profiler import profile
import networkx as nx
from graphpartitioning import SpectralBisection, KernighanLin
from memory_profiler import profile


@profile
def my_func():
    timings = 0
    g = nx.powerlaw_cluster_graph(100, 2, 0.6)
    for i in range(100):
        start = time.perf_counter()
        SpectralBisection(g).partition(2)
        finish = time.perf_counter()
        timings = timings + (finish - start)
    return timings/100


if __name__ == '__main__':
    x = my_func()
    print(x)




