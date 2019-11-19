from flask import Blueprint
from app import db
from app.models import File, Rol, User


bp = Blueprint('manage', __name__)

@bp.cli.command('dbinit')
def dbinit():
    data = []
    data.append(File(filename="default.png"))
    data.append(Rol(descripcion="administrador"))
    data.append(Rol(descripcion="agente"))
    db.session.add_all(data)
    db.session.commit()
    rolAdm =  Rol.query.filter_by(descripcion="administrador").first()
    administrador = User(
        username="admin",
        nombre = "Super",
		apellido = "admin",
		email = "admin@piradesktest.com",
		rol_id = rolAdm.id
    )
    administrador.set_password("admin")
    db.session.add(administrador)
    db.session.commit()