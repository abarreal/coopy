# Coopy: Introductory Tutorial (Part 3)

In this part of the tutorial we will be using Coopy to analyze a state machine.
The goal is to find a sequence of states that go from an initial known state 
to a final desired state. The full code is available [here](../examples/example-3.py).

The concrete problem that we will be solving is the 
[puzzle from the movie Die Hard 3](https://www.youtube.com/watch?v=BVtQNK_ZUJg).
The idea is the following: we have two buckets (or jugs, however you want to call them): 
one which has a capacity of precisely 3 gallons, and another which has a capacity of 
precisely 5 gallons. We also have access to a fountain, which we may use to fill 
the buckets with as much water as we need. The goal of the problem is to get
precisely 4 gallons into the 5 gallon bucket.

The problem may be modeled as a state machine in which a state is defined
as a tuple (`a`,`b`), where `a` is the amount of water in the 3 gallon bucket,
and `b` is the amount of water in the 5 gallon bucket. The initial state is (0,0).
The list of valid state transitions is the following:

1. We can empty one of the buckets while leaving the other as it is.

2. We can fill one of the buckets completely while leaving the other as it is.

3. We can pour the contents of one bucket into the other.

To solve this problem using Coopy, let us first define a `Bucket` class:

```python
class Bucket:

    def __init__(self, capacity):
        # All buckets have a concrete capacity.
        self._capacity = capacity
        # Initialize the water level of the bucket, which is to be symbolic.
        self._water_volume = self._new_state()
        # At the beginning, the amount of water in the bucket must be 0.
        (self.empty).require()
        # Have the bucket remember its state history.
        self._state_history = [self._water_volume]

    @property
    def capacity(self):
        return self._capacity

    @property
    def state_history(self):
        return self._state_history

    @property
    def water_volume(self):
        return self._water_volume

    @property
    def empty(self):
        return self.water_volume == 0

    @property
    def filled(self):
        return self._water_volume == self._capacity

    @property
    def unchanged(self):
        return self.water_volume == self._previous_water_volume

    @property
    def _previous_water_volume(self):
        return self._state_history[-2]

    def poured_into(self, other):

        sum = self._previous_water_volume + other._previous_water_volume
        outcome_1 = self.empty & (other.water_volume == sum)

        delta = other.capacity - other._previous_water_volume
        outcome_2 = (self.water_volume == self._previous_water_volume - delta) & other.filled

        # Other constraints (i.e. non negativiy and boundedness) will ensure
        # that only valid transitions happen, so we can just OR these without
        # worrying about other conditions.
        return outcome_1 | outcome_2

    def advance(self):
        # Create a symbolic variable for the new water level.
        self._water_volume = self._new_state()
        # Add this new volume to the history.
        self._state_history.append(self._water_volume)

    def _new_state(self):
        # Create a symbolic variable for the new water volume.
        water_volume = coopy.symbolic_int('wv')
        # Impose basic constraints on the new water volume.
        (water_volume >= 0).require()
        (water_volume <= self._capacity).require()
        # Return the new water volume.
        return water_volume
```

This class has a symbolic attribute `_water_volume`, which represents the amount of 
water held in the bucket. Whenever we instantiate a `Bucket`, an initial value
for this attribute is instantiated and forced to be zero. The state of the
bucket can evolve, however, by calling its method `advance`, which brings
the bucket to a new state, with a new symbolic value for the bucket's content.
A priori, the only restrictions on this new water volume are that
it must be greater than or equal to zero, and it must be less than or equal
to the capacity of the bucket. Another interesting detail is that the
bucket remembers its history of states, as this is used later to
display the solution after solving.

Notice that the `Bucket` class implements several methods that return
predicates that describe the state of the bucket. There is one that
is particularly interesting, `poured_into`, that describes the state
of the bucket after its contents being poured into another bucket.

After having modeled our bucket in detail, we proceed to model
state transitions too. The class in question is the following:

```python
class StateTransition:

    def __init__(self, bucket_a, bucket_b):
        self._a = bucket_a
        self._b = bucket_b

    def execute(self):
        a = self._a
        b = self._b

        # First, have both buckets advance to a new state.
        a.advance()
        b.advance()

        # Now we proceed to evaluate all valid state transitions.
        possible_outcomes = []

        # Fill one bucket completely.
        possible_outcomes.append(a.filled & b.unchanged)
        possible_outcomes.append(a.unchanged & b.filled)

        # Empty one bucket.
        possible_outcomes.append(a.empty & b.unchanged)
        possible_outcomes.append(a.unchanged & b.empty)

        # Pour the contents of one bucket into another.
        possible_outcomes.append(a.poured_into(b))
        possible_outcomes.append(b.poured_into(a))

        # Impose a disjunction of all possible resulting states.
        reduce(lambda x,y: x | y, possible_outcomes).require()
```

The `execute` method calls `advance` on both buckets, and 
imposes a disjunction of all valid state transitions.

The solution to the problem may then be found with a bounded model
checking kind of approach:

```python
# Define the maximum step count.
B = 10

for N in range(1,B+1):

    # Clean previous constraints.
    coopy.reset()

    # Instantiate new buckets for this pass.
    bucket_a = Bucket(3)
    bucket_b = Bucket(5)

    for n in range(N):
        StateTransition(bucket_a, bucket_b).execute()

    # Check if there is a solution.
    try:
        (bucket_b.water_volume == 4).require()
        model = coopy.concretize()
        print('Solution found with N =',N)

        # Iterate through state histories for each bucket.
        a_history = bucket_a.state_history
        b_history = bucket_b.state_history
        assert(len(a_history) == len(b_history))

        for i in range(len(a_history)):
            print((a_history[i], b_history[i]))

        break

    except:
        print('No solution found with N =',N)
```

In this case, we are imposing a maximum bound `B` on the number of steps.
Then, for each `N` such that `1 <= N <= B`, we check if there is a 
solution in `N` steps. If the solution is not found, we increase `N`;
if found, on the other hand, we just print the history of states
for each bucket. If we run the program, we should get an output
that looks like the following:

```
No solution found with N = 1
No solution found with N = 2
No solution found with N = 3
No solution found with N = 4
No solution found with N = 5
Solution found with N = 6
(0, 0)
(0, 5)
(3, 2)
(0, 2)
(2, 0)
(2, 5)
(3, 4)
```