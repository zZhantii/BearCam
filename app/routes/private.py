from flask import Blueprint
from flask_login import login_required

private_route = Blueprint('private_route', __name__)

@private_route.route('/profile')
@login_required
def profile():
    return 'profile'

@private_route.route('/products')
@login_required
def products():
    return 'products'

def register_private_routes(app):
    app.register_blueprint(private_route)