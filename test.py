import math
import numpy as np

a = (5, 5)
b = (2, 2)

angle = math.atan2(a[0] - b[0], a[1] - b[1])
print(np.cos(angle), np.sin(angle))

