# solutions_tp_mongodb.py
from pymongo import MongoClient
import json

def connexion():
    """Établit la connexion à MongoDB et charge les données"""
    client = MongoClient('mongodb://admin:password@localhost:27017/?authSource=admin')
    db = client['tp_mongodb']
    collection = db['students']
    collection.drop()
    data = []
 
    with open("students.json", "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))

    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)
        

    return client, collection

def afficher_separateur(titre):
    """Affiche un séparateur visuel"""
    print("\n" + "="*70)
    print(f"  {titre}")
    print("="*70)

# ============================================================
# PARTIE 1 - REQUÊTES SIMPLES 
# ============================================================

def question_1():
    """Q1: Affichez le premier document de la collection"""
    afficher_separateur("Question 1 - Premier document")
    
    client, collection = connexion()
    
    premier = collection.find_one()
    
    print(f"ID: {premier['_id']}")
    print(f"Nom: {premier['name']}")
    print(f"Scores:")
    for score in premier['scores']:
        print(f"  - {score['type']}: {score['score']:.2f}")
    
   
    client.close()

def question_2():
    """Q2: Comptez le nombre total d'étudiants"""
    afficher_separateur("Question 2 - Nombre total d'étudiants")
    
    client, collection = connexion()
    
 
    total = collection.count_documents({})
    
    print(f"Nombre total d'étudiants: {total}")
    
    client.close()

def question_3():
    """Q3: Trouvez et affichez l'étudiant nommé 'Aurelia Menendez'"""
    afficher_separateur("Question 3 - Recherche par nom")
    
    client, collection = connexion()
    
    
    etudiant = collection.find_one({"name": "Aurelia Menendez"})
    
    if etudiant:
        print(f"ID: {etudiant['_id']}")
        print(f"Nom: {etudiant['name']}")
        print(f"Scores:")
        for score in etudiant['scores']:
            print(f"  - {score['type']}: {score['score']:.2f}")
    else:
        print("Étudiant non trouvé")
    
    client.close()

def question_4():
    """Q4: Trouvez l'étudiant avec _id = 50"""
    afficher_separateur("Question 4 - Recherche par ID")
    
    client, collection = connexion()
    
   
    etudiant = collection.find_one({"_id": 50})
    
    if etudiant:
        print(f"ID: {etudiant['_id']}")
        print(f"Nom: {etudiant['name']}")
        print(f"Scores:")
        for score in etudiant['scores']:
            print(f"  - {score['type']}: {score['score']:.2f}")
    
    client.close()

def question_5():
    """Q5: Trouvez tous les étudiants qui n'ont pas de nom"""
    afficher_separateur("Question 5 - Étudiants sans nom")
    
    client, collection = connexion()
       
    etudiants_sans_nom = collection.find({"name": ""})
    
    print("Étudiants sans nom:")
    count = 0
    for etudiant in etudiants_sans_nom:
        print(f"  - ID: {etudiant['_id']}")
        count += 1
    
    print(f"\nTotal: {count} étudiant(s) sans nom")
    
    client.close()

def question_6():
    """Q6: Affichez uniquement les noms des 10 premiers étudiants"""
    afficher_separateur("Question 6 - Noms des 10 premiers")
    
    client, collection = connexion()
    
    etudiants = collection.find({}, {"name": 1, "_id": 0}).limit(10)
    
    print("Les 10 premiers noms:")
    for i, etudiant in enumerate(etudiants, 1):
        print(f"  {i}. {etudiant['name']}")
    
    client.close()

def question_7():
    """Q7: Affichez les 5 premiers étudiants triés par ordre alphabétique"""
    afficher_separateur("Question 7 - Tri alphabétique")
    
    client, collection = connexion()
    
    etudiants = collection.find({"name": {"$ne": ""}}).sort("name", 1).limit(5)
    
    print("Les 5 premiers noms (ordre alphabétique):")
    for i, etudiant in enumerate(etudiants, 1):
        print(f"  {i}. {etudiant['name']} (ID: {etudiant['_id']})")
    
    client.close()

# ============================================================
# PARTIE 2 - MANIPULATION DES TABLEAUX 
# ============================================================

def question_8():
    """Q8: Extrayez la note d'examen de l'étudiant _id=0"""
    afficher_separateur("Question 8 - Note d'examen d'un étudiant")
    
    client, collection = connexion()
    
   
    etudiant = collection.find_one({"_id": 0})
    
    if etudiant:
        for score in etudiant['scores']:
            if score['type'] == 'exam':
                print(f"Étudiant: {etudiant['name']}")
                print(f"Note d'examen: {score['score']:.2f}")
                break
    
    client.close()

