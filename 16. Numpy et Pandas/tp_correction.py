import numpy as np

annees = np.genfromtxt("./Cleaned_Energy_Consumption_Data.csv", delimiter=",", usecols=range(4, 66), max_rows=1)
data = np.genfromtxt("./Cleaned_Energy_Consumption_Data.csv", delimiter=",", usecols=range(4, 66), skip_header=1)
nom_pays = np.genfromtxt("./Cleaned_Energy_Consumption_Data.csv", delimiter=",", usecols=0, skip_header=1, encoding="utf-8", dtype=str)

print(nom_pays)

moyenne_annuelle = np.nanmean(data, axis=0)
mediane_annuelle = np.nanmedian(data, axis=0)
ecart_type_annuelle = np.nanstd(data, axis=0)

for i, annee in enumerate(annees):
    if not np.isnan(moyenne_annuelle[i]):
        print(f"{int(annee)} => Moyenne : {moyenne_annuelle[i]} => Médiane {mediane_annuelle[i]} => Ecart-type : {ecart_type_annuelle[i]}")

moyenne_par_pays = np.nanmean(data, axis=1)

index_max = np.nanargmax(moyenne_par_pays)
index_min = np.nanargmin(moyenne_par_pays)

valeur_max = moyenne_par_pays[index_max]
valeur_min = moyenne_par_pays[index_min]

print(f"Pays le plus consommateur : {nom_pays[index_max]} avec {valeur_max}")
print(f"Pays le moins consommateur : {nom_pays[index_min]} avec {valeur_min}")