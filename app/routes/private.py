from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, logout_user

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

@private_route.route('/products')
@login_required
def products():
    return render_template('product.html')

@private_route.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.login'))

@private_route.route('/newPlan')
@login_required
def new_plan():
    return render_template('newPlan.html')

def register_private_routes(app):
    app.register_blueprint(private_route)