from flask import Blueprint, render_template, request, redirect, url_for, session
from app.auth.routes import users_data

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/', methods=['GET', 'POST'])
def user_list():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in users_data:
            if user['username'] == username:
                error = 'User already exists'
                break

        if not error:
            users_data.append({
                'username': username,
                'password': password,
                'projects': []
            })
            return redirect(url_for('users.user_list'))

    return render_template('users.html', users=users_data, error=error)
