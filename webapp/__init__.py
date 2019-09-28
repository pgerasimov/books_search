from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from webapp.forms import LoginForm, RegistrationForm, SearchForm
from flask_migrate import Migrate
from webapp.model import db, Users, SearchRequest, Authors, Books
import logging
import goodreads_api_client as gr


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
                logging.error('Неправильное имя пользователя или пароль')
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
                logging.error('Такой пользователь уже есть')
                return redirect(url_for('registration'))

            new_user = Users(email=username)
            new_user.set_password(password)
            db.session.add(new_user)
            # new_book = Books(book_name='Chris Nord', isbn='343243243', book_publisher='MoscowLit', book_genre='Роман', book_annotation='Если бы не звон буддийского колокольчика по ночам, если бы не ')
            # db.session.add(new_book)
            # new_author = Authors(name='Jack Smith', author_bio='Родился в 1949 году в Киото, окончил школу, женился на однокласснице и открыл бар.')
            # db.session.add(new_author)
            # news_book = Books(book_name='Tailor', isbn='343243241', book_publisher='Piter', book_genre='Приключения', book_annotation='Книга о том, как биохакеры, трансгуманисты, ученные и миллиардеры пытаются решить проблему смерти с помощью технологий и искусственного интеллекта.')
            # db.session.add(news_book)
            # news_author = Authors(name='Bill Grindge', author_bio='Занимался литературным переводом с японского и английского языков, был заместителем главного редактора журнала')
            # db.session.add(news_author)
            db.session.commit()

            flash('Вы успешно зарегистрировались')
            return redirect(url_for('index'))

        flash('Пароль должен содержать хотя бы одну заглавную букву, хотя бы одну цифру и быть не менее 8 символов')
        logging.error('Пароль должен содержать хотя бы одну заглавную букву, хотя бы одну цифру и быть не менее 8 символов')
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

    @app.route('/process-search', methods=['POST'])
    @login_required
    def process_search():
        search_form = SearchForm()
        if search_form.validate_on_submit():
            for i in range(len(db.session.query(Books.book_name).all())):
                if (db.session.query(Books.book_name).all()[i][0] == search_form.search_by_book_name.data) and search_form.search_by_book_name.data != '':
                    if (db.session.query(Books.book_name).all()[i][0] == search_form.search_by_book_name.data) and search_form.search_by_book_name.data != '':
                        responses = db.session.query(Books).join(Authors, Authors.id == Books.author_id).all()
                        for item in responses:
                            result = {'Название книги': item.book_name,
                                    'Автор': item.thread.name,
                                    'Издательство': item.book_publisher,
                                    'Аннотация': item.book_annotation,
                                    'Жанр': item.book_genre,
                                    'Биография автора': item.thread.author_bio}
                            return render_template('response.html', data=result)

            # for i in range(len(db.session.query(Authors.name).all())):
            #     if (db.session.query(Authors.name).all()[i][0] == search_form.search_by_author_name.data) and search_form.search_by_author_name.data != '':
            #         response = db.session.query(Authors).filter_by(name=search_form.search_by_author_name.data)
            #         for record in response:
            #             return render_template('response.html', data=record.__dict__)

            # for i in range(len(db.session.query(Books.isbn).all())):
            #     if db.session.query(Books.isbn).all()[i][0] == search_form.search_by_ISBN.data:
            #         flash('Книга с таким IBSN есть в нашей базе данных!')

        return redirect(url_for('search'))

    return app
