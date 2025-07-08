from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
users_data = []

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        for user in users_data:
            if user['username'] == username:
                return render_template('register.html', error="User already exists")

        users_data.append({'username': username, 'password': password, 'projects': []})
        session['username'] = username
        return redirect(url_for('auth.dashboard'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        for user in users_data:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                return redirect(url_for('auth.dashboard'))

        return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.login'))


@auth_bp.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    username = session['username']
    user = next((u for u in users_data if u['username'] == username), None)

    return render_template('dashboard.html', user=user)
