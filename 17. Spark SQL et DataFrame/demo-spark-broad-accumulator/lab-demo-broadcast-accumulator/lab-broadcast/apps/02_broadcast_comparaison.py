from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast, col, sum, avg, count
import time
import random



spark = SparkSession.builder \
    .appName("BroadcastComparison") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")


transactions_data = [
    (i, f"P{random.randint(1, 100):03d}", f"C{random.randint(1, 1000):04d}", 
     random.choice(["Paris", "Lyon", "Marseille", "Toulouse", "Nice"]),
     round(random.uniform(10, 500), 2), random.randint(1, 10))
    for i in range(2_000_000)
]

transactions = spark.createDataFrame(
    transactions_data,
    ["transaction_id", "produit_id", "client_id", "ville", "montant", "quantite"]
).repartition(12)

transactions.cache()
nb_transactions = transactions.count()

produits_data = [
    (f"P{i:03d}", f"Produit {i}", f"Cat_{i % 10}", round(random.uniform(5, 100), 2))
    for i in range(1, 101)
]

produits = spark.createDataFrame(
    produits_data,
    ["produit_id", "nom_produit", "categorie", "cout_achat"]
)

produits.cache()
nb_produits = produits.count()


print(f"\n Transactions: {nb_transactions:,} lignes")
print(f" Produits: {nb_produits} lignes")


print("\n" + "=" * 60)
print("TEST 1 : JOIN SANS BROADCAST (Shuffle Join)")
print("=" * 60)

start = time.time()

resultat_shuffle = transactions.join(
    produits,
    on="produit_id",
    how="inner"
).groupBy("categorie") \
 .agg(
     sum(col("montant") * col("quantite")).alias("ca_total"),
     count("*").alias("nb_ventes")
 )

resultat_shuffle.collect()
temps_shuffle = time.time() - start

print(f"\n Temps SANS broadcast: {temps_shuffle:.2f} secondes")


print("\n" + "=" * 60)
print("TEST 2 : JOIN AVEC BROADCAST ")
print("=" * 60)
print(" Seule la table produits (100 lignes) est envoyée aux workers...")


start = time.time()

resultat_bro = transactions.join(
    broadcast(produits),
    on="produit_id",
    how="inner"
).groupBy("categorie") \
 .agg(
     sum(col("montant") * col("quantite")).alias("ca_total"),
     count("*").alias("nb_ventes")
 )

resultat_bro.collect()
temps_bro= time.time() - start

print(f"\n Temps AVEC broadcast: {temps_bro:.2f} secondes")


print("\n" + "=" * 60)
print("RÉSULTATS COMPARATIFS")
print("=" * 60)
print(f" Shuffle Join  : {temps_shuffle:.2f}s")
print(f" Broadcast Join: {temps_bro:.2f}s")

if temps_shuffle > temps_bro:
    gain = ((temps_shuffle - temps_bro) / temps_shuffle * 100)
    print(f" Gain de performance: {gain:.1f}%")
else:
    print("  Pas de gain significatif (données trop petites ou cache)")