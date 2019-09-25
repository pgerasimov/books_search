from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()],
                           render_kw={"class": "form-control", "placeholder": "Enter email", "type": "email"})
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={"class": "form-control", "placeholder": "Enter Password", "type": "password"})
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary", "Type": "submit"})


class RegistrationForm(FlaskForm):
    username_reg = StringField('Имя пользователя', validators=[DataRequired()],
                               render_kw={"class": "form-control", "placeholder": "Enter email", "type": "email"})
    password_reg = PasswordField('Пароль', validators=[DataRequired()],
                                 render_kw={"class": "form-control", "placeholder": "Enter Password",
                                            "type": "password"})
    submit_reg = SubmitField('Отправить', render_kw={"class": "btn btn-primary", "Type": "submit"})
