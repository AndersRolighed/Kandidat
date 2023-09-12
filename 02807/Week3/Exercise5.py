def parse_adjacency_list(line):
    node, adjacent_nodes = line.strip().split(' : ')
    return int(node), set(map(int, adjacent_nodes.split(',')))

def find_common_nodes(adjacency_list):
    common_nodes = {}

    for node1, adjacent1 in adjacency_list.items():
        for node2, adjacent2 in adjacency_list.items():
            if node1 < node2:
                common = adjacent1.intersection(adjacent2)
                common_nodes[(node1, node2)] = common

    return common_nodes

# Read the graph file
with open('data/friends.txt', 'r') as file:
    lines = file.readlines()
    adjacency_list = {parse_adjacency_list(line)[0]: parse_adjacency_list(line)[1] for line in lines}

common_nodes = find_common_nodes(adjacency_list)

for (node1, node2), common in common_nodes.items():
    print(f'Nodes {node1} and {node2} have the following nodes in common: {common}')
