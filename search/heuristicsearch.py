#heuristicsearch.py
from collections import defaultdict
from heapdict import heapdict
from math import inf
def search(start, goal, heuristic):
    """
    Finds the optimal path between initial_node and goal_node optimally given a heuristic.
    """
    
    came_from = dict()
    path_cost = defaultdict(lambda : inf)
    
    # Setup queue.
    open_nodes = heapdict()
    open_nodes[start_node] = 0
    best_cost[start_node] = 0
    
    while open_nodes:
        current, _ = open_nodes.popitem()
        if current == goal:
            # Start at the goal and traverse back to the start.
            traversed = goal
            path = [traversed]
            while traversed != start:
                traversed = came_from[traversed]
                path = [traversed] + path
            return path
        for neighbor, edge_weight in current.neighbors():
            cost_thru_current = best_cost[opened_node] + edge_weight 
            if cost_thru_current < best_cost[neighbor]:
                best_cost[neighbor] = cost_thru_current
                open_nodes[neighbor] = best_cost[neighbor] + heuristic(neighbor)
    else:
        return None
    
