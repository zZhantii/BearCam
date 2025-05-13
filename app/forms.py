from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TelField, TextAreaField, IntegerField, HiddenField, SelectField
from wtforms.validators import DataRequired, Email, NumberRange, Length, Regexp

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message="El email es obligatorio"), Email()])
    password = PasswordField('Password', validators=[DataRequired(message="La contraseña es obligatoria")])

class CameraContractForm(FlaskForm):
    full_name = StringField(
        'Nombre completo',
        validators=[
            DataRequired(message="Este campo es obligatorio."),
            Length(min=2, max=50, message="El nombre debe tener entre 2 y 50 caracteres.")
        ]
    )

    address = StringField(
        'Dirección',
        validators=[
            DataRequired(message="Este campo es obligatorio."),
            Length(min=5, max=100, message="La dirección debe tener entre 5 y 100 caracteres.")
        ]
    )

    phone = StringField(
        'Teléfono',
        validators=[
            DataRequired(message="Este campo es obligatorio."),
            Regexp(r'^\d{9}$', message="Introduce un teléfono válido de 9 dígitos.")
        ]
    )

    plan = HiddenField(validators=[DataRequired()])

    price = HiddenField(validators=[DataRequired()])

    duration = SelectField(
        'Duración del servicio',
        choices=[
            ('1', '1 mes'),
            ('3', '3 meses'),
            ('6', '6 meses'),
            ('12', '12 meses')
        ],
        validators=[DataRequired(message="Selecciona una duración.")]
    )

    comments = TextAreaField('Comentarios opcionales')

    submit = SubmitField('Contratar ahora')
