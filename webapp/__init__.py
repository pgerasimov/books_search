from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user
from webapp.forms import LoginForm, RegistrationForm
from flask_migrate import Migrate
from webapp.model import db, Users, SearchRequest, Authors, Books, AdditionalInfo


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'registration'

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(user_id)

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

    @app.route('/process-registration', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(email=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы вошли на сайт')
                return redirect(url_for('/'))

        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('registration'))

    return app
