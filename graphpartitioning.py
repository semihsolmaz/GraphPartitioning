import matplotlib.pyplot as plt
from networkx.algorithms.community import kernighan_lin, girvan_newman
from networkx.linalg.laplacianmatrix import laplacian_matrix
from networkx.linalg.algebraicconnectivity import fiedler_vector, spectral_ordering
from networkx.classes.function import subgraph
import networkx as nx
import itertools
import seaborn as sns


class SpectralBisection:
    """
    Divide graph into partitons using spectral bisection algorithm
    :param g: networkX graph
    :return: list of networkX graphs
    """
    def __init__(self, g):
        self.graph = g
        self.partitions = [self.graph]

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
                edge_list_after_removal.append(set(edge))
        for edge in self.graph.edges:
            if set(edge) not in edge_list_after_removal:
                removed_edges.append(edge)
        return removed_edges

    def drawPartitions(self):
        options = {"node_color": "yellow", "node_size": 100, "linewidths": 0, "width": 0.1, "with_labels": True}
        pos = nx.kamada_kawai_layout(self.graph, scale=100)

        for n, graph in enumerate(self.partitions):
            nx.draw(graph, pos, **options)
            if n == 1:
                plt.savefig("PartedGraph.png", format="PNG")

    def drawInitialWithColor(self, outfile):
        # Generate colormap
        colors = sns.color_palette(None, len(self.partitions)).as_hex()
        combined = nx.Graph()
        for ind, part in enumerate(self.partitions):
            nx.set_node_attributes(part, colors[ind], 'color')
            combined = nx.compose(combined, part)
        node_colors = nx.get_node_attributes(combined, 'color').values()
        nx.set_edge_attributes(combined, 'b', 'color')

        for edge in self.getRemovedEdges():
            combined.add_edge(*edge, color='r')

        colors = nx.get_edge_attributes(combined, 'color').values()
        options = {"node_size": 300, "linewidths": 0.5, "width": 0.2, "with_labels": True}
        plt.figure(3, figsize=(15, 15))
        pos = nx.kamada_kawai_layout(combined, scale=100)

        nx.draw(combined, pos, edge_color=colors, node_color=node_colors, **options)
        plt.savefig(outfile, format="PNG")

        return combined

    def numberOfEdgesCut(self):
        number_of_edges_cut = fiedler_vector(self.graph) @ laplacian_matrix(self.graph) @ fiedler_vector(self.graph).T

        return number_of_edges_cut


class KernighanLin:
    """
    Divide graph into partitons using Kernighan-Lin algorithm
    :param g: networkX graph
    :return: list of networkX graphs
    """
    def __init__(self, g):
        self.graph = g
        self.partitions = [self.graph]

    def partition(self, number_of_partitions):
        if number_of_partitions > len(self.graph.nodes):
            raise ValueError('Number of partitions cant be larger than number of nodes',
                             '#ofnodes:' + str(len(self.graph.nodes)) + ' < #ofpartitions:' + str(number_of_partitions))
        partitions_list = [self.graph]
        while len(partitions_list) < number_of_partitions:
            graph_to_bisect = partitions_list.pop(0)
            bisections = kernighan_lin.kernighan_lin_bisection(graph_to_bisect)
            bisect_1 = graph_to_bisect.subgraph(bisections[0])
            bisect_2 = graph_to_bisect.subgraph(bisections[1])

            partitions_list.append(subgraph(graph_to_bisect, bisect_1))
            partitions_list.append(subgraph(graph_to_bisect, bisect_2))
        self.partitions = partitions_list
        return self.partitions

    def getRemovedEdges(self):
        removed_edges = []
        edge_list_after_removal = []
        for part in self.partitions:
            for edge in part.edges:
                edge_list_after_removal.append(set(edge))
        for edge in self.graph.edges:
            if set(edge) not in edge_list_after_removal:
                removed_edges.append(edge)
        return removed_edges

    def drawPartitions(self):
        options = {"node_color": "white", "node_size": 100, "linewidths": 0, "width": 0.1, "with_labels": True}
        pos = nx.kamada_kawai_layout(self.graph)

        for n, graph in enumerate(self.partitions):
            nx.draw(graph, pos, **options)
            if n == 1:
                plt.savefig("PartedGraph.png", format="PNG")

    def drawInitialWithColor(self, outfile):
        # Generate colormap
        colors = sns.color_palette(None, len(self.partitions)).as_hex()
        combined = nx.Graph()
        for ind, part in enumerate(self.partitions):
            nx.set_node_attributes(part, colors[ind], 'color')
            combined = nx.compose(combined, part)
        node_colors = nx.get_node_attributes(combined, 'color').values()
        nx.set_edge_attributes(combined, 'b', 'color')

        for edge in self.getRemovedEdges():
            combined.add_edge(*edge, color='r')

        colors = nx.get_edge_attributes(combined, 'color').values()
        options = {"node_size": 300, "linewidths": 0.5, "width": 0.2, "with_labels": True}
        plt.figure(3, figsize=(15, 15))
        pos = nx.kamada_kawai_layout(combined)

        nx.draw(combined, pos, edge_color=colors, node_color=node_colors, **options)
        plt.savefig(outfile, format="PNG")

        return combined


