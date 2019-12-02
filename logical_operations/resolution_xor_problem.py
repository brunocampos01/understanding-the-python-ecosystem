import matplotlib.pyplot as plt
import numpy as np


def NAND(x1, x2):
    i = np.array([x1, x2])
    # Wegith and threshold is defined manually for correct AND
    w = np.array([-0.5, -0.5])
    b = 0.7
    tmp = np.sum(i * w) + b
    if tmp <= 0:
        return 0
    else:
        return 1


def OR(x1, x2):
    i = np.array([x1, x2])
    # Wegith and threshold is defined manually for correct AND
    w = np.array([0.5, 0.5])
    b = -0.2
    tmp = np.sum(i * w) + b
    if tmp <= 0:
        return 0
    else:
        return 1


def AND(x1, x2):
    i = np.array([x1, x2])
    # Wegith and threshold is defined manually for correct AND
    w = np.array([0.5, 0.5])
    b = -0.7
    tmp = np.sum(i * w) + b
    if tmp <= 0:
        return 0
    else:
        return 1


def layer1(x1, x2):
    s1 = NAND(x1, x2)
    s2 = OR(x1, x2)
    return s1, s2


def layer2(x1, x2):
    return AND(x1, x2)


X = [[0, 0], [0, 1], [1, 0], [1, 1]]

for x in X:
    s1, s2 = layer1(x[0], x[1])
    y = layer2(s1, s2)
    color = None
    if y == 0:
        color = "b"
    else:
        color = "r"
    plt.plot(x[0], x[1], "o" + color)

plt.grid()
plt.xlim(-0.2, 1.2)
plt.ylim(-0.2, 1.2)
plt.title("XOR")
plt.xlabel("x1")
plt.ylabel("x2")
plt.show()
