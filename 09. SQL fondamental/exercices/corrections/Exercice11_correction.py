import psycopg

DSN = "dbname=mydb user=admin password=admin host=localhost port=5432"

def init_db():
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS animaux;")
            cur.execute("DROP TABLE IF EXISTS regimes_alimentaires;")

            cur.execute("""
                CREATE TABLE IF NOT EXISTS regimes_alimentaires (
                    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    nom VARCHAR(50) UNIQUE NOT NULL
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS animaux (
                    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    nom VARCHAR(255) NOT NULL,
                    age INT NOT NULL,
                    regime_id INT REFERENCES regimes_alimentaires(id),
                    date_arrivee DATE NOT NULL
                );
            """)

            cur.execute("""
                INSERT INTO regimes_alimentaires (nom)
                VALUES ('herbivore'), ('carnivore'), ('omnivore');
            """)

    print("Base initialisée !")

def menu_regime():
    print("\n===== Regime alimentaire =====")
    print("1 - Herbivore")
    print("2 - Carnivore")
    print("3 - Omnivore")

def creer_animal():
    nom = input("Nom de l'animal : ")
    age = int(input("Âge : "))
    menu_regime()
    regime_id = input("Choix : ")
    date_arrivee = input("Date d'arrivée (YYYY-MM-DD) : ")

    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM regimes_alimentaires WHERE id = %s", (regime_id,))
            regime = cur.fetchone()

            if not regime:
                print("Régime inconnu !")
                return

            regime_id = regime[0]

            cur.execute("""
                INSERT INTO animaux (nom, age, regime_id, date_arrivee)
                VALUES (%s, %s, %s, %s)
            """, (nom, age, regime_id, date_arrivee))

    print("Animal ajouté !")

def rechercher_par_id():
    animal_id = input("ID de l'animal : ")

    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT a.id, a.nom, a.age, r.nom AS regime, a.date_arrivee
                FROM animaux a
                INNER JOIN regimes_alimentaires r ON a.regime_id = r.id
                WHERE a.id = %s
            """, (animal_id,))
            animal = cur.fetchone()

    if not animal:
        print("Aucun animal trouvé.")
    else:
        print("Animal trouvé :")
        print(animal)

def rechercher_par_nom():
    nom = input("Nom de l'animal : ")

    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT a.id, a.nom, a.age, r.nom AS regime, a.date_arrivee
                FROM animaux a
                INNER JOIN regimes_alimentaires r ON a.regime_id = r.id
                WHERE LOWER(a.nom) = LOWER(%s)
            """, (nom,))
            animaux = cur.fetchall()

    if not animaux:
        print("Aucun animal trouvé.")
    else:
        print("Animaux trouvés :")
        for a in animaux:
            print(a)

def rechercher_par_regime():
    menu_regime()
    regime_id = input("Choix : ")

    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT a.id, a.nom, a.age, r.nom AS regime, a.date_arrivee
                FROM animaux a
                INNER JOIN regimes_alimentaires r ON a.regime_id = r.id
                WHERE r.id = %s
            """, (regime_id,))
            animaux = cur.fetchall()

    if not animaux:
        print("Aucun animal avec ce régime.")
    else:
        print("Animaux :")
        for a in animaux:
            print(a)

def afficher_menu():
    print("\n===== MENU ZOO =====")
    print("1 - Ajouter un animal")
    print("2 - Rechercher par ID")
    print("3 - Rechercher par nom")
    print("4 - Rechercher par régime")
    print("0 - Quitter")
    print()

def ihm():
    while True:
        afficher_menu()
        choix = input("Votre choix : ")

        match choix:
            case "1":
                creer_animal()
            case "2":
                rechercher_par_id()
            case "3":
                rechercher_par_nom()
            case "4":
                rechercher_par_regime()
            case "0":
                print("Au revoir !")
                break
            case _:
                print("Choix invalide.")

if __name__ == "__main__":
    init_db()
    ihm()