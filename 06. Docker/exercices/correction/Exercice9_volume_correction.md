1. Créer un volume Docker nommé `data`.

```bash
docker volume create data
```

2. Lancer un premier conteneur basé sur `alpine`, en montant le volume dans `/home/votre-prenom`.

```bash
docker run -dit -v data:/home/loick --name container1 alpine 
```

3. Ouvrir un terminal dans le premier conteneur et créer un fichier dans le volume partagé.

```bash
docker exec -it container1 sh 
    cd /home/loick
    echo "Un nouveau fichier" > fichier.txt
    exit
```

4. Lancer un second conteneur utilisant le même volume.

```bash
docker run -dit -v data:/home/app --name container2 alpine 
```

5. Vérifier que le fichier créé par le premier conteneur est visible dans le second.

6. Modifier le fichier depuis le second conteneur.

```bash
docker exec -it container2 sh 
    cd /home/app
    ls 
    echo "Une modification depuis container2" >> fichier.txt
    exit
```

7. Vérifier dans le premier conteneur que la modification est bien visible.

```bash
docker exec -it container1 sh 
    cd /home/loick
    cat fichier.txt
    exit
```

8. Supprimer les conteneurs et le volume après le test.

```bash
docker stop container1
docker rm container1
docker stop container2
docker rm container2

docker volume rm data
```