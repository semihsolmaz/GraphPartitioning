import csv

import matplotlib.pyplot as plt
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
        # Maybe cut into 2 rpt spectral ordering?
        # spectral_ordering_g = spectral_ordering(self.graph)

        for index, node in enumerate(self.graph.nodes):
            if fiedler_vector_g[index] < 0:
                part_1.append(node)
            else:
                part_2.append(node)

        self.partitions = [subgraph(self.graph, part_1), subgraph(self.graph, part_2)]
        return self.partitions

    def getRemovedEdges(self):
        removed_edges = []
        for edge in self.graph.edges:
            if set(edge) not in [set(item) for item in list(self.partitions[0].edges) + list(self.partitions[1].edges)]:
                removed_edges.append(edge)
        return removed_edges

    def drawPartitions(self):
        options = {"node_color": "white", "node_size": 100, "linewidths": 0, "width": 0.1, "with_labels": True}
        pos = nx.kamada_kawai_layout(g)

        for n, graph in enumerate(self.partitions):
            nx.draw(graph, pos, **options)
            if n == 1:
                plt.savefig("PartedGraph.png", format="PNG")

    def drawInitialWithColor(self, outfile):

        combined = nx.compose(self.partitions[0], self.partitions[1])
        nx.set_edge_attributes(combined, 'b', 'color')
        # combined.add_edges_from(self.getRemovedEdges(), color='r')
        for edge in self.getRemovedEdges():
            combined.add_edge(*edge, color='r')

        colors = nx.get_edge_attributes(combined, 'color').values()
        options = {"node_color": "white", "node_size": 100, "linewidths": 0, "width": 0.1, "with_labels": True}
        pos = nx.kamada_kawai_layout(combined)

        nx.draw(combined, pos, edge_color=colors, **options)
        plt.savefig(outfile, format="PNG")

        return combined

    def numberOfEdgesCut(self):
        number_of_edges_cut = fiedler_vector(self.graph) @ laplacian_matrix(self.graph) @ fiedler_vector(self.graph).T

        return number_of_edges_cut


if __name__ == '__main__':
    # g = nx.karate_club_graph()
    # g = nx.powerlaw_cluster_graph(50, 2, 0.6)
    g = nx.read_edgelist('soc-karate.csv', delimiter=',', nodetype=str)
    g.name = 'karate'
    bisection = SpectralBisection(g)

    partitions = bisection.partition()
