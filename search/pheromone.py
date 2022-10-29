from collections import defaultdict
from random import choose
def search(start, goal, moves, distance, distance_power=1, pheromones_power=0, evaporation_power=0, reward_power=1):
    pheromones = defaultdict(int)
    swarm = range(ant_count)
    location = [start for ant in swarm]
    tour = [[start] for ant in swarm]

    while True: # need an exit condition
        # The ants go marching. One by One.
        for ant in swarm:
            possiblities = [m for m in moves if m[0] == location[ant]]
            for move in possibilities:
                desirability[move] = pheromones[move]**pheromones_power / distance(move)**distance_power
            next_move = choose(possibilities, weight=desirability)
            location[ant] = next_move[1]
            tour[ant].append(next_edge)
        
        # Update the pheromones.
        for move in pheromones:
            pheromones[move] = (1-evaporation_power) * pheromones[move]
        for ant in swarm:
            if location[ant] == goal:
                # Reward ants who reach the goal.
                tour_length = sum(distance(move) for move in tour[ant])
                for edge in path:
                    pheromone[edge] += reward_power / tour_length[ant]
                # But also make them start again.
                location[ant] = start
                tour = [start]
