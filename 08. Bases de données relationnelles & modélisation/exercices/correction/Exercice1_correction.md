### Scénario 1 : Système de messagerie distribué

**Scénario** : Un utilisateur envoie un message à un ami.

**Opérations** :

1. Enregistrer le message dans la base de données.
2. Propager le message aux différents nœuds du système.

**Question** : Quelle propriété (ACID ou BASE) doit être utilisée pour garantir que le message finira par être visible pour tous les utilisateurs, même s'il n'est pas immédiatement disponible ? Justifiez votre réponse.


**Reponse**: 
BASE -> Cohérence éventuelle: Le message peut ne pas être immédiatement visible par tous les utilisateurs. 
Cependant, après un certain délai, tous les noeuds du système finiront par avoir une copie cohérente du système.

### Scénario 2 : Réservation de billets d'avion

**Scénario** : Un client réserve un billet d'avion.

**Opérations** :

1. Vérifier la disponibilité du siège.
2. Réserver le siège.
3. Débiter le compte du client.

**Question** : Quelle propriété (ACID ou BASE) doit être utilisée pour garantir que le siège n'est pas réservé deux fois ? Justifiez votre réponse.

**Reponse**: 
ACID -> Cohérence: La base de donnée doit garantir que le siège n'est pas réservé deux fois. Si le siège est déjà reservé, la transaction doit échouer et le compte du client ne doit pas être débité.

### Scénario 3 : Système de recommandation

**Scénario** : Un système de recommandation met à jour les préférences des utilisateurs en fonction de leurs interactions.

**Opérations** :

1. Enregistrer les interactions des utilisateurs.
2. Mettre à jour les recommandations en fonction des interactions.

**Question** : Quelle propriété (ACID ou BASE) doit être utilisée pour permettre au système d'être dans un état intermédiaire où les recommandations ne sont pas immédiatement cohérentes ? Justifiez votre réponse.

**Reponse**: 
BASE -> Soft state: Le système peut être dans un état intermédiaire ou les recommandation ne sont pas immédiatement cohérentes avec les interactions les plus récentes. Elles finiront par converger vers un état cohérent, après un délai. 


### Scénario 4 : Sauvegarde de données

**Scénario** : Un utilisateur enregistre un nouveau document dans une base de données.

**Opérations** :

1. Insérer le document dans la base de données.
2. Valider la transaction (commit).

**Question** : Quelle propriété (ACID ou BASE) doit être utilisée pour garantir que les données ne seront pas perdues en cas de panne du système ? Justifiez votre réponse.

**Reponse**: 
ACID -> Durabilité: Une fois la transaction validé, le document doit être enregistré de manière permanente, même en cas de panne système. La base de donnée doit garantir que les données ne seront pas perdues. 

### Scénario 5 : Transfert bancaire

**Scénario** : Un client souhaite transférer 100 € de son compte d'épargne à son compte courant.

**Opérations** :

1. Débiter 100 € du compte d'épargne.
2. Créditer 100 € sur le compte courant.

**Question** : Quelle propriété (ACID ou BASE) doit être utilisée pour garantir que l'argent n'est pas perdu si une partie de la transaction échoue ? Justifiez votre réponse.

**Reponse**: 
ACID -> Atomicité : Si le début échoue, le crédit ne doit pas être effectué. La transaction doit être annulé (rollback) pour garantir que l'argent n'est pas perdu.


### Scénario 6 : Réseau social

**Scénario** : Un utilisateur publie un message sur un réseau social.

**Opérations** :

1. Enregistrer le message dans la base de données.
2. Notifier les amis de l'utilisateur.

**Question** : Quelle propriété (ACID ou BASE) doit être utilisée pour garantir que le message soit disponible même si certaines parties du système sont en panne ? Justifiez votre réponse.

**Reponse**: 
BASE -> Disponibilité de base : Même si certaines parties du système sont en panne. Le système doit toujours permettre à l'utilisateur de publier le message. Ce message sera disponible pour les utilisateurs qui peuvent accéder au système.

### Scénario 7 : Mise à jour de stock

**Scénario** : Deux transactions tentent de mettre à jour le stock d'un produit en même temps.

**Opérations** :

1. Transaction 1 : Vérifier le stock disponible.
2. Transaction 2 : Vérifier le stock disponible.
3. Transaction 1 : Mettre à jour le stock.
4. Transaction 2 : Mettre à jour le stock.

**Question** : Quelle propriété (ACID ou BASE) doit être utilisée pour éviter les conflits entre les transactions ? Justifiez votre réponse.

**Reponse**: 
ACID -> Isolation: Les transactions doivent être isolées pour éviter tout conflits. Si les deux transactions lisent le même stock disponible et tentent de le mettre à jour simultanément, cela pourrait entrainer des incohérences. L'isolation garantit que chaque transaction voit un état cohérent de la base de donnée.
