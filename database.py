import sqlite3

DATABASE_FILENAME = 'bucket_list.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILENAME)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn


def init_db():
    """Initialize the database with our schema"""
    conn = get_db_connection()
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS user (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL,
                            email TEXT UNIQUE NOT NULL)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS item (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            description TEXT,
                            completion_date TEXT,
                            achieved BOOLEAN NOT NULL DEFAULT 0,
                            user_id INTEGER NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES user (id))''')


def add_user(username, password, email):
    """Add a new user to the database"""
    conn = get_db_connection()
    with conn:
        conn.execute('INSERT INTO user (username, password, email) VALUES (?, ?, ?)',
                     (username, password, email))


def fetch_user(username):
    """Retrieve a user by username"""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
    return user


def add_item(name, description, completion_date, achieved, user_id):
    """Add a new bucket list item for a user"""
    conn = get_db_connection()
    with conn:
        conn.execute('''INSERT INTO item (name, description, completion_date, achieved, user_id)
                        VALUES (?, ?, ?, ?, ?)''',
                     (name, description, completion_date, achieved, user_id))


def fetch_items(user_id):
    """Retrieve all items for a user"""
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM item WHERE user_id = ?', (user_id,)).fetchall()
    return items


def fetch_item(item_id):
    """Retrieve a single item by item ID"""
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM item WHERE id = ?', (item_id,)).fetchone()
    return item


def update_item(item_id, name, description, completion_date, achieved):
    """Update an existing bucket list item"""
    conn = get_db_connection()
    with conn:
        conn.execute('''UPDATE item SET name = ?, description = ?, completion_date = ?, achieved = ?
                        WHERE id = ?''',
                     (name, description, completion_date, achieved, item_id))


def delete_item(item_id):
    """Delete a bucket list item"""
    conn = get_db_connection()
    with conn:
        conn.execute('DELETE FROM item WHERE id = ?', (item_id,))


if __name__ == '__main__':
    init_db()
