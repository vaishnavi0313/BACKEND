from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    projects = db.relationship('Project', backref='user', lazy=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def view_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        name = request.form['name']
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('view_users'))
    return render_template('new_user.html')

@app.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    for project in user.projects:
        if project.image:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], project.image))
            except FileNotFoundError:
                pass
        db.session.delete(project)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('view_users'))


@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    users = User.query.all()
    if request.method == 'POST':
        title = request.form['title']
        user_id = request.form['user_id']
        image_file = request.files['image']
        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        project = Project(title=title, user_id=user_id, image=filename)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('view_users'))
    return render_template('new_project.html', users=users)

@app.route('/projects/delete/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.image:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], project.image))
        except FileNotFoundError:
            pass
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('view_users'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
