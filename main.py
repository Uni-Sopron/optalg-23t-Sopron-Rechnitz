"""
Sopronból Rechnitzbe szeretnénk eljutni a legrövidebb úton, 
de az osztrák határőrök lekapcsolnak gyanús tevékenységért, 
ha egy nap egy irányba többször is átlépünk a határon.
"""

import sys
import json

# import graph from json file
# path = "./python_test/15nodes39edges.json"
path = "./python_test/sample.json"
with open(path, 'r') as file:
    GRAPH = json.load(file)

def get_hungarian_nodes():
    "Returns the hungarian nodes of the graph."
    return GRAPH["hungarian"]

def get_austrian_nodes():
    "Returns the austrian nodes of the graph."
    return GRAPH["austrian"]

def get_nodes():
    "Returns all nodes of the graph."
    return GRAPH["hungarian"] + GRAPH["austrian"]

def get_edges():
    "Returns the edges of the graph."
    return GRAPH["roads"]

def get_neighbours(node):
    "Returns the neighbors of a node."
    neighbours = []
    edges = get_edges()
    for edge in edges:
        if edge[0] == node:
            neighbours.append(edge[1])
                
        elif edge[1] == node:
            neighbours.append(edge[0])
                
    return neighbours

  
def get_distance(node1, node2):
    "Returns the distance of an edge between two nodes."
    edges = get_edges()
    for edge in edges:
        if (edge[0] == node1 and edge[1] == node2) or (edge[0] == node2 and edge[1] == node1):
            return edge[2]
        
# print(get_neighbours(1))
# print(get_distance(9,0))
# print(get_distance(0,9))

HUNGARIAN_NODES = get_hungarian_nodes()
AUSTRIAN_NODES = get_austrian_nodes()

def cross_border(node1, node2):
    "Check whether two nodes are crossing border or not. Crossing means one of them is in Austria, and the other is in Hungary."
    return (node1 in HUNGARIAN_NODES and node2 in AUSTRIAN_NODES) or (node1 in AUSTRIAN_NODES and node2 in HUNGARIAN_NODES)

# print(cross_border(0,4)) # True
# print(cross_border(2,3)) # False
# print(cross_border(7,9)) # False
 
def dijkstra_algorithm(start_node):
    "Run the dijkstra algorithm considering that maximum one crossing is allowed."
    unvisited_nodes = get_nodes()
    shortest_path = {}  # the cost of visiting each node and update it as we move along the graph
    previous_nodes = {}  # the shortest known path to a node found so far
    crossed_border = {}  # whether a border has been crossed to reach a node

    max_value = sys.maxsize  # initialize the "infinity" value of the unvisited nodes
    for node in unvisited_nodes:
        shortest_path[node] = max_value
        crossed_border[node] = False
    shortest_path[start_node] = 0  # initialize the starting node's value with 0

    while unvisited_nodes:  # The algorithm executes until we visit all nodes
        # The code block below finds the node with the lowest score
        current_min_node = None
        for node in unvisited_nodes:
            if current_min_node is None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        # The code block below retrieves the current node's neighbors and updates their distances
        neighbors = get_neighbours(current_min_node)
        for neighbor in neighbors:
            if not cross_border(current_min_node, neighbor) or not crossed_border[current_min_node]:
                tentative_value = shortest_path[current_min_node] + get_distance(current_min_node, neighbor)
                if tentative_value < shortest_path[neighbor]:
                    shortest_path[neighbor] = tentative_value
                    crossed_border[neighbor] = crossed_border[current_min_node] or cross_border(current_min_node, neighbor)
                    # update the best path to the current node
                    previous_nodes[neighbor] = current_min_node

        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)

    return crossed_border, previous_nodes, shortest_path


def print_result(crossed_border, previous_nodes, shortest_path, start_node, target_node):
    "Print the shortest path from start node to destination node, it's distance and whether crossing happened or not."
    if target_node not in previous_nodes:
        print("No path exists from the start node to the destination node or we would cross the border multiple times.")
        return
    
    path = []
    node = target_node
    crossed = crossed_border[target_node]

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]
 
    # Add the start node
    path.append(start_node)
    
    if crossed:
        print("Once we crossed the border.")
    else:
        print("No border crossing happened.")
    
    print("The shortest path has a value of {}.".format(shortest_path[target_node]))
    print(" -> ".join(str(city) for city in reversed(path)))

START = 0
DESTINATION = 8

crossed_border, previous_nodes, shortest_path = dijkstra_algorithm(start_node=START)
# print(crossed_border)
# print(previous_nodes)
# print(shortest_path)
print_result(crossed_border, previous_nodes, shortest_path, start_node=START, target_node=DESTINATION)