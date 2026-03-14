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
    db_connection.commit()

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
