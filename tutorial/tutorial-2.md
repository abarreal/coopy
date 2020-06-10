# Coopy: Introductory Tutorial (Part 2)

In this part of the tutorial we will be using Coopy to generate a solution
for a graph coloring problem. We will also see how easy it is to integrate
Coopy into an object oriented model. The full code for this tutorial is available 
[here](../examples/example-2.py).

When using Coopy to solve a mathematical problem in an object oriented way,
we have first to describe our problem in terms of classes and objects.
Consider for example the following code:

```python
class Node:

    def __init__(self):
        self._color = coopy.symbolic_int()

    @property
    def valid(self):
        color = self._color
        return ((color == 0) | (color == 1) | (color == 2))

    def same_color_as(self, other):
        return self._color == other._color
```

This code defines a `Node` type, which will represent a colored node
of our graph. As we can see, it's just a plain class save for one
small detail: it has a symbolic attribute. When we instantiate a `Node`
object then, its color will be essentially an unknown. Notice, however,
the methods `valid` and `same_color_as`. These methods return a truth
value that depends on the symbolic attribute `_color`; until the
color variable is concretized, then, these methods will return constraints,
which may be required just like we saw in the previous part of the tutorial.
But let's incorporate this node into a more complex structure. Let
us proceed by defining a class `Edge`, for example:

```python
class Edge:

    def __init__(self, a, b):
        self._a = a
        self._b = b

    @property
    def valid(self):
        return neg(self._a.same_color_as(self._b))
```

Again, real simple. An `Edge` has only two attributes: the nodes which 
it connects. An edge also has a `valid` property which is true when the 
connected nodes are *not* of the same color. Notice that the `neg` function
of Coopy is used, rather than the `not` keyword of Python. Unfortunately,
Python does not allow to override the behavior of `and`, `or` and `not`,
so `&`, `|`  and `neg`, respectively, had to be used instead. The `neg` 
function, when given a plain boolean, is just equivalent to `not`. When given
a symbolic variable or an AST, however, it returns another AST that 
represents the logical negation of the original.

Let us now proceed to put nodes and edges together in a full graph:

```python
class Graph:

    def __init__(self, nodes, edges):
        self._nodes = nodes
        self._edges = edges

    @property
    def valid(self):
        # Assert that nodes are valid.
        nodes_valid = [node.valid for node in self._nodes]
        nodes_valid = reduce(lambda x,y: x & y, nodes_valid)
        # Assert that edges are valid.
        edges_valid = [edge.valid for edge in self._edges]
        edges_valid = reduce(lambda x,y: x & y, edges_valid)
        # Both conditions must be met for the graph to be valid.
        return nodes_valid & edges_valid
```

As we can see, the `Graph` class has two attributes: a collection of
nodes, and a collection of edges. A graph also has a property `valid`
which requires all nodes to be valid and all edges to be valid.

> **Note**: The above example uses `functools.reduce` to conjoin the 
constraints. Coopy implements a function `all`, however, which can be used 
instead. There is also a function `any` for disjunction.

With that, our model has been defined. We now proceed to generate
an actual, concrete graph that meets all validity conditions.
Take a look then at the following code:

```python
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
```

In the above snippet we just begin by instantiating some nodes and connecting
them randomly. This constructs a graph, a symbolic one in essence because
its nodes have symbolic colors. These colors are our problem unknowns.
We can proceed then to impose validity by calling `require` on
the output of the `valid` method of the graph, 
which gathers all constraints for all objects on it:

```python
# Assert that the graph is valid.
graph.valid.require()

# Concretize everything.
coopy.concretize()

# Iterate through edges asserting that all nodes are indeed valid.
# Methods that return constraints now behave (mostly) like plain booleans,
# and the colors were assigned concrete values.
for edge in edges:
    assert(edge.valid)
```

After requiring the constraints, we just concretize everything
by calling the `concretize` method. The graph is from then on concrete;
the color variables will start behaving just like regular Python integers. 
We just saw then how a valid three-colored graph object can be constructed 
from a declarative specification only, without needing us to provide a 
concrete construction procedure.

The [next part of the tutorial](tutorial-3.md) shows how to use
Coopy to analyze state machines for bounded model checking. 