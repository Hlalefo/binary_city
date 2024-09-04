from flask import Flask, redirect, render_template, request, jsonify, url_for
# from models.client import Client
# from models.contact import Contact

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



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/clients', methods=['GET', 'POST'])
def client_list():
    if request.method == 'POST':
        name = request.form['name']
        if not name:
            return jsonify({'success': False, 'message': 'Client name is required.'})
        
        client = Client(name)
        client.save()
        return jsonify({'success': True})
    
    clients = Client.get_all_clients()
    print(clients)
    return render_template('client_list.html', clients=clients, Client=Client)

@app.route('/contacts', methods=['GET', 'POST'])
def contact_list():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']

        if not name or not surname or not email:
            return jsonify({'success': False, 'message': 'All fields are required.'})

        if not validate_email(email):
            return jsonify({'success': False, 'message': 'Invalid email address.'})

        contact = Contact(name, surname, email)
        contact.save()
        return jsonify({'success': True})

    contacts = Contact.get_all_contacts()
    print(contacts)
    return render_template('contact_list.html', contacts=contacts, Contact=Contact)

def validate_email(email):
    return '@' in email and '.' in email

@app.route('/clients/<int:client_id>/link/<int:contact_id>')
def link_contact(client_id, contact_id):
    Client.link_contact(client_id, contact_id)
    return redirect(url_for('client_list'))

@app.route('/clients/<int:client_id>/unlink/<int:contact_id>')
def unlink_contact(client_id, contact_id):
    Client.unlink_contact(client_id, contact_id)
    return redirect(url_for('client_list'))

if __name__ == '__main__':
    app.run(debug=True)
