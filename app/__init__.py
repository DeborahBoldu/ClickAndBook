import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key')

    uri = os.getenv('DATABASE_URL', 'sqlite:///click_book.db')
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.ia import ia_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(ia_bp, url_prefix='/ia')

    from app.models.models import Servicio, Fotografo, Reserva

    with app.app_context():
        db.create_all()

        # Crear datos iniciales solo si no hay servicios
        if Servicio.query.count() == 0:

            fotografo = Fotografo(
                nombre="Maria",
                apellido="Estudio",
                email="maria@clickbook.com",
                especialidad="Retrato"
            )

            db.session.add(fotografo)
            db.session.commit()

            servicio1 = Servicio(
                titulo="Book de Fotos Exterior",
                descripcion="Sesión de 2 horas en parque con 20 fotos editadas.",
                precio=7500.0,
                duracion=2,
                id_fotografo=fotografo.id_fotografo
            )

            servicio2 = Servicio(
                titulo="Fotografía de Producto E-commerce",
                descripcion="Sesión de 4 horas en estudio para catálogos digitales.",
                precio=15000.0,
                duracion=4,
                id_fotografo=fotografo.id_fotografo
            )

            db.session.add_all([servicio1, servicio2])
            db.session.commit()

    return app