import sqlite3

def get_db_connection():
    """Establish and return a connection to the SQLite database."""
    return sqlite3.connect('db/sql.db')

def get_user(username, password):
    """Fetch a user from the database with the given username and password."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        return user
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
            cursor.close()
            conn.close()

def update_user_username(current_username, new_username):
    """Update the username of the user in the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Users SET username = ? WHERE username = ?", (new_username, current_username))
        conn.commit()
        return "Username Updated Successfully"
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return "Username Update Failed"
    finally:
        if conn:
            cursor.close()
            conn.close()

def update_user_password(username, new_password):
    """Update the password of the user in the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Users SET password = ? WHERE username = ?", (new_password, username))
        conn.commit()
        return "Password Updated Successfully"  # Returns the number of rows updated
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return "Password Update Failed"
    finally:
        if conn:
            cursor.close()
            conn.close()

def get_inventory_items():
    """Fetch all inventory items from the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Inventory")
        items = cursor.fetchall()
        return items
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if conn:
            cursor.close()
            conn.close()

def add_inventory_item(item_name, quantity, price):
    """Add a new inventory item to the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Inventory (item_name, quantity, price) VALUES (?, ?, ?)", (item_name, quantity, price))
        conn.commit()
        return cursor.lastrowid  # Returns the ID of the inserted row
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
            cursor.close()
            conn.close()

def update_inventory_item(item_id, item_name, quantity, price):
    """Update an existing inventory item in the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Inventory SET item_name = ?, quantity = ?, price = ? WHERE id = ?",
            (item_name, quantity, price, item_id)
        )
        conn.commit()
        return cursor.rowcount  # Returns the number of rows updated
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return 0
    finally:
        if conn:
            cursor.close()
            conn.close()

def delete_inventory_item(item_id):
    """Delete an inventory item from the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Inventory WHERE id = ?", (item_id,))
        conn.commit()
        return cursor.rowcount  # Returns the number of rows deleted
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return 0
    finally:
        if conn:
            cursor.close()
            conn.close()

def get_billing_records():
    """Fetch all billing records from the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Billing")
        records = cursor.fetchall()
        return records
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if conn:
            cursor.close()
            conn.close()

def add_billing_record(customer_name, total_amount):
    """Add a new billing record to the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Billing (customer_name, total_amount) VALUES (?, ?)", 
            (customer_name, total_amount)
        )
        conn.commit()
        return cursor.lastrowid  # Returns the ID of the inserted row
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
            cursor.close()
            conn.close()

def update_billing_record(record_id, customer_name, total_amount):
    """Update an existing billing record in the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Billing SET customer_name = ?, total_amount = ? WHERE id = ?",
            (customer_name, total_amount, record_id)
        )
        conn.commit()
        return cursor.rowcount  # Returns the number of rows updated
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return 0
    finally:
        if conn:
            cursor.close()
            conn.close()

def delete_billing_record(record_id):
    """Delete a billing record from the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Billing WHERE id = ?", (record_id,))
        conn.commit()
        return cursor.rowcount  # Returns the number of rows deleted
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return 0
    finally:
        if conn:
            cursor.close()
            conn.close()


def InventoryDB():
    pass

def BillingDB():
    pass


