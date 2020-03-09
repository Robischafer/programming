## Problem Set 2

import numpy

# exercise 1

#triangle1 = area([[0, 0], [1, 0], [0, 2]])
# or
v1 = (0, 0);
v2 = (10, 0);
v3 = (0, 2);
vertices = [v1, v2, v3]

def area(v):
    dist = []
    dist.append(numpy.linalg.norm(v[0], v[1]))
    dist.append(numpy.linalg.norm(v[0], v[2]))
    dist.append(numpy.linalg.norm(v[1], v[2]))
    s = sum(dist)/2
    area = (s * (s - dist[0]) * (s - dist[1]) * (s - dist[2])) ** 0.5
    return(area)


triangle1 = area(vertices)
print( "Area of triangle is" %.2 f % triangle1)
