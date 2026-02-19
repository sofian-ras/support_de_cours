import os
import psycopg
from datetime import datetime
from zoneinfo import ZoneInfo # pour le fuseau horaire Europe/Paris


DB_NAME = os.getenv("DB_NAME", "supershop")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))

def run_query_one(conn, sql, params=None):
    with conn.cursor() as cur:
        cur.execute(sql, params or ())
        return cur.fetchone()


def run_query_all(conn, sql, params=None):
    with conn.cursor() as cur:
        cur.execute(sql, params or ())
        return cur.fetchall()
    


def main():
    # Date/heure en Europe/Paris, même si le conteneur est en UTC
    now = datetime.now(ZoneInfo("Europe/Paris"))
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    now_filename = now.strftime("%Y-%m-%d_%H-%M-%S")

    conn = psycopg.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )

    os.makedirs("rapport", exist_ok=True)
    filename = f"rapport/rapport_supershop_{now_filename}.txt"

    with conn, open(filename, "w", encoding="utf-8") as f:
        f.write("RAPPORT SUPERSHOP - ANALYSE DES VENTES\n")
        f.write(f"Généré le : {now_str}\n")
        f.write("=" * 60 + "\n\n")

        # 1) Chiffre d'affaires total
        sql_total_ca = """
            SELECT SUM(oi.quantity * oi.unit_price) AS total_revenue
            FROM order_items oi
            JOIN orders o ON o.order_id = oi.order_id
            WHERE o.status <> 'CANCELLED';
        """
        total_ca_row = run_query_one(conn, sql_total_ca)
        total_ca = total_ca_row[0] if total_ca_row and total_ca_row[0] is not None else 0

        f.write("1) Chiffre d'affaires total\n")
        f.write("-" * 60 + "\n")
        f.write(
            f"Le chiffre d'affaires total (hors commandes annulées) est de "
            f"{total_ca:.2f} €.\n\n\n"
        )

        # 2) Panier moyen
        sql_panier_moyen = """
            WITH order_totals AS (
                SELECT
                    o.order_id,
                    SUM(oi.quantity * oi.unit_price) AS total
                FROM orders o
                JOIN order_items oi ON oi.order_id = o.order_id
                WHERE o.status <> 'CANCELLED'
                GROUP BY o.order_id
            )
            SELECT AVG(total) AS average_order_value
            FROM order_totals;
        """
        panier_row = run_query_one(conn, sql_panier_moyen)
        panier_moyen = panier_row[0] if panier_row and panier_row[0] is not None else 0

        f.write("2) Panier moyen\n")
        f.write("-" * 60 + "\n")
        f.write(
            f"Le panier moyen (hors commandes annulées) est de "
            f"{panier_moyen:.2f} € par commande.\n\n\n"
        )

        # 3) Article le plus vendu
        sql_top_product = """
            SELECT
                p.name,
                SUM(oi.quantity) AS total_quantity
            FROM products p
            JOIN order_items oi ON oi.product_id = p.product_id
            GROUP BY p.product_id, p.name
            ORDER BY total_quantity DESC
            LIMIT 1;
        """
        top_prod_row = run_query_one(conn, sql_top_product)
        if top_prod_row:
            top_product_name = top_prod_row[0]
            top_product_qty = top_prod_row[1]
        else:
            top_product_name = "(aucun produit vendu)"
            top_product_qty = 0

        f.write("3) Article le plus vendu\n")
        f.write("-" * 60 + "\n")
        f.write(
            "L'article ayant généré le plus de ventes (en quantité totale) est "
        )
        f.write(f"« {top_product_name} » avec {top_product_qty} unités vendues.\n\n\n")

        # 4) Top 3 des clients
        sql_top_clients = """
            SELECT
                c.firstname,
                c.lastname,
                SUM(oi.quantity * oi.unit_price) AS total_spent
            FROM customers c
            JOIN orders o ON o.customer_id = c.customer_id
            JOIN order_items oi ON oi.order_id = o.order_id
            WHERE o.status <> 'CANCELLED'
            GROUP BY c.customer_id, c.firstname, c.lastname
            ORDER BY total_spent DESC
            LIMIT 3;
        """
        top_clients = run_query_all(conn, sql_top_clients)

        f.write("4) Top 3 des clients ayant le plus dépensé\n")
        f.write("-" * 60 + "\n")

        if top_clients:
            f.write(
                "Les trois clients ayant le plus dépensé (hors commandes annulées) sont :\n"
            )
            for idx, (firstname, lastname, total_spent) in enumerate(
                top_clients, start=1
            ):
                f.write(f"{idx}. {firstname} {lastname} — {total_spent:.2f} €\n")
        else:
            f.write("Aucun client n'a été trouvé.\n")
        f.write("\n\n")

        # 5) CA par catégorie
        sql_ca_par_categorie = """
            SELECT
                c.name AS category_name,
                SUM(oi.quantity * oi.unit_price) AS category_revenue
            FROM order_items oi
            JOIN orders o     ON o.order_id = oi.order_id
            JOIN products p   ON p.product_id = oi.product_id
            JOIN categories c ON c.category_id = p.category_id
            WHERE o.status <> 'CANCELLED'
            GROUP BY c.name
            ORDER BY category_revenue DESC;
        """
        ca_categories = run_query_all(conn, sql_ca_par_categorie)

        f.write("5) Chiffre d'affaires par catégorie\n")
        f.write("-" * 60 + "\n")

        if ca_categories:
            f.write(
                "Répartition du chiffre d'affaires (hors commandes annulées) "
                "par catégorie de produits :\n"
            )
            for category_name, category_revenue in ca_categories:
                f.write(f"- {category_name} : {category_revenue:.2f} €\n")
        else:
            f.write("Aucune catégorie n'a généré de chiffre d'affaires.\n")

        f.write("\n")

    conn.close()


if __name__ == "__main__":
    main()