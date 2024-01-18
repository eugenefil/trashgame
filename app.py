from flask import Flask, render_template, session, request
from flask import redirect, abort, url_for
from hashlib import sha256
import os

app = Flask(__name__)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('underground_boss'))
    return render_template('index.html')

def create_user(form):
    try:
        os.mkdir(f"users/{form['username']}")
    except FileExistsError:
        return abort(509)
    except:
        return abort(500)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if 'username' in session:
        return abort(400)
    if 'username' not in request.form:
        return abort(400)
    if not 'password' in request.form:
        return abort(400)

    if 'creating' in request.form:
        return create_user(request.form)
    
    try:
        with open(f'users/{username}/password', 'r') as f:
            pwhash = f.read().strip()
    except (FileNotFoundError, IOError):
        return abort(401)

    h = sha256()
    h.update(request.form['password'])
    if h.hexdigest() != pwhash:
        return abort(401)

    return redirect(url_for('underground_boss'))

@app.route('/underground_boss')
def underground_boss():
    return abort(404)


os.makedirs('users', exist_ok=True)
