import sqlite3

# connect to server.db
conn = sqlite3.connect('./Database/server.db', check_same_thread=False)

# create a cursor object
cursor = conn.cursor()

class Database:
    def __init__(self):
        pass

    def create_table(self):
        # create a table
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT,
                        name TEXT,
                        phone TEXT,
                        file_path TEXT,
                        file_name TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')
        conn.commit()

    def insert(self, email, name, phone, file_path, file_name):
        # insert data
        cursor.execute('''INSERT INTO users
                        (email, name, phone, file_path, file_name)
                        VALUES (?, ?, ?, ?, ?)''',
                        (email, name, phone, file_path, file_name))
        conn.commit()

    def select(self, username, password):
        # select data
        cursor.execute('''SELECT * FROM users
                        WHERE username = ? AND password = ?''',
                        (username, password))
        return cursor.fetchone()
    
    def getFiles(self, file_id):
        file_name = f"{file_id}.pdf"
        print(file_name)
        # select data
        cursor.execute('''SELECT * FROM users
                        WHERE file_name = ?''',
                        (file_name,))
        return cursor.fetchone()

    def close(self):
        # close the connection
        conn.close()
