import numpy as np

x = np.load('x_file.npy')

x[x == 1] = 999

# Replace -1 with 1
x[x == -1] = 1

# Replace temporary value with -1
x[x == 999] = -1

print(x)
np.save('x2_file.npy', x)