from flask import Blueprint

from app.controllers import googleController
from app.controllers.trainings_controller import TrainingsController
from app.guards.auth import login_required, role_required
from app.utils.enums import UserRole

google_auth_bp = Blueprint('google_auth', __name__, url_prefix='/auth')
trainings_bp = Blueprint("trainings", __name__)

_admin_coord = role_required(UserRole.ADMIN, UserRole.COORDINATOR)

trainings_bp.add_url_rule("/", "list", view_func=login_required(TrainingsController.list_page))
trainings_bp.add_url_rule("/form", "form", view_func=_admin_coord(TrainingsController.form_page))
trainings_bp.add_url_rule("/add", "add", view_func=_admin_coord(TrainingsController.create), methods=["POST"])
trainings_bp.add_url_rule("/<int:id>/detail", "detail", view_func=login_required(TrainingsController.detail))
trainings_bp.add_url_rule("/delete/<int:id>", "delete", view_func=_admin_coord(TrainingsController.delete), methods=["POST"])

# 4. Registro do sub-blueprint com o prefixo correto de URL (/auth)
trainings_bp.register_blueprint(google_auth_bp, url_prefix='/auth')

# 5. Regras de rotas para Autenticação do Google
# O nome do endpoint foi alterado para 'NovaCredenciaisGoogle' para bater com o seu controller
google_auth_bp.add_url_rule(
    "/configurar-google", 
    "NovaCredenciaisGoogle", 
    view_func=login_required(googleController.NovaCredenciaisGoogle), 
    methods=["GET"]
)

# Rota de retorno do Google (Callback)
google_auth_bp.add_url_rule(
    '/oauth2callback', 
    'oauth2callback', 
    view_func=googleController.oauth2callback, 
    methods=['GET']
)