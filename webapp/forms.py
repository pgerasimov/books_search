from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired()],
                           render_kw={"class": "form-control", "placeholder": "Enter email", "type": "email"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"class": "form-control", "placeholder": "Enter Password", "type": "password"})
    submit = SubmitField('Войти', render_kw={"class": "btn btn-primary", "Type": "submit"})


class RegistrationForm(FlaskForm):
    username_reg = StringField('Email', validators=[DataRequired()],
                               render_kw={"class": "form-control", "placeholder": "Enter email", "type": "email"})
    password_reg = PasswordField('Password', validators=[DataRequired()],
                                 render_kw={"class": "form-control", "placeholder": "Enter Password",
                                            "type": "password"})
    submit_reg = SubmitField('Зарегистрироваться', render_kw={"class": "btn btn-primary", "Type": "submit"})
