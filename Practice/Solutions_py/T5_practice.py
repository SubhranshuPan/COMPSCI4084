import numpy as np 

a = np.array([10, 20, 30, 40, 50])
m = np.arange(1, 10).reshape(3,3)
print(a.shape, m.shape, m.ndim, a.dtype)

z = np.zeros(3)
o = np.ones((2, 2))
f = np.full(3, 5)
r = np.arange(0, 10, 2)

# print(a[0], a[-1], a[1:4], a[::2])
# print(m[1, 2], m[0], m[:, 0], m[1, :])

# print(m[0:2, 1:3])
# print(m[-2:], m[:, :2])

mask = a > 25
print(a[mask])
b = a.copy()
b[b <= 20] = 0
print(b)
print(a)

print(a[[0, 2, 4]])
g = np.arange(1, 17).reshape(4,4)
print(g[[0, 1, 2, 3], [0, 2, 3, 1]])

