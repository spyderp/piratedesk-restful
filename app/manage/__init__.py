from flask import Blueprint
from app import db
from app.models import File, Rol, User, State, Department, Client, Priority
import string, random

bp = Blueprint('manage', __name__)

@bp.cli.command('dbinit')
def dbinit():
		data = []
		data.append(File(filename="default.png"))
		data.append(Rol(descripcion="administrador"))
		data.append(Rol(descripcion="supervisor"))
		data.append(Rol(descripcion="agente"))
		data.append(Rol(descripcion="cliente"))
		data.append(State(descripcion="New"))
		data.append(State(descripcion="Proccess"))
		data.append(State(descripcion="Pending"))
		data.append(State(descripcion="Close"))
		data.append(State(descripcion="Re-Open"))
		data.append(State(descripcion="Abandoned"))
		data.append(Department(descripcion="IT"))
		data.append(Priority(descripcion="standar", respuesta = 8, resuelto = 72))
		data.append(Priority(descripcion="High", respuesta = 4, resuelto = 24, escalable = 1))
		data.append(Priority(descripcion="Critical", respuesta = 1, resuelto = 4 ))
		data.append(Priority(descripcion="Scheduled or Low", respuesta = 3, resuelto = 7))
		data.append(Client(nombre="Default"))
		db.session.add_all(data)
		db.session.commit()
		rolAdm =  Rol.query.filter_by(descripcion="administrador").first()
		sys = User(
			username="SYSTEM",
			nombre = "COMPUTER",
			apellido = "SYS",
			email = "NOEMAIL@NOEMAIL.com",
			rol_id = rolAdm.id
		)
		administrador = User(
			username="admin",
			nombre = "Super",
			apellido = "admin",
			email = "admin@piradesktest.com",
			rol_id = rolAdm.id
		)
		administrador.set_password("admin")
		sys.set_password(''.join(random.choices(string.ascii_uppercase + string.digits, k = N)))
		db.session.add(sys)
		db.session.add(administrador)
		db.session.commit()