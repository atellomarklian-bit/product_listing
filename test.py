"""One-time setup: creates the food_db database and food_products table."""

import mysql.connector
from mysql.connector import Error

from config import DB_CONFIG


def setup():
    conn = None
    cursor = None
    try:
        # Connect without a database first so we can create it.
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
        )
        cursor = conn.cursor()
        with open("schema.sql") as f:
            for statement in f.read().split(";"):
                if statement.strip():
                    cursor.execute(statement)
        conn.commit()
        print("Database 'food_db' and table 'food_products' are ready.")
    except Error as e:
        print(f"Setup failed: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    setup()
