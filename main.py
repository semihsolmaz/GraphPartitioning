from networkx.algorithms import community
from networkx.linalg.laplacianmatrix import laplacian_matrix
from networkx.linalg.algebraicconnectivity import algebraic_connectivity, fiedler_vector, spectral_ordering
from networkx.linalg.spectrum import laplacian_spectrum
import networkx as nx

g = nx.karate_club_graph()

laplacian_g = laplacian_matrix(g)
laplacian_spectrum_g = laplacian_spectrum(g)
algebraic_con_g = algebraic_connectivity(g)
fiedler_vector_g = fiedler_vector(g)
spectral_ordering_g = spectral_ordering(g)
print(laplacian_g)
print(laplacian_spectrum_g)
print(algebraic_con_g)
print(g.nodes)
print(fiedler_vector_g)
for i in spectral_ordering_g:
    print(fiedler_vector_g[i])
# print(spectral_ordering_g[:18])
# print(spectral_ordering_g[18:])

