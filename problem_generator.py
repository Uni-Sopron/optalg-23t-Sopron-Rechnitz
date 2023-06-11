import os
import json
import random

OUTPUT_DIR = "./test/"
INSTANCE_COUNT = 15
WEIGHT_MIN, WEIGHT_MAX = 1, 10
MIN_HU_VERTICES = 2
NUM_VERTICES = 10

def generate_graph(num_vertices):
    graph = [[] for _ in range(num_vertices)]
    
    for vertex1 in range(num_vertices):
        num_edges = random.randint(1, num_vertices - 1)
        edges = random.sample(range(num_vertices), num_edges)
        
        for vertex2 in edges:
            weight = random.randint(WEIGHT_MIN, WEIGHT_MAX)
            graph[vertex1].append((vertex2, weight))
            graph[vertex2].append((vertex1, weight))
    
    return graph

def generate_hu_vertices(num_vertices):
    num_hu_vertices = random.randint(MIN_HU_VERTICES, num_vertices-1)
    hu_vertices = random.sample(range(num_vertices), num_hu_vertices)
    return set(hu_vertices)


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    for instance in range(INSTANCE_COUNT):
        graph_data = {"graph": generate_graph(NUM_VERTICES), "hu": list(generate_hu_vertices(NUM_VERTICES))}
        
        with open(f'{OUTPUT_DIR}/{instance+1:03}.json', 'w') as file:
            json.dump(graph_data, file)
