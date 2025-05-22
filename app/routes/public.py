from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, current_user
from ..models import User
from ..forms import LoginForm
from flask import Blueprint, render_template, redirect, url_for, request, flash
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask_login import login_required, logout_user, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, TextAreaField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Email, NumberRange
from ..forms import PlanForm
from ..models import Plan, User
from app import db
from werkzeug.security import generate_password_hash
import secrets
import string
from werkzeug.security import generate_password_hash

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

@public_route.route('/products')
def products():
    return render_template('product.html')

def generar_password_segura(longitud=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    password_plana = ''.join(secrets.choice(caracteres) for _ in range(longitud))
    return generate_password_hash(password_plana), password_plana

@public_route.route('/newPlan', methods=['GET', 'POST'])
def new_plan():
    
    plan = request.args.get('plan')
    price = request.args.get('price')
    
    form = PlanForm(plan=plan, price=price)
    
    if form.validate_on_submit():
        email = form.email.data
        hashed_password, password_plana = generar_password_segura()
        full_name = form.full_name.data
        
        name_parts = full_name.split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""
        duration_months = int(form.duration.data)
        
        existing_plan = Plan.query.filter_by(name=plan, price=price).first()
        if not existing_plan:
            new_plan = Plan(
                name=form.plan.data,
                price=form.price.data,
                duration_months=duration_months,
            )
            db.session.add(new_plan)
            db.session.commit()
            existing_plan = new_plan
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Este correo ya está registrado", "danger")
            return redirect(url_for('public.new_plan', plan=plan, price=price))
            
        activation_date_end = datetime.utcnow() + relativedelta(months=duration_months)
        
        # Crear nuevo usuario con los nuevos campos
        user = User(
            email=email,
            password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            plan_status=1,
            plan_id=existing_plan.plan_id,
            activation_date=datetime.utcnow(),
            activation_end_date=activation_date_end,
            username=None, 
            has_changed_default_password=False 
        )
        db.session.add(user)
        db.session.commit()
        
        # Login del usuario
        login_user(user)
        
        flash("Plan activado y usuario creado correctamente. Por favor, actualiza tus credenciales.", "success")
        return redirect(url_for('private_route.profile'))
    
    return render_template('newPlan.html', form=form, plan=plan, price=price)

@public_route.route('/support')
def support():
    return render_template('support.html')

def register_public_routes(app):
    app.register_blueprint(public_route)
