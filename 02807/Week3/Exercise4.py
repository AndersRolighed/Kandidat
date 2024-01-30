def read_graph_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        edges = [tuple(map(int, line.strip().split())) for line in lines]
        return edges

def calculate_degrees(edges):
    degrees = {}

    for edge in edges:
        for node in edge:
            degrees[node] = degrees.get(node, 0) + 1

    return degrees

# Replace 'graph_file.txt' with the actual path of your graph file.
graph_file_path = 'data/eulerGraphs3.txt'
edges = read_graph_file(graph_file_path)

if edges:
    degrees = calculate_degrees(edges)

    for node, degree in degrees.items():
        print(f'Node {node} has degree {degree}')
else:
    print("Error: No edges found in the file.")
