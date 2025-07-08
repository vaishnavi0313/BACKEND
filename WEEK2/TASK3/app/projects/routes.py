from flask import Blueprint, render_template, request, redirect, url_for, session
from app.auth.routes import users_data

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

@projects_bp.route('/', methods=['GET', 'POST'])
def project_list():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    username = session['username']
    user = next((u for u in users_data if u['username'] == username), None)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        user['projects'].append({'title': title, 'description': description})
        return redirect(url_for('projects.project_list'))

    return render_template('projects.html', projects=user['projects'])
