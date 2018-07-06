from functools import wraps
from app.models import User
from flask_jwt_extended import get_jwt_identity
from flask_restful import abort, fields
from flask_mail import Message
from app import mail
from time import time
import string
from random import *
import hashlib
from  datetime import datetime

def roles_required(*role_names):
	def wrapper(func):
		@wraps(func)
		def decorated_view(*args, **kwargs):
			current_user = get_jwt_identity()
			user = User.query.filter_by(username=current_user).first()
			rol = user.rols.descripcion	
			if not (rol in role_names):
				return abort(404)
			# Call the actual view
			return func(*args, **kwargs)
		return decorated_view
	return wrapper



def send_email(subject, sender, recipients, text_body, html_body):
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html = html_body
	mail.send(msg)

def password_generator(min_char = 8, max_char = 12):
	allchar = string.ascii_letters + string.digits
	return "".join(choice(allchar) for x in range(randint(min_char, max_char)))

def token_generator():
	t = long( time() * 1000 )
	allchar = string.ascii_letters + string.digits + str(t)
	return hashlib.md5(allchar).hexdigest()

#Field format
class DateTimeLatinFormat(fields.Raw):
    def format(self, value):
        return datetime.strftime(value,'%d/%m/%Y %H:%I:%S')

class DaysWeek(fields.Raw):
    def format(self, value):
        return datetime.strftime(value,'%d/%m/%Y %H:%I:%S')