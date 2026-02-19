from playlist_app import (
    init_db,
    create_user,
    get_user_by_id,
    search_users_by_name,
    update_user,
    delete_user,
    create_song,
    get_song_by_id,
    search_songs,
    update_song,
    delete_song,
    create_playlist,
    get_playlist_by_id,
    search_playlists,
    update_playlist_name,
    add_song_to_playlist,
    remove_song_from_playlist,
    delete_playlist_by_id,
    delete_playlist_by_name,
)


def input_int(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("Veuillez entrer un entier valide.")


def menu_utilisateurs():
    while True:
        print("\n=== Menu Utilisateurs ===")
        print("1. Créer un utilisateur")
        print("2. Rechercher un utilisateur par ID")
        print("3. Rechercher des utilisateurs par nom")
        print("4. Mettre à jour un utilisateur")
        print("5. Supprimer un utilisateur")
        print("0. Retour au menu principal")
        choix = input("Votre choix: ").strip()

        if choix == "1":
            nom = input("Nom d'utilisateur: ").strip()
            email = input("Email: ").strip()
            user_id = create_user(nom, email)
            print(f"Utilisateur créé avec id {user_id}")

        elif choix == "2":
            id_u = input_int("ID utilisateur: ")
            user = get_user_by_id(id_u)
            if user:
                print(user)
            else:
                print("Aucun utilisateur trouvé.")

        elif choix == "3":
            nom = input("Nom (partiel): ").strip()
            users = search_users_by_name(nom)
            if users:
                for u in users:
                    print(u)
            else:
                print("Aucun utilisateur trouvé.")

        elif choix == "4":
            id_u = input_int("ID utilisateur à modifier: ")
            nom = input("Nouveau nom d'utilisateur: ").strip()
            email = input("Nouvel email: ").strip()
            ok = update_user(id_u, nom, email)
            print("Utilisateur mis à jour." if ok else "Utilisateur introuvable.")

        elif choix == "5":
            id_u = input_int("ID utilisateur à supprimer: ")
            ok = delete_user(id_u)
            print("Utilisateur supprimé." if ok else "Utilisateur introuvable.")

        elif choix == "0":
            break

        else:
            print("Choix invalide.")


def menu_chansons():
    while True:
        print("\n=== Menu Chansons ===")
        print("1. Créer une chanson")
        print("2. Rechercher une chanson par ID")
        print("3. Rechercher des chansons (titre / artiste / genre)")
        print("4. Mettre à jour une chanson")
        print("5. Supprimer une chanson")
        print("0. Retour au menu principal")
        choix = input("Votre choix: ").strip()

        if choix == "1":
            titre = input("Titre: ").strip()
            artiste = input("Artiste: ").strip()
            album = input("Album (optionnel): ").strip() or None
            duree = input("Durée (optionnel, ex: 03:25): ").strip() or None
            genre = input("Genre (optionnel): ").strip() or None
            annee_str = input("Année de sortie (optionnel): ").strip()
            annee = int(annee_str) if annee_str.isdigit() else None
            id_chanson = create_song(titre, artiste, album, duree, genre, annee)
            print(f"Chanson créée avec id {id_chanson}")

        elif choix == "2":
            id_c = input_int("ID chanson: ")
            song = get_song_by_id(id_c)
            if song:
                print(song)
            else:
                print("Aucune chanson trouvée.")

        elif choix == "3":
            titre = input("Filtre titre (laisser vide si aucun): ").strip() or None
            artiste = input("Filtre artiste (laisser vide si aucun): ").strip() or None
            genre = input("Filtre genre (laisser vide si aucun): ").strip() or None
            songs = search_songs(titre=titre, artiste=artiste, genre=genre)
            if songs:
                for s in songs:
                    print(s)
            else:
                print("Aucune chanson trouvée.")

        elif choix == "4":
            id_c = input_int("ID chanson à modifier: ")
            song = get_song_by_id(id_c)
            if not song:
                print("Chanson introuvable.")
                continue
            print("Laisser vide pour conserver la valeur actuelle.")
            titre = input(f"Titre [{song['titre']}]: ").strip() or song["titre"]
            artiste = input(f"Artiste [{song['artiste']}]: ").strip() or song["artiste"]
            album = input(f"Album [{song['album']}]: ").strip() or song["album"]
            duree = input(f"Durée [{song['duree']}]: ").strip() or song["duree"]
            genre = input(f"Genre [{song['genre']}]: ").strip() or song["genre"]
            annee_str = input(f"Année de sortie [{song['annee_sortie']}]: ").strip()
            annee = song["annee_sortie"]
            if annee_str.isdigit():
                annee = int(annee_str)
            ok = update_song(id_c, titre, artiste, album, duree, genre, annee)
            print("Chanson mise à jour." if ok else "Erreur lors de la mise à jour.")

        elif choix == "5":
            id_c = input_int("ID chanson à supprimer: ")
            ok = delete_song(id_c)
            print("Chanson supprimée." if ok else "Chanson introuvable.")

        elif choix == "0":
            break

        else:
            print("Choix invalide.")


def afficher_playlist_detaillee(playlist: dict):
    print(f"\nPlaylist #{playlist['id_playlist']} - {playlist['nom_playlist']}")
    print(f"Créateur : {playlist['nom_utilisateur']} (id {playlist['id_utilisateur']})")
    print(f"Date de création : {playlist['date_creation']}")
    print("Chansons :")
    if playlist["chansons"]:
        for c in playlist["chansons"]:
            print(f"  - [{c['id_chanson']}] {c['titre']} - {c['artiste']}")
    else:
        print("  (aucune chanson)")


def menu_playlists():
    while True:
        print("\n=== Menu Playlists ===")
        print("1. Créer une playlist")
        print("2. Rechercher une playlist par ID")
        print("3. Rechercher des playlists (par nom ou par utilisateur)")
        print("4. Renommer une playlist")
        print("5. Ajouter une chanson à une playlist")
        print("6. Supprimer une chanson d'une playlist")
        print("7. Supprimer une playlist par ID")
        print("8. Supprimer des playlists par nom")
        print("0. Retour au menu principal")
        choix = input("Votre choix: ").strip()

        if choix == "1":
            nom = input("Nom de la playlist: ").strip()
            id_utilisateur = input_int("ID du créateur (utilisateur): ")
            ids_str = input("IDs de chansons séparés par des virgules (ex: 1,2,3): ").strip()
            ids_chansons = []
            if ids_str:
                for part in ids_str.split(","):
                    part = part.strip()
                    if part.isdigit():
                        ids_chansons.append(int(part))
            id_playlist = create_playlist(nom, id_utilisateur, ids_chansons)
            print(f"Playlist créée avec id {id_playlist}")

        elif choix == "2":
            id_p = input_int("ID playlist: ")
            playlist = get_playlist_by_id(id_p)
            if playlist:
                afficher_playlist_detaillee(playlist)
            else:
                print("Aucune playlist trouvée.")

        elif choix == "3":
            nom = input("Filtre nom de playlist (laisser vide si aucun): ").strip() or None
            nom_user = input("Filtre nom d'utilisateur (laisser vide si aucun): ").strip() or None
            pls = search_playlists(nom_playlist=nom, nom_utilisateur=nom_user)
            if pls:
                for p in pls:
                    print(p)
            else:
                print("Aucune playlist trouvée.")

        elif choix == "4":
            id_p = input_int("ID playlist à renommer: ")
            nouveau_nom = input("Nouveau nom de la playlist: ").strip()
            ok = update_playlist_name(id_p, nouveau_nom)
            print("Playlist renommée." if ok else "Playlist introuvable.")

        elif choix == "5":
            id_p = input_int("ID playlist: ")
            id_c = input_int("ID chanson à ajouter: ")
            ok = add_song_to_playlist(id_p, id_c)
            print("Chanson ajoutée à la playlist." if ok else "Pas d'ajout (déjà présente ou erreur).")

        elif choix == "6":
            id_p = input_int("ID playlist: ")
            id_c = input_int("ID chanson à supprimer de la playlist: ")
            ok = remove_song_from_playlist(id_p, id_c)
            print("Chanson retirée de la playlist." if ok else "Aucune ligne supprimée.")

        elif choix == "7":
            id_p = input_int("ID playlist à supprimer: ")
            ok = delete_playlist_by_id(id_p)
            print("Playlist supprimée." if ok else "Playlist introuvable.")

        elif choix == "8":
            nom = input("Nom de playlist à supprimer: ").strip()
            nb = delete_playlist_by_name(nom)
            print(f"{nb} playlist(s) supprimée(s).")

        elif choix == "0":
            break

        else:
            print("Choix invalide.")


def menu_principal():
    init_db()
    while True:
        print("\n=== Menu principal ===")
        print("1. Gérer les utilisateurs")
        print("2. Gérer les chansons")
        print("3. Gérer les playlists")
        print("0. Quitter")
        choix = input("Votre choix: ").strip()

        if choix == "1":
            menu_utilisateurs()
        elif choix == "2":
            menu_chansons()
        elif choix == "3":
            menu_playlists()
        elif choix == "0":
            print("Au revoir.")
            break
        else:
            print("Choix invalide.")


if __name__ == "__main__":
    menu_principal()
