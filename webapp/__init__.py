from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
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
        author_id = ''

        # field Books
        book_name = Books.query.filter_by(book_name=all_args['search_by_book_name']).all()
        # field Authors
        author_object = Authors.query.filter_by(name=all_args['search_by_author_name']).all()
        if author_object != []:
            author_id = author_object[0].id
            name_of_author = Authors.query.filter_by(id=author_id).all()[0].name
        else:
            for book in book_name:
                name_of_author = Authors.query.filter_by(id=book.author_id)[0].name
        author_books_id = Books.query.filter_by(author_id=author_id).all()
        # field ISBN
        isbn = Books.query.filter_by(isbn=all_args['search_by_ISBN']).all()
        for item in isbn:
            name_of_author = Authors.query.filter_by(id=Books.author_id)[0].name

        return render_template('search_result.html', page_title=title, book_info=book_name,
                                    author_name=author_books_id, name_of_author=name_of_author, isbn=isbn)

    @app.route('/profile/<id>')
    def profile(id):
        title = "Об авторе"
        all_books_of_author = Books.query.filter_by(id=id).all()
        for person in all_books_of_author:
            person = Authors.query.filter_by(id=person.author_id)[0]
            return render_template('profile.html', page_title=title, person=person)

    @app.route('/about_book/<id>')
    def about_book(id):
        title = "О книге"
        books = Books.query.filter_by(id=id).all()
        for book in books:
            return render_template('book.html', page_title=title, book=book)

    return app
