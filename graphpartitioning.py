from networkx.algorithms import community
from networkx.linalg.laplacianmatrix import laplacian_matrix
from networkx.linalg.algebraicconnectivity import algebraic_connectivity, fiedler_vector, spectral_ordering
from networkx.linalg.spectrum import laplacian_spectrum
from networkx.classes.function import subgraph
import networkx as nx

class SpectralBisection:

    def __init__(self, g):
        self.graph = g
        self.partitions = self.graph
        self.removed_edges = []
        # self.laplacian_matrix = laplacian_matrix(g)
        # self.laplacian_spectrum = laplacian_spectrum(g)
        # self.algebraic_connectivity = algebraic_connectivity(g)

    def partition(self):
        part_1 = []
        part_2 = []
        fiedler_vector_g = fiedler_vector(self.graph)
        spectral_ordering_g = spectral_ordering(self.graph)

        for node in spectral_ordering_g:
            if fiedler_vector_g[node] < 0:
                part_1.append(node)
            else:
                part_2.append(node)

        self.partitions = [subgraph(self.graph, part_1), subgraph(self.graph, part_2)]

        for edge in self.graph.edges:
            if edge not in list(self.partitions[0].edges) + list(self.partitions[1].edges):
                self.removed_edges.append(edge)
        return self.partitions

    def getRemovedEdges(self):

        return self.removed_edges




# laplacian_g = laplacian_matrix(g)
# laplacian_spectrum_g = laplacian_spectrum(g)
# algebraic_con_g = algebraic_connectivity(g)
# fiedler_vector_g = fiedler_vector(g)
# spectral_ordering_g = spectral_ordering(g)

if __name__ == '__main__':
    g = nx.karate_club_graph()
    bisec = SpectralBisection(g)
    parts = bisec.partition()
    for i in parts:
        print(list(i.edges))

    print(bisec.getRemovedEdges())