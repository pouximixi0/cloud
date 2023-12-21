from flask import Flask, request, render_template, send_from_directory, redirect
import os
import uuid

app = Flask(__name__)

# Dossier de base pour stocker les fichiers téléchargés
BASE_UPLOADS_FOLDER = 'uploads_users'
app.config['BASE_UPLOADS_FOLDER'] = BASE_UPLOADS_FOLDER

# Créer le dossier d'uploads s'il n'existe pas
if not os.path.exists(BASE_UPLOADS_FOLDER):
    os.makedirs(BASE_UPLOADS_FOLDER)

# Page d'accueil avec le formulaire pour télécharger le fichier
@app.route('/')
def index():
    return render_template('index.html')

# Route pour traiter le fichier téléchargé
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    # Récupérer la valeur du champ de texte
    username = request.form.get('username')

    # Créer un dossier pour l'utilisateur s'il n'existe pas
    user_upload_folder = os.path.join(app.config['BASE_UPLOADS_FOLDER'], username)
    if not os.path.exists(user_upload_folder):
        os.makedirs(user_upload_folder)

    if file:
        # Générer un nom de fichier unique
        unique_filename = str(uuid.uuid4()) + '_' + file.filename
        # Sauvegarder le fichier dans le dossier de l'utilisateur
        file.save(os.path.join(user_upload_folder, unique_filename))
        # Retourner le lien d'accès au fichier
        file_url = f"{request.url_root}uploads_users/{username}/{unique_filename}"
        return f"Le fichier a été téléchargé avec succès par l'utilisateur {username}. Lien d'accès : {file_url}"

# Route pour accéder directement aux fichiers téléchargés
@app.route('/uploads_users/<username>/<filename>')
def uploaded_file(username, filename):
    user_upload_folder = os.path.join(app.config['BASE_UPLOADS_FOLDER'], username)
    return send_from_directory(user_upload_folder, filename)

if __name__ == '__main__':
    # Démarrer l'application Flask
    app.run(debug=True)
