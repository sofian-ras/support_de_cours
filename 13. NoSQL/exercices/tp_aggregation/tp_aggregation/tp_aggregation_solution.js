use("biblio");

// // 1. Trier les publications de « Toru Ishida » par titre de livre et par page de début.
db.livres.aggregate([
    { $match: { "authors": "Toru Ishida" } },
    { $sort: { "title": 1, "pages.start": 1 } }
])

// // 2. Projeter le résultat sur le titre de la publication, et les pages.
db.livres.aggregate([
    { $match: { "authors": "Toru Ishida" } },
    { $sort: { "title": 1, "pages.start": 1 } },
    { $project: { "title": 1, "pages.start": 1 } }
])

// // 3. Compter le nombre de ses publications.
db.livres.aggregate([
    { $match: { "authors": "Toru Ishida" } },
    { $count: "nombres_publications" }
])

// // 4. Compter le nombre de publications depuis 2011 et par type.
db.livres.aggregate([
    {
        $match: {
            "year": {
                $gte: 2011
            }
        }
    },
    {
        $group: {
            _id: "$type",
            total_par_type_publication: {
                $sum: 1
            }
        }
    }
])


// 5. Compter le nombre de publications par auteur et trier le résultat par ordre croissant.
db.livres.aggregate([
    {
        $unwind: "$authors",
    },
    {
        $group: {
            _id: "$authors",
            total_par_auteur_publication: {
                $sum: 1
            }
        }
    },
    {
        $sort: {
            total_par_auteur_publication: 1
        }
    }
])