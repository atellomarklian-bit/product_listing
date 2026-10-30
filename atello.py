"""Food product listing system - CRUD operations via CLI menu.

Run setup_db.py once, then run this file:  python food_app.py
"""

import mysql.connector
from mysql.connector import Error

from config import DB_CONFIG


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ---------- CRUD operations ----------

def create_product(name, category, price, quantity):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO food_products (name, category, price, quantity) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (name, category, price, quantity))
    conn.commit()
    product_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return product_id


def list_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, price, quantity FROM food_products ORDER BY id")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, category, price, quantity FROM food_products WHERE id = %s",
        (product_id,),
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def update_product(product_id, name, category, price, quantity):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """UPDATE food_products
             SET name = %s, category = %s, price = %s, quantity = %s
             WHERE id = %s"""
    cursor.execute(sql, (name, category, price, quantity, product_id))
    conn.commit()
    updated = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return updated


def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM food_products WHERE id = %s", (product_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return deleted


# ---------- CLI helpers ----------

def print_products(rows):
    if not rows:
        print("\nNo products found.\n")
        return
    print(f"\n{'ID':<5}{'Name':<25}{'Category':<15}{'Price':>10}{'Qty':>7}")
    print("-" * 62)
    for row in rows:
        print(f"{row[0]:<5}{row[1]:<25}{row[2]:<15}{row[3]:>10.2f}{row[4]:>7}")
    print()


def prompt_float(message):
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("Please enter a valid number.")


def prompt_int(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Please enter a valid integer.")


# ---------- Menu actions ----------

def add_product():
    print("\n--- Add Product ---")
    name = input("Name: ").strip()
    if not name:
        print("Name cannot be empty.\n")
        return
    category = input("Category: ").strip() or "General"
    price = prompt_float("Price: ")
    quantity = prompt_int("Quantity: ")
    product_id = create_product(name, category, price, quantity)
    print(f"Product added with ID {product_id}.\n")


def show_products():
    print("\n--- All Products ---")
    print_products(list_products())


def search_product():
    print("\n--- Find Product ---")
    product_id = prompt_int("Product ID: ")
    row = get_product(product_id)
    if row:
        print_products([row])
    else:
        print("Product not found.\n")


def edit_product():
    print("\n--- Update Product ---")
    product_id = prompt_int("Product ID: ")
    row = get_product(product_id)
    if not row:
        print("Product not found.\n")
        return
    print("Press Enter to keep the current value.")
    name = input(f"Name [{row[1]}]: ").strip() or row[1]
    category = input(f"Category [{row[2]}]: ").strip() or row[2]
    price_input = input(f"Price [{row[3]}]: ").strip()
    price = float(price_input) if price_input else float(row[3])
    qty_input = input(f"Quantity [{row[4]}]: ").strip()
    quantity = int(qty_input) if qty_input else int(row[4])
    if update_product(product_id, name, category, price, quantity):
        print("Product updated.\n")
    else:
        print("Update failed.\n")


def remove_product():
    print("\n--- Delete Product ---")
    product_id = prompt_int("Product ID: ")
    row = get_product(product_id)
    if not row:
        print("Product not found.\n")
        return
    print_products([row])
    confirm = input("Delete this product? (y/n): ").strip().lower()
    if confirm == "y":
        delete_product(product_id)
        print("Product deleted.\n")
    else:
        print("Cancelled.\n")


MENU = """
==== Food Product Manager ====
1. Add product
2. List all products
3. Find product by ID
4. Update product
5. Delete product
6. Exit
"""


def main():
    try:
        while True:
            print(MENU)
            choice = input("Choose an option: ").strip()
            if choice == "1":
                add_product()
            elif choice == "2":
                show_products()
            elif choice == "3":
                search_product()
            elif choice == "4":
                edit_product()
            elif choice == "5":
                remove_product()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid option, try again.\n")
    except Error as e:
        print(f"Database error: {e}")
        print("Check your settings in config.py and run setup_db.py first.")


if __name__ == "__main__":
    main()
