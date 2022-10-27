from heapdict import heapdict
swarm_size = 500
predict_parameter = 1 #>=1
measure_parameter = 0
def search(start, goal, edges):
    swarm = [start for i in range(swarm_size)]
    for ant in swarm:
        for next_state, next_weight in edges(ant):
            pass
        
        
        
