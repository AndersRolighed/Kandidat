import networkx as nx
G = nx.karate_club_graph()
print(G.edges)
shortest_path = nx.all_shortest_paths(G, 8, 1)
print(shortest_path)
for path in shortest_path:
    print(path)
    for i in range(len(path)-1):
        edge = (min(path[i], path[i+1]), max(path[i], path[i+1]))
        print(edge)