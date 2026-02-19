import numpy as np

data = np.genfromtxt("./pays.csv", delimiter=",", skip_header=1, usecols=(1,2))

print(data)
valeurs_2015 = data[:,0].astype(int)
valeurs_2020 = data[:,1].astype(int)

print("Moyenne de 2015", valeurs_2015.mean())
print("Moyenne de 2020", valeurs_2020.mean())

augmentation = valeurs_2020 - valeurs_2015
print(augmentation)

nom_pays = np.genfromtxt("./pays.csv", delimiter=",", skip_header=1, usecols=0, dtype=str)
print(nom_pays)

print("Pays avec la plus grande augmentation :", nom_pays[np.argmax(augmentation)])