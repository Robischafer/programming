### Programming
### Take Home Exam 1

import numpy as np
import random
from matplotlib import pyplot as plt

## Q4
# tic-tac-toe

# create empty board
# player 1 place token "1"
# player 2 place token "2"


board = np.zeros((3, 3))


def randplay(board):
    turn = np.count_nonzero(board)
    n = random.randrange(1, 10, 1)
    if turn % 2 == 1 and turn < 9:
        if n / 3 <= 1:
            if n % 3 == 1 and board[0, 0] == 0:
                x = np.vstack((np.array([1, 0, 0]), np.zeros(3), np.zeros(3)))
                board = np.add(board, x)
            elif n % 3 == 2 and board[0, 1] == 0:
                x = np.vstack((np.array([0, 1, 0]), np.zeros(3), np.zeros(3)))
                board = np.add(board, x)
            elif n % 3 == 0 and board[0, 2] == 0:
                x = np.vstack((np.array([0, 0, 1]), np.zeros(3), np.zeros(3)))
                board = np.add(board, x)
            else:
                randplay(board)
        elif n / 3 <= 2:
            if n % 3 == 1 and board[1, 0] == 0:
                x = np.vstack((np.zeros(3), np.array([1, 0, 0]), np.zeros(3)))
                board = np.add(board, x)
            elif n % 3 == 2 and board[1, 1] == 0:
                x = np.vstack((np.zeros(3), np.array([0, 1, 0]), np.zeros(3)))
                board = np.add(board, x)
            elif n % 3 == 0 and board[1, 2] == 0:
                x = np.vstack((np.zeros(3), np.array([0, 0, 1]), np.zeros(3)))
                board = np.add(board, x)
            else:
                randplay(board)
        elif n / 3 > 2:
            if n % 3 == 1 and board[2, 0] == 0:
                x = np.vstack((np.zeros(3), np.zeros(3), np.array([1, 0, 0])))
                board = np.add(board, x)
            elif n % 3 == 2 and board[2, 1] == 0:
                x = np.vstack((np.zeros(3), np.zeros(3), np.array([0, 1, 0])))
                board = np.add(board, x)
            elif n % 3 == 0 and board[2, 2] == 0:
                x = np.vstack((np.zeros(3), np.zeros(3), np.array([0, 0, 1])))
                board = np.add(board, x)
            else:
                randplay(board)
    elif turn % 2 == 0 and turn < 9:
        if n / 3 <= 1:
            if n % 3 == 1 and board[0, 0] == 0:
                x = np.vstack((np.array([2, 0, 0]), np.zeros(3), np.zeros(3)))
                board = np.add(board, x)
            elif n % 3 == 2 and board[0, 1] == 0:
                x = np.vstack((np.array([0, 2, 0]), np.zeros(3), np.zeros(3)))
                board = np.add(board, x)
            elif n % 3 == 0 and board[0, 2] == 0:
                x = np.vstack((np.array([0, 0, 2]), np.zeros(3), np.zeros(3)))
                board = np.add(board, x)
            else:
                randplay(board)
        elif n / 3 <= 2:
            if n % 3 == 1 and board[1, 0] == 0:
                x = np.vstack((np.zeros(3), np.array([2, 0, 0]), np.zeros(3)))
                board = np.add(board, x)
            elif n % 3 == 2 and board[1, 1] == 0:
                x = np.vstack((np.zeros(3), np.array([0, 2, 0]), np.zeros(3)))
                board = np.add(board, x)
            elif n % 3 == 0 and board[1, 2] == 0:
                x = np.vstack((np.zeros(3), np.array([0, 0, 2]), np.zeros(3)))
                board = np.add(board, x)
            else:
                randplay(board)
        elif n / 3 > 2:
            if n % 3 == 1 and board[2, 0] == 0:
                x = np.vstack((np.zeros(3), np.zeros(3), np.array([2, 0, 0])))
                board = np.add(board, x)
            elif n % 3 == 2 and board[2, 1] == 0:
                x = np.vstack((np.zeros(3), np.zeros(3), np.array([0, 2, 0])))
                board = np.add(board, x)
            elif n % 3 == 0 and board[2, 2] == 0:
                x = np.vstack((np.zeros(3), np.zeros(3), np.array([0, 0, 2])))
                board = np.add(board, x)
            else:
                randplay(board)
    else:
        return board
    return board


player_1 = np.ones(3)
player_2 = 2 * np.ones(3)


def win(board, player):

    if (np.diagonal(board) == player).all() and board[0][0] != 0:
        winner = board[0][0]
        # print("player", winner, "is the winner!!!")
        return winner

    if (np.fliplr(board).diagonal() == player).all() and board[2][0] != 0:
        winner = board[2][0]
        # print("player", winner, "is the winner!!!!")
        return winner

    for i in range(0, 2):
        if (board[i, :] == player).all() and board[i][0] != 0:
            winner = board[i][0]
            # print("player", winner, "is the winner!")
            return winner

    for j in range(0, 2):
        if (board[:, j] == player).all() and board[0][j] != 0:
            winner = board[0][j]
            # print("player", winner, "is the winner!!")
            return winner
    else:
        return False


def randgame():
    board = np.zeros((3, 3))
    win_cond = False
    i = 0
    while i < 9 and win_cond is False:
        board = randplay(board)
        win_cond = win(board, player_1) or win(board, player_2)
        i = i + 1
    return win_cond


L = []
for k in range(0, 1000):
    L.append(randgame())

density1 = [L.count(1)/1000, L.count(2)/1000, L.count(False)/1000]
position = np.arange(len(density1))
label = ["1 win", "2 win", "draw"]
plt.bar(position, density1)
plt.title("number of win, given player 2 is the first to play")
plt.xticks(position, label)
plt.show()


def randgame():
    board = np.array([[0, 0, 0], [0, 2, 0], [0, 0, 0]])
    win_cond = False
    i = 0
    while i < 9 and win_cond is False:
        board = randplay(board)
        win_cond = win(board, player_1) or win(board, player_2)
        i = i + 1
    return win_cond


M = []
for k in range(0, 1000):
    M.append(randgame())

density2 = [M.count(1)/1000, M.count(2)/1000, M.count(False)/1000]
position = np.arange(len(density2))
label = ["1 win", "2 win", "draw"]
plt.bar(position, density2)
plt.title("number of win, given player 2 is the first to play and play in the center")
plt.xticks(position, label)
plt.show()
