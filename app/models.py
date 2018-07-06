# -*- coding: utf-8 -*-
import os, re
from app import app
from app import db
from datetime import datetime
from time import time
import jwt 
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
department_user = db.Table('department_user',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('department_id', db.Integer, db.ForeignKey('department.id'), primary_key=True)
) 
calendar_festive = db.Table('calendar_festive',
	db.Column('calendar_id', db.Integer, db.ForeignKey('calendar.id'), primary_key=True),
	db.Column('festive_id', db.Integer, db.ForeignKey('festive.id'), primary_key=True)
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
	dias          = db.Column(db.String(15), nullable=False)
	hora_inicio   = db.Column(db.Time)
	hora_final    = db.Column(db.Time)
	fulltime      = db.Column(db.Boolean, default=False)
	clients    	  = db.relationship('Client')
	festives	  = db.relationship('Festive', secondary=calendar_festive , lazy='subquery', backref=db.backref('calendar_festive', lazy=True))
	
	@hybrid_property
	def semana(self):
		return self.dias.replace('0','D').replace('1','L').replace('2','M').replace('3','Mi').replace('4','J').replace('5','V').replace('6','S')

class Category(db.Model):
	id          = db.Column(db.Integer, primary_key=True)
	name        = db.Column(db.String(30), nullable=False)
	descripcion = db.Column(db.String(250), nullable=False)

class Client(db.Model):
	id         = db.Column(db.Integer, primary_key=True)
	nombre 	   = db.Column(db.String(60), nullable=False)
	direccion  = db.Column(db.String(250))
	telefono   = db.Column(db.String(30))
	celular    = db.Column(db.String(12))
	email      = db.Column(db.String(60) , unique=True)
	calendar_id = db.Column(db.Integer, db.ForeignKey('calendar.id'),default=1)	
	calendars    = db.relationship('Calendar')
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

class Faq(db.Model):
	id              = db.Column(db.Integer, primary_key=True)
	title           = db.Column(db.String(100), nullable=False, unique=True)
	content         = db.Column(db.Text)
	orden           = db.Column(db.Integer) 
	creado          = db.Column(db.DateTime, default=datetime.utcnow)
	modificado      = db.Column(db.DateTime, onupdate=datetime.utcnow)
	category_id 	= db.Column(db.Integer, db.ForeignKey('category.id'),default=1)
	categories      = db.relationship('Category')

class Festive(db.Model):
	id          = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(50), nullable=False)
	fecha       = db.Column(db.DateTime, nullable=False)

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
	rating        = db.Column(db.Integer, default=0)
	access        = db.Column(db.Integer, default=0)
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
	respuesta   = db.Column(db.Integer)
	resuelto    = db.Column(db.Integer)
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
	content	      = db.Column(db.Text)
	keys          = db.Column(db.String(100))
	creado        = db.Column(db.DateTime, default=datetime.utcnow)
	modificado    = db.Column(db.DateTime, onupdate=datetime.utcnow)
	client_id     = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)
	department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
	priority_id   = db.Column(db.Integer, db.ForeignKey('priority.id'))
	state_id      = db.Column(db.Integer, db.ForeignKey('state.id'))
	user_id	      = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
	clients       = db.relationship('Client')
	departments   = db.relationship('Department')
	priorities    = db.relationship('Priority')
	states        = db.relationship('State')
	users         = db.relationship('User')
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
	
	@validates('username')
	def validate_username(self, key, username):
		if not username:
			raise AssertionError('No username provided')
		if User.query.filter(User.username == username).first():
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


	def __repr__(self):
		return '<User %r %r>' % (self.nombre, self.apellido)
	def get_creado(self):
		return datetime.strftime(self.creado, '%d/%m/%Y')

	def set_password(self, password):
		if not password:
			raise AssertionError('Password not provided')

		if not re.match('\d.*[A-Z]|[0-9].*\d', password):
			raise AssertionError('Password must contain 1 capital letter and 1 number')

		if len(password) < 8 or len(password) > 24:
			raise AssertionError('La contraseña debe ser entre 8 y 24 caracteres')
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)
	
	
