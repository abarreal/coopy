import coopy

x = coopy.symbolic_int('x')
y = coopy.symbolic_int('y')

((x == 3) & (x > y)).require()

coopy.concretize()

assert(x == 3 and x > y)