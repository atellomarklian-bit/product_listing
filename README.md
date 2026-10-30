# Food Product Manager

A command-line system for listing food products, built with Python and `mysql-connector-python`. Supports full CRUD operations against a MySQL database.

## Features

- **Create** — add products with name, category, price, and quantity
- **Read** — list all products in a formatted table, or find one by ID
- **Update** — edit any field (press Enter to keep the current value)
- **Delete** — remove a product, with a confirmation prompt
- Parameterized queries throughout (safe against SQL injection)
- Clear error messages for invalid input and connection problems

## Requirements

- Python 3.8+
- A running MySQL server (local or remote)
- `mysql-connector-python`

## Project structure

| File | Purpose |
|------|---------|
| `config.py` | MySQL connection settings — edit before first use |
| `schema.sql` | Creates the `food_db` database and `food_products` table |
| `test.py` | One-time script that applies the schema |
| `atello.py` | Main application with the interactive CLI menu |

`food_products` table columns:

| Column | Type | Notes |
|--------|------|-------|
| `id` | INT AUTO_INCREMENT | Primary key |
| `name` | VARCHAR(100) | Required |
| `category` | VARCHAR(50) | Required |
| `price` | DECIMAL(10,2) | Required |
| `quantity` | INT | Defaults to 0 |
| `created_at` | TIMESTAMP | Set automatically |

## Setup

1. Install the dependency:

   ```bash
   pip install mysql-connector-python
   ```

2. Edit `config.py` with your MySQL credentials:

   ```python
   DB_CONFIG = {
       "host": "localhost",
       "user": "root",
       "password": "your_password",
       "database": "food_db",
   }
   ```

3. Create the database and table (run once):

   ```bash
   python test.py
   ```

4. Start the app:

   ```bash
   python atello.py
   ```

## Usage

The main menu:

```
==== Food Product Manager ====
1. Add product
2. List all products
3. Find product by ID
4. Update product
5. Delete product
6. Exit
```

Example listing output:

```
ID   Name                     Category            Price     Qty
--------------------------------------------------------------
1    Apple                    Fruit                1.50    120
2    Cheddar Cheese           Dairy                4.99     35
```

## Reusing the CRUD functions

Each operation is a standalone function in `atello.py` that can be imported:

```python
from atello import create_product, list_products, get_product, update_product, delete_product

pid = create_product("Rice", "Grains", 2.75, 200)   # returns the new ID
rows = list_products()                             # all products as tuples
row = get_product(pid)                             # one product or None
update_product(pid, "Brown Rice", "Grains", 3.10, 150)
delete_product(pid)                                # True if something was deleted
```

## Troubleshooting

- **`Setup failed: 1045 Access denied`** — wrong user/password in `config.py`.
- **`Setup failed: 2003 Can't connect`** — MySQL server isn't running, or `host` is wrong.
- **`Table 'food_db.food_products' doesn't exist`** — run `python test.py` first.
