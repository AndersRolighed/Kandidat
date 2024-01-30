import networkx as nx
from itertools import combinations


def edge_betweenness_centrality(G):
    edge_centrality = {edge: 0 for edge in G.edges()}
    for source in G.nodes():
        for target in G.nodes():
            if source != target:
                shortest_paths = nx.all_shortest_paths(G, source=source, target=target)
                
                temp_edge_centrality = dict()
                n_of_paths = 0
                for path in shortest_paths:
                    if len(path) > 0:
                        n_of_paths += 1
                        for i in range(len(path)-1):
                            edge = (min(path[i], path[i+1]), max(path[i], path[i+1]))
                            try:
                                temp_edge_centrality[edge] += 1
                            except KeyError:
                                temp_edge_centrality[edge] = 1
                for edge in temp_edge_centrality:
                    temp_edge_centrality[edge] /= n_of_paths*2*len(list(combinations(G.nodes(),2)))
                    edge_centrality[edge] += temp_edge_centrality[edge]
    return edge_centrality

G = nx.karate_club_graph()

print(len(G.edges()))
print(len(G.nodes()))
#G = nx.Graph()
#G.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4), (4, 5)])
edge_betweenness = edge_betweenness_centrality(G)

for edge, centrality in edge_betweenness.items():
    print(f"Edge {edge}: {centrality}")


NX_edge_betweenness = nx.edge_betweenness_centrality(G)
for edge, centrality in NX_edge_betweenness.items():
    print(f"Edge {edge}: {centrality}")