def question_9():
    """Q9: Calculez la moyenne des 3 notes de l'étudiant _id=1"""
    afficher_separateur("Question 9 - Moyenne d'un étudiant")
    
    client, collection = connexion()
    

    etudiant = collection.find_one({"_id": 1})
    
    if etudiant:
       
        total = sum(score['score'] for score in etudiant['scores'])
        moyenne = total / len(etudiant['scores'])
        
        print(f"Étudiant: {etudiant['name']}")
        print(f"Notes:")
        for score in etudiant['scores']:
            print(f"  - {score['type']}: {score['score']:.2f}")
        print(f"\nMoyenne: {moyenne:.2f}")
    
    client.close()

def question_10():
    """Q10: Utilisez $unwind pour déplier le tableau scores"""
    afficher_separateur("Question 10 - Utilisation de $unwind")
    
    client, collection = connexion()
    
    pipeline = [
        {"$unwind": "$scores"},  # Déplie le tableau scores
        {"$limit": 5}            # Limite à 5 résultats
    ]
    
    resultats = collection.aggregate(pipeline)
    
    print("5 premiers résultats après $unwind:")
    for i, doc in enumerate(resultats, 1):
        print(f"\n{i}. ID: {doc['_id']} - {doc['name']}")
        print(f"   Type: {doc['scores']['type']}")
        print(f"   Score: {doc['scores']['score']:.2f}")
    
    client.close()

# ============================================================
# PARTIE 3 - AGRÉGATIONS
# ============================================================

def question_11():
    """Q11: Calculez la moyenne générale de chaque étudiant (top 10)"""
    afficher_separateur("Question 11 - Top 10 des moyennes")
    
    client, collection = connexion()
    
    pipeline = [
        {"$unwind": "$scores"},                    # Déplie les scores
        {"$group": {                               # Groupe par étudiant
            "_id": "$_id",
            "name": {"$first": "$name"},
            "moyenne": {"$avg": "$scores.score"}   # Calcule la moyenne
        }},
        {"$sort": {"moyenne": -1}},                # Tri décroissant
        {"$limit": 10}                             # Top 10
    ]
    
    resultats = collection.aggregate(pipeline)
    
    print("Top 10 des meilleures moyennes:")
    for i, etudiant in enumerate(resultats, 1):
        print(f"  {i}. {etudiant['name']} (ID: {etudiant['_id']}): {etudiant['moyenne']:.2f}")
    
    client.close()

def question_12():
    """Q12: Moyenne par type d'évaluation"""
    afficher_separateur("Question 12 - Moyenne par type")
    
    client, collection = connexion()

    pipeline = [
        {"$unwind": "$scores"},                    # Déplie les scores
        {"$group": {                               # Groupe par type
            "_id": "$scores.type",
            "moyenne": {"$avg": "$scores.score"}   # Calcule la moyenne
        }},
        {"$sort": {"_id": 1}}                      # Tri alphabétique
    ]
    
    resultats = collection.aggregate(pipeline)
    
    print("Moyenne par type d'évaluation:")
    for resultat in resultats:
        print(f"  {resultat['_id']}: {resultat['moyenne']:.2f}")
    
    client.close()

def question_13():
    """Q13: Meilleure note par type d'évaluation"""
    afficher_separateur("Question 13 - Meilleure note par type")
    
    client, collection = connexion()
    
    pipeline = [
        {"$unwind": "$scores"},                    # Déplie les scores
        {"$sort": {"scores.score": -1}},           # Tri décroissant par score
        {"$group": {                               # Groupe par type
            "_id": "$scores.type",
            "meilleur_etudiant": {"$first": "$name"},
            "meilleur_score": {"$first": "$scores.score"}
        }},
        {"$sort": {"_id": 1}}                      # Tri alphabétique
    ]
    
    resultats = collection.aggregate(pipeline)
    
    print("Meilleure note par type:")
    for resultat in resultats:
        print(f"  {resultat['_id']}: {resultat['meilleur_score']:.2f} par {resultat['meilleur_etudiant']}")
    
    client.close()

def question_14():
    """Q14: Min, max, moyenne pour chaque étudiant"""
    afficher_separateur("Question 14 - Statistiques par étudiant")
    client, collection = connexion()
    pipeline = [
        {"$unwind": "$scores"},
        {"$group": {
            "_id": "$_id",
            "name": {"$first": "$name"},
            "minimum": {"$min": "$scores.score"},
            "maximum": {"$max": "$scores.score"},
            "moyenne": {"$avg": "$scores.score"}
        }},
        {"$sort": {"moyenne": -1}},
        {"$limit": 10}  
    ]
    resultats = collection.aggregate(pipeline)
    print("Statistiques des 10 meilleurs étudiants:")
    for i, etudiant in enumerate(resultats, 1):
        print(f"\n{i}. {etudiant['name']} (ID: {etudiant['_id']})")
        print(f"   Min: {etudiant['minimum']:.2f}")
        print(f"   Max: {etudiant['maximum']:.2f}")
        print(f"   Moyenne: {etudiant['moyenne']:.2f}")
    
    client.close()

