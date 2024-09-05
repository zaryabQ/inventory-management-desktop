import sqlite3
from datetime import datetime
from db.db_handler import get_db_connection
from db.inv_handler import InventoryHandler

class BillingHandler:
    
    @staticmethod
    def load_billing():
        """Load billing data from the database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM billing")
            billing = cursor.fetchall()
            print("Loaded billing records:", billing)  # Debugging line
            return billing
        except sqlite3.Error as e:
            print(f"Error loading billing records: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def search_inventory(keyword):
        """Search for items in the inventory to add to a bill."""
        return InventoryHandler.search_items(keyword)

    @staticmethod
    def add_bill(name, item_list):
        """Add a new bill to the billing table and update inventory and bill_item."""
        if not name or not item_list:
            raise ValueError("Name and item list are required")

        billing_date = datetime.now().strftime('%Y-%m-%d')
        total_cost = 0
        total_items = 0
        total_profit = 0

        try:
            # Use a context manager to handle the connection
            with get_db_connection() as conn:
                conn.execute("PRAGMA busy_timeout = 5000")  # Set timeout to handle busy database
                
                cursor = conn.cursor()

                # Start a transaction
                cursor.execute("BEGIN TRANSACTION")

                # Insert the new bill into the billing table
                cursor.execute('''
                    INSERT INTO billing (name, billingdate, items, total_cost, profit, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, billing_date, 0, 0, 0, 'Unpaid'))
                
                # Get the last inserted bill ID
                bill_id = cursor.lastrowid
                print(item_list)

                # Process each item in the item list
                for item in item_list:
                    item_id = item['id']
                    quantity = item['quantity']
                    selling_price = item['selling_price']
                    
                    # Fetch the inventory item to get the cost price and current quantity
                    inventory_item = InventoryHandler.search_items_billing(conn, item['name'])
                    
                    if not inventory_item:
                        raise ValueError(f"Item {item['name']} not found in inventory.")
                    
                    cost_price = inventory_item[3]  # Assuming cost is at index 3
                    current_inventory_quantity = inventory_item[2]  # Assuming inventory quantity is at index 2

                    # Calculate profit for the item
                    profit = (selling_price - cost_price) * quantity

                    # Update total items, total cost, and total profit
                    total_items += quantity
                    total_cost += selling_price * quantity
                    total_profit += profit

                    # Check if there is enough inventory
                    new_quantity = current_inventory_quantity - quantity
                    if new_quantity < 0:
                        raise ValueError(f"Not enough stock for item: {item['name']}. Available: {current_inventory_quantity}")

                    # If the new quantity matches the inventory quantity, remove the item from inventory
                    if new_quantity == 0:
                        InventoryHandler.remove_item_from_inventory(conn, inventory_item[0])  # Assuming remove_item_from_inventory handles deletion
                    else:
                        # Update inventory quantity
                        InventoryHandler.update_item_billing(conn, inventory_item[0], {'quantity': new_quantity})

                    # Insert the item into the bill_item table
                    cursor.execute('''
                        INSERT INTO bill_item (bill_id, item_name, quantity, price)
                        VALUES (?, ?, ?, ?)
                    ''', (bill_id, item['name'], quantity, selling_price))

                # Update the billing table with the total items, total cost, and total profit
                cursor.execute('''
                    UPDATE billing
                    SET items = ?, total_cost = ?, profit = ?
                    WHERE id = ?
                ''', (total_items, total_cost, total_profit, bill_id))

                # Commit the transaction
                conn.commit()

                print(f"Bill {bill_id} saved successfully.")

        except sqlite3.Error as e:
            print(f"Error adding bill: {e}")
            # Rollback if there is an error
            conn.rollback()
            raise e


    @staticmethod
    def update_bill(bill_id, update_data):
        """Update an existing bill in the billing table."""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Fetch the existing bill details
            cursor.execute("SELECT * FROM billing WHERE id = ?", (bill_id,))
            bill = cursor.fetchone()
            if not bill:
                raise ValueError("Bill not found")
            
            # Prepare the fields for updating
            fields_to_update = []
            values = []

            if 'status' in update_data and update_data['status']:
                fields_to_update.append("status = ?")
                values.append(update_data['status'])

            # Handle item changes (e.g., quantities or removing items)
            if 'item_list' in update_data:
                new_item_list = update_data['item_list']
                total_items = 0
                total_cost = 0
                total_profit = 0

                for item in new_item_list:
                    item_id = item['id']
                    quantity = item['quantity']
                    selling_price = item['selling_price']

                    # Fetch inventory item to get the cost price
                    inventory_item = InventoryHandler.search_items(item['name'])[0]
                    cost_price = inventory_item[3]
                    profit = (selling_price - cost_price) * quantity

                    total_items += quantity
                    total_cost += selling_price * quantity
                    total_profit += profit

                    # Update inventory based on quantity change
                    inventory_quantity = inventory_item[2]
                    original_quantity = quantity  # Assuming original quantity was stored

                    if quantity > original_quantity:
                        new_inventory_quantity = inventory_quantity - (quantity - original_quantity)
                    else:
                        new_inventory_quantity = inventory_quantity + (original_quantity - quantity)

                    InventoryHandler.update_item(item_id, {'quantity': new_inventory_quantity})

                fields_to_update.append("items = ?")
                fields_to_update.append("total_cost = ?")
                fields_to_update.append("profit = ?")
                values.extend([total_items, total_cost, total_profit])

            values.append(bill_id)  # Add bill_id for WHERE clause

            if fields_to_update:
                query = f"UPDATE billing SET {', '.join(fields_to_update)} WHERE id = ?"
                cursor.execute(query, values)
                conn.commit()
            else:
                print("No fields to update.")
        except sqlite3.Error as e:
            print(f"Error updating bill: {e}")
        finally:
            conn.close()

    @staticmethod
    def remove_bill(bill_id, show_snackbar):
        """Remove a bill from the billing table and handle inventory based on bill status."""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Fetch the bill details
                cursor.execute("SELECT * FROM billing WHERE id = ?", (bill_id,))
                bill = cursor.fetchone()
                if not bill:
                    raise ValueError("Bill not found")

                status = bill[6]  # Assuming status is at index 6

                if status == 'Paid':
                    # Remove bill from billing table
                    cursor.execute("DELETE FROM billing WHERE id = ?", (bill_id,))
                    
                    # Remove related items from bill_item table
                    cursor.execute("DELETE FROM bill_item WHERE bill_id = ?", (bill_id,))
                
                elif status == 'Unpaid':
                    # Retrieve items from the bill_item table
                    cursor.execute("SELECT item_name, quantity, price FROM bill_item WHERE bill_id = ?", (bill_id,))
                    items = cursor.fetchall()
                    
                    for item_name, quantity, price in items:
                        # Fetch the inventory item to get the current quantity
                        cursor.execute("SELECT id, quantity FROM inventory WHERE name = ?", (item_name,))
                        inventory_item = cursor.fetchone()
                        
                        if inventory_item:
                            inventory_id, current_quantity = inventory_item
                            # Increase the inventory quantity
                            updated_quantity = current_quantity + quantity
                            cursor.execute("UPDATE inventory SET quantity = ? WHERE id = ?", (updated_quantity, inventory_id))
                        else:
                            # Re-add the item to inventory if not found
                            # We assume `price` here is the selling price, and we need to alert the user
                            alert_message = (
                                f"Item '{item_name}' not found in inventory. "
                                "Re-adding with current quantity and price. Please update the price to the buying price."
                            )
                            show_snackbar(alert_message)  # Show alert using snackbar
                            
                            # Insert the item into the inventory with the current selling price as a placeholder
                            cursor.execute("INSERT INTO inventory (name, quantity, cost, date) VALUES (?, ?, ?, ?)",
                                        (item_name, quantity, price, datetime.now().strftime('%Y-%m-%d')))
                
                    # Remove related items from bill_item table
                    cursor.execute("DELETE FROM bill_item WHERE bill_id = ?", (bill_id,))
                    
                    # Remove the bill from billing table
                    cursor.execute("DELETE FROM billing WHERE id = ?", (bill_id,))
                
                else:
                    raise ValueError("Invalid bill status")

                # Commit the transaction
                conn.commit()
                print(f"Bill {bill_id} removed successfully.")

        except sqlite3.Error as e:
            print(f"Error removing bill: {e}")
            # Rollback if there is an error
            conn.rollback()
            raise e



    @staticmethod
    def search_bills(keyword):
        """Search for bills in the billing table by name."""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM billing WHERE name LIKE ?", ('%' + keyword + '%',))
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Error searching bills: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def sort_bills(criteria):
        """Sort bills based on the given criteria."""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            query = "SELECT * FROM billing ORDER BY " + criteria
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Error sorting bills: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def fetch_bill_items(bill_id):
        """Fetch all items for a given bill_id from the bill_item table."""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, item_name, quantity, price FROM bill_item WHERE bill_id = ?", (bill_id,))
        items = cursor.fetchall()

        conn.close()

        # Convert the items to a list of dictionaries for easier use in the UI
        return [{"id": item[0], "name": item[1], "quantity": item[2], "price": item[3]} for item in items]
    

    @staticmethod
    def update_bill_item(bill_item_id, quantity, price):
        """Update the quantity and price of an item in the bill_item table."""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE bill_item
            SET quantity = ?, price = ?
            WHERE id = ?
        ''', (quantity, price, bill_item_id))

        conn.commit()
        conn.close()


    @staticmethod
    def remove_bill_item(bill_item_id):
        """Remove an item from the bill_item table."""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM bill_item
            WHERE id = ?
        ''', (bill_item_id,))

        conn.commit()
        conn.close()

    @staticmethod
    def update_bill_status(bill_id, status):
        """Update the status of a bill in the billing table."""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE billing
            SET status = ?
            WHERE id = ?
        ''', (status, bill_id))

        conn.commit()
        conn.close()


    @staticmethod
    def fetch_bill_details(bill_id):
        # Connect to the SQLite database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch the bill details (you can add more fields if needed)
        query = "SELECT id, name FROM billing WHERE id = ?"
        cursor.execute(query, (bill_id,))

        # Fetch one row of result (assuming bill_id is unique)
        result = cursor.fetchone()

        # Close the connection
        conn.close()

        # If result is found, return it as a dictionary
        if result:
            return {
                'id': result[0],    # Bill ID
                'name': result[1]   # Bill Name
            }
        else:
            # If no result, return None or handle it as needed
            return None
        
    @staticmethod
    def save_bill_changes(bill_id, updated_items, status):
        """Update bill details, including item quantities, prices, and status."""
        if not updated_items:
            raise ValueError("No items to update.")

        try:
            with get_db_connection() as conn:
                conn.execute("PRAGMA busy_timeout = 5000")  # Set timeout to handle busy database
                
                cursor = conn.cursor()

                # Start a transaction
                cursor.execute("BEGIN TRANSACTION")

                # Fetch current bill items from the bill_item table
                cursor.execute("SELECT item_name, quantity FROM bill_item WHERE bill_id = ?", (bill_id,))
                current_bill_items = cursor.fetchall()
                
                # Create a dictionary for current quantities in the bill
                current_quantities = {item_name: qty for item_name, qty in current_bill_items}

                # Update or remove items
                for item in updated_items:
                    item_name = item['name']
                    new_quantity = item['quantity']
                    new_price = item['price']
                    is_removed = item['removed']
                    
                    if not is_removed:
                        # Fetch current inventory data
                        cursor.execute("SELECT id, quantity FROM inventory WHERE name = ?", (item_name,))
                        inventory_item = cursor.fetchone()
                        if not inventory_item:
                            raise ValueError(f"Item {item_name} not found in inventory.")

                        inventory_id, current_inventory_quantity = inventory_item
                        quantity_difference = new_quantity - current_quantities.get(item_name, 0)

                        # Update inventory quantity
                        updated_inventory_quantity = current_inventory_quantity - quantity_difference
                        cursor.execute("UPDATE inventory SET quantity = ? WHERE id = ?", (updated_inventory_quantity, inventory_id))
                        
                        # Check if item exists in bill_item and update or insert accordingly
                        cursor.execute("SELECT id FROM bill_item WHERE bill_id = ? AND item_name = ?", (bill_id, item_name))
                        existing_item = cursor.fetchone()
                        
                        if existing_item:
                            # Update existing item
                            cursor.execute("""
                                UPDATE bill_item
                                SET quantity = ?, price = ?
                                WHERE bill_id = ? AND item_name = ?
                            """, (new_quantity, new_price, bill_id, item_name))
                        else:
                            # Insert new item
                            cursor.execute("""
                                INSERT INTO bill_item (bill_id, item_name, quantity, price)
                                VALUES (?, ?, ?, ?)
                            """, (bill_id, item_name, new_quantity, new_price))

                    else:
                        # If the item is removed, increase the inventory quantity
                        cursor.execute("SELECT id, quantity FROM inventory WHERE name = ?", (item_name,))
                        inventory_item = cursor.fetchone()
                        if not inventory_item:
                            raise ValueError(f"Item {item_name} not found in inventory.")

                        inventory_id, current_inventory_quantity = inventory_item

                        # Update inventory quantity by adding back the removed item's quantity
                        cursor.execute("UPDATE inventory SET quantity = ? WHERE id = ?", (current_inventory_quantity + current_quantities.get(item_name, 0), inventory_id))
                        
                        # Remove item from bill_item table
                        cursor.execute("DELETE FROM bill_item WHERE bill_id = ? AND item_name = ?", (bill_id, item_name))

                # Calculate total cost, total items, and profit
                cursor.execute("SELECT SUM(quantity * price) FROM bill_item WHERE bill_id = ?", (bill_id,))
                total_cost = cursor.fetchone()[0] or 0

                cursor.execute("SELECT SUM(quantity) FROM bill_item WHERE bill_id = ?", (bill_id,))
                total_items = cursor.fetchone()[0] or 0

                # Calculate profit
                cursor.execute("""
                    SELECT SUM((bi.price - i.cost) * bi.quantity)
                    FROM bill_item bi
                    JOIN inventory i ON bi.item_name = i.name
                    WHERE bi.bill_id = ?
                """, (bill_id,))
                total_profit = cursor.fetchone()[0] or 0

                # Update billing table with new values and status
                cursor.execute("""
                    UPDATE billing
                    SET total_cost = ?, items = ?, profit = ?, status = ?
                    WHERE id = ?
                """, (total_cost, total_items, total_profit, status, bill_id))

                # Commit the transaction
                conn.commit()

                print(f"Bill {bill_id} updated successfully.")

        except sqlite3.Error as e:
            print(f"Error updating bill: {e}")
            # Rollback if there is an error
            conn.rollback()
            raise e

