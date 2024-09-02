# # Dictionary with keys and values
# person_info = {
#     "name": "John Doe",
#     "age": 30,
#     "city": "New York",
#     "occupation": "Engineer"
# }

# # Loop through the dictionary using a for loop
# for key in person_info:
#     print(key)
#     # Access the value corresponding to the current key
#     value = person_info[key]
#     # Print the key and its corresponding value
#     print(f"{key}: {value}")


import sqlite3
import os

# def initialize_database():
#     db_path = 'db/sql.db'
    
#     # Check if the file already exists
#     if not os.path.exists(db_path):
#         try:
#             # Connect to the SQLite database (it will create the file if it doesn't exist)
#             conn = sqlite3.connect(db_path)
#             cursor = conn.cursor()
            
#             # Create Users table if it doesn't exist
#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS Users (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     username TEXT UNIQUE,
#                     password TEXT
#                 )
#             ''')
            
#             conn.commit()
#             conn.close()
#         except sqlite3.Error as e:
#             print(f"Error initializing database: {e}")
#         finally:
#             if conn:
#                 conn.close()

# initialize_database()
# import sqlite3

# def add_user(username, password):
#     db_path = 'db/sql.db'
    
#     try:
#         # Connect to the SQLite database
#         conn = sqlite3.connect(db_path)
#         cursor = conn.cursor()
        
#         # Insert a new user into the Users table
#         cursor.execute('''
#             INSERT INTO Users (username, password) 
#             VALUES (?, ?)
#         ''', (username, password))
        
#         conn.commit()
#         print(f"User '{username}' added successfully.")
        
#     except sqlite3.IntegrityError:
#         print(f"User '{username}' already exists.")
#     except sqlite3.Error as e:
#         print(f"Database error: {e}")
#     finally:
#         if conn:
#             conn.close()

# # Example usage
# username = 'test1'
# password = 'test78999'
# add_user(username, password)

# import sqlite3

def update_username(old_username, new_username):
    # Path to your SQLite database
    db_path = 'db/sql.db'
    
    # Check for valid input
    # if not new_username:
    #     print("New username is required")
    #     return

    # if len(new_username) < 5 or not new_username.isalpha():
    #     print("Username must be more than 4 characters and only alphabets")
    #     return
    
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Search for the username
        cursor.execute('''
            SELECT username FROM Users WHERE username = ?
        ''', (old_username,))
        result = cursor.fetchone()
        
        if result is None:
            print("Username not found")
            return
        
        # Update the username
        cursor.execute('''
            UPDATE Users SET username = ? WHERE username = ?
        ''', (new_username, old_username))
        
        # Commit the changes
        conn.commit()
        
        print("Username updated successfully!")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Example usage
old_username = 'newuser'
new_username = 'Ammar'
update_username(old_username, new_username)

