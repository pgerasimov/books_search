from flask import Flask, render_template
from webapp.forms import LoginForm, RegistrationForm
from flask_migrate import Migrate
from webapp.model import db


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route('/login')
    def login():
        title = "Авторизация"
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/registration')
    def registration():
        title = "Регистрация"
        login_form = RegistrationForm()
        return render_template('registration.html', page_title=title, form=login_form)

    return app
