import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	SQLALCHEMY_DATABASE_URI ='mysql://prueba:123456@localhost/piratedesk'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	JWT_SECRET_KEY = 'lodsf9032o4jkdsfguj8j8bqw34r5t9b0q32'
	JWT_BLACKLIST_ENABLED=True
	JWT_BLACKLIST_TOKEN_CHECKS=['access', 'refresh']

class ConfigCors:
	origins = '*'