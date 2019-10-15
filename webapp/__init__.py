from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from webapp.find_book import find_book_in_db, find_book_in_api
from webapp.forms import LoginForm, RegistrationForm, SearchForm
from flask_migrate import Migrate
from webapp.model import db, Users, SearchRequest, Authors, Books
import logging


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    logging.basicConfig(filename='app.log',
                        filemode='w',
                        level=logging.ERROR,
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        format='%(name)s - %(levelname)s - %(message)s')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'registration'

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(user_id)

    @app.route("/")
    def index():
        form = LoginForm()
        return render_template('base.html', form=form, active='index')

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            flash('Вы уже авторизованы')
            return redirect(url_for('search'))

        title = "Авторизация"
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form, active='login')

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
                logging.error('Неправильное имя пользователя или пароль')
                return redirect(url_for('login'))

    @app.route('/registration')
    def registration():
        if current_user.is_authenticated:
            flash('Вы уже авторизованы')
            return redirect(url_for('search'))

        title = "Регистрация"
        registration_form = RegistrationForm()
        return render_template('registration.html', page_title=title, form=registration_form, active='registration')

    @app.route('/process_registration', methods=['POST'])
    def process_registration():

        form = RegistrationForm()
        if form.validate_on_submit():

            username = form.username_reg.data
            password = form.password_reg.data
            password_confirm = form.password_reg_confirm.data

            if Users.query.filter(Users.email == username).count():
                flash('Такой пользователь уже есть')
                logging.error('Такой пользователь уже есть')
                return redirect(url_for('registration'))

            if not password == password_confirm:
                flash('Пароли не совпадают. Повторите ввод')
                return redirect(url_for('registration'))

            new_user = Users(email=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            flash('Вы успешно зарегистрировались')
            return redirect(url_for('index'))

        flash('Пароль должен содержать хотя бы одну заглавную букву, хотя бы одну цифру и быть не менее 8 символов')
        logging.error(
            'Пароль должен содержать хотя бы одну заглавную букву, хотя бы одну цифру и быть не менее 8 символов')
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
        return render_template('search.html', page_title=title, form=search_form, active='search')

    @app.route('/process-search', methods=['POST'])
    def process_search():
        title = "Поиск книги"
        all_args = request.form.to_dict()
        all_args.pop('csrf_token')
        all_args.pop('submit_search')

        db_request = find_book_in_db(all_args)
        book_name = db_request[0]
        books_by_author_id = db_request[1]
        isbn = db_request[2]

        if book_name == [] and books_by_author_id == [] and isbn == [] and all_args['search_by_book_name'] != '':

            api_request = find_book_in_api(all_args)

            book_name = api_request[0]
            books_by_author_id = api_request[1]
            isbn = books_by_author_id = api_request[2]

        return render_template('search_result.html', page_title=title, book_info=book_name,
                               author_name=books_by_author_id, isbn=isbn)

    @app.route('/profile/<id>')
    def profile(id):
        title = "Об авторе"
        all_books_of_author = Books.query.filter_by(id=id).all()

        for person in all_books_of_author:
            return render_template('profile.html', page_title=title, person=person)

    @app.route('/about_book/<id>')
    def about_book(id):
        title = "О книге"
        books = Books.query.filter_by(id=id).all()
        for book in books:
            return render_template('book.html', page_title=title, book=book)

    return app
