from networkx.algorithms import community
from networkx.linalg.laplacianmatrix import laplacian_matrix
from networkx.linalg.algebraicconnectivity import algebraic_connectivity, fiedler_vector, spectral_ordering
from networkx.linalg.spectrum import laplacian_spectrum
from networkx.classes.function import subgraph
import networkx as nx


class SpectralBisection:
    """
    Divide graph into partitons using spectral bisection algorithm
    :param g: networkX graph
    :return: list  networkX graphs
    """
    def __init__(self, g):
        self.graph = g
        self.partitions = self.graph
        # self.laplacian_matrix = laplacian_matrix(g)
        # self.laplacian_spectrum = laplacian_spectrum(g)
        # self.algebraic_connectivity = algebraic_connectivity(g)

    def partition(self):
        part_1 = []
        part_2 = []
        fiedler_vector_g = fiedler_vector(self.graph)
        spectral_ordering_g = spectral_ordering(self.graph)

        for index, node in enumerate(g.nodes):
            if fiedler_vector_g[index] < 0:
                part_1.append(node)
            else:
                part_2.append(node)

        self.partitions = [subgraph(self.graph, part_1), subgraph(self.graph, part_2)]
        return self.partitions

    def getRemovedEdges(self):
        removed_edges = []
        for edge in self.graph.edges:
            if edge not in list(self.partitions[0].edges) + list(self.partitions[1].edges):
                removed_edges.append(edge)
        return removed_edges

    def numberOfEdgesCut(self):
        number_of_edges_cut = fiedler_vector(self.graph) @ laplacian_matrix(self.graph) @ fiedler_vector(self.graph).T

        return number_of_edges_cut


if __name__ == '__main__':
    g = nx.les_miserables_graph()
    bisec = SpectralBisection(g)
    parts = bisec.partition()
    for i in parts:
        print(list(i.nodes))

    print(bisec.numberOfEdgesCut())