# Coopy: Gotchas

* Keep in mind that the fact that you can request something does not
mean that it exists. If the imposed constraints are simply not satisfiable, 
`concretize` will just throw an exception, possibly after taking what
seems like forever to realize the fact.

* Along with the previous point, while constraint solving can be
reasonably fast in many cases, it can also be painfully slow in others, 
and this will mostly depend on the amount of variables and the complexity 
of the constraints. Disjunctions and non-linearities are especially burdensome 
for the solver. This does not mean you should avoid them, but if solving
seems to take forever, these are potential causes. Outside of that, it is
said that modern (current?) solvers (which Z3 is) can handle problems
with hundreds of thousands of variables and constraints.

* While Coopy attempts to integrate as seamlessly as possible into the
Python syntax, it's just a library and nothing more. It is, therefore, 
limited in capabilities to what the language allows programs to do. 
Concretely, Coopy is based on operator overloading, and not all
Python operators can be overloaded. While this still works pretty well
in practice, there are some caveats to keep in mind:

    * The `&` and `|` operators used for conjunction and disjunction of 
    constraints, respectively, take precedence over other operators 
    such as `==`, `!=`. Therefore, if used along other operators in the 
    same sentence, expressions connected by `&` and `|` should be
    appropriately parenthesized
    (e.g. `((x > y) & (x == 3)) | (x == 5) | someobject.valid`).

    * The `not` operator keyword cannot be overloaded. Coopy exposes a `neg`
    function instead, which is equivalent to `not` if given a concrete
    boolean. If given a constraint, on the other hand, `neg` returns 
    another one which represents the logical negation of the original.
    This `neg` function should be used instead of `not` if the parameter 
    is expected to be a constraint. Check the 
    [graph coloring example](../examples/example-2.py) 
    to see how to use it.

    * When defining classes with symbolic attributes and
    overloaded `__eq__` and `__ne__` operators that return constraints, 
    keep the following in mind: the operator `__ne__` of a symbolic object 
    is not just `not self.__eq__(other)`. The `not` keyword transforms whatever 
    is to the right into a boolean; before concretization, however, constraints 
    cannot be casted to booleans. The appropriate way to implement these operators 
    is shown in the [Custom Sorts and Uninterpreted Functions](../examples/example-4.py)
    example.