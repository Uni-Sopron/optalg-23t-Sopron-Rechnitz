import random
import json
import os

HU_NODES_NUM = 10
AT_NODES_NUM = 5
NODES = HU_NODES_NUM + AT_NODES_NUM
MAX_EDGES_NUM = (NODES * (NODES - 1)) // 2
RANDOM_EDGES_NUM = random.randint(1, MAX_EDGES_NUM)
MIN_DISTANCE, MAX_DISTANCE = 1, 25
OUTPUT_DIR = "./python_test/"

def make_nodes(hu_number, at_number):
    nodes = [_ for _ in range(hu_number + at_number)]
    hu_nodes = []
    at_nodes = []

    for _ in range(hu_number):
        node = random.choice(nodes)
        hu_nodes.append(node)
        nodes.remove(node)

    for _ in range(at_number):
        node = random.choice(nodes)
        at_nodes.append(node)
        nodes.remove(node)

    return hu_nodes, at_nodes

hu_nodes, at_nodes = make_nodes(HU_NODES_NUM, AT_NODES_NUM)
all_nodes = hu_nodes + at_nodes
# print('hu_nodes: ', hu_nodes)
# print('at_nodes: ', at_nodes)

def exist_edge(edges, node1, node2):
    "Check if edge exist betweem node1 and node2."
    for edge in edges:
        if (edge[0] == node1 and edge[1] == node2) or (edge[0] == node2 and edge[1] == node1):
            return True
    return False

def make_edges(edge_number, nodes_list):
    counter = 0
    roads = []

    while counter != edge_number:
        node1, node2 = random.choice(nodes_list), random.choice(nodes_list)
        if node1 != node2 and not exist_edge(roads, node1, node2):
            roads.append((node1, node2, random.randint(MIN_DISTANCE, MAX_DISTANCE)))
            counter += 1

    return roads

# edges = make_edges(5, all_nodes)
edges = make_edges(RANDOM_EDGES_NUM, all_nodes)
# print(edges)

def make_graph():
    graph = {
        "hungarian": hu_nodes,
        "austrian": at_nodes, 
        "roads": edges
    }
    return graph

graph = make_graph()
# print(graph)

def output_to_json():
    os.makedirs(os.path.dirname(OUTPUT_DIR), exist_ok=True)
    path = "{dir}{filename}.json".format(dir=OUTPUT_DIR, filename=str(NODES)+"nodes" + str(RANDOM_EDGES_NUM) +"edges")
    with open(path, 'w') as file:
        json.dump(graph, file)

if __name__ == "__main__":
    output_to_json()