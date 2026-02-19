# Numpy est une bibliotheque pour la manipulation de données numériques pour :

# - Créer et manipuler efficacement des tableaux multidimensionnels
# - Effectuer des calculs performents
# - Travailler avec des fichiers CSV
# - Servir de base à des bibliothèques comme Pandas ou Scikit-learn

# pip install numpy
import numpy as np


# Création d'un tableau numpy à partir d'une liste :
ma_liste = [1, 2, 3]

a = np.array(ma_liste)

print(a)
print(type(a))

b = np.array([[1,2,3], [4,5,6], [7,8,9]])
print(b)

print("====== avec les méthodes ======")

# Avec des méthodes comme : arange, zeros, ones, random
print(np.arange(0, 10, 2))
print(np.zeros((5, 6)))
print(np.ones((2, 3)))
print(np.random.rand(2,3))

print("==== Indexing et slicing ====")

arr = np.arange(10)
print("tableau de base :", arr)
print("tableau[1] =", arr[1])
print("tableau[2:5]", arr[2:5]) # [index_debut : index_fin (exclut)]

mat = np.arange(1, 10).reshape(3,3)
print("Matrice : \n", mat)
print("mat[1,2] :", mat[1,2])
print("mat[:2,1:] \n", mat[:2,1:]) # [lignes, colones]

print("==== Opérations mathématiques ====")

x = np.array([1,2,3])
y = np.array([4,5,6])

print("Addition :", x + y)
print("Multiplication :", x * y)

# Statistiques sur les tableaux
mat = np.arange(1, 10).reshape(3,3)
print(mat)
print("La somme des valeurs du tableau :", mat.sum())
print("La somme horizontal :", mat.sum(axis=1)) # axis = 1 => Lignes
print("La somme vertical :", mat.sum(axis=0)) # axis = 0 => colones
print("La medianne :", np.median(mat))
print("La medianne en excluant les nan :", np.nanmedian(mat))
print("La moyenne :", np.mean(mat))
print("Ecart type :", np.std(mat))
print("min :", mat.min())
print("position de min :", mat.argmin())
print("max :", mat.max())
print("position de max :", mat.argmax())

