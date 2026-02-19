# Commandes docker compose

## Démarrer tous les services :

```bash
docker compose up 
```

## Démarrer tous les services en arrière-plan : 

```bash
docker compose up -d  
```

## Démarrer un ou plusieurs services spécifiques : 

```bash
docker compose up service1 service2 
```

## Arrêter tous les services : 

```bash
docker compose down 
```

## Arrêter tous les services, supprimer les volumes et les images : 

```bash
docker compose down --volumes --rmi all 
```

## Arrêter les conteneurs sans les supprimer : 

```bash
docker compose stop  
```

## Relancer les conteneurs arrêté : 

```bash
docker compose start  
```

## Supprimer les conteneurs arrêté :

```bash
docker compose rm
```

## Voir l'état des services : 

```bash
docker compose ps 
```

## Afficher les logs de tout les services : 

```bash
docker compose logs 
```

## Afficher les logs en direct : 

```bash
docker compose logs -f  
```

## Exécuter une commande dans un service en cours d'executions : 

```bash
docker compose exec service commande 
```

## Exécuter une commande dans un nouveau conteneur : 

```bash
docker compose run service commande
```

## Afficher les images utilisé par les services : 

```bash
docker compose images
```

## Afficher les volumes crées : 

```bash
docker compose volume ls
```