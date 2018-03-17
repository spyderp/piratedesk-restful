import os
from app import app
from app import db
from datetime import datetime
from time import time
import jwt 
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

department_user = db.Table('department_user',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('department_id', db.Integer, db.ForeignKey('department.id'), primary_key=True)
) 
# class Assigment(db.Model):
# 	id 			 	= db.Column(db.Integer, primary_key=True)
# 	abierto 		= db.Column(db.Integer)
# 	modificado		= db.Column(db.DateTime, default=datetime.utcnow)
# 	user_id 		= db.Column(db.Integer, ForeignKey('user.id'))
# 	ticket_id	= db.Column(db.Integer, db.ForeignKey('ticket.id'))

class Calendar(db.Model):
	id            = db.Column(db.Integer, primary_key=True)
	descripcion   = db.Column(db.String(15), nullable=False)
	hora_inicio   = db.Column(db.Time)
	hora_final    = db.Column(db.Time)
	fulltime      = db.Column(db.Boolean, default=False)
	dias_festivos = db.Column(db.String(1024))
	priorities    = db.relationship('Priority')

class Client(db.Model):
	id         = db.Column(db.Integer, primary_key=True)
	nombre 	   = db.Column(db.String(60), nullable=False)
	direccion  = db.Column(db.String(250))
	telefono   = db.Column(db.String(30))
	celular    = db.Column(db.String(12))
	email      = db.Column(db.String(60) , unique=True)
	tickets    = db.relationship('Ticket')

class Department(db.Model):
	id 			  = db.Column(db.Integer, primary_key=True)
	descripcion   = db.Column(db.String(45), nullable=False)
	parent_id 	  = db.Column(db.Integer, db.ForeignKey('department.id'))
	user_id 	  = db.Column(db.Integer, db.ForeignKey('user.id'))
	children 	  = db.relationship('Department')
	users         = db.relationship('User')
	knowledges    = db.relationship('Knowledge')
	tickets       = db.relationship('Ticket')

class File(db.Model):
	id         = db.Column(db.Integer, primary_key=True)
	filename   = db.Column(db.String(250), nullable=False)
	uri        = db.Column(db.String(250))
	size       = db.Column(db.Integer)
	type       = db.Column(db.String(15))
	creado     = db.Column(db.DateTime, default=datetime.utcnow)
	modificado = db.Column(db.DateTime, onupdate=datetime.utcnow)
	trophys    = db.relationship('Trophy')
	users      = db.relationship('User',    backref='avatar')
	
	def set_file(self, file):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		uri = app.config['UPLOAD_FOLDER']+'/'+filename
		self.uri      = uri
		self.filename = filename
		self.type     = file.content_type
		self.size     = file.content_length

class ForgotPassword(db.Model):
	id       = db.Column(db.Integer, primary_key=True)
	token    = db.Column(db.String(120))
	password = db.Column(db.String(12))
	expired  = db.Column(db.Integer)
	status   = db.Column(db.Boolean, default=1)
	user_id  = db.Column(db.Integer, db.ForeignKey('user.id'))
	users    = db.relationship('User')

class Knowledge(db.Model):
	id            = db.Column(db.Integer, primary_key=True)
	title         = db.Column(db.String(100), nullable=False, unique=True)
	keys          = db.Column(db.String(100))
	content       = db.Column(db.Text)
	creado        = db.Column(db.DateTime, default=datetime.utcnow)
	modificado    = db.Column(db.DateTime, onupdate=datetime.utcnow)
	department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

class Message(db.Model):
	id           = db.Column(db.Integer, primary_key=True)
	body         = db.Column(db.Text, nullable=False)
	creado       = db.Column(db.DateTime, default=datetime.utcnow)
	privado      = db.Column(db.Boolean, default=False)
	ticket_id    = db.Column(db.Integer, db.ForeignKey('ticket.id'))
	from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	to_user_id   = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
	fromUser     = db.relationship('User',  foreign_keys=from_user_id,)
	toUser       = db.relationship('User', foreign_keys=to_user_id,)

class Priority(db.Model):
	id          = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(10), nullable=False)
	respuesta   = db.Column(db.Time)
	resuelto    = db.Column(db.Time)
	escalabre   = db.Column(db.Boolean)
	calendar_id = db.Column(db.Integer, db.ForeignKey('calendar.id'))	
	tickets     = db.relationship('Ticket') 

class RevokedToken(db.Model):
    __tablename__ = 'revoked_tokens'
    id            = db.Column(db.Integer, primary_key = True)
    jti           = db.Column(db.String(120))
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)

class Rol(db.Model):
	id          = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(15), nullable=False)
	privileges  = db.Column(db.String(1024))
	users     = db.relationship('User') 

class State(db.Model):
	id          = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(15), nullable=False)
	tickets     = db.relationship('Ticket')

class Template(db.Model):
	id          = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(45), nullable=False)
	body        = db.Column(db.Text) 	 
	creado      = db.Column(db.DateTime, default=datetime.utcnow)
	modificado  = db.Column(db.DateTime, onupdate=datetime.utcnow)

class Ticket(db.Model):
	id            = db.Column(db.Integer, primary_key=True)
	titulo        = db.Column(db.String(100), nullable=False)
	content	      = db.Column(db.Text)
	keys          = db.Column(db.String(100))
	creado        = db.Column(db.DateTime, default=datetime.utcnow)
	modificado    = db.Column(db.DateTime, onupdate=datetime.utcnow)
	client_id     = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)
	department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
	priority_id   = db.Column(db.Integer, db.ForeignKey('priority.id'))
	state_id      = db.Column(db.Integer, db.ForeignKey('state.id'))
	user_id	      = db.Column(db.Integer, db.ForeignKey('user.id'))
	messages      = db.relationship('Message')

class Trophy(db.Model):
	id          = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(60), nullable=False)
	puntos      = db.Column(db.Integer, nullable=False)
	creado      = db.Column(db.DateTime, default=datetime.utcnow)
	modificado 	= db.Column(db.DateTime, onupdate=datetime.utcnow)
	file_id	    = db.Column(db.Integer, db.ForeignKey('file.id'))

class User(db.Model):
	id            = db.Column(db.Integer, primary_key=True)
	username      = db.Column(db.String(30), index=True, unique=True)
	password      = db.Column(db.String(128))
	nombre        = db.Column(db.String(15),nullable=False)
	apellido      = db.Column(db.String(15),nullable=False) 
	email         = db.Column(db.String(60) , unique=True, nullable=False)
	activo        = db.Column(db.Boolean, default=1)
	creado        = db.Column(db.DateTime, default=datetime.utcnow)
	modificado    = db.Column(db.DateTime, onupdate=datetime.utcnow)
	ultimo_acceso = db.Column(db.DateTime)
	puntaje	      = db.Column(db.Integer, default=0)
	rol_id 	      = db.Column(db.Integer, db.ForeignKey('rol.id'))
	file_id	      = db.Column(db.Integer, db.ForeignKey('file.id'), default=1)
	# assignments 	= db.relationship('Assignment')
	#knowledges 		= db.relationship('Knowledge')
	tickets 		= db.relationship('Ticket')
	rols 		    = db.relationship('Rol')
	departments		= db.relationship('Department', secondary=department_user , lazy='subquery', backref=db.backref('department_user', lazy=True))
	
	def __repr__(self):
		return '<User %r %r>' % (self.nombre, self.apellido)
	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)
	
	def get_creado(self):
		return datetime.strftime(self.creado, '%d/%m/%Y')
