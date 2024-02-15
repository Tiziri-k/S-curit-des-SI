
from flask import Flask, render_template, request, redirect, url_for, session, logging
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
import sqlite3
import secrets
from flask import send_from_directory
import os
from dotenv import load_dotenv

load_dotenv()  

DATABASE_URL = os.getenv("DATABASE_URL")

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = secrets.token_hex(16)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)

logging.basicConfig(filename='error.log', level=logging.INFO)


def get_db_connection(DATABASE_URL):
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return render_template('index.html', error_message=' ', success_message='')



@app.route('/login', methods=['POST'])
def login():
    identifiant = request.form['identifiant']
    mot_de_passe = request.form['mot_de_passe']


    if not identifiant or not mot_de_passe:
        return render_template('index.html', error_message="Identifiant ou mot de passe manquant.", success_message=' ')

    with get_db_connection() as conn:
        cursor = conn.cursor()

        if 'ajout_compte' in request.form:
            # Vérifiez d'abord si le compte existe déjà
            cursor.execute("SELECT * FROM compte WHERE identifiant=?", (identifiant,))
            existing_account = cursor.fetchone()

            if existing_account:
                error_message = "Ce compte existe déjà. Choisissez un autre identifiant."
                return render_template('index.html', error_message=error_message, success_message=' ')
            
            hashed_password = bcrypt.generate_password_hash(mot_de_passe).decode('utf-8')

            try:
                cursor.execute("INSERT INTO compte (identifiant, mot_de_passe) VALUES (?, ?)", (identifiant, hashed_password))
                conn.commit()
                success_message = "Compte ajouté avec succès!"
                return render_template('index.html', error_message=' ', success_message=success_message)
            except sqlite3.Error as e:
                error_message = "Erreur lors de l'ajout du compte."
                return render_template('index.html', error_message=error_message, success_message=' ')
        else:
            try:
                cursor.execute("SELECT mot_de_passe FROM compte WHERE identifiant=?", (identifiant,))
                result = cursor.fetchone()

                if result and bcrypt.check_password_hash(result[0], mot_de_passe):
                    success_message = "Vous êtes connecté!"
                    session['user_id'] = identifiant 
                    return render_template('logedIN.html')
                else:
                    error_message = "Identifiant ou mot de passe incorrect."
                    return render_template('index.html', error_message=error_message, success_message=' ')
            except sqlite3.Error as e:
                error_message = "Erreur lors de la vérification des identifiants."
                return render_template('index.html', error_message=error_message, success_message=None)



def is_logged_in():
    return 'user_id' in session


@app.route('/protected')
def protected_route():
    if not is_logged_in():
        return redirect(url_for('login'))

    return "Ceci est une page protégée"


@app.route('/templates/<path:filename>')
def protected_static(filename):
    if not is_logged_in():
        return "Accès refusé", 403

    return send_from_directory('templates/', filename)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error('Erreur serveur interne', exc_info=True)
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=False)


