from app import api
from app.resources.auth import Auth, TokenRefresh, LogoutAccess, LogoutRefresh
from app.resources.clients import Clients
from app.resources.departments import Departments
from app.resources.files import Files
from app.resources.priorities import Priorities
from app.resources.rols import Rols
from app.resources.states import States
from app.resources.templates import Templates
from app.resources.tickets import Tickets
from app.resources.users import Users, Reset_password_request, Reset_password

api.add_resource(Auth, '/login')
api.add_resource(Clients, '/clients', '/clients/<client_id>')
api.add_resource(Departments, '/departments', '/departments/<department_id>')
api.add_resource(Files, '/files', '/files/<filename>')
api.add_resource(LogoutAccess, '/logout/access')
api.add_resource(LogoutRefresh, '/logout/refresh')
api.add_resource(Priorities, '/priorities', '/priorities/<priority_id>')
api.add_resource(Reset_password, '/reset/token/<token>')
api.add_resource(Reset_password_request, '/reset/password')
api.add_resource(Rols, '/rols', '/rols/<rol_id>')
api.add_resource(States, '/states', '/states/<state_id>')
api.add_resource(Templates, '/templates', '/templates/<template_id>')
api.add_resource(Tickets, '/tickets', '/tickets/<ticket_id>')
api.add_resource(TokenRefresh, '/token/refresh')
api.add_resource(Users, '/users', '/users/<user_id>')
