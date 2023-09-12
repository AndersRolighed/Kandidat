def read_graph_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        edges = [tuple(map(int, line.strip().split())) for line in lines]
        return edges

def count_triangles(edges):
    graph = {}
    for edge in edges:
        u, v = edge
        if u not in graph:
            graph[u] = set()
        if v not in graph:
            graph[v] = set()
        graph[u].add(v)
        graph[v].add(u)

    num_triangles = 0
    for u in graph:
        for v in graph[u]:
            for w in graph[v]:
                if w in graph[u]:
                    num_triangles += 1

    return num_triangles // 6  # Each triangle is counted 6 times (3! permutations)

# Replace 'graph_file.txt' with the actual path of your graph file.
graph_file_path = 'data/roadnet.txt'
edges = read_graph_file(graph_file_path)

if edges:
    num_triangles = count_triangles(edges)
    print(f'Number of triangles in the graph: {num_triangles}')
else:
    print("Error: No edges found in the file.")
