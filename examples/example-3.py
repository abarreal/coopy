#
# Bounded Model Checking example with coopy
#
import coopy

from functools import reduce

#==================================================================================================
#--------------------------------------------------------------------------------------------------
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

#==================================================================================================
#--------------------------------------------------------------------------------------------------
class StateTransition:

    def __init__(self, bucket_a, bucket_b):
        self._a = bucket_a
        self._b = bucket_b

    def execute(self):
        a = self._a
        b = self._b

        # First, have both buckets advance 
        # to a new state.
        a.advance()
        b.advance()

        # Now we proceed to disjoin all 
        # valid state transitions.
        outcome = False

        # Fill one bucket completely.
        outcome |= a.filled & b.unchanged
        outcome |= a.unchanged & b.filled

        # Empty one bucket.
        outcome |= a.empty & b.unchanged
        outcome |= a.unchanged & b.empty

        # Pour the contents of one bucket 
        # into another.
        outcome |= a.poured_into(b)
        outcome |= b.poured_into(a)

        outcome.require()

#==================================================================================================
#--------------------------------------------------------------------------------------------------

# Define the maximum step count.
B = 10

for N in range(1,B):

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