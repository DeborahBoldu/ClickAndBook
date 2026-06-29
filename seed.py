import os
from dotenv import load_dotenv
from app import create_app, db, bcrypt
from app.models.models import Fotografo, Servicio, Cliente, Reserva 

load_dotenv()

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    f = Fotografo(nombre="Maria", apellido="Estudio", email="maria@clickbook.com", especialidad="Retrato")
    db.session.add(f)
    db.session.commit()
    
    s1 = Servicio(titulo="Book de Fotos Exterior", descripcion="Sesión de 2 horas en parque con 20 fotos editadas.", precio=7500.0, duracion=2, id_fotografo=f.id_fotografo)
    s2 = Servicio(titulo="Fotografía de Producto E-commerce", descripcion="Sesión de 4 horas en estudio para catálogos digitales.", precio=15000.0, duracion=4, id_fotografo=f.id_fotografo)
    
    db.session.add_all([s1, s2])
    db.session.commit()

    admin_email = os.getenv('ADMIN_EMAIL')
    admin_password = os.getenv('ADMIN_PASSWORD')

    if admin_email and admin_password:
        password_hasheada = bcrypt.generate_password_hash(admin_password).decode('utf-8')
        admin = Cliente(
            nombre=os.getenv('ADMIN_NAME', 'Admin'),
            apellido=os.getenv('ADMIN_LASTNAME', 'Click'),
            email=admin_email,
            contraseña=password_hasheada,
            es_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("admin creado.")
    else:
        print("no se encontraron variables ADMIN_EMAIL / ADMIN_PASSWORD en el .env")