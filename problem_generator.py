import os
import json
import random

OUTPUT_DIR = "./test/"
INSTANCE_COUNT = 15
WEIGHT_MIN, WEIGHT_MAX = 1, 10
HU_N = 4
NUM_VERTICES = 10

def generate_graph(num_vertices):
    graph = []
    for i in range(num_vertices):
        neighbors = []
        for j in range(num_vertices):
            if i != j and random.random() < 0.5:
                weight = random.randint(WEIGHT_MIN, WEIGHT_MAX)
                neighbors.append([j, weight])
        graph.append(neighbors)
    return graph


def generate_hu_vertices(num_vertices, hu_n):
    hu_vertices = random.sample(range(num_vertices), hu_n)
    return hu_vertices

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    for instance in range(INSTANCE_COUNT):
        graph_data = {"graph": generate_graph(NUM_VERTICES), "hu": list(generate_hu_vertices(NUM_VERTICES, HU_N))}
        
        with open(f'{OUTPUT_DIR}/{instance+1:03}.json', 'w') as file:
            json.dump(graph_data, file)
