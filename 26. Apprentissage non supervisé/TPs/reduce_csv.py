import pandas as pd

# Lire tout le fichier puis échantillonner 10 000 lignes aléatoires
df = pd.read_csv('yellow_tripdata_2016-03.csv')
df_sample = df.sample(n=10000, random_state=42)

# Sauvegarder dans un nouveau fichier
df_sample.to_csv('yellow_tripdata_2016-03_sample.csv', index=False)

print(f"Fichier original: {len(df)} lignes")
print(f"Fichier réduit créé avec {len(df_sample)} lignes (échantillon aléatoire)")
print(f"Colonnes: {list(df.columns)}")
