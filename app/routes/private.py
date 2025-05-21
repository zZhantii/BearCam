from datetime import datetime
import os
from flask import Blueprint, jsonify, render_template, redirect, url_for, request, flash
from flask_login import login_required, logout_user, login_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, TextAreaField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Email, NumberRange
from ..forms import ChangePasswordUsernameForm
from ..models import Media, Plan, User
from app import db
import requests
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from functools import wraps

private_route = Blueprint('private_route', __name__)
# Configuración para la cámara ESP32

def capture_image_and_save_file(user_id, custom_filename=None):
    try:
        camera_url = f"http://{ESP32_CAM_IP}:{ESP32_CAM_PORT}/{ESP32_CAM_ENDPOINT}"
        print(f"Intentando conectar a la cámara en: {camera_url}")
        
        response = requests.get(camera_url, timeout=10)
        print(f"Respuesta de la cámara: {response.status_code}")
        
        if response.status_code == 200:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{custom_filename or 'imagen'}_{timestamp}.jpg"
            filename = secure_filename(filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            with open(filepath, 'wb') as f:
                f.write(response.content)

            media_entry = Media(
                user_id=user_id,
                type="imagen",
                url=f"/{filepath}"
            )
            db.session.add(media_entry)
            db.session.commit()

            print(f"Imagen guardada como archivo y asociada al usuario {user_id}")
            return {"status": "success", "media_id": media_entry.media_id, "url": media_entry.url}
        else:
            return {"status": "error", "message": f"Error al contactar con la cámara: {response.status_code}"}
    
    except Exception as e:
        print(f"Error al capturar imagen: {str(e)}")
        return {"status": "error", "message": f"Error al capturar imagen: {str(e)}"}

ESP32_CAM_IP = "172.16.7.192"  # IP de tu ESP32-CAM
ESP32_CAM_PORT = 80  # Puerto correcto (sin especificar se usa el puerto 80 por defecto)
ESP32_CAM_ENDPOINT = "capture"  # Endpoint para captura de fotos, confirmado en navegador
UPLOAD_FOLDER = './static/img'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@private_route.route('/detectado', methods=['POST'])
def detectado():
    data = request.get_json()
    user_id = data.get("user_id")
    print(f"Persona detectada. User ID recibido: {user_id}")

    if not user_id:
        return jsonify({
            "status": "error",
            "message": "Falta el user_id en la solicitud"
        }), 400

    try:
        result = capture_image_and_save_file(user_id=user_id)

        if result["status"] == "success":
            return jsonify({
                "status": "success",
                "message": "Imagen capturada y guardada correctamente",
                "media_id": result["media_id"],
                "url": result["url"]
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": result["message"]
            }), 500

    except Exception as e:
        print("Error general:", e)
        return jsonify({
            "status": "error",
            "message": f"Error al guardar la imagen: {str(e)}"
        }), 500

@private_route.route('/upload_foto', methods=['POST'])
def upload_foto():
    if 'file' not in request.files:
        return jsonify({'error': 'No se envió ningún archivo'}), 400
   
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Archivo sin nombre'}), 400

    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return jsonify({'message': 'Foto guardada correctamente', 'path': filepath}), 200

# Esta función se mantiene por compatibilidad, pero ahora usa nuestra nueva implementación
def tomar_foto_desde_esp32():
    result = capture_image_from_esp32("foto_esp32")
    return result

# Perfil

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