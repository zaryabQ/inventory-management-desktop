import sqlite3
from datetime import datetime
from db.db_handler import get_db_connection

class InventoryHandler:
    
    @staticmethod
    def load_inventory():
        """Load inventory data from the database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM inventory")
            inventory = cursor.fetchall()
            print("Loaded inventory:", inventory)  # Debugging line
            return inventory
        except sqlite3.Error as e:
            print(f"Error loading inventory: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def add_item(name, quantity, cost):
        """Add a new item to the inventory."""
        if not name or not quantity or not cost:
            raise ValueError("All fields are required")

        # Get current date and time
        date_added = datetime.now().strftime('%Y-%m-%d')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO inventory (name, quantity, cost, date) VALUES (?, ?, ?, ?)",
                (name, quantity, cost, date_added)
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding item: {e}")
        finally:
            conn.close()

    @staticmethod
    def update_item(item_id, name, quantity, cost):
        """Update an existing item in the inventory."""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE inventory SET name = ?, quantity = ?, cost = ? WHERE id = ?",
                           (name, quantity, cost, item_id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating item: {e}")
        finally:
            conn.close()

    @staticmethod
    def remove_item(item_id):
        """Remove an item from the inventory."""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error removing item: {e}")
        finally:
            conn.close()

    @staticmethod
    def search_items(keyword):
        """Search for items in the inventory."""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM inventory WHERE name LIKE ?", ('%' + keyword + '%',))
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Error searching items: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def sort_items(criteria):
        """Sort inventory items based on the given criteria."""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            query = "SELECT * FROM inventory ORDER BY " + criteria
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Error sorting items: {e}")
            return []
        finally:    
            conn.close()        

    @staticmethod
    def update_item_in_db(item_id, name, quantity, price):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE inventory SET name = ?, quantity = ?, price = ? WHERE id = ?",
                (name, quantity, price, item_id)
            )
            conn.commit()
            print("Item updated successfully.")
        except Exception as e:
            print(f"Error updating item: {e}")
        finally:
            conn.close()

    @staticmethod
    def remove_item_from_db(item_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
            conn.commit()
            print("Item removed successfully.")
        except Exception as e:
            print(f"Error removing item: {e}")
        finally:
            conn.close()
