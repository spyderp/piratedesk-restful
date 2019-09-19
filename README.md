# PiratedeskFrontend

Mesa de ayuda de software libre.  (Backend)
Debido a la necesidad de tener una opción de sofware libre que use las nuevas tendencia se ha desarrollado este proyecto. 

Si deseas colaborar solo revisa los issue. 

## Caracteisticas

 - Administración de usuarios.
 - Manejo calendario de trabajo.
 - Adminsitración de clientes.
 - Admkinsitración de Departamento
 - Manejo de caso por estados.
 - Configurar días festivos.
 - Gamificación
 - Creación de plantilla para maenejo de casos. 
 - Base de Datos de conocimiento (Knowledges DB)
 - Bandeja de Entrada
 - Seguimiento de caso, chat en tiempo real  
 - Creación y administración de FAQ
 - Configuración

## Caracteristicas técnicas

 - Creado en python 
 - Uso de Framework FLASK
 - RESTFULL
 - Control de usuario y manejo de webtokken. (JWT)
 - CORS. 
 - SQLALCHEMY
 - Envio de correo. 
 - Conexión con mysql/mariadb.
 - Log de errores
 - Socket (pendiente)

## Configuración 

 1. crear el archivo *config.py* en la raiz del proyecto y configurar

```python
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'llave-secreta'
	SQLALCHEMY_DATABASE_URI ='mysql://user:password@localhost/dbname'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	JWT_SECRET_KEY = 'secret-hash-jwt'
	JWT_BLACKLIST_ENABLED=False #lista de blacklist se puede habilitar en producción
	JWT_BLACKLIST_TOKEN_CHECKS=['access', 'refresh'],
	MAIL_SERVER='SMTP MAIL URL'
	MAIL_PORT=254 #PUERTO DE ENVIO DE CORRE
	MAIL_USE_TLS=0 #ACTIVAR si el correo necesita TLS
	MAIL_USERNAME='usuario de correo'
	MAIL_PASSWORD='contraseña de correo'
	UPLOAD_FOLDER = '/ruta de archivos estaticos/piratedeskrestful/app/static/files'
	ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']) #Tipo de archivos permitidos para subir al sistema
	ADMINS = ['correo.administrado@correo.com'] 

class ConfigCors:
	origins = '*' #RUTAS PERMITIDAS PARA ACCEDER en desarrollo trabajar con *
```

 2. Instalar los paquete de dependencia.

```bash
pip install -r requirements.txt
```
***Nota:***  La instalación puede ser en un ambiente virtual (venv) o en contenedor de Docker pueden usar este[Entorno de desarrollo para FLASK](https://github.com/spyderp/Flask-enviroment)

 3. Crear la base de datos.

 Acceder desde una terminal y ejecutar el siguiente comando

```bash
python flask db upgrade
```

 4. Iniciar Servidor

 ```bash
export FLASK_APP=piratedesk.py
export FLASK_DEBUG=1
flask piratedesl.py
```

 5. Acceder a localhost para probar. (verificar el puerto que salio en consola)
 



