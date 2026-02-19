# Exercice : Volume Docker

## Objectifs :

- Comprendre le fonctionnement des volumes Docker.
- Mettre en place un volume partagé entre deux conteneurs.
- Vérifier la synchronisation des fichiers entre les conteneurs.

## Tâches :

1. Créer un volume Docker nommé `data`.

2. Lancer un premier conteneur basé sur `alpine`, en montant le volume.

3. Ouvrir un terminal dans le premier conteneur et créer un fichier dans le volume partagé.

4. Lancer un second conteneur utilisant le même volume.

5. Vérifier que le fichier créé par le premier conteneur est visible dans le second.

6. Modifier le fichier depuis le second conteneur.

7. Vérifier dans le premier conteneur que la modification est bien visible.

8. Supprimer les conteneurs et le volume après le test.