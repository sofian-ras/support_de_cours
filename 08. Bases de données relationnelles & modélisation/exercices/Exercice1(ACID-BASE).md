# Exercice : Identification des Propriétés ACID et BASE

## Contexte

Dans le domaine des bases de données, les propriétés ACID (Atomicité, Cohérence, Isolation, Durabilité) et BASE (Disponibilité de base, État souple, Cohérence éventuelle) sont cruciales pour garantir la fiabilité et la disponibilité des systèmes de gestion de bases de données. Cet exercice vise à vous aider à comprendre et à appliquer ces propriétés dans des contextes réels.

## Instructions

Pour chaque scénario décrit ci-dessous, identifiez quelle propriété (ACID ou BASE) doit être utilisée pour garantir la fiabilité et la disponibilité du système. Justifiez votre choix en expliquant pourquoi cette propriété est nécessaire dans le contexte donné.

### Scénario 1 : Système de messagerie distribué

**Scénario** : Un utilisateur envoie un message à un ami.

**Opérations** :

1. Enregistrer le message dans la base de données.
2. Propager le message aux différents nœuds du système.

**Question** : Quelle propriété (ACID ou BASE) doit être utilisée pour garantir que le message finira par être visible pour tous les utilisateurs, même s'il n'est pas immédiatement disponible ? Justifiez votre réponse.

### Scénario 2 : Réservation de billets d'avion

**Scénario** : Un client réserve un billet d'avion.

**Opérations** :

1. Vérifier la disponibilité du siège.
2. Réserver le siège.
3. Débiter le compte du client.

**Question** : Quelle propriété (ACID ou BASE) doit être utilisée pour garantir que le siège n'est pas réservé deux fois ? Justifiez votre réponse.

### Scénario 3 : Système de recommandation

**Scénario** : Un système de recommandation met à jour les préférences des utilisateurs en fonction de leurs interactions.

**Opérations** :

1. Enregistrer les interactions des utilisateurs.
2. Mettre à jour les recommandations en fonction des interactions.

**Question** : Quelle propriété (ACID ou BASE) doit être utilisée pour permettre au système d'être dans un état intermédiaire où les recommandations ne sont pas immédiatement cohérentes ? Justifiez votre réponse.

### Scénario 4 : Sauvegarde de données

**Scénario** : Un utilisateur enregistre un nouveau document dans une base de données.

**Opérations** :

1. Insérer le document dans la base de données.
2. Valider la transaction (commit).

**Question** : Quelle propriété (ACID ou BASE) doit être utilisée pour garantir que les données ne seront pas perdues en cas de panne du système ? Justifiez votre réponse.

### Scénario 5 : Transfert bancaire

**Scénario** : Un client souhaite transférer 100 € de son compte d'épargne à son compte courant.

**Opérations** :

1. Débiter 100 € du compte d'épargne.
2. Créditer 100 € sur le compte courant.

**Question** : Quelle propriété (ACID ou BASE) doit être utilisée pour garantir que l'argent n'est pas perdu si une partie de la transaction échoue ? Justifiez votre réponse.

### Scénario 6 : Réseau social

**Scénario** : Un utilisateur publie un message sur un réseau social.

**Opérations** :

1. Enregistrer le message dans la base de données.
2. Notifier les amis de l'utilisateur.

**Question** : Quelle propriété (ACID ou BASE) doit être utilisée pour garantir que le message soit disponible même si certaines parties du système sont en panne ? Justifiez votre réponse.

### Scénario 7 : Mise à jour de stock

**Scénario** : Deux transactions tentent de mettre à jour le stock d'un produit en même temps.

**Opérations** :

1. Transaction 1 : Vérifier le stock disponible.
2. Transaction 2 : Vérifier le stock disponible.
3. Transaction 1 : Mettre à jour le stock.
4. Transaction 2 : Mettre à jour le stock.

**Question** : Quelle propriété (ACID ou BASE) doit être utilisée pour éviter les conflits entre les transactions ? Justifiez votre réponse.

## Soumission

Rédigez vos réponses dans un document séparé et soumettez-le pour évaluation. Assurez-vous d'inclure une justification claire pour chaque choix de propriété.

Bonne chance !