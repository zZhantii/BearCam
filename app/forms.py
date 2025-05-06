from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message="El email es obligatorio"), Email()])
    password = PasswordField('Password', validators=[DataRequired(message="La contraseña es obligatoria")])
