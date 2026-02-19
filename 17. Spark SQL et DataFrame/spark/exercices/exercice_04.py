from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, DoubleType
from pyspark.sql.functions import udf, col

# Créer la session Spark
spark = SparkSession.builder.master("local").appName("demo-udf").getOrCreate()

ventesData = [
  ("CMD001", "Alice Martin", "2024-03-15", "Électronique", 1299.99, 1, "Premium", "alice.martin@email.com"),
  ("CMD002", "Bob Durand", "2024-03-16", "Vêtements", 89.50, 3, "Standard", "bob.durand@email.com"),
  ("CMD003", "Claire Dubois", "2024-03-17", "Maison", 45.00, 2, "Premium", "claire.dubois@email.com"),
  ("CMD004", "David Moreau", "2024-03-18", "Sport", 199.99, 1, "Standard", "david.moreau@email.com"),
  ("CMD005", "Emma Petit", "2024-03-19", "Électronique", 799.00, 2, "VIP", "emma.petit@email.com"),
  ("CMD006", "Frank Lambert", "2024-03-20", "Livres", 29.99, 5, "Standard", "frank.lambert@email.com"),
  ("CMD007", "Grace Bernard", "2024-03-21", "Beauté", 156.75, 1, "Premium", "grace.bernard@email.com"),
  ("CMD008", "Henri Rousseau", "2024-03-22", "Électronique", 2199.00, 1, "VIP", "henri.rousseau@email.com")
]

df = spark.createDataFrame(ventesData, ["id_commande", "nom_client", "date_commande", "categorie", "prix_unitaire", "quantite", "statut_client", "email"])

df.show()

def classifier_ventes_func(prixUnitaire):
    if prixUnitaire < 50.0:
        return "Vente faible"
    elif 50.0 <= prixUnitaire <= 200:
        return "Vente moyenne"
    elif 200 <= prixUnitaire <= 1000:
        return "Vente élevée"
    else:
        return "vente prenium"
    
classifier_vente = udf(classifier_ventes_func, StringType())

def calculer_montant_total_func(prixUnitaire, quantite, statutClient):
    montantBrut = prixUnitaire * quantite

    if statutClient == "Standard":
        tauxRemise = 0.0
    elif statutClient == "Prenium":
        tauxRemise = 0.05
    elif statutClient == "VIP":
        tauxRemise = 0.10
    else:
        tauxRemise = 0.0

    montantFinal = montantBrut * (1 - tauxRemise)
    return montantFinal

calculer_montant_total = udf(calculer_montant_total_func, DoubleType())

def calculer_score_func(statutClient, montantTotal, categorie):
    if statutClient == "Standard":
        scoreBase = 1
    elif statutClient == "Prenium":
        scoreBase = 2
    elif statutClient == "VIP":
        scoreBase = 3
    else:
        scoreBase = 0

    if categorie == "Électronique":
        bonusCategorie = 2
    elif categorie == "Sport":
        bonusCategorie = 1
    else:
        bonusCategorie = 0

    bonusMontant = montantTotal // 100.0
    # bonusMontant = int(montantTotal / 100.0)
    return scoreBase + bonusCategorie + bonusMontant

calculer_score = udf(calculer_score_func, DoubleType())

dfFinal = df.withColumn("classifierVentes", classifier_vente(col("prix_unitaire"))) \
.withColumn("calculerMontantTotal", calculer_montant_total(col("prix_unitaire"), col("quantite"), col("statut_client"))) \
.withColumn("calculerScore", calculer_score(col("statut_client"), col("calculerMontantTotal"), col("categorie")))

dfFinal.show()