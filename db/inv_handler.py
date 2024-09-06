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

    @staticmethod
    def remove_item_from_inventory(conn, item_id):
        """Remove an item from the inventory by its ID."""
        try:
            cursor = conn.cursor()
            
            # Delete the item from the inventory table
            cursor.execute('''
                DELETE FROM inventory
                WHERE id = ?
            ''', (item_id,))
            
            # Commit the transaction
            conn.commit()
            
            print(f"Item with ID {item_id} removed from inventory.")
        
        except sqlite3.Error as e:
            print(f"Error removing item from inventory: {e}")
            # Rollback if there is an error
            conn.rollback()
            raise e

    @staticmethod
    def search_items_billing(conn, name):
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, quantity, cost FROM inventory WHERE name = ?", (name,))
        item = cursor.fetchone()
        return item

    @staticmethod
    def update_item_billing(conn, item_id, updates):
        """
        Updates the inventory item for a specific item_id with the provided updates.
        In this case, it specifically updates the quantity of the item.
        """
        cursor = conn.cursor()

        # Ensure the 'updates' dictionary contains the 'quantity' field
        if 'quantity' in updates:
            cursor.execute('''
                UPDATE inventory
                SET quantity = ?
                WHERE id = ?
            ''', (updates['quantity'], item_id))
        
        # Commit the update to the database
        conn.commit()



