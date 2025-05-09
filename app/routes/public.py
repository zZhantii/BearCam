from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, current_user
from ..models import User
from ..forms import LoginForm

public_route = Blueprint('public', __name__)

# Route Home
@public_route.route('/')
def home():
    return render_template('home.html')

@public_route.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('private_route.profile'))
        else:
            form.email.errors.append("Invalid email")
            form.password.errors.append("Invalid password")

    return render_template('login.html', form=form)


@public_route.route('/support')
def support():
    return render_template('support.html')

def register_public_routes(app):
    app.register_blueprint(public_route)
