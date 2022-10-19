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
