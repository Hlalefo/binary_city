import sqlite3

class Client:
    def __init__(self, name, client_code=None):
        self.name = name
        self.client_code = client_code

    @staticmethod
    def generate_client_code(name):
        alpha_part = name[:3].upper().ljust(3, 'A')
        connection = sqlite3.connect('assessment.db')
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Clients WHERE client_code LIKE ?", (alpha_part + '%',))
        count = cursor.fetchone()[0]
        numeric_part = f'{count + 1:03}'
        connection.close()
        return alpha_part + numeric_part

    def save(self):
        if not self.client_code:
            self.client_code = self.generate_client_code(self.name)
        connection = sqlite3.connect('assessment.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Clients (name, client_code) VALUES (?, ?)', (self.name, self.client_code))
        connection.commit()
        connection.close()

    @staticmethod
    def get_all_clients():
        connection = sqlite3.connect('assessment.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Clients ORDER BY name ASC')
        clients = cursor.fetchall()
        connection.close()
        return clients

    @staticmethod
    def link_contact(client_id, contact_id):
        connection = sqlite3.connect('assessment.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO ClientContact (client_id, contact_id) VALUES (?, ?)', (client_id, contact_id))
        connection.commit()
        connection.close()

    @staticmethod
    def unlink_contact(client_id, contact_id):
        connection = sqlite3.connect('assessment.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM ClientContact WHERE client_id=? AND contact_id=?', (client_id, contact_id))
        connection.commit()
        connection.close()

    @staticmethod
    def get_linked_contacts(client_id):
        connection = sqlite3.connect('assessment.db')
        cursor = connection.cursor()
        cursor.execute('''
            SELECT Contacts.name, Contacts.surname, Contacts.id 
            FROM Contacts 
            JOIN ClientContact 
            ON Contacts.id = ClientContact.contact_id 
            WHERE ClientContact.client_id=?
        ''', (client_id,))
        contacts = cursor.fetchall()
        connection.close()
        return contacts
