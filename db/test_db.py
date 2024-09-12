import sqlite3

# def get_db_connection():
#     """Establish and return a connection to the SQLite database."""
#     return sqlite3.connect('db/sql.db')

# def drop_table():
#     """Drop the 'inventory' table if it exists."""
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("DROP TABLE IF EXISTS inventory;")
#     conn.commit()
#     conn.close()

# def create_inventory_table():
#     """Create the 'inventory' table with the specified columns."""
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS inventory (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             quantity INTEGER NOT NULL,
#             cost REAL NOT NULL,
#             date TEXT NOT NULL
#         );
#     ''')
#     conn.commit()
#     conn.close()

# def populate_inventory_table():
#     """Insert sample data into the 'inventory' table."""
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO inventory (name, quantity, cost, date) VALUES
#         ('Item A', 100, 10.50, '2024-09-01'),
#         ('Item B', 50, 20.00, '2024-09-02'),
#         ('Item C', 200, 5.75, '2024-09-03'),
#         ('Item D', 75, 15.30, '2024-09-04'),
#         ('Item E', 150, 7.99, '2024-09-05');
#     ''')
#     conn.commit()
#     conn.close()

# def delete_all_inventory_values():
#     """Delete all records from the 'inventory' table."""
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM inventory;")
#     conn.commit()
#     conn.close()

# def truncate_inventory_table():
#     """Truncate the 'inventory' table, removing all records and resetting any auto-increment."""
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM inventory;")
#     cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'inventory';")
#     conn.commit()
#     conn.close()

# # Example usage
# if __name__ == "__main__":
#     # drop_table()
#     create_inventory_table()
#     populate_inventory_table()
#     # Uncomment the line below to delete all records
#     # delete_all_inventory_values()
#     # Uncomment the line below to truncate the table (deletes all records and resets autoincrement)
#     # truncate_inventory_table()






def get_db_connection():
    """Establish and return a connection to the SQLite database."""
    return sqlite3.connect('db/sql.db')

def drop_billing_table():
    """Drop the 'billing' table if it exists."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Bills;")
    conn.commit()
    conn.close()

def create_billing_table():
    """Create the 'billing' table with the specified columns."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE bill_item (
            id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Unique identifier for each entry
            bill_id INTEGER NOT NULL,               -- Foreign key referencing the bill ID from the billing table
            item_name TEXT NOT NULL,                -- Name or ID of the item
            quantity INTEGER NOT NULL,              -- Quantity of the item in the bill
            price REAL NOT NULL,                    -- Price of the item in the bill
            FOREIGN KEY (bill_id) REFERENCES billing(id) -- Ensures bill_id exists in the billing table
        );

    ''')
    conn.commit()
    conn.close()

def populate_billing_table():
    """Insert sample data into the 'billing' table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO billing (name, billingdate, items, total_cost, profit, status) VALUES
        ('Customer A', '2024-09-01', 8, 150.50, 25.00, 'Paid'),
        ('Customer B', '2024-09-02', 12, 250.00, 40.00, 'Unpaid'),
        ('Customer C', '2024-09-03', 5, 75.75, 10.00, 'Paid'),
        ('Customer D', '2024-09-04', 15, 300.30, 50.00, 'Unpaid'),
        ('Customer E', '2024-09-05', 10, 120.99, 20.00, 'Paid');
    ''')
    conn.commit()
    conn.close()

def delete_all_billing_values():
    """Delete all records from the 'billing' table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM billing;")
    conn.commit()
    conn.close()

def truncate_billing_table():
    """Truncate the 'billing' table, removing all records and resetting any auto-increment."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM billing;")
    cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'billing';")
    conn.commit()
    conn.close()

# Example usage
if __name__ == "__main__":
    
    # drop_billing_table()  # Uncomment this line to drop the billing table if it exists
    # create_billing_table()
    # populate_billing_table()
    # Uncomment the line below to delete all records
    delete_all_billing_values()
    # Uncomment the line below to truncate the table (deletes all records and resets autoincrement)
    # truncate_billing_table()
    pass