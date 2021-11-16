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
        self.partitions = [self.graph]
        # self.laplacian_matrix = laplacian_matrix(g)
        # self.laplacian_spectrum = laplacian_spectrum(g)
        # self.algebraic_connectivity = algebraic_connectivity(g)

    def partition(self, number_of_partitions):
        if number_of_partitions > len(self.graph.nodes):
            raise ValueError('Number of partitions cant be larger than number of nodes',
                             '#ofnodes:' + str(len(self.graph.nodes)) + ' < #ofpartitions:' + str(number_of_partitions))
        partitions_list = [self.graph]
        while len(partitions_list) < number_of_partitions:
            part_1 = []
            part_2 = []
            graph_bisect = partitions_list.pop(0)
            spectral_ordering_g = spectral_ordering(graph_bisect)

            for index, node in enumerate(spectral_ordering_g):
                if index < int(len(spectral_ordering_g)/2):
                    part_1.append(node)
                else:
                    part_2.append(node)

            partitions_list.append(subgraph(self.graph, part_1))
            partitions_list.append(subgraph(self.graph, part_2))
        self.partitions = partitions_list
        return self.partitions

    def getRemovedEdges(self):
        removed_edges = []
        edge_list_after_removal = []
        for part in self.partitions:
            for edge in part.edges:
                edge_list_after_removal.append(edge)
        for edge in self.graph.edges:
            if set(edge) not in [set(item) for item in edge_list_after_removal]:
                removed_edges.append(edge)
        return removed_edges

    def drawPartitions(self):
        options = {"node_color": "white", "node_size": 100, "linewidths": 0, "width": 0.1, "with_labels": True}
        pos = nx.kamada_kawai_layout(g)

        for n, graph in enumerate(self.partitions):
            nx.draw(graph, pos, **options)
            if n == 1:
                plt.savefig("PartedGraph.png", format="PNG")

    # todo: limit node number for drawing
    # todo: color nodes for partitions (optional: add legend)
    def drawInitialWithColor(self, outfile):

        combined = nx.compose(*self.partitions)
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

    partitions = bisection.partition(4)
    bisection.drawInitialWithColor('test.png')
    print(bisection.getRemovedEdges())
    for i in partitions:
        print((len(i.nodes)))
