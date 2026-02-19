# - Créer un script `main.py` :
#     - Créer une fonction `login()` qui boucle tant que l'utilisateur n'a pas entrée un nom et un mot de passe précis. 
#     - Afficher un message d'erreur si les logs saisies sont incorrects
#     - Afficher un message de succès `Login accepté` si les logs sont correct. 

def login():
    while True:
        user_name = input("Veuillez entrer votre nom : ")
        user_pwd = input("Veuillez entrer votre mot de passe : ")

        if user_name == "Toto" and user_pwd == "1234":
            print("Login accepté")
            break

        print("Vos identifiants sont incorrects !")

if __name__ == "__main__":
    login() 