import psycopg
from typing import Optional, List, Dict, Any

DB_CONFIG = {
    "dbname": "playlist_db",
    "user": "admin",
    "password": "admin",
    "host": "localhost",
    "port": 5432,
}


def get_connection():
    return psycopg.connect(**DB_CONFIG)


def init_db():
    sql = """
    CREATE TABLE IF NOT EXISTS utilisateurs (
        id_utilisateur   SERIAL PRIMARY KEY,
        nom_utilisateur  TEXT NOT NULL,
        email            TEXT UNIQUE NOT NULL,
        date_inscription TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS chansons (
        id_chanson    SERIAL PRIMARY KEY,
        titre         TEXT NOT NULL,
        artiste       TEXT NOT NULL,
        album         TEXT,
        duree         TEXT,
        genre         TEXT,
        annee_sortie  INT
    );

    CREATE TABLE IF NOT EXISTS playlists (
        id_playlist   SERIAL PRIMARY KEY,
        nom_playlist  TEXT NOT NULL,
        id_utilisateur INT NOT NULL REFERENCES utilisateurs(id_utilisateur) ON DELETE CASCADE,
        date_creation TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS playlists_chansons (
        id_playlist INT NOT NULL REFERENCES playlists(id_playlist) ON DELETE CASCADE,
        id_chanson  INT NOT NULL REFERENCES chansons(id_chanson) ON DELETE CASCADE,
        PRIMARY KEY (id_playlist, id_chanson)
    );
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()


def create_user(nom_utilisateur: str, email: str) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO utilisateurs (nom_utilisateur, email)
                VALUES (%s, %s)
                RETURNING id_utilisateur
                """,
                (nom_utilisateur, email),
            )
            user_id = cur.fetchone()[0]
        conn.commit()
    return user_id


def get_user_by_id(id_utilisateur: int) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id_utilisateur, nom_utilisateur, email, date_inscription
                FROM utilisateurs
                WHERE id_utilisateur = %s
                """,
                (id_utilisateur,),
            )
            row = cur.fetchone()
    if row is None:
        return None
    return {
        "id_utilisateur": row[0],
        "nom_utilisateur": row[1],
        "email": row[2],
        "date_inscription": row[3],
    }


def search_users_by_name(nom_partiel: str) -> List[Dict[str, Any]]:
    pattern = f"%{nom_partiel}%"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id_utilisateur, nom_utilisateur, email, date_inscription
                FROM utilisateurs
                WHERE nom_utilisateur ILIKE %s
                ORDER BY nom_utilisateur
                """,
                (pattern,),
            )
            rows = cur.fetchall()
    return [
        {
            "id_utilisateur": r[0],
            "nom_utilisateur": r[1],
            "email": r[2],
            "date_inscription": r[3],
        }
        for r in rows
    ]


def update_user(id_utilisateur: int, nom_utilisateur: str, email: str) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE utilisateurs
                SET nom_utilisateur = %s,
                    email = %s
                WHERE id_utilisateur = %s
                """,
                (nom_utilisateur, email, id_utilisateur),
            )
            updated = cur.rowcount
        conn.commit()
    return updated == 1


def delete_user(id_utilisateur: int) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM utilisateurs WHERE id_utilisateur = %s",
                (id_utilisateur,),
            )
            deleted = cur.rowcount
        conn.commit()
    return deleted == 1


def create_song(
    titre: str,
    artiste: str,
    album: Optional[str] = None,
    duree: Optional[str] = None,
    genre: Optional[str] = None,
    annee_sortie: Optional[int] = None,
) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO chansons (titre, artiste, album, duree, genre, annee_sortie)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_chanson
                """,
                (titre, artiste, album, duree, genre, annee_sortie),
            )
            song_id = cur.fetchone()[0]
        conn.commit()
    return song_id


def get_song_by_id(id_chanson: int) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id_chanson, titre, artiste, album, duree, genre, annee_sortie
                FROM chansons
                WHERE id_chanson = %s
                """,
                (id_chanson,),
            )
            row = cur.fetchone()
    if row is None:
        return None
    return {
        "id_chanson": row[0],
        "titre": row[1],
        "artiste": row[2],
        "album": row[3],
        "duree": row[4],
        "genre": row[5],
        "annee_sortie": row[6],
    }


def search_songs(
    titre: Optional[str] = None,
    artiste: Optional[str] = None,
    genre: Optional[str] = None,
) -> List[Dict[str, Any]]:
    filters = []
    params: List[Any] = []
    if titre:
        filters.append("titre ILIKE %s")
        params.append(f"%{titre}%")
    if artiste:
        filters.append("artiste ILIKE %s")
        params.append(f"%{artiste}%")
    if genre:
        filters.append("genre ILIKE %s")
        params.append(f"%{genre}%")

    where_clause = ""
    if filters:
        where_clause = "WHERE " + " AND ".join(filters)

    sql = f"""
        SELECT id_chanson, titre, artiste, album, duree, genre, annee_sortie
        FROM chansons
        {where_clause}
        ORDER BY titre
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, tuple(params))
            rows = cur.fetchall()

    return [
        {
            "id_chanson": r[0],
            "titre": r[1],
            "artiste": r[2],
            "album": r[3],
            "duree": r[4],
            "genre": r[5],
            "annee_sortie": r[6],
        }
        for r in rows
    ]


