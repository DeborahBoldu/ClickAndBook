from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app.models.models import Cliente
from app import db, bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        password = request.form.get('password')

        user_exists = Cliente.query.filter_by(email=email).first()
        if user_exists:
            flash('El correo electrónico ya existe.', 'danger')
            return redirect(url_for('auth.register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        nuevo_cliente = Cliente(nombre=nombre, apellido=apellido, email=email, contraseña=hashed_password)

        db.session.add(nuevo_cliente)
        db.session.commit()
        flash('Registro exitoso. Iniciá sesión.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Cliente.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.contraseña, password):
            session['user_id'] = user.id_cliente
            session['user_name'] = user.nombre
            session['es_admin'] = user.es_admin 
            return redirect(url_for('main.index'))
            
        flash('Credenciales incorrectas.', 'danger')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
