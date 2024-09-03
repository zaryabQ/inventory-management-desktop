import sqlite3

def get_db_connection():
    """Establish and return a connection to the SQLite database."""
    return sqlite3.connect('db/sql.db')

def drop_table():
    """Drop the 'inventory' table if it exists."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS inventory;")
    conn.commit()
    conn.close()

def create_inventory_table():
    """Create the 'inventory' table with the specified columns."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            cost REAL NOT NULL,
            date TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

def populate_inventory_table():
    """Insert sample data into the 'inventory' table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO inventory (name, quantity, cost, date) VALUES
        ('Item A', 100, 10.50, '2024-09-01'),
        ('Item B', 50, 20.00, '2024-09-02'),
        ('Item C', 200, 5.75, '2024-09-03'),
        ('Item D', 75, 15.30, '2024-09-04'),
        ('Item E', 150, 7.99, '2024-09-05');
    ''')
    conn.commit()
    conn.close()

def delete_all_inventory_values():
    """Delete all records from the 'inventory' table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory;")
    conn.commit()
    conn.close()

def truncate_inventory_table():
    """Truncate the 'inventory' table, removing all records and resetting any auto-increment."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory;")
    cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'inventory';")
    conn.commit()
    conn.close()

# Example usage
if __name__ == "__main__":
    # drop_table()
    create_inventory_table()
    populate_inventory_table()
    # Uncomment the line below to delete all records
    # delete_all_inventory_values()
    # Uncomment the line below to truncate the table (deletes all records and resets autoincrement)
    # truncate_inventory_table()
