from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, logout_user, login_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, TextAreaField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Email, NumberRange
from ..forms import ChangePasswordUsernameForm
from ..models import Plan, User
from app import db
from werkzeug.security import generate_password_hash
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from functools import wraps

private_route = Blueprint('private_route', __name__)

@private_route.route('/profile')
@login_required
def profile():
    needs_credentials_update = not current_user.has_changed_default_password or not current_user.username
    
    form = ChangePasswordUsernameForm()
    
    return render_template('profile.html', needs_credentials_update=needs_credentials_update, form=form)

@private_route.route('/update_credentials', methods=['POST'])
@login_required
def update_credentials():
    form = ChangePasswordUsernameForm()
    
    if form.validate_on_submit():
        # Verificar si el nombre de usuario ya existe
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user and existing_user.user_id != current_user.user_id:
            flash('Este nombre de usuario ya está en uso.', 'danger')
            return redirect(url_for('private_route.profile'))
        
        # Actualizar los datos del usuario
        current_user.username = form.username.data
        current_user.password = generate_password_hash(form.new_password.data)
        current_user.has_changed_default_password = True
        
        db.session.commit()
        flash('Tus credenciales han sido actualizadas correctamente.', 'success')
        
    return redirect(url_for('private_route.profile'))

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