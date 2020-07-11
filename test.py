from rand48 import Rand48
from math import log



min = 0
max = 0
sum = 0

iterations = 1000000

# using rand48 to seed
rand = Rand48(1)
rand.srand(rand.n)

i = 0
while(i < iterations):
    lamb = 0.001
    r = rand.drand()
    x = -log(r)/lamb
    i += 1

    if x > 3000:
        i -= 1
        continue
    if i < 20:
        print(f'x is {x}')
    sum += x
    if i == 0 or x < min:
        min = x
    if i == 0 or x > max :
        max = x

avg = sum / iterations
print(f'minimum value: {min}')
print(f'maximum value: {max}')
print(f'average value: {avg}')