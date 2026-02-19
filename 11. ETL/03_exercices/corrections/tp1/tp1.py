import pandas as pd
import glob # permet de rechercher des fichiers selon un pattern


# 1. Charger tous les fichiers CSV
# 2. Ajouter une colonne `magasin` (A, B ou C)


fichiers = glob.glob('magasin_*.csv')

dataframes = []

for fichier in fichiers:
    # recup nom du magasin
    magasin = fichier.split('_')[1].split('.')[0]
    df = pd.read_csv(fichier)
    df['magasin'] = magasin
    dataframes.append(df)


# 3. Concaténer tous les DataFrames
df_consolide = pd.concat(dataframes,ignore_index=True)

print(df_consolide)

# 4. Nettoyer (doublons, valeurs manquantes)
df_consolide = df_consolide.drop_duplicates()

df_consolide['vendeur'] = df_consolide['vendeur'].fillna('Inconnu')
df_consolide['date'] = pd.to_datetime(df_consolide['date'])

# 5. Calculer `montant_total`

df_consolide['montant_total'] = (
    df_consolide['quantite'] *
    df_consolide['prix_unitaire']
)


par_magasin = df_consolide.groupby('magasin').agg({
    'montant_total': 'sum',
    'quantite': 'sum',
    'produit': 'count'
}).reset_index()


par_vendeur = (
    df_consolide
    .groupby(['magasin', 'vendeur'])['montant_total']
    .sum()
    .reset_index()
    .sort_values('montant_total', ascending=False)
)

top_produits = (
    df_consolide
    .groupby('produit')
    .agg({'quantite': 'sum', 'montant_total': 'sum'})
    .reset_index()
    .sort_values('montant_total', ascending=False)
    .head(10)
)


# 6. Créer un rapport Excel avec :
#    - Feuille "Consolidé" : Toutes les données
#    - Feuille "Par magasin" : Totaux par magasin
#    - Feuille "Par vendeur" : Performance des vendeurs
#    - Feuille "Top produits" : 10 produits les plus vendus

with pd.ExcelWriter('rapport_ventes.xlsx',engine='openpyxl') as writer:
    df_consolide.to_excel(writer,sheet_name="Consolidé",index=False)
    par_magasin.to_excel(writer,sheet_name="Par magasin",index=False)
    par_vendeur.to_excel(writer,sheet_name="Par vendeur",index=False)
    top_produits.to_excel(writer,sheet_name="Top produits",index=False)