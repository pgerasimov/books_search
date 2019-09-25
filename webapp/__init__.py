from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from webapp.forms import LoginForm, RegistrationForm, SearchForm
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

    @app.route("/")
    def index():
        form = LoginForm()
        return render_template('base.html', form=form)

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            flash('Вы уже авторизованы')
            return redirect(url_for('search'))

        title = "Авторизация"
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(email=form.username.data).first()

            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы вошли на сайт')
                return redirect(url_for('search'))

            else:
                flash('Неправильное имя пользователя или пароль')
                return redirect(url_for('login'))

    @app.route('/registration')
    def registration():
        if current_user.is_authenticated:
            flash('Вы уже авторизованы')
            return redirect(url_for('search'))

        title = "Регистрация"
        registration_form = RegistrationForm()
        return render_template('registration.html', page_title=title, form=registration_form)

    @app.route('/process_registration', methods=['POST'])
    def process_registration():

        form = RegistrationForm()
        if form.validate_on_submit():

            username = form.username_reg.data
            password = form.password_reg.data

            if Users.query.filter(Users.email == username).count():
                flash('Такой пользователь уже есть')
                return redirect(url_for('registration'))

            new_user = Users(email=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            flash('Вы успешно зарегистрировались')
            return redirect(url_for('index'))

        flash('Пароль должен содеражть хотя бы одну заглавную букву, хотя бы одну цифру и быть не менее 8 символов')
        return redirect(url_for('registration'))

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы успешно вышли из системы')
        return redirect(url_for('index'))

    @app.route('/search')
    @login_required
    def search():
        title = "Поиск книги"
        search_form = SearchForm()
        return render_template('search.html', page_title=title, form=search_form)

    return app
