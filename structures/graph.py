# Graph.py
class Graph:
    def __init__(self, adjacencyList):
        self.buildFromAdjacencyList(adjacencyList)

    def __getitem__(self,  key):
        return self.nodes[key]

    def buildFromAdjacencyList(self, adjacencyList):
        """Creates a list of nodes from an Adjacency List"""
        self.nodes = [Node(index)
                      for index, neighbor in enumerate(adjacencyList)]
        for node, neighbors in zip(self.nodes, adjacencyList):
            for index, weight in neighbors:
                node.addEdge(self.nodes[index], weight)


class Node:
    """
    Node Class
    Graph formulation where nodes know their neighbors
    """

    def __init__(self, label):
        self.label = label
        self.neighbors = list()

    def __eq__(self, other):
        pass

    def __str__(self):
        return str(self.label)

    def __repr__(self):
        return repr(self.label)

    def addEdge(self, node, weight):
        self.neighbors.append((node, weight))


class TaxiNode(Node):
    def __init__(self, coordinate):
        self.label = coordinates

    def neighbors(self):
        neighborCoordinates = [[(coordinate if ind1 != ind2 else coordinate + inc)
                                for ind1, coordinate in enumerate(coordinates)]
                               for ind2, _ in enumerate(coordinates)
                               for inc in [-1, 1]]
