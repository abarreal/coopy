# Coopy: Introductory Tutorial (Part 1)

This is the first part of the Coopy tutorial. In this tutorial we will study
how to use Coopy to solve mathematical problems in an object oriented way.
In this first part, however, we will start with the very basics. 

> **Note**: it is assumed that, at this point, Coopy has already been installed.

## Symbolic Variables

Coopy relies on the concept of *symbolic variables*. A symbolic variable is
essentially an unknown, the `x` part of the equation. Coopy allows to
instantiate symbolic variables of several types, including integers,
reals and booleans. Take a look at the following shell session:

```python
>>> import coopy

>>> n = coopy.symbolic_int('n')
>>> n
n:1

>>> p = coopy.symbolic_bool('p')
>>> p
p:2

>>> x = coopy.symbolic_real('x')
>>> x
x:3
```

When we instantiate symbolic variables, what we get is just that,
an uninterpreted object that has a name, a type, and an increasing
numeric identifier (the number after the colon).

When just instantiated, Coopy has no information on these variables
other than those properties mentioned above. We may declare additional
conditions for these variables, however, by requiring or imposing
*constraints*. For example:

```python
>>> ((x > 10) == p).require()
```

Logical operators on symbolic variables do not return primitive
booleans, but *abstract syntax trees* (ASTs) instead. If you don't know
what that means, just know that these trees encode the whole
history of the operations on the variables.

Coopy ASTs that represent logical operations expose the key 
method `require`. When we call this method, a constraint
is imposed on the involved variables. In the previous example,
we are stating "the truth value of `x` being greater than 10
is the same value as that of the boolean variable `p`."
That is a constraint, a predicate that must be true, 
and this one relates variables `x` and `p`.

> **Note**: The syntax `(...).require()` may feel kind of 
awkward, so there is an alternative function `coopy.require(...)`
which may be used instead. This function is just a wrapper
that calls the `.require()` method on the object it
receives as an argument, which should in general be an AST.

We may then ask Coopy to generate a *model* that satisfies these
constraints. A model is essentially an assignment of values
for the variables such that all constraints are met:

```python
>>> coopy.model()
[p:2 = True, x:3 = 11]
```

Having required the previously stated constraint, when we call
`model` we get back an assignment of values for all stated
conditions to be met (if such an assignment exists!).
Suppose that we impose an additional constraint, then:

```python
>>> (p == False).require()
```

Now we are stating "`p` is false." If we request a new model,
this time we get back the following:

```python
>>> coopy.model()
[p:2 = False, x:3 = 0]
```

Now we get an answer that is consistent with *both*
constraints. Coopy has a back-end that remembers constraints
as they are imposed, so the whole history is used when
we call `model`. To reset constraints, then, we must call
the method `coopy.reset()`, which makes Coopy forget all
previously imposed restrictions.

> **Important**: Notice that Coopy only assigns values to
variables present in the imposed constraints.

## Concretization

A very interesting feature of Coopy is that of *concretization*.
Basically, after having imposed a set of constraints, we may
call the method `concretize` of Coopy to have two things happen:
first, Coopy will compute a model that satisfies the constraints;
second and most important, Coopy will update all symbolic variables
present in the constraints with their corresponding model values. 
From then on, those previously symbolic variables start behaving as 
concrete Python types. Check for example the following code:

```python
import coopy

n = coopy.symbolic_int('n')
m = coopy.symbolic_int('m')

# Impose some constraints. When working with Coopy ASTs, the 
# 'and' and 'or' operators are & and |, respectively.
((n > 10) & (n < 15) & (m == n + 7)).require()

# Concretize everything.
coopy.concretize()

# Now n and m can be used mostly like normal integers.
assert(n > 10 and n < 15)
assert(m == n + 7)

print(n) # 11
print(m) # 18
```

As we will see in the [next part of the tutorial](tutorial-2.md), 
this feature of concretization allows to construct complex objects 
declaratively, as in some sort of declarative factory pattern. 