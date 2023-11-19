from typing import List;
import os;
from array import *
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt  # Optional, for visualizati


def read_input(file_name):
    current_path = os.path.dirname(__file__)
    lines = []
    try:
        with open(os.path.join(current_path, file_name), 'r') as file:
            for line in file:
                lines.append(line.strip())  # Remove any leading or trailing whitespace
    except Exception as e:
        print(f"An error occurred: {e}")
    return lines

def convert_map(lines):
    map = []

    for line_idx, line in enumerate(lines):
        current_line =  []
        for ele_idx, element in enumerate(line):
            if element >= 'a' and element <= 'z':
                element = ord(element) - ord('a')
            current_line.append(element)
        map.append(current_line)
    return map            


def create_directional_graph(num_nodes, connections):
    boolean_map = np.full((num_nodes, num_nodes), False)
    
    for connection in connections:
        from_node, to_node = connection
        boolean_map[from_node, to_node] = True  # Set True for directional connection
        
    return boolean_map


def is_climbable(node_from, node_to) -> bool:
    if node_from == 'S' or node_to == 'S' or node_from == 'E' or node_to == 'E' : 
        return True
    if node_from < node_to or node_from - node_to == 1: #can go down and 1 step up
        return True
    return False


def create_directional_tuples(input_data):
    #input data should be list(list())
    #iterate throgh lines
    len_cols = len(input_data[0])
    len_rows = len(input_data)

    directional_tuples = []
    for row_idx, row in enumerate(input_data):
        for col_idx, element in enumerate(row):

            if row_idx != 0:#below
                if is_climbable(element,input_data[row_idx - 1][col_idx]):
                    directional_tuples.append((row_idx * len_cols + col_idx, row_idx - 1 * len_cols + col_idx))
            if row_idx != len_rows - 1:#above
                if is_climbable(element,input_data[row_idx + 1][col_idx]):
                    directional_tuples.append((row_idx * len_cols + col_idx, row_idx + 1 * len_cols + col_idx))
            if col_idx != len_cols - 1:#left
                if is_climbable(element,input_data[row_idx][col_idx + 1]):
                    directional_tuples.append((row_idx * len_cols + col_idx, row_idx * len_cols + col_idx + 1))
            if col_idx != 0:#right
                if is_climbable(element,input_data[row_idx][col_idx - 1]):
                    directional_tuples.append((row_idx * len_cols + col_idx, row_idx * len_cols + col_idx - 1))
    return directional_tuples
                

def dijkstra_algorithm(graph, source):
    num_of_nodes = len(graph)
    visited = np.full(num_of_nodes, False)
    previous = np.full(num_of_nodes, None)
    distances = np.full(num_of_nodes, np.inf)
    distances[source] = 0

    for _ in range(num_of_nodes):
        current = np.argmin(distances * ~visited)
        visited[current] = True

        for neighbor in range(num_of_nodes):
            if not visited[neighbor] and graph[current, neighbor]:
                new_distance = distances[current] + 1  # Assuming all edges have weight 1
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
    
    return distances
                

def dijkstra_boolean_map(boolean_map, source):
    num_nodes = boolean_map.shape[0]
    distances = np.full(num_nodes, np.inf)
    visited = np.full(num_nodes, False)
    distances[source] = 0

    for _ in range(num_nodes):
        current = np.argmin(distances * ~visited)
        visited[current] = True

        for neighbor in range(num_nodes):
            if not visited[neighbor] and boolean_map[current, neighbor]:
                new_distance = distances[current] + 1  # Assuming all edges have weight 1
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance

    return distances

"""

 1  function Dijkstra(Graph, source):
 2      
 3      for each vertex v in Graph.Vertices:
 4          dist[v] ← INFINITY
 5          prev[v] ← UNDEFINED
 6          add v to Q
 7      dist[source] ← 0
 8      
 9      while Q is not empty:
10          u ← vertex in Q with min dist[u]
11          remove u from Q
12          
13          for each neighbor v of u still in Q:
14              alt ← dist[u] + Graph.Edges(u, v)
15              if alt < dist[v]:
16                  dist[v] ← alt
17                  prev[v] ← u
18
19      return dist[], prev[]

"""

lines = read_input("text_input.txt")
map = convert_map(lines)

dir_tuples = create_directional_tuples(map)

adjacency_matrix =  create_directional_graph(len(dir_tuples), dir_tuples)
for line in adjacency_matrix:
    print(line)
    
ret_val = dijkstra_algorithm(adjacency_matrix, 0)
for line in ret_val:
    print(line)

# Create a directed graph from the adjacency matrix
G = nx.DiGraph()

num_nodes = len(adjacency_matrix)
G.add_nodes_from(range(num_nodes))  # Add nodes to the graph

# Add directed edges based on the adjacency matrix
for i in range(num_nodes):
    for j in range(num_nodes):
        if adjacency_matrix[i][j]:
            G.add_edge(i, j)

# Visualize the graph (optional)
pos = nx.spring_layout(G)  # Position nodes using Fruchterman-Reingold force-directed algorithm
nx.draw(G, pos, with_labels=True, node_size=500, node_color='skyblue', font_weight='bold', font_size=10, arrows=True)
plt.show()