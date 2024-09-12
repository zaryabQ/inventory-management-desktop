import sqlite3

def add_columns_to_table(db_name, table_name, column1, column1_type, column2, column2_type):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Add the first column
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column1} {column1_type}")

        # Add the second column
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column2} {column2_type}")

        # Commit the changes
        conn.commit()
        print(f"Columns {column1} and {column2} added successfully to {table_name}")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()

    finally:
        conn.close()

# Example usage
db_name = 'db/sql.db'  # Replace with your database name
table_name = 'billing'     # Replace with your table name
column1 = 'paid'      # Replace with the first column name
column1_type = 'REAL'         # Replace with the first column type (e.g., REAL, INTEGER, TEXT)
column2 = 'remaining'      # Replace with the second column name
column2_type = 'REAL'         # Replace with the second column type

add_columns_to_table(db_name, table_name, column1, column1_type, column2, column2_type)
