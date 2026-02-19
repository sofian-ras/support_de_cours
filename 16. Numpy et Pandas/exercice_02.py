import numpy as np

mois = np.genfromtxt("./ventes_mensuelles.csv", delimiter=",", encoding="utf-8", skip_header=1, usecols=0, dtype=str)
data = np.genfromtxt("./ventes_mensuelles.csv", delimiter=",", skip_header=1, usecols=range(1, 4))

articles_vendus = data[:, 0]
prix_moyen = data[:, 1]
chiffre_affaires = data[:, 2]

#1 
print("Total articles vendus :", np.sum(articles_vendus))

# 2
print("Chiffre d'affaires total :", np.sum(chiffre_affaires))

# 3
print("Mois avec le plus gros CA :", mois[np.argmax(chiffre_affaires)])

# 4
print("Prix moyen :", np.mean(prix_moyen))

# 5
print("Corrélation ventes/CA :", np.corrcoef(articles_vendus, chiffre_affaires))

print("Corrélation ventes/CA :", np.corrcoef(articles_vendus, chiffre_affaires)[0,1])