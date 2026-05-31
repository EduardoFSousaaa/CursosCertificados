from flask import Blueprint

from app.controllers.reports_controller import ReportsController
from app.guards.auth import login_required, role_required
from app.utils.enums import UserRole

reports_bp = Blueprint("reports", __name__)

_admin_coord = role_required(UserRole.ADMIN, UserRole.COORDINATOR)

reports_bp.add_url_rule(
    "/setores",
    "sectors",
    view_func=_admin_coord(login_required(ReportsController.sectors)),
    methods=["GET"],
)
