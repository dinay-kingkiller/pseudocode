from random import choose

def search(start, goal, edges, distance, distance_power=1, pheromone_power=0, evaporation_power=0, reward_power=1):
    d
    pheromone = dict.fromkeys(edges, 0)
    pheromone_weight = dict.fromkeys(edges, 1)
    distance_weight = {edge: 1/distance(edge)^distance_power for edge in edges}
    desidict(distance_weight)

    neighbors = dict()
    for current, _ in edges:
        neighbors[current] = [edge for edge in edges if current == edge[0]]
    swarm = range(ant_count)

    while exploring:
        # move ants
        for ant in swarm
            next_edges = neighbors[location[ant]]
            possibilities = [likelihood[edge] for edge in next_edges]
            next_edge = choose(next_edges, weight=possibilities)
            location[ant] = next_edge[1]
            tour[ant].append(next_edge)
            tour_length[ant] += distance[next_edge]
        for edge in edges:
            pheromone[edge] *= 1 - evaporation_power
        for ant in swarm
            if location[ant] != goal:
                continue
            for edge in path:
                pheromone[edge] += deposit_power / tour_length[ant]
            location[ant] = start
            tour = [start]
        for edge in edges:
            pheromone_weight[edge] = pheromone[edge]**pheromone_power
            likelihood[edge] = 
