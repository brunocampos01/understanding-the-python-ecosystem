import numpy as np
import matplotlib.pyplot as plt

X = [[0, 0], [0, 1], [1, 0], [1, 1]]
Y = [0, 1, 1, 0]

for i in range(len(X)):
    x = X[i]
    y = Y[i]
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
