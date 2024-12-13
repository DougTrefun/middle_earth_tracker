import sqlite3

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to database: {db_file}")
    except sqlite3.Error as e:
        print(e)
    return conn

def create_tables(conn):
    """Create the necessary tables in the database."""
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        distance REAL
    );
    """
    try:
        cur = conn.cursor()
        cur.execute(create_users_table)
        print("Tables created successfully")
    except sqlite3.Error as e:
        print(e)

def get_all_users(conn):
    """Retrieve all users from the database."""
    query = "SELECT name FROM users"
    cur = conn.cursor()
    cur.execute(query)
    return [row[0] for row in cur.fetchall()]

def get_user_id(conn, name):
    """Get the user ID for the given user name."""
    query = "SELECT id FROM users WHERE name=?"
    cur = conn.cursor()
    cur.execute(query, (str(name),))  # Ensure the name is a string
    row = cur.fetchone()
    return row[0] if row else None

def add_user(conn, name, distance):
    """Add a new user to the database."""
    query = "INSERT INTO users (name, distance) VALUES (?, ?)"
    cur = conn.cursor()
    cur.execute(query, (name, distance))
    conn.commit()
    print(f"New user added with ID: {cur.lastrowid}")
    return cur.lastrowid

def save_progress(conn, user_id, distance):
    """Save the user's progress to the database."""
    query = "UPDATE users SET distance = ? WHERE id = ?"
    cur = conn.cursor()
    cur.execute(query, (distance, user_id))
    conn.commit()
    print(f"Progress saved for user_id {user_id}: Total Distance - {distance}")

def load_progress(conn, user_id):
    """Load the user's progress from the database."""
    query = "SELECT distance FROM users WHERE id = ?"
    cur = conn.cursor()
    cur.execute(query, (user_id,))
    return cur.fetchone()
