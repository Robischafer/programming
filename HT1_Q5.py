### Programming
### Take Home Exam 1

import numpy as np
from matplotlib import pyplot as plt

## Q5

# maze

np.random.seed(12345)
L = 4
C = 6

# create maze where wall = 0
maze = (np.random.uniform(size=(L, C)) > 0.2) * 1
# source
maze[0, 0] = -1
# maze ending
maze[-1, -1] = 3
plt.imshow(maze)
plt.show()

# find source
# find its neighbours and its walls
# increment neighbours value by 1
# repeat for neighbours (where val = 2)

source = (np.concatenate(np.where(maze == -1)))
maxRow = maze.shape[0]
maxCol = maze.shape[1]

# 4 direction
dx = [0, 1, 0, -1]
dy = [-1, 0, 1, 0]


def stepmatrix(maze):

    maxRow = maze.shape[0]
    maxCol = maze.shape[1]
    # create matrix of visited cell
    # initialize source as visited
    visited = np.zeros([maxRow, maxCol], dtype=bool)
    visited[0, 0] = True
    # create stepmatrix
    sm = np.zeros([maxRow, maxCol])
    sm[0, 0] = 1

    # start at the source (0, 0)
    X = [0]
    Y = [0]

    # continue until all cell have been visited
    while not visited.all():
        x = X[0]
        y = Y[0]
        for i in range(0, 3):
            if 0 <= x + dx[i] <= maxRow - 1 and 0 <= y + dy[i] <= maxCol - 1:
                xx = x + dx[i]
                yy = y + dy[i]
            else:
                continue
            try:
                if visited[xx][yy] == False and maze[xx][yy] != 0 \
                        and xx in range(0, maxRow) and yy in range(0, maxCol):
                    # add cell to queue
                    X = np.append(X, xx)
                    Y = np.append(Y, yy)
                    # check neighbours value and
                    # if not wall, cell value =
                    # neighbours + 1
                    if sm[xx - 1, yy] != 0:
                        sm[xx][yy] = sm[xx - 1, yy] + 1
                        visited[xx][yy] = True
                    elif sm[xx, yy - 1] != 0:
                        sm[xx][yy] = sm[xx, yy - 1] + 1
                        visited[xx][yy] = True
                    elif sm[xx + 1, yy] != 0:
                        sm[xx][yy] = sm[xx + 1, yy] + 1
                        visited[xx][yy] = True
                    elif sm[xx, yy + 1] != 0:
                        sm[xx][yy] = sm[xx, yy + 1] + 1
                        visited[xx][yy] = True
                elif visited[xx][yy] == False and maze[xx][yy] == 0:
                    X = np.append(X, xx)
                    Y = np.append(Y, yy)
                    visited[xx][yy] = True

            except:
                continue

        # remove visited cell from queue
        X = np.delete(X, 0)
        Y = np.delete(Y, 0)

    return sm


sm = stepmatrix(maze)



