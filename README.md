# Coopy

Coopy is a library that integrates 
declarative constraint programming into the Python syntax, allowing for objects
to be defined by means of facts or predicates that describe their properties rather 
than step-by-step construction procedures. When working with Coopy, we first describe 
our model in terms of classes that have certain properties and implement certain operations. 
We then proceed to instantiate objects of these classes and have 
them interact with each other in different ways. The key point with Coopy is that some 
of these objects may be *symbolic*. Symbolic objects have attributes that are in 
fact unknowns, like variables in a system of equations.
When symbolic objects interact, then, *constraints* may be imposed on 
their attributes. Eventually, after all the desired constraints have been 
imposed, we can request Coopy to engage an automated theorem prover to 
find values for all symbolic properties in a process called *concretization*. 
After concretization, symbolic attributes acquire concrete values and start 
behaving just like regular Python types, transitioning back seamlessly 
into an imperative object oriented programming model.

For a detailed introduction and usage examples, check the [tutorial](tutorial) files in 
this same repository. If you'd rather read code, on the other hand, check the [examples](examples)
and [tests](test) in this same repository. There are also some code samples listed below.
Finally, be sure to read the [gotchas](tutorial/gotchas.md) section of the tutorial, 
as there are some details that must be kept in mind when using Coopy.  

## Installation and Requirements

Coopy requires the automated theorem prover [Z3](https://github.com/Z3Prover/z3) 
to be installed first. The library may then be installed like most other
typical Python packages:

```bash
# Clone this repository.
git clone https://github.com/abarreal/coopy.git coopy && cd coopy

# Install requirements (just Z3 bindings for Python).
pip install -r requirements.txt

# Setup. Installing in a virtualenv environment is recommended.
python3 setup.py install
```

## Basic Examples

### Example 1

The following example demonstrates the basic mechanics of Coopy. We first 
define some symbolic variables, two integers in this case. We then proceed to 
impose  constraints on them, which is in fact very easy. Finally,
we call the method `concretize` to solve the constraints and assign concrete values
to these variables. From then on, symbolic objects start behaving like
regular Python primitives.

```python
import coopy

x = coopy.symbolic_int('x')
y = coopy.symbolic_int('y')

coopy.require((x == 3) & (x > y))
coopy.concretize()

assert(x == 3 and x > y)
```

### Example 2: Object Models

The next example shows how Coopy may be used to construct
more complex objects.
In this case, concretely, a graph is built in which each node is 
colored with an unknown symbolic color. Validity constraints are 
then imposed to ensure that no two adjacent nodes are of the same 
color. Once done, `concretize` is called to give values to the
colors such that the required constraints are respected. The end 
result is a graph colored according to the specified
restrictions, which can be used from then on as a regular
Python object.

```python
import coopy
import random

from coopy import neg
from functools import reduce

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
```

## Additional Examples

More examples may be found in the [examples](examples) folder.
Currently, in addition to those listed above, the following
two are available:

* [Bounded Model Checking](examples/example-3.py): In this example, Coopy is 
used to solve the water jug puzzle from the movie Die Hard 3. This example shows 
how to encode state machines as object models and then use Coopy to analyze
their evolution.

* [Custom Sorts and Uninterpreted Functions](examples/example-4.py): 
This example shows how to define custom sorts (i.e. domains) 
and symbolic (i.e. uninterpreted) functions. Concretely, we define a 
`Boolean` type for which two values exist: `T` and `F`. 
Uninterpreted functions `*` (and), `+` (or), and `~` (negation) 
mapping booleans to booleans are also defined. A `BooleanAlgebra`
then defines axioms over these entities. The `concretize` method is 
finally called, which assigns a concrete interpretation to these objects.
From then on, booleans and functions alike can be used as regular Python objects.

## TODO

* Write more tests.

* Implement support for constraint solver layers (i.e. `push`, `pop`) 
and optional constraints (e.g. `pop` if failed and try again).

* Implement support for multiple solver scopes (`coopy.activate('myscope')`).

* Implement a wrapper to encapsulate Z3 exceptions in case of unsolvability.

## License

Coopy is released under the terms of the [MIT license](LICENSE).

© Copyright 2020, Adrián Barreal. All rights reserved.