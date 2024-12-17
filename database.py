import sqlite3
from datetime import datetime

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
        distance REAL,
        start_date TEXT,
        last_entry_date TEXT
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
    start_date = datetime.now().strftime("%m/%d/%Y %H:%M")
    query = "INSERT INTO users (name, distance, start_date, last_entry_date) VALUES (?, ?, ?, ?)"
    cur = conn.cursor()
    cur.execute(query, (name, distance, start_date, start_date))
    conn.commit()
    print(f"New user added with ID: {cur.lastrowid}")
    return cur.lastrowid

def save_progress(conn, user_id, distance):
    """Save the user's progress to the database."""
    last_entry_date = datetime.now().strftime("%m/%d/%Y %H:%M")
    query = "UPDATE users SET distance = ?, last_entry_date = ? WHERE id = ?"
    cur = conn.cursor()
    cur.execute(query, (distance, last_entry_date, user_id))
    conn.commit()
    print(f"Progress saved for user_id {user_id}: Total Distance - {distance}")

def load_progress(conn, user_id):
    """Load the user's progress from the database."""
    query = "SELECT distance, last_entry_date FROM users WHERE id = ?"
    cur = conn.cursor()
    cur.execute(query, (user_id,))
    return cur.fetchone()

def load_start_and_last_entry_dates(conn, user_id):
    """Load the user's start date and last entry date from the database."""
    query = "SELECT start_date, last_entry_date FROM users WHERE id = ?"
    cur = conn.cursor()
    cur.execute(query, (user_id,))
    return cur.fetchone()
