import numpy as np

x = np.array([
    [1, 2, 3], # 6
    [50,60,70], # 180
    [0, 1, 0] # 1
    # 51, 63, 73
])

print(x.sum(axis=1)) # moving horizontally across, Column #[  6 180   1]
print(x.sum(axis=0)) # moving vertically down, Row #[51 63 73]