from flask import Blueprint

from app.controllers.class_group_controller import ClassGroupController
from app.guards.auth import login_required, role_required
from app.utils.enums import UserRole

class_groups_bp = Blueprint("class_groups", __name__)

_admin_coord = role_required(UserRole.ADMIN, UserRole.COORDINATOR)

class_groups_bp.add_url_rule(
    "/treinamento/<int:training_id>",
    "manage",
    view_func=_admin_coord(login_required(ClassGroupController.manage)),
    methods=["GET"],
)
class_groups_bp.add_url_rule(
    "/treinamento/<int:training_id>/criar",
    "create",
    view_func=_admin_coord(login_required(ClassGroupController.create)),
    methods=["POST"],
)
class_groups_bp.add_url_rule(
    "/treinamento/<int:training_id>/<int:group_id>/excluir",
    "delete",
    view_func=_admin_coord(login_required(ClassGroupController.delete)),
    methods=["POST"],
)
class_groups_bp.add_url_rule(
    "/treinamento/<int:training_id>/<int:group_id>/inscrever",
    "enroll_manual",
    view_func=_admin_coord(login_required(ClassGroupController.enroll_manual)),
    methods=["POST"],
)
