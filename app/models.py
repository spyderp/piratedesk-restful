# -*- coding: utf-8 -*-
import os, re
from app import db, app
from datetime import datetime
from time import time
import jwt 
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

SYSUSER = 2

client_user = db.Table('client_user',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('client_id', db.Integer, db.ForeignKey('client.id'), primary_key=True)
) 
department_user = db.Table('department_user',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('department_id', db.Integer, db.ForeignKey('department.id'), primary_key=True)
) 

file_ticket = db.Table('file_ticket',
	db.Column('file_id', db.Integer, db.ForeignKey('file.id'), primary_key=True),
	db.Column('ticket_id', db.Integer, db.ForeignKey('ticket.id'), primary_key=True)
) 

class Assigment(db.Model):
	id 			 	= db.Column(db.Integer, primary_key=True)
	abierto 		= db.Column(db.Boolean, default=True)
	supervisor 		= db.Column(db.Boolean, default=False)
	edit 			= db.Column(db.Boolean, default=False)
	creado          = db.Column(db.DateTime, default=datetime.utcnow)
	user_id 		= db.Column(db.Integer, db.ForeignKey('user.id'))
	ticket_id	= db.Column(db.Integer, db.ForeignKey('ticket.id'))

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
	user_id 	    = db.Column(db.Integer, db.ForeignKey('user.id'))
	children 	    = db.relationship('Department')
	tickets       = db.relationship('Ticket')


class File(db.Model):
	id         = db.Column(db.Integer, primary_key=True)
	filename   = db.Column(db.String(250), nullable=False)
	uri        = db.Column(db.String(250))
	size       = db.Column(db.Integer)
	type       = db.Column(db.String(15))
	creado     = db.Column(db.DateTime, default=datetime.utcnow)
	modificado = db.Column(db.DateTime, onupdate=datetime.utcnow)
	users      = db.relationship('User', backref='avatar', lazy=True)
	
	def set_file(self, file):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		uri = app.config['UPLOAD_FOLDER']+'/'+filename
		self.uri      = uri
		self.filename = filename
		self.type     = file.content_type
		self.size     = os.stat(uri).st_size

class ForgotPassword(db.Model):
	id       = db.Column(db.Integer, primary_key=True)
	token    = db.Column(db.String(120))
	password = db.Column(db.String(12))
	expired  = db.Column(db.Integer)
	status   = db.Column(db.Boolean, default=1)
	user_id  = db.Column(db.Integer, db.ForeignKey('user.id'))
	users    = db.relationship('User')

class Key(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	word = db.Column(db.String(60)) 


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
	def set_message_sys(self, msg):
		self.body = msg
		self.from_user_id = SYSUSER

class Priority(db.Model):
	id          = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(10), nullable=False)
	respuesta   = db.Column(db.Integer, nullable=False)
	resuelto    = db.Column(db.Integer, nullable=False)
	escalable   = db.Column(db.Boolean, default=False)
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
	content	      = db.Column(db.Text, nullable=False)
	keys          = db.Column(db.String(100))
	email         = db.Column(db.String(60), nullable=False)
	telefono   	  = db.Column(db.String(30))
	celular    	  = db.Column(db.String(12))
	creado        = db.Column(db.DateTime, default=datetime.utcnow)
	modificado    = db.Column(db.DateTime, onupdate=datetime.utcnow)
	client_id     = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)
	department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
	priority_id   = db.Column(db.Integer, db.ForeignKey('priority.id'))
	state_id      = db.Column(db.Integer, db.ForeignKey('state.id'))
	user_id	      = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
	files				  = db.relationship('File', secondary=file_ticket, lazy='subquery', backref=db.backref('tickets', lazy=True))
	clients       = db.relationship('Client')
	departments   = db.relationship('Department')
	priorities    = db.relationship('Priority')
	states        = db.relationship('State')
	users         = db.relationship('User')
	messages      = db.relationship('Message')
	assigments 	  = db.relationship('Assigment')


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
	Assigments 	  = db.relationship('Assigment')
	tickets 	  = db.relationship('Ticket')
	rols 		  = db.relationship('Rol')
	clients		  = db.relationship('Client', secondary=client_user , lazy='subquery', backref=db.backref('users', lazy=True))
	departments	  = db.relationship('Department', secondary=department_user , lazy='subquery', backref=db.backref('users', lazy=True))
	
	@validates('username')
	def validate_username(self, key, username):
		if not username:
			raise AssertionError('No username provided')
		if User.query.filter(User.username == username).first() and not self.id: 
			raise AssertionError('El usuario esta en uso')
		if len(username) < 5 or len(username) > 20:
			raise AssertionError('El usuario debe tener entre 5 y 20 caracteres')
		return username

	@validates('email')
	def validate_email(self, key, email):
		if not email:
			raise AssertionError('No email provided')

		if not re.match("[^@]+@[^@]+\.[^@]+", email):
			raise AssertionError('correo no valido')

		return email

	# @validates('password')
	# def validate_password(self, key, password):
	# 	if not password:
	# 		raise AssertionError('Password not provided')

	# 	# if not re.match('\d.*[A-Z]|[0-9].*\d', password):
	# 	# 	raise AssertionError('Password must contain 1 capital letter and 1 number')

	# 	if len(password) < 8 or len(password) > 24:
	# 		raise AssertionError('La contraseña debe ser entre 8 y 24 caracteres')
	# 	return password

	def __repr__(self):
		return '<User %r %r>' % (self.nombre, self.apellido)
	def get_creado(self):
		return datetime.strftime(self.creado, '%d/%m/%Y')

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)
	
	
