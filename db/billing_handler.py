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
        """Add a new bill to the billing table."""
        if not name or not item_list:
            raise ValueError("Name and item list are required")

        billing_date = datetime.now().strftime('%Y-%m-%d')
        total_cost = 0
        total_items = 0
        total_profit = 0

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Process each item in the list
            for item in item_list:
                item_id = item['id']
                quantity = item['quantity']
                selling_price = item['selling_price']
                
                # Fetch inventory item to get the cost price
                inventory_item = InventoryHandler.search_items(item['name'])[0]  # Assuming exact match
                cost_price = inventory_item[3]  # Assuming cost is at index 3
                profit = (selling_price - cost_price) * quantity

                total_items += quantity
                total_cost += selling_price * quantity
                total_profit += profit

                # Update inventory quantity
                new_quantity = inventory_item[2] - quantity  # Assuming quantity is at index 2
                if new_quantity < 0:
                    raise ValueError(f"Not enough stock for item: {item['name']}")
                InventoryHandler.update_item(item_id, {'quantity': new_quantity})

            # Insert the bill into the billing table
            cursor.execute('''
                INSERT INTO billing (name, billingdate, items, total_cost, profit, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, billing_date, total_items, total_cost, total_profit, 'Unpaid'))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding bill: {e}")
        finally:
            conn.close()

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
    def remove_bill(bill_id, return_items=False):
        """Remove a bill from the billing table and handle inventory based on bill status."""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Fetch the bill details
            cursor.execute("SELECT * FROM billing WHERE id = ?", (bill_id,))
            bill = cursor.fetchone()
            if not bill:
                raise ValueError("Bill not found")

            status = bill[6]  # Assuming status is at index 6

            if status == 'Paid':
                # Just remove the bill
                cursor.execute("DELETE FROM billing WHERE id = ?", (bill_id,))
            elif status == 'Returned' or (status == 'Unpaid' and return_items):
                # Return items to inventory
                item_list = bill[3]  # Assuming items are stored in some way in the DB
                for item in item_list:
                    inventory_item = InventoryHandler.search_items(item['name'])[0]
                    InventoryHandler.update_item(item['id'], {'quantity': inventory_item[2] + item['quantity']})

                # Remove the bill
                cursor.execute("DELETE FROM billing WHERE id = ?", (bill_id,))
            else:
                # For unpaid and not returned bills, ask the user about returning items
                if not return_items:
                    raise ValueError("Need to confirm if items are returned")

            conn.commit()
        except sqlite3.Error as e:
            print(f"Error removing bill: {e}")
        finally:
            conn.close()

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
