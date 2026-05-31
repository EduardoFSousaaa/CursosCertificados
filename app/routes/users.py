from flask import Blueprint

from app.controllers.user_controller import UserController
from app.guards.auth import login_required, role_required
from app.utils.enums import UserRole

users_bp = Blueprint("users", __name__)

_admin_coord = role_required(UserRole.ADMIN, UserRole.COORDINATOR)

users_bp.add_url_rule(
    "/perfil",
    "own_profile",
    view_func=login_required(UserController.own_profile),
    methods=["GET"],
)
users_bp.add_url_rule(
    "/<int:user_id>/perfil",
    "profile",
    view_func=login_required(UserController.profile),
    methods=["GET"],
)
users_bp.add_url_rule(
    "/",
    "list_users",
    view_func=_admin_coord(login_required(UserController.list_users)),
    methods=["GET"],
)
users_bp.add_url_rule(
    "/criar",
    "create_user",
    view_func=_admin_coord(login_required(UserController.create_user)),
    methods=["POST"],
)
