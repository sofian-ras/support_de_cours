class Utilisateur:
    def __init__(self, nom, prenom, age) -> None:
        self.nom = nom
        self.prenom = prenom
        self.age = age

    def nom_complet(self):
        return f"{self.prenom} {self.nom}"
    
    def est_majeur(self):
        return self.age >= 18