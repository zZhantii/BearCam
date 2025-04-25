from flask import Blueprint, render_template

public_route = Blueprint('public', __name__)

# Route Home
@public_route.route('/')
def home():
    return render_template('home.html')

def register_public_routes(app):
    app.register_blueprint(public_route)