class EdgeBetweennessCentrality:
    """
    Divide graph into partitons using edge betweenness centrality score
    remove edge with highest edge betweenness centrality until a partition is acquired
    :param g: networkX graph
    :return: list of networkX graphs
    """
    def __init__(self, g):
        self.graph = g
        self.partitions = [self.graph]

    def partition(self, number_of_partitions):
        if number_of_partitions > len(self.graph.nodes):
            raise ValueError('Number of partitions cant be larger than number of nodes',
                             '#ofnodes:' + str(len(self.graph.nodes)) + ' < #ofpartitions:' + str(number_of_partitions))
        partitions_list = []
        com_list =[]
        graph_to_part = self.graph
        comp = girvan_newman(graph_to_part)
        for communities in itertools.islice(comp, number_of_partitions):
            com_list.append(communities)

        for node_list in com_list[-1]:
            partitions_list.append(graph_to_part.subgraph(node_list))

        self.partitions = partitions_list
        return self.partitions

    def getRemovedEdges(self):
        removed_edges = []
        edge_list_after_removal = []
        for part in self.partitions:
            for edge in part.edges:
                edge_list_after_removal.append(set(edge))
        for edge in self.graph.edges:
            if set(edge) not in edge_list_after_removal:
                removed_edges.append(edge)
        return removed_edges

    def drawPartitions(self):
        options = {"node_color": "white", "node_size": 100, "linewidths": 0, "width": 0.1, "with_labels": True}
        pos = nx.kamada_kawai_layout(self.graph)

        for n, graph in enumerate(self.partitions):
            nx.draw(graph, pos, **options)
            if n == 1:
                plt.savefig("PartedGraph.png", format="PNG")

    def drawInitialWithColor(self, outfile):
        # Generate colormap
        colors = sns.color_palette(None, len(self.partitions)).as_hex()
        combined = nx.Graph()
        for ind, part in enumerate(self.partitions):
            nx.set_node_attributes(part, colors[ind], 'color')
            combined = nx.compose(combined, part)
        node_colors = nx.get_node_attributes(combined, 'color').values()
        nx.set_edge_attributes(combined, 'b', 'color')

        for edge in self.getRemovedEdges():
            combined.add_edge(*edge, color='r')

        colors = nx.get_edge_attributes(combined, 'color').values()
        options = {"node_size": 300, "linewidths": 0.5, "width": 0.2, "with_labels": True}
        plt.figure(3, figsize=(15, 15))
        pos = nx.kamada_kawai_layout(combined)

        nx.draw(combined, pos, edge_color=colors, node_color=node_colors, **options)
        plt.savefig(outfile, format="PNG")

        return combined
