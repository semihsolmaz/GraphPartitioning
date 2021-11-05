import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms import community
from networkx.convert_matrix import to_numpy_matrix
from networkx.linalg.laplacianmatrix import laplacian_matrix
from networkx.linalg.algebraicconnectivity import algebraic_connectivity, fiedler_vector, spectral_ordering
from networkx.linalg.spectrum import laplacian_spectrum
import networkx as nx


# g = nx.karate_club_graph()
g = nx.read_edgelist('soc-karate.csv', delimiter=' ', nodetype=str)
laplacian_g = laplacian_matrix(g)
laplacian_spectrum_g = laplacian_spectrum(g)
algebraic_con_g = algebraic_connectivity(g)
fiedler_vector_g = fiedler_vector(g)
spectral_ordering_g = spectral_ordering(g)
# print(laplacian_g)
print(laplacian_spectrum_g)
print(algebraic_con_g)
print(spectral_ordering_g)
print(fiedler_vector_g)
print(sum(fiedler_vector_g))
# for i in spectral_ordering_g:
#     print(fiedler_vector_g[i])
# print(spectral_ordering_g[:18])
# print(spectral_ordering_g[18:])
number_of_edges_cut = fiedler_vector(g).dot(laplacian_matrix(g).todense()).dot(fiedler_vector(g)[:, np.newaxis])

print(number_of_edges_cut)


options = {"node_color": "white", "node_size": 100, "linewidths": 0, "width": 0.1, "with_labels": True}
pos = nx.spring_layout(g, seed=34)

nx.draw(g, pos, **options)
plt.savefig("Graph.png", format="PNG")

