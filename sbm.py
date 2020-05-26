import networkx as nx
from scipy.special import comb

class SBM():

    def __init__(self, n, p, q, seed=0):
        self.n = n
        self.p = p
        self.q = q
        self.g = nx.generators.community.stochastic_block_model(
            [int(self.n / 2), int(self.n / 2)],
            [[p, q], [q, p]],
            seed=seed)

    def is_bichromatic(self, u, v):
        return (u < self.n / 2) != (v < self.n / 2)

    def get_bichromatic_fraction(self):
        bichromatic = 0
        for (x, y) in self.g.edges():
            if self.is_bichromatic(x, y):
                bichromatic += 1
        return bichromatic / len(self.g.edges())

    def is_local_bridge(self, u, v):
        return not set(self.g.neighbors(u)).intersection(set(self.g.neighbors(v)))

    def count_local_bridges(self):
        monochromatic, bichromatic = 0, 0
        for (u, v) in self.g.edges():
            if self.is_local_bridge(u, v):
                if self.is_bichromatic(u, v):
                    bichromatic += 1
                else:
                    monochromatic += 1
        return monochromatic, bichromatic
    
    def _count_possible_edges(self, local_bridge):
        monochromatic, bichromatic = 0, 0
        for u in range(self.n):
            for v in range(u+1, self.n):
                if not self.g.has_edge(u, v) and \
                     (self.is_local_bridge(u, v) == local_bridge):
                    if self.is_bichromatic(u, v):
                        bichromatic += 1
                    else:
                        monochromatic += 1
        return monochromatic, bichromatic

    def count_possible_local_bridges(self):
        return self._count_possible_edges(local_bridge=True)
    
    def count_possible_closures(self):
        return self._count_possible_edges(local_bridge=False)

    def count_wedges(self):
        monochromatic, bichromatic = 0, 0
        for v in self.g.nodes():
            sorted_neighbors = sorted(self.g.neighbors(v))
            for i in range(len(sorted_neighbors)):
                for j in range(i + 1, len(sorted_neighbors)):
                    if not self.g.has_edge(sorted_neighbors[i], sorted_neighbors[j]):
                        if self.is_bichromatic(sorted_neighbors[i], sorted_neighbors[j]):
                            bichromatic += 1
                        else:
                            monochromatic += 1
        return monochromatic, bichromatic

    def predicted_monochromatic_wedges(self):
        return 3 * 2 * comb(self.n/2, 3) * self.p**2 * (1-self.p) \
            + self.n * comb(self.n/2, 2) * self.q**2 * (1-self.p)
    
    def predicted_bichromatic_wedges(self):
        return 2 * self.n * comb(self.n/2, 2) * self.p * self.q * (1-self.q)

    def predicted_monochromatic_local_bridges(self):
        return 2 * (1-self.p) * comb(self.n/2, 2) - self.predicted_monochromatic_wedges()

    def predicted_bichromatic_local_bridges(self):
        return (1-self.q) * (self.n/2) ** 2 - self.predicted_bichromatic_wedges()