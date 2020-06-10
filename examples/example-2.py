import coopy
import random

from coopy import neg

class Node:

    def __init__(self):
        self._color = coopy.symbolic_int()

    @property
    def valid(self):
        color = self._color
        return ((color == 0) | (color == 1) | (color == 2))

    def same_color_as(self, other):
        return self._color == other._color

class Edge:

    def __init__(self, a, b):
        self._a = a
        self._b = b

    @property
    def valid(self):
        return neg(self._a.same_color_as(self._b))

class Graph:

    def __init__(self, nodes, edges):
        self._nodes = nodes
        self._edges = edges

    @property
    def valid(self):
        # Assert that nodes are valid.
        nodes_valid = coopy.all([node.valid for node in self._nodes])
        # Assert that edges are valid.
        edges_valid = coopy.all([edge.valid for edge in self._edges])
        # Both conditions must be met for the graph to be valid.
        return nodes_valid & edges_valid

# Instantiate some nodes.
N = 10
nodes = [Node() for i in range(N)]

# Connect nodes randomly (This is just for demonstrative purposes;
# note that this random connection may not always produce a satisfiable solution).
edges = []

for i in range(N-1):
    for j in range(i+1, N):

        if random.randint(0,100) < 20:
            a = nodes[i]
            b = nodes[j]
            edges.append(Edge(a,b))

# Create a graph from nodes and edges.
graph = Graph(nodes, edges)

# Assert that the graph is valid.
graph.valid.require()

# Concretize everything.
coopy.concretize()

# Iterate through edges asserting that all nodes are indeed valid.
# Methods that return constraints now behave (mostly) like plain booleans.
for edge in edges:
    assert(edge.valid)