def question_15():
    """Q15: Nombre d'étudiants avec moyenne > 70"""
    afficher_separateur("Question 15 - Étudiants avec moyenne > 70")
    
    client, collection = connexion()
    
    pipeline = [
        {"$unwind": "$scores"},
        {"$group": {
            "_id": "$_id",
            "name": {"$first": "$name"},
            "moyenne": {"$avg": "$scores.score"}
        }},
        {"$match": {"moyenne": {"$gt": 70}}},  # Filtre moyenne > 70
        {"$count": "nombre"}                    # Compte les résultats
    ]
    
    resultats = list(collection.aggregate(pipeline))
    
    if resultats:
        print(f"Nombre d'étudiants avec moyenne > 70: {resultats[0]['nombre']}")
    else:
        print("Aucun étudiant avec moyenne > 70")
    
    client.close()

# ============================================================
# PARTIE 4 - MISES À JOUR 
# ============================================================

def question_16():
    """Q16: Ajoutez un champ moyenne à tous les documents"""
    afficher_separateur("Question 16 - Ajout champ moyenne")
    
    client, collection = connexion()
    etudiants = collection.find()
    count = 0
    for etudiant in etudiants:
        total = sum(score['score'] for score in etudiant['scores'])
        moyenne = total / len(etudiant['scores'])
        collection.update_one(
            {"_id": etudiant['_id']},
            {"$set": {"moyenne": moyenne}}
        )
        count += 1
    print(f"✓ Champ 'moyenne' ajouté à {count} étudiants")
    

    print("\nExemples:")
    exemples = collection.find().limit(3)
    for etudiant in exemples:
        print(f"  {etudiant['name']}: moyenne = {etudiant.get('moyenne', 'N/A'):.2f}")
    
    client.close()

def question_17():
    """Q17: Ajoutez un champ niveau selon la moyenne"""
    afficher_separateur("Question 17 - Ajout champ niveau")
    
    client, collection = connexion()
    
 
    if collection.find_one({"moyenne": {"$exists": False}}):
        print("Calcul des moyennes d'abord...")
        question_16()
        client, collection = connexion()
    

    etudiants = collection.find()
    
    count = 0
    for etudiant in etudiants:
        moyenne = etudiant.get('moyenne', 0)
        
        if moyenne >= 80:
            niveau = "Excellent"
        elif moyenne >= 60:
            niveau = "Bien"
        elif moyenne >= 40:
            niveau = "Passable"
        else:
            niveau = "Insuffisant"
        
       
        collection.update_one(
            {"_id": etudiant['_id']},
            {"$set": {"niveau": niveau}}
        )
        count += 1
    
    print(f"✓ Champ 'niveau' ajouté à {count} étudiants")
    

    pipeline = [
        {"$group": {
            "_id": "$niveau",
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]
    
    stats = collection.aggregate(pipeline)
    print("\nRépartition par niveau:")
    for stat in stats:
        print(f"  {stat['_id']}: {stat['count']} étudiant(s)")
    
    client.close()

def question_18():
    """Q18: Supprime la plus faible note de homework (globale)"""
    afficher_separateur("Question 18 - Suppression du pire homework global")
 
    client, collection = connexion()
 
    pipeline = [
        {"$unwind": "$scores"},
        {"$match": {"scores.type": "homework"}},
        {"$sort": {"scores.score": 1}},
        {"$limit": 1}
    ]
 
    result = list(collection.aggregate(pipeline))
 
    if not result:
        print("Aucune note de homework trouvée")
        client.close()
        return
 
    worst = result[0]
    student_id = worst["_id"]
    score = worst["scores"]["score"]
 
    collection.update_one(
        {"_id": student_id},
        {"$pull": {"scores": {"type": "homework", "score": score}}}
    )
 
    print(f"✓ Homework le plus faible supprimé : {score:.2f}")
    print(f"  Étudiant concerné : ID {student_id}")
 
    client.close()

def question_19():
    """Q19: Mettez à jour le nom de l'étudiant _id=113"""
    afficher_separateur("Question 19 - Mise à jour nom étudiant 113")
    
    client, collection = connexion()
    

    avant = collection.find_one({"_id": 113})
    print(f"Avant: ID 113, nom = '{avant['name']}'")

    resultat = collection.update_one(
        {"_id": 113},
        {"$set": {"name": "Nom Inconnu"}}
    )
    

    apres = collection.find_one({"_id": 113})
    print(f"Après: ID 113, nom = '{apres['name']}'")
    print(f"\n✓ {resultat.modified_count} document modifié")
    
    client.close()


# ============================================================
# FONCTION PRINCIPALE
# ============================================================

def main():
            question_1()
   
            question_2()

            question_3()

            question_4()
   
            question_5()
    
            question_6()
     
            question_7()

            question_8()
  
            question_9()
   
            question_10()
  
            question_11()

            question_12()

            question_13()
      
            question_14()
      
            question_15()
   
            question_16()
       
            question_17()
    
            question_18()
    
            question_19()
   

if __name__ == "__main__":
    main()