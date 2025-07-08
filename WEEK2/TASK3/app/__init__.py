from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    app.secret_key = '013027uvxyz'

    from .auth.routes import auth_bp
    from .users.routes import users_bp
    from .projects.routes import projects_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(projects_bp)

    @app.route('/')
    def home():
        return render_template('base.html')

    return app
