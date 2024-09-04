from flask import Flask, redirect, render_template, request, jsonify, url_for
from models.client import Client
from models.contact import Contact

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
    return render_template('client_list.html', clients=clients)

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
    return render_template('contact_list.html', contacts=contacts)

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
