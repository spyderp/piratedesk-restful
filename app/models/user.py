from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
# from common.association_table import association


class User(db.Model):
	id 					= db.Column(db.Integer, primary_key=True)
	username 			= db.Column(db.String(30), index=True, unique=True)
	password  			= db.Column(db.String(128))
	nombre     		= db.Column(db.String(15))
	apellido    			= db.Column(db.String(15))
	email        		= db.Column(db.String(60) , unique=True)
	activo       			= db.Column(db.Boolean)
	creado      		= db.Column(db.DateTime, default=datetime.utcnow)
	modificado      	= db.Column(db.DateTime)
	ultimo_acceso      = db.Column(db.DateTime)
	puntaje 			= db.Column(db.Integer)
	rol_id 				= db.Column(db.Integer, db.ForeignKey('rol.id'))
	# assignments 		= db.relationship('Assignment')
	# histories 			= db.relationship('History')
	# knowledges 		= db.relationship('Knowledge')
	# messages 			= db.relationship('Message')
	# tickets 				= db.relationship('Ticket')
	# deparments		 = db.relationship('Deparment', secondary=association.deparments , lazy='subquery', backref=db.backref('deparments', lazy=True))
	
	def __repr__(self):
		return '<User %r %r>' % (self.nombre, self.apellido)
	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)