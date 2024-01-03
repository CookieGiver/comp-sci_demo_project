import math

# reimann sums calculator
n_list = [5, 10, 50, 100]
sum_list = [0, 0, 0, 0]

f = lambda x: math.sin(x)
a, b = 0, math.pi

for index, n in enumerate(n_list):
    for i in range(n):
        sum_list[index] += f((i+1) * ((b-a)/n)) * ((b-a)/n)

print(sum_list)

        