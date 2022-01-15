import time
from memory_profiler import profile
import networkx as nx
from graphpartitioning import SpectralBisection, KernighanLin
from memory_profiler import profile


@profile
def speed_test(method, graph):
    start = time.perf_counter()
    method(graph).partition(2)
    finish = time.perf_counter()
    timings = finish - start
    return timings


if __name__ == '__main__':
        # g = nx.powerlaw_cluster_graph(100, 3, 0.2)
        # print(nx.info(g))
        # nx.readwrite.write_edgelist(g, 'test_graph-100.csv', delimiter=',')
        # g2 = nx.powerlaw_cluster_graph(10000, 3, 0.2)
        # print(nx.info(g2))
        # nx.readwrite.write_edgelist(g2, 'test_graph-10K.csv', delimiter=',')
        # g3 = nx.powerlaw_cluster_graph(100000, 3, 0.2)
        # print(nx.info(g3))
        # nx.readwrite.write_edgelist(g3, 'test_graph-100K.csv', delimiter=',')
        print('100 =======================================')
        g = nx.read_edgelist('test_graph-100.csv', delimiter=',', nodetype=str)
        x1 = speed_test(SpectralBisection, g)
        print(x1)
        print('1K =======================================')
        g = nx.read_edgelist('test_graph-1K.csv', delimiter=',', nodetype=str)
        x2 = speed_test(SpectralBisection, g)
        print(x2)
        print('10K =======================================')
        g = nx.read_edgelist('test_graph-10K.csv', delimiter=',', nodetype=str)
        x3 = speed_test(SpectralBisection, g)
        print(x3)
        print('100K =======================================')
        g = nx.read_edgelist('test_graph-100K.csv', delimiter=',', nodetype=str)
        x4 = speed_test(SpectralBisection, g)
        print(x4)





