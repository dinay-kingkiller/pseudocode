from collections import defaultdict
from random import choose


def search(start, goal, moves, distance, distance_power=1, pheromones_power=0, evaporation_power=0, reward_power=1):
    """
    search tries to constantly improve an optimal path from start to goal.

    Note: does not currently return anything or halt. It will run forever until broken.

    Arguments:
    start - the initial vertex of a graph
    goal - the vertex on the other side of the path
    moves - an iterable of tuples (current, neighbor) all possible moves within the graph
    distance - a map: move -> cost of making that move
    distance_power (>=1, default=1) - higher values will force ants to try easy moves
    pheromones_power (>=0, default=0) - higher values will force ants to try their favorite moves
    evaporation_power (>=0 and <=1, default=0) - how long should pheromones stay on the edges:
        0 -> pheromones never leave, 1 -> pheromones only affect paths for a single round 
    reward_power (default=1) - how much pheromone is dropped on reaching a goal
    """
    pheromones = defaultdict(int)
    swarm = range(ant_count)
    location = [start for ant in swarm]
    tour = [[start] for ant in swarm]

    while True:  # need an exit condition
        # The ants go marching. One by One.
        for ant in swarm:
            possiblities = [m for m in moves if m[0] == location[ant]]
            for move in possibilities:
                desirability[move] = pheromones[move]**pheromones_power / \
                    distance(move)**distance_power
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
                    pheromones[edge] += reward_power / tour_length[ant]
                # But also make them start again.
                location[ant] = start
                tour = [start]
