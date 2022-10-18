from MinHeap import MinHeap
from Graph import Graph
def aStar(start, goal, heuristic):
	cameFrom = dict()
	distance = dict()
	queue = MinHeap(start)
	distance[start] = 0
	for node in queue:
		if node == goal:
			return pathTo(start, goal, cameFrom)
		else:
			for neighbor, weight in node.neighbors:
				newDistance = distance[node] + weight
				newValue = newDistance + heuristic(neighbor)
				if neighbor not in queue:
					queue.insert(neighbor, newValue)
					cameFrom[neighbor] = node
					distance[neighbor] = newDistance
				elif queue[neighbor] > newValue:
					queue[neighbor] = newValue
					cameFrom[neighbor] = node
					distance[neighbor] = newDistance
def dijkstra(start, goal):
	cameFrom = dict() 
	queue = MinHeap(start, 0)
	for node in queue:
		if node == goal:
			return pathTo(start, goal, cameFrom)
		else:
			for neighbor, weight in node.neighbors:
				pathDistance = queue[node] + weight
				if neighbor not in queue:
					queue.insert(neighbor, pathDistance)
					cameFrom[neighbor] = node
				elif queue[neighbor] > pathDistance
					cameFrom[neighbor] = node
def goalDistance(goal):
	heuristic = dict()
	queue = MinHeap()
	heuristic[goal] = 0
	queue.insert(goal, heuristic[goal])
	for node in queue:
		for neighbor, weight in node.neighbors:
			if neighbor not in queue:
				heuristic[neighbor] = heuristic[node] + 1
				queue.insert(neighbor, heuristic[neighbor])
	return lambda node: heuristic[node]
def pathTo(start, goal, cameFrom):
	"""Unpacks cameFrom dictionary/tree"""
	path = [goal]
	while start != path[0]:
		path = [cameFrom[path[0]]] + path
	return path
if __name__=="__main__":
	nodes = Graph([
		[(1,4),(7,8)],#0
		[(0,4),(2,8),(7,11)],#1
		[(1,8),(3,7),(5,4),(8,2)],#2
		[(2,7),(4,10),(5,14)],#3
		[(3,9),(5,10)],#4
		[(2,4),(3,14),(4,10),(6,2)],#5
		[(5,2),(7,1),(8,6)],#6
		[(0,8),(1,11),(6,1),(8,7)],#7
		[(2,2),(6,6),(7,7)],#8
		])
	start = nodes[0]
	goal = nodes[4]
	heuristic = goalDistance(goal)
	for node in nodes:
		print(dijkstra(start, node))
		print(aStar(start, node, heuristic))
