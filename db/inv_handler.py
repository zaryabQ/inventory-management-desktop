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
    def update_item(item_id, update_data):
        """Update an existing item in the inventory."""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Prepare the SQL query based on provided fields
            fields_to_update = []
            values = []
            
            if 'name' in update_data and update_data['name']:
                fields_to_update.append("name = ?")
                values.append(update_data['name'])
            if 'quantity' in update_data and update_data['quantity']:
                fields_to_update.append("quantity = ?")
                values.append(update_data['quantity'])
            if 'price' in update_data and update_data['price']:
                fields_to_update.append("cost = ?")
                values.append(update_data['price'])
            
            values.append(item_id)  # Add item_id to the end for the WHERE clause

            if fields_to_update:
                query = f"UPDATE inventory SET {', '.join(fields_to_update)} WHERE id = ?"
                cursor.execute(query, values)
                conn.commit()
            else:
                print("No fields to update.")
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

    
    
