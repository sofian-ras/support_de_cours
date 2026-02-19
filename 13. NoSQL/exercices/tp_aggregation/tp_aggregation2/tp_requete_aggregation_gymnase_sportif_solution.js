use("sport")


// 1. Quels sont les sportifs (identifiant, nom et prénom) qui ont un
// âge entre 20 et 30 ans ?
db.sportifs.find({ "Age": { $gte: 20, $lte: 30 } }, { _id: 0, "IdSportif": 1, "Nom": 1, "Prenom": 1, "Age": 1 })


// 2. Quels sont les gymnases de ville “Villetaneuse” ou de
// “Sarcelles” qui ont une surface de plus de 400 m2 ?
db.gymnase.find({ $or: [{ "Ville": "VILLETANEUSE" }, { "Ville": "SARCELLES" }], "Surface": { $gt: 400 } })

// 3. Quels sont les sportifs (identifiant et nom) qui pratiquent du
// handball ?
db.sportifs.find({ "Sports.Jouer": "Hand ball" }, { _id: 0, "IdSportif": 1 ,"Nom": 1})

// 4. Quels sportifs (identifiant et nom) ne pratiquent aucun sport ?
db.sportifs.find({ "Sports.Jouer": { $exists: false } }, { _id: 0, "IdSportif": 1 ,"Nom": 1})

// 5. Quels gymnases n’ont pas de séances le dimanche ? (attention à la casse !)
db.gymnase.find({ "Seances.Jour": { $not: {$regex: /^dimanche/, $options: 'i'}} }) 


// 6. Quels gymnases ne proposent que des séances de basket ball ou de volley ball ? ?
db.gymnase.find({
  Seances: {
    $not: {
      $elemMatch: {
        Libelle: { $nin: ["Basket ball", "Volley ball"] }
      }
    }
  }
})



// 7. Quels sont les entraîneurs qui sont aussi joueurs ?
db.sportifs.find({ $and: [{ "Sports.Entrainer": { $exists: true } }, { "Sports.Jouer": { $exists: true } }] })



// 8. Pour le sportif “Kervadec” quel est le nom de son conseiller ?
db.sportifs.aggregate([
    { $match: { "Nom": "KERVADEC" } },
    {
        $lookup: {
            from: "sportifs", // table externe
            localField: "IdSportifConseiller", // id de l'utilisateur
            foreignField: "IdSportif", // la clé de l'adresse
            as: "Coach" // nom de la nouvelle clé (sans espace à la fin)
        }
    }
])


// 9. Quelle est la moyenne d’âge des sportives qui pratiquent du
// basket ball ?
db.sportifs.aggregate([
    { $match: { "Sports.Jouer": "Basket ball" } },
    { $group: { _id: null, "Moyenne": { $avg: "$Age" } } }
])


// 10.Quels entraîneurs n’entraînent que du hand ball ou du basket ball ? TODO
db.sportifs.aggregate([
  {
    $addFields: {
      entrainerArray: {
        $cond: {
          if: { $isArray: "$Sports.Entrainer" },
          then: "$Sports.Entrainer",
          else: [ "$Sports.Entrainer" ]
        }
      }
    }
  },
  {
    $match: {
      $expr: {
        $setIsSubset: ["$entrainerArray", ["Hand ball", "Basket ball"]]
      }
    }
  },
  {
    $project: { Nom: 1, Prenom: 1, "Sports.Entrainer": 1 }
  }
])


// 11. Pour chaque sportif donner le nombre de sports qu’il arbitre?
db.sportifs.aggregate([
    { $unwind: "$Sports.Arbitrer" },
    { $group: { _id: "$IdSportif", "NbSports_arbitrer": { $sum: 1 }, "Nom": { $first: "$Nom" } } },
    { $project: {
      _id: 0,  
      Nom: 1,
      NbSports_arbitrer: 1
    }},
    { $sort: { NbSports_arbitrer: -1 } }  
])
