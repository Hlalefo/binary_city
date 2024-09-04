import sqlite3

def init_db():
    connection = sqlite3.connect('assessment.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        client_code TEXT UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ClientContact (
        client_id INTEGER,
        contact_id INTEGER,
        PRIMARY KEY (client_id, contact_id),
        FOREIGN KEY (client_id) REFERENCES Clients(id),
        FOREIGN KEY (contact_id) REFERENCES Contacts(id)
    )
    ''')

    connection.commit()
    connection.close()

if __name__ == '__main__':
    init_db()
