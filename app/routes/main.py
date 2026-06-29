from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.models import Servicio, Fotografo, Reserva
from datetime import datetime
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    servicios_publicados = Servicio.query.all()
    return render_template('main/index.html', servicios=servicios_publicados)

@main_bp.route('/servicio/nuevo', methods=['GET', 'POST'])
def nuevo_servicio():
    if 'user_id' not in session:
        flash('Por favor, iniciá sesión primero.', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        precio = float(request.form.get('precio'))
        duracion = int(request.form.get('duracion'))

        fotografo = Fotografo.query.first()
        if not fotografo:
            fotografo = Fotografo(nombre="Estudio", apellido="Click", email="info@click.com")
            db.session.add(fotografo)
            db.session.commit()

        nuevo = Servicio(titulo=titulo, descripcion=descripcion, precio=precio, duracion=duracion, id_fotografo=fotografo.id_fotografo)
        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('main/nuevo_servicio.html')

@main_bp.route('/servicio/editar/<int:id_servicio>', methods=['GET', 'POST'])
def editar_servicio(id_servicio):
    if 'user_id' not in session:
        flash('Por favor, iniciá sesión primero.', 'warning')
        return redirect(url_for('auth.login'))
        
    servicio = Servicio.query.get_or_404(id_servicio)
    
    if request.method == 'POST':
        servicio.titulo = request.form.get('titulo')
        servicio.descripcion = request.form.get('descripcion')
        servicio.precio = float(request.form.get('precio'))
        servicio.duracion = int(request.form.get('duracion'))
        
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('main/editar_servicio.html', servicio=servicio)

@main_bp.route('/servicio/eliminar/<int:id_servicio>', methods=['POST'])
def eliminar_servicio(id_servicio):
    servicio = Servicio.query.get_or_404(id_servicio)
    db.session.delete(servicio)
    db.session.commit()
    return redirect(url_for('main.index'))

@main_bp.route('/servicio/reservar/<int:id_servicio>', methods=['GET', 'POST'])
def reservar(id_servicio):

    if 'user_id' not in session:
        flash('Tenés que iniciar sesión para poder reservar un servicio.', 'warning')
        return redirect(url_for('auth.login'))
        
    servicio = Servicio.query.get_or_404(id_servicio)

    hoy = datetime.today().strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        nueva_reserva = Reserva(
            fecha_reserva=fecha,
            hora_reserva=hora,
            id_cliente=session['user_id'],
            id_servicio=id_servicio
        )
        
        db.session.add(nueva_reserva)
        db.session.commit()
        
        flash(f'¡Reserva registrada con éxito para: {servicio.titulo}!', 'success')
        return redirect(url_for('main.mis_reservas'))
        
    return render_template('main/reservar.html', servicio=servicio, min_date=hoy)

@main_bp.route('/mis-reservas')
def mis_reservas():
    if 'user_id' not in session:
        flash('Por favor, iniciá sesión para ver tus reservas.', 'warning')
        return redirect(url_for('auth.login'))
    
    lista_reservas = Reserva.query.filter_by(id_cliente=session['user_id']).all()
    
    return render_template('main/mis_reservas.html', reservas=lista_reservas)


@main_bp.route('/cancelar-reserva/<int:id_reserva>', methods=['POST'])
def cancelar_reserva(id_reserva):
    if 'user_id' not in session:
        flash('Por favor, iniciá sesión para realizar esta acción.', 'warning')
        return redirect(url_for('auth.login'))
    
    reserva = Reserva.query.filter_by(id_reserva=id_reserva, id_cliente=session['user_id']).first_or_404()
    
    try:
        db.session.delete(reserva)
        db.session.commit()
        flash('Tu reserva ha sido cancelada con éxito.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Hubo un error al intentar cancelar la reserva.', 'danger')
        
    return redirect(url_for('main.mis_reservas'))


@main_bp.route('/admin/reservas')
def ver_reservas_admin():
    if not session.get('user_id') or not session.get('es_admin'):
        flash('No tienes permisos para acceder a esta sección.', 'danger')
        return redirect(url_for('main.index'))
    todas_las_reservas = Reserva.query.all()
    
    return render_template('main/ver_reservas.html', reservas=todas_las_reservas)


@main_bp.route('/admin/reservas/toggle/<int:id_reserva>', methods=['POST'])
def toggle_reserva(id_reserva):
    if not session.get('es_admin'):
        return redirect(url_for('main.index'))
    
    reserva = Reserva.query.get_or_404(id_reserva)
    
    if reserva.estado == 'confirmada':
        reserva.estado = 'pendiente'
    else:
        reserva.estado = 'confirmada'
        
    db.session.commit()
    flash(f'Estado de reserva {id_reserva} actualizado a {reserva.estado}', 'info')
    return redirect(url_for('main.ver_reservas_admin'))