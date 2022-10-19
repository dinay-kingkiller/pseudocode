#heuristicsearch.py
from collections import defaultdict
from math import inf
from heapdict import heapdict
def search(start, goal, edges, heuristic=lambda x: 0):
    """
    search finds the best path between the start and goal. If there is
    no path, return None.
    
    Keyword Arguments:
    start - the initial vertex of a graph
    goal - the vertex on the other side of the path
    edges - a map to describe the graph edges. It should return a list
        of tuples (neighbor, weight)
    heuristic - a function to aid with optimally opening vertices:
        a heuristic should be admissible:
            best_cost[node] + heuristic(node) < best_cost[goal]
        where best_cost is the sum of the weights from start.
        A heuristic is consistent if for every vertex and every
        (neighbor, weight) in edges(vertex):
                heuristic(node) >= heuristic(neighbor) + weight
        If a heuristic is also consistent, search will find the optimal
        path without expanding a vertex more than once.
    """
    # came_from: vertex -> previous vertex of best path to vertex
    came_from = dict()
    # path_cost: vertex -> sum of edge weights of best path to vertex
    path_cost = defaultdict(lambda: inf)
    # open_vertices: vertex -> priority of that vertex
    open_vertices = heapdict()
    
    # Add the start vertex to the queue
    open_vertices[start] = 0
    path_cost[start] = 0
    
    while open_vertices:
        current, priority = open_vertices.popitem()
        if current == goal:
            # Start at the goal and traverse back to the start.
            traversed = goal
            path = [traversed]
            while traversed != start:
                traversed = came_from[traversed]
                path = [traversed] + path
            return path
        for neighbor, weight in edges(current):
            # current_cost is the distance to neighbor through current.
            current_cost = path_cost[opened_node] + weight 
            if current_cost < path_cost[neighbor]:
                best_cost[neighbor] = current_cost
                open_vertices[neighbor] = current_cost + heuristic(neighbor)
    else:
        # If the queue runs out of vertices, return no path.
        return None
