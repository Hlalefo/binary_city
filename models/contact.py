import sqlite3

class Contact:
    def __init__(self, name, surname, email):
        self.name = name
        self.surname = surname
        self.email = email

    def save(self):
        connection = sqlite3.connect('assessment.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Contacts (name, surname, email) VALUES (?, ?, ?)', (self.name, self.surname, self.email))
        connection.commit()
        connection.close()

    @staticmethod
    def get_all_contacts():
        connection = sqlite3.connect('assessment.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Contacts ORDER BY surname ASC, name ASC')
        contacts = cursor.fetchall()
        connection.close()
        return contacts

    @staticmethod
    def get_linked_clients(contact_id):
        connection = sqlite3.connect('assessment.db')
        cursor = connection.cursor()
        cursor.execute('''
            SELECT Clients.name, Clients.client_code 
            FROM Clients 
            JOIN ClientContact 
            ON Clients.id = ClientContact.client_id 
            WHERE ClientContact.contact_id=?
        ''', (contact_id,))
        clients = cursor.fetchall()
        connection.close()
        return clients
