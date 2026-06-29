from app import db
from datetime import datetime

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False) 
    telefono = db.Column(db.String(20))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    es_admin = db.Column(db.Boolean, default=False)
    reservas = db.relationship('Reserva', backref='cliente', lazy=True)

class Fotografo(db.Model):
    __tablename__ = 'fotografos'
    id_fotografo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    especialidad = db.Column(db.String(100))
    servicios = db.relationship('Servicio', backref='fotografo', lazy=True)

class Servicio(db.Model):
    __tablename__ = 'servicios'
    id_servicio = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    duracion = db.Column(db.Integer, nullable=False)
    id_fotografo = db.Column(db.Integer, db.ForeignKey('fotografos.id_fotografo'), nullable=False)
    reservas = db.relationship('Reserva', backref='servicio', lazy=True)

class Reserva(db.Model):
    __tablename__ = 'reservas'
    id_reserva = db.Column(db.Integer, primary_key=True)
    fecha_reserva = db.Column(db.String(10), nullable=False)  
    hora_reserva = db.Column(db.String(5), nullable=False)    
    estado = db.Column(db.String(20), default='pendiente')
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    id_servicio = db.Column(db.Integer, db.ForeignKey('servicios.id_servicio'), nullable=False)
