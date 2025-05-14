from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TelField, TextAreaField, IntegerField, FloatField, HiddenField, SelectField
from wtforms.validators import DataRequired, Email, NumberRange, Length, Regexp, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message="El email es obligatorio"), Email()])
    password = PasswordField('Password', validators=[DataRequired(message="La contraseña es obligatoria")])

class PlanForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    plan = StringField('Plan', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    duration = SelectField('Duration', choices=[('1', '1 mes'), ('3', '3 meses'), ('6', '6 meses')])
    submit = SubmitField('Activar Plan')

class ChangePasswordUsernameForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=4, max=64)])
    new_password = PasswordField('Nueva contraseña', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('new_password', message='Las contraseñas deben coincidir')])
    submit = SubmitField('Guardar cambios')