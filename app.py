import os
from app import create_app, db
from sqlalchemy import text
from app.models import User
from werkzeug.security import generate_password_hash

os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_DEBUG'] = '1'

app = create_app()

def check_database():
    try:
        with app.app_context():
            db.session.execute(text('SELECT 1'))
            print("Conexión a la base de datos exitosa.")
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")

def create_tables():
    with app.app_context():
        db.create_all()
        print("Tablas creadas exitosamente.")

def insert_User_data():
    with app.app_context():
        if User.query.filter(User.user_id.in_([1, 2])).first() is None:
            Users = [
                User(user_id=1, username='admin', first_name='Admin1', last_name='Admin2', email='admin@demo.com', password=generate_password_hash('admin')),
                User(user_id=2, username='user', first_name='User1', last_name='User2', email='user@demo.com', password=generate_password_hash('12345678'))
            ]
            db.session.bulk_save_objects(Users)
            db.session.commit()
            print("Insertado el usuario admin y el usuario user.")
        else:
            print("Los usuarios no se han podido insertar porque ya existen.")

if __name__ == '__main__':
    with app.app_context():
        check_database()
        create_tables()
        insert_User_data()
        app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=81, debug=True,  use_reloader=True)