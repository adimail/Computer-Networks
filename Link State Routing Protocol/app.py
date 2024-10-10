#             .___.__               .__.__   
# _____     __| _/|__| _____ _____  |__|  |  
# \__  \   / __ | |  |/     \\__  \ |  |  |  
#  / __ \_/ /_/ | |  |  Y Y  \/ __ \|  |  |__
# (____  /\____ | |__|__|_|  (____  /__|____/
#      \/      \/          \/     \/         
# 
#     Author: Aditya Godse (https://adimail.github.io)
#     Description: A program to implement link state routing protocol to find a suitable path for transmission.

import heapq

def dijkstra(graph, start_node):
    shortest_path = {node: float('infinity') for node in graph}
    shortest_path[start_node] = 0
    
    priority_queue = [(0, start_node)]
    predecessor = {node: None for node in graph}

    while priority_queue:
        (current_distance, current_node) = heapq.heappop(priority_queue)

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            if distance < shortest_path[neighbor]:
                shortest_path[neighbor] = distance
                predecessor[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return shortest_path, predecessor

def print_path(predecessor, start_node, target_node):
    path = []
    current_node = target_node

    while current_node != start_node:
        path.insert(0, current_node)
        current_node = predecessor[current_node]
    
    path.insert(0, start_node)
    print(f"Shortest path from {start_node} to {target_node}: {' -> '.join(path)}")

# Network topology as a graph (router connections and their link costs)
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

if __name__ == "__main__":
    start_router = 'A' 
    shortest_paths, predecessors = dijkstra(graph, start_router)

    # Print the shortest path to all other routers
    for router in graph:
        if router != start_router:
            print(f"Shortest distance from {start_router} to {router}: {shortest_paths[router]}")
            print_path(predecessors, start_router, router)
            print('---')
