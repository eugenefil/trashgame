import os
import re

from flask import (Flask, render_template, session, request,
    redirect, abort, url_for, flash)
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='dev')
users_dir = os.path.join(app.instance_path, 'users')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username:
            flash('Нужно ввести логин')
        elif not password:
            flash('Нужно ввести пароль')
        elif re.fullmatch('[-_a-zA-Z0-9]+', username) is None:
            flash('Логин может включать только буквы, цифры, дефисы и подчеркивания')
        else:
            user_dir = os.path.join(users_dir, username)
            try:
                os.mkdir(user_dir)
            except FileExistsError:
                flash(f'Пользователь с логином {username} уже существует')
            else:
                with open(os.path.join(user_dir, 'password'), 'w') as f:
                    f.write(generate_password_hash(password))
                return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username:
            flash('Нужно ввести логин')
        elif not password:
            flash('Нужно ввести пароль')
        elif re.fullmatch('[-_a-zA-Z0-9]+', username) is None:
            flash('Неверный логин или пароль')
        else:
            user_dir = os.path.join(users_dir, username)
            try:
                with open(os.path.join(user_dir, 'password')) as f:
                    h = f.read()
            except FileNotFoundError:
                pass
            else:
                if check_password_hash(h, password):
                    session.clear()
                    session['username'] = username
                    return redirect(url_for('index'))

            flash('Неверный логин или пароль')

    return render_template('login.html')


os.makedirs(users_dir, exist_ok=True)
