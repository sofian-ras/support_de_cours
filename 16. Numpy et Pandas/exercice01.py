import numpy as np

# 1 
a = np.full((3,3), 7)
print(a)

# 2 
b = np.random.rand(4,4)
print(b)

# 3
c = np.arange(10)
print(c[3:8])

# 4
d = np.arange(9).reshape(3,3)
print(d[:,-1])

# 5
e = np.random.rand(10)
print("Moyenne :", e.mean())

# 6
f = np.random.randint(1, 10, size=(4,3))
print(f)
print("Somme par colonne :", f.sum(axis=0))