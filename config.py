import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'piratedesk7865674765476'
	SQLALCHEMY_DATABASE_URI ='mysql://prueba:123456@localhost/piratedesk'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	JWT_SECRET_KEY = 'lodsf9032o4jkdsfguj8j8bqw34r5t9b0q32'
	JWT_BLACKLIST_ENABLED=False
	JWT_BLACKLIST_TOKEN_CHECKS=['access', 'refresh'],
	MAIL_SERVER='zimbra.meduca.gob.pa'
	MAIL_PORT=587
	MAIL_USE_TLS=1
	MAIL_USERNAME='ricardo.portillo'
	MAIL_PASSWORD='RgpR987?'
	UPLOAD_FOLDER = '/home/spyder/Workspaces/piratedesk-restful/app/static/files'
	ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


class ConfigCors:
	origins = '*'