"""
Sopronból Rechnitzbe szeretnénk eljutni a legrövidebb úton, 
de az osztrák határőrök lekapcsolnak gyanús tevékenységért, 
ha egy nap egy irányba többször is átlépünk a határon.
"""

import sys

g = {
    "hungarian" : [0, 1, 2, 3, 8], # nodes in Hungary
    "austrian" : [4, 5, 6, 7, 9], # nodes in Austria
    "roads": [ # (node1, node2, distance)
        (0, 1, 5), # equal to (1, 0, 5)
        (0, 9, 40),
        (0, 8, 11),
        (1, 2, 1),
        (2, 4, 2),
        (1, 4, 10),
        (4, 8, 15),
        (8, 9, 2)
    ],
    
    "roads2" :  {
        0: [(1,5), (9,40), (8, 11)] # neighbours of 0, (node2, distance)
    }
}

def get_hungarian_nodes():
    "Returns the hungarian nodes of the graph."
    return g["hungarian"]

def get_austrian_nodes():
    "Returns the austrian nodes of the graph."
    return g["austrian"]

def get_nodes():
    "Returns all nodes of the graph."
    return g["hungarian"] + g["austrian"]

def get_edges():
    "Returns the edges of the graph."
    return g["roads"]

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

def dijkstra_algorithm(start_node):
    unvisited_nodes = get_nodes()
    shortest_path = {} # the cost of visiting each node and update it as we move along the graph 
    previous_nodes = {} # the shortest known path to a node found so far
 
    max_value = sys.maxsize # initialize the "infinity" value of the unvisited nodes
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    shortest_path[start_node] = 0 # initialize the starting node's value with 0  
    
    while unvisited_nodes: # The algorithm executes until we visit all nodes
        # The code block below finds the node with the lowest score
        current_min_node = None
        for node in unvisited_nodes:
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
                
        # The code block below retrieves the current node's neighbors and updates their distances
        neighbors = get_neighbours(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + get_distance(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # update the best path to the current node
                previous_nodes[neighbor] = current_min_node
 
        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)
    
    return previous_nodes, shortest_path

def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node
    
    while node != start_node:
        path.append(node)
        node = previous_nodes[node]
 
    # Add the start node
    path.append(start_node)
    
    print("The shortest path has a value of {}.".format(shortest_path[target_node]))
    print(" -> ".join(str(city) for city in reversed(path)))

START = 0
DESTINATION = 4
previous_nodes, shortest_path = dijkstra_algorithm(start_node=START)
# print(previous_nodes)
# print(shortest_path)
print_result(previous_nodes, shortest_path, start_node=START, target_node=DESTINATION)