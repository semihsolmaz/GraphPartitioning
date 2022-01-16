import time
from memory_profiler import profile
import networkx as nx
from graphpartitioning import SpectralBisection, KernighanLin, EdgeBetweennessCentrality
from memory_profiler import profile


@profile
def speed_test(method, graph):
    start = time.perf_counter()
    method(graph).partition(2)
    finish = time.perf_counter()
    timings = finish - start
    return timings


if __name__ == '__main__':

    for i in [2**x for x in range(6, 15)]:
        print(i)
        print('+++++++++++++++++++++++++++++++++++++++++++++++++')
        g = nx.powerlaw_cluster_graph(i, 3, 0.2)
        print(str(i) + ' spec=======================================')
        x1 = speed_test(SpectralBisection, g)
        print(x1)
        if i < 520:
            print(str(i) + ' kern=======================================')
            x2 = speed_test(KernighanLin, g)
            print(x2)
        if i < 520:
            print(str(i) + ' Edge=======================================')
            x3 = speed_test(EdgeBetweennessCentrality, g)
            print(x3)
        print('+++++++++++++++++++++++++++++++++++++++++++++++++')




