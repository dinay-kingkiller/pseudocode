from collections import defaultdict
from heapdict import heapdict
from random import choose
distance_power = 1 #>=1
pheromone_power = 0 #>=0
reward_power = 0
decay_power = 0
def search(start, goal, edges, distance, total_ants):
    """
    edges: state -> next_state
    """
    weighted_pheromone = defaultdict(int)
    ant_count = defaultdict(int)
    vertices = [start]
    ant_count[start] = total_ants
    for _ in range(10):
        for current in vertices:
            if ant_count[current] == 0:
                continue
            likelihood = [0] * len(edges)
            for i, neighbor in enumerate(edges(current)):
                if (current, neighbor) not in weighted_distance:
                    weighted_distance[(current, neighbor)] = 1/distance[(current, neighbor)]**distance_power
                likelihood[i] = weighted_pheromone[(ant, neighbor)] * weighted_distance[(ant, neighbor)])
            next_vertices = choose(edges(current), weight=likelihood, k=)
            for neighbor in next_vertices:
                ant_count[neighbor] += 1
            ant_count[current] = 0
    ##
        for ant in swarm:
            path[ant].append(current)
            likelihood = []
            for neighbor, distance in edges(current):
                if (current, neighbor) not in weighted_distance:
                    weighted_distance[(current, neighbor)] = 1/distance**distance_power
                likelihood.append(weighted_pheromone[(ant, neighbor)] * weighted_distance[(ant, neighbor)])
            next_node = choose(edges(ant), weight=likelihood)
        
        # ants move
        # ants talk
        
            
            
        
        
        
