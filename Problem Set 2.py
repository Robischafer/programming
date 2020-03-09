## Problem Set 2

import numpy
import math

# exercise 1

# calculate area of a triangle with coordinate of 3 point

# triangle1 = area([[0, 0], [1, 0], [0, 2]])
# or
v1 = (0, 0);
v2 = (10, 0);
v3 = (0, 2);
vertices = [v1, v2, v3]


def area(v):
    dist = []
    dist.append(math.sqrt((v[0][0] - v[0][1]) ** 2 + (v[1][0] - v[1][1]) ** 2))
    dist.append(math.sqrt((v[0][0] - v[0][1]) ** 2 + (v[2][0] - v[2][1]) ** 2))
    dist.append(math.sqrt((v[2][0] - v[2][1]) ** 2 + (v[1][0] - v[1][1]) ** 2))
    s = sum(dist) / 2
    area = (s * (s - dist[0]) * (s - dist[1]) * (s - dist[2])) ** 0.5
    return (area)


area = area(vertices)
print('The area of the triangle is %0.2f' % area)

# exercise 2

def gauss(list):
    """
    parameter: list of xi
    return list of gaussian N(0,1) distributed elements
    """
    x = list
    m = 0
    s = 1
    g = []
    for i in list:
        g.append((1/(math.sqrt(2*math.pi)*s))*math.exp(-(1/2)*((x[i]-m)/s)**2))
    return(g)

gauss(range(-5,5,1))

# exercise 3

numbers = list(range(10))
print(numbers)
for n in numbers:
    # i is the median value or the one preceding it
    i = len(numbers)//2
    del numbers[i]
    # n goes from 0, 1, 2, 3, 8 because the length of n changes
    # del is the position of the deleted value
    # numbers is the updated list of value
    print ("n=%d, del %d" %(n,i), numbers)

# exercise 4