def update_song(
    id_chanson: int,
    titre: str,
    artiste: str,
    album: Optional[str],
    duree: Optional[str],
    genre: Optional[str],
    annee_sortie: Optional[int],
) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE chansons
                SET titre = %s,
                    artiste = %s,
                    album = %s,
                    duree = %s,
                    genre = %s,
                    annee_sortie = %s
                WHERE id_chanson = %s
                """,
                (titre, artiste, album, duree, genre, annee_sortie, id_chanson),
            )
            updated = cur.rowcount
        conn.commit()
    return updated == 1


def delete_song(id_chanson: int) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM chansons WHERE id_chanson = %s",
                (id_chanson,),
            )
            deleted = cur.rowcount
        conn.commit()
    return deleted == 1


def create_playlist(
    nom_playlist: str,
    id_utilisateur: int,
    ids_chansons: List[int],
) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO playlists (nom_playlist, id_utilisateur)
                VALUES (%s, %s)
                RETURNING id_playlist
                """,
                (nom_playlist, id_utilisateur),
            )
            id_playlist = cur.fetchone()[0]

            for song_id in ids_chansons:
                cur.execute(
                    """
                    INSERT INTO playlists_chansons (id_playlist, id_chanson)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """,
                    (id_playlist, song_id),
                )
        conn.commit()
    return id_playlist


def get_playlist_by_id(id_playlist: int) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT p.id_playlist,
                       p.nom_playlist,
                       p.date_creation,
                       u.id_utilisateur,
                       u.nom_utilisateur
                FROM playlists p
                JOIN utilisateurs u ON p.id_utilisateur = u.id_utilisateur
                WHERE p.id_playlist = %s
                """,
                (id_playlist,),
            )
            playlist_row = cur.fetchone()
            if playlist_row is None:
                return None

            cur.execute(
                """
                SELECT c.id_chanson, c.titre, c.artiste
                FROM playlists_chansons pc
                JOIN chansons c ON pc.id_chanson = c.id_chanson
                WHERE pc.id_playlist = %s
                ORDER BY c.titre
                """,
                (id_playlist,),
            )
            songs_rows = cur.fetchall()

    songs = [
        {
            "id_chanson": r[0],
            "titre": r[1],
            "artiste": r[2],
        }
        for r in songs_rows
    ]

    return {
        "id_playlist": playlist_row[0],
        "nom_playlist": playlist_row[1],
        "date_creation": playlist_row[2],
        "id_utilisateur": playlist_row[3],
        "nom_utilisateur": playlist_row[4],
        "chansons": songs,
    }


def search_playlists(
    nom_playlist: Optional[str] = None,
    nom_utilisateur: Optional[str] = None,
) -> List[Dict[str, Any]]:
    filters = []
    params: List[Any] = []
    if nom_playlist:
        filters.append("p.nom_playlist ILIKE %s")
        params.append(f"%{nom_playlist}%")
    if nom_utilisateur:
        filters.append("u.nom_utilisateur ILIKE %s")
        params.append(f"%{nom_utilisateur}%")

    where_clause = ""
    if filters:
        where_clause = "WHERE " + " AND ".join(filters)

    sql = f"""
        SELECT p.id_playlist,
               p.nom_playlist,
               p.date_creation,
               u.id_utilisateur,
               u.nom_utilisateur
        FROM playlists p
        JOIN utilisateurs u ON p.id_utilisateur = u.id_utilisateur
        {where_clause}
        ORDER BY p.nom_playlist
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, tuple(params))
            rows = cur.fetchall()

    return [
        {
            "id_playlist": r[0],
            "nom_playlist": r[1],
            "date_creation": r[2],
            "id_utilisateur": r[3],
            "nom_utilisateur": r[4],
        }
        for r in rows
    ]


def update_playlist_name(id_playlist: int, nouveau_nom: str) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE playlists
                SET nom_playlist = %s
                WHERE id_playlist = %s
                """,
                (nouveau_nom, id_playlist),
            )
            updated = cur.rowcount
        conn.commit()
    return updated == 1


def add_song_to_playlist(id_playlist: int, id_chanson: int) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO playlists_chansons (id_playlist, id_chanson)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                """,
                (id_playlist, id_chanson),
            )
            inserted = cur.rowcount
        conn.commit()
    return inserted == 1


def remove_song_from_playlist(id_playlist: int, id_chanson: int) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM playlists_chansons
                WHERE id_playlist = %s AND id_chanson = %s
                """,
                (id_playlist, id_chanson),
            )
            deleted = cur.rowcount
        conn.commit()
    return deleted == 1


def delete_playlist_by_id(id_playlist: int) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM playlists WHERE id_playlist = %s",
                (id_playlist,),
            )
            deleted = cur.rowcount
        conn.commit()
    return deleted == 1


def delete_playlist_by_name(nom_playlist: str) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM playlists WHERE nom_playlist = %s",
                (nom_playlist,),
            )
            deleted = cur.rowcount
        conn.commit()
    return deleted


