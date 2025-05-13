from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, TextAreaField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Email, NumberRange
from ..forms import CameraContractForm

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
    form = CameraContractForm()
    plan = request.args.get('plan')
    precio = request.args.get('precio')

    return render_template('newPlan.html',form=form, plan=plan, precio=precio)

@private_route.route("/procesar_plan", methods=["GET", "POST"])
@login_required
def procesar_plan():
    print("Procesando formulario...")
    form = CameraContractForm()

    # Inicializamos plan y precio para el render_template
    plan = ""
    precio = ""

    if request.method == "GET":
        plan = request.args.get("plan", "")
        precio = request.args.get("precio", "")
        form.plan.data = plan
        form.price.data = precio
    else:
        # En POST, tomamos lo que venga del form
        plan = form.plan.data
        precio = form.price.data

    if form.validate_on_submit():
        full_name = form.full_name.data
        address = form.address.data
        phone = form.phone.data
        duration = form.duration.data

        # Mostrar en consola para verificar
        print("full_name:", full_name)
        print("Dirección:", address)
        print("Teléfono:", phone)
        print("Plan:", plan)
        print("Precio:", precio)
        print("Duración:", duration)

        flash("¡Plan contratado con éxito!", "success")
        return redirect(url_for("private_route.profile"))
    else:
        # Gestión personalizada de errores
        if form.full_name.errors:
            form.full_name.errors.append("Error en el nombre completo.")
        if form.address.errors:
            form.address.errors.append("Error en la dirección.")
        if form.phone.errors:
            form.phone.errors.append("Error en el teléfono.")
        if form.plan.errors:
            form.plan.errors.append("Error en el plan seleccionado.")
        if form.price.errors:
            form.price.errors.append("Error en el precio.")
        if form.duration.errors:
            form.duration.errors.append("Error en la duración del plan.")

    return render_template("newPlan.html", form=form, plan=plan, precio=precio)



    

def register_private_routes(app):
    app.register_blueprint(private_route)