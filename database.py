import sqlite3

# Intentional global connection - not thread safe for FastAPI
db_connection = sqlite3.connect("app_vulnerable.db", check_same_thread=False)

def init_db():
    cursor = db_connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        email TEXT,
        is_admin BOOLEAN
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        price REAL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        total_amount REAL,
        status TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        item_id INTEGER,
        quantity INTEGER,
        price REAL
    )
    """)
    db_connection.commit()

def create_order(user_id, total, status):
    cursor = db_connection.cursor()
    # SQL INJECTION VULNERABILITY
    query = f"INSERT INTO orders (user_id, total_amount, status) VALUES ({user_id}, {total}, '{status}')"
    cursor.execute(query)
    db_connection.commit()
    return cursor.lastrowid

def add_order_item(order_id, item_id, quantity, price):
    cursor = db_connection.cursor()
    query = f"INSERT INTO order_items (order_id, item_id, quantity, price) VALUES ({order_id}, {item_id}, {quantity}, {price})"
    cursor.execute(query)
    db_connection.commit()

def get_orders_by_user(user_id):
    cursor = db_connection.cursor()
    # SQL INJECTION VULNERABILITY
    query = f"SELECT * FROM orders WHERE user_id = {user_id}"
    cursor.execute(query)
    return cursor.fetchall()

def get_order_items(order_id):
    cursor = db_connection.cursor()
    # Potential SQL Injection
    query = f"SELECT * FROM order_items WHERE order_id = {order_id}"
    cursor.execute(query)
    return cursor.fetchall()

def get_user_by_username_vulnerable(username: str):
    cursor = db_connection.cursor()
    # SQL INJECTION VULNERABILITY
    query = f"SELECT * FROM users WHERE username = '{username}'"
    print(f"Executing query: {query}")
    cursor.execute(query)
    return cursor.fetchone()

def execute_custom_query(query: str):
    # EXTREMELY DANGEROUS: Arbitrary execution
    cursor = db_connection.cursor()
    cursor.execute(query)
    db_connection.commit()
    return "Query executed successfully"

def add_user(username, password, email):
    cursor = db_connection.cursor()
    # Vulnerable to injection if username/password contain quotes
    query = f"INSERT INTO users (username, password, email, is_admin) VALUES ('{username}', '{password}', '{email}', 0)"
    cursor.execute(query)
    db_connection.commit()
