# Pour importer psycopg, il est nécessaire d'installer au préalable la bibliothèque correspondante
# commande : pip install psycopg
#            pip install --upgrade psycopg[binary]
import psycopg

# Pour créer une connection, il est nécessaire de donnée les informations lié à notre base de données.
connection = psycopg.connect(
    dbname="mydb",
    user="admin",
    password="admin",
    host="localhost",
    port="5433"
)

# Création d'un curseur (il permet de se déplacer dans la bdd et d'envoyer des requêtes)
cur = connection.cursor()

# Pour préparer une requete SQL, nous devons utiliser le curseur suivit du mot-clé execute.
# Les execute ne sont pas transmit directement à la BDD mais mis en attente d'envoie.
cur.execute("DROP TABLE IF EXISTS users;")

cur.execute("""
    CREATE TABLE users (
        id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,    
        age INT
    );
""")

# Le commit, va permettre d'envoyer toutes les requêtes préparer dans le curseur à la BDD (l'ordre est respecté)
connection.commit() 

print("Table users créée.")


# Je supprime le "pointeur" de ma BDD
cur.close()

# Fermer la connection après utilisation
connection.close()

# Une façon plus propre serait d'ouvrir la connection, effectuer une requete puis refermer celle-ci directement.
# De cette manière, nous somme sur de n'avoir aucun conflits entre plusieurs connections.
DSN = "dbname=mydb user=admin password=admin host=localhost port=5433"

# Un moyen pratique est d'utiliser l'ouverture avec ressources via le mot-clé "with"
with psycopg.connect(DSN) as conn:
    with conn.cursor() as cur:
        cur.execute("INSERT INTO users (first_name, last_name, age) VALUES ('toto','titi',32)")
        # Le commit est automatique après chaque execute
        cur.execute("SELECT * FROM users;")
        rows = cur.fetchall() # Recupération des informations reçu par le curseur.
        print(rows)
    # Fermeture du curseur
# Fermeture de notre connections

# Bien entendu, il est possible de récupérer des exceptions lié à la BDD ou au requete SQL.
# Pour les gérer, nous pouvons placer la connection ainsi que les requete dans un bloc try.
try:
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELEC * FROM users;") # users n'a pas de s, cette requete va provoquer une exceptions
            rows = cur.fetchall()
            print(rows)
except psycopg.errors.SyntaxError as e: 
    print ("Erreur SQL : ", e)
except psycopg.errors.UniqueViolation as e:
    print ("Violation Unique : ", e)
except psycopg.OperationalError as e:
    print ("Problème de connection :" , e)
except Exception as e:
    print ("Autre erreurs : ", e)


# ================ INSERTION ====================

user_id = 0

try:
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            # Pour éviter l'injection SQL, nous n'écrivons pas les données fournit par l'utilisateur directement dans notre requete
            # Nous lui fournissons un tuple contenant les informations qui ne seront pas interprété.
            cur.execute(
                "INSERT INTO users (first_name, last_name, age) VALUES (%s, %s, %s) RETURNING id;",
                ("titi", "tutu", 30)
            )
            user_id = cur.fetchone()[0] # Ici, je recupère l'information reçu par le curseur.
            print("User crée avec l'id : ", user_id)
except Exception as e:
    print ("Erreur à l'insertion d'un utilisateur : ", e)

# ================ UPDATE ====================

try:
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE users
                SET age = %s
                WHERE id = %s
                RETURNING id
            """, (25, user_id)
            )
            updated = cur.fetchone() # Si aucun resultat correspondant, alors nous recevons NULL

            if updated:
                print("Utilisateur d'id ", user_id, " mis à jours.")
            else:
                print("Utilsateur avec id inconnue : ", user_id)
except Exception as e:
    print ("Erreur à l'insertion d'un utilisateur : ", e)

# ================ LECTURE ====================

try:
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users;")
            rows = cur.fetchall()
except Exception as e:
    print ("Autre erreurs : ", e)

for row in rows:
    print(row)

try:
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
            row = cur.fetchone()
            print(row[1], row[2], row[3])
except Exception as e:
    print ("Autre erreurs : ", e)

# ================ Suppression ====================

try:
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM users WHERE id = %s RETURNING id"
                , (user_id,)
            )
            deleted = cur.fetchone()

            if deleted:
                print("Utilisateur d'id ", user_id, " supprimé.")
            else:
                print("Utilisateur avec id inconnue : ", user_id)
except Exception as e:
    print ("Erreur à l'insertion d'un utilisateur : ", e)