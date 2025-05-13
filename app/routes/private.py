from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, logout_user, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, TextAreaField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Email, NumberRange
from ..forms import PlanForm
from ..models import Plan, User
from app import db
from werkzeug.security import generate_password_hash

private_route = Blueprint('private_route', __name__)

@private_route.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@private_route.route('/profile/camaras')
@login_required
def camaras():
    return render_template('camaras.html')

@private_route.route('/profile/fotografias')
@login_required
def fotografias():
    return render_template('fotografias.html')

@private_route.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.login'))




    

def register_private_routes(app):
    app.register_blueprint(private_route)