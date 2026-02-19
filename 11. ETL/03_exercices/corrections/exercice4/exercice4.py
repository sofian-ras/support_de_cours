import requests
import pandas as pd

# 1. Récupérer tous les pays d'Europe
response = requests.get("https://restcountries.com/v3.1/region/europe")
pays_europe = response.json()

# 2. Créer un DataFrame avec : nom, capitale, population, superficie
data = []
for pays in pays_europe:
    data.append({
        'nom' : pays.get('name').get('common'),
        'capitale' : pays.get('capital')[0],
        'population' : pays.get('population',0),
        'superficie' : pays.get('area')
    })

df = pd.DataFrame(data)
print(df)

# 3. Calculer la densité de population (population / superficie)
df['densite'] = df['population'] / df['superficie']

# 4. Identifier les 5 pays les plus peuplés d'Europe
top5_population = df.nlargest(5, 'population')[['nom','population']]
print("top 5 population :")
print(top5_population)

# 5. Calculer la population totale de l'Europe
population_total =df['population'].sum()
print(f"population total en europe : {population_total}")

# 6. Trouver le pays avec la plus grande densité
pays_dense = df.nlargest(1, 'densite')[['nom','densite']]
print("pay le plus dense :")
print(f"{pays_dense.iloc[0]['nom']} avec {pays_dense.iloc[0]['densite']}")

# 7. Sauvegarder les résultats dans `pays_europe.xlsx`
df.to_excel('pays_europe.xlsx', index=False)