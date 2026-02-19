import pandas as pd

# 1. Charger les données avec Pandas

df = pd.read_excel('ventes_janvier.xlsx')

# 2. Nettoyer :
#    - Supprimer les doublons
#    - Remplir les valeurs manquantes de `region` par "Non spécifié"
#    - Convertir `date` en datetime

df = df.drop_duplicates()
df['region'].fillna("Non spécifié", inplace=True)
df['date'] = pd.to_datetime(df['date'])

# 3. Transformer :
#    - Créer `montant_total` = quantite × prix_unitaire
#    - Extraire le `jour` et `jour_semaine` de la date

df['montant_total'] = df['quantite'] * df['prix_unitaire']
df['jour'] = df['date'].dt.day
#df['jour_semaine'] = df['date'].dt.day_name()
df['jour_semaine'] = df['date'].dt.day_name(locale='fr_FR')

# 4. Analyser :
#    - Total des ventes par région
#    - Produit le plus vendu (en quantité)
#    - Jour de la semaine avec le plus de ventes

par_region = df.groupby('region')['montant_total'].sum().reset_index()
par_region.columns = ['region','total_ventes']
par_region = par_region.sort_values('total_ventes',ascending=False)


par_produit = df.groupby('produit')['quantite'].sum().reset_index()
par_produit = par_produit.sort_values('quantite',ascending=False)
meilleur_produit = par_produit.iloc[0]
print(f"{meilleur_produit['produit']} et en quantite {meilleur_produit['quantite']} ")

par_jour = df.groupby('jour_semaine')['montant_total'].sum().reset_index()
par_jour = par_jour.sort_values('montant_total',ascending=False)
meilleur_jour = par_jour.iloc[0]
print(f"{meilleur_jour['jour_semaine']}  {meilleur_jour['montant_total']} ")


# 5. Créer un fichier Excel avec 3 feuilles :
#    - Feuille "Données" : Données nettoyées
#    - Feuille "Par région" : Agrégation par région
#    - Feuille "Par produit" : Agrégation par produit

with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer,sheet_name="Données",index=False)
    par_region.to_excel(writer,sheet_name="Par région",index=False)
    par_produit.to_excel(writer,sheet_name="Par produit",index=False)