# Exercice dockerfile - python 

## Objectifs 

On souhaite créer une app python puis créer son image afin d'en faire un conteneur

# Taches

- Créer un script `main.py` :
    - Créer une fonction `login()` qui boucle tant que l'utilisateur n'a pas entrée un nom et un mot de passe précis. 
    - Afficher un message d'erreur si les logs saisies sont incorrects
    - Afficher un message de succès `Login accepté` si les logs sont correct. 

- Cree un dockerfile :
    - Récupérer une image `python` de dockerhub
    - Définisser le répertoire de travail dans /home/votre-nom
    - Copier le script python à l'intérieur
    - Et executer le script au lancement du conteneur

- Lancer un conteneur à partir de cette image et vérifier le bon fonctionnement. 
    - Il sera nécessaire de lancé le conteneur avec le terminal pour éviter que le conteneur se ferme automatiquement.