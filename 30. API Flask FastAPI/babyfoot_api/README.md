# guide api babyfoot

pour lancer le projet
- installer les dependances avec la commande **`pip install -r requirements.txt`**
- puis lancer le serveur avec **`python -m app.main`** et ouvrir http://127.0.0.1:8000/docs dans le navigateur

pour tester l'inscription
- aller sur auth register avec un pseudo et un mot de passe de 8 caracteres minimum contenant une majuscule et un chiffre

pour tester la connexion
- aller sur auth token avec les identifiants pour recuperer la chaine de caracteres access_token

pour tester l'acces securise
- cliquer sur le bouton authorize en haut de la page docs et coller le token dedans pour debloquer les cadenas des autres routes

pour tester les joueurs
- creer des pseudos via sport players et regarder les id attribues dans la reponse

pour tester les equipes
- creer une equipe via sport teams avec les id des joueurs et verifier que mettre deux fois le meme id de joueur provoque bien une erreur 422 de validation

information importante
**les donnees sont stockees en memoire vive donc tout est efface si le serveur s'arrete ou si le code est modifie**