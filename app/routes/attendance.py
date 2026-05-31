from flask import Blueprint

from app.controllers.attendance_controller import AttendanceController
from app.guards.auth import login_required, role_required
from app.utils.enums import UserRole

attendance_bp = Blueprint("attendance", __name__)

_admin_coord = role_required(UserRole.ADMIN, UserRole.COORDINATOR)
_admin_coord_instructor = role_required(UserRole.ADMIN, UserRole.COORDINATOR, UserRole.INSTRUCTOR)

attendance_bp.add_url_rule(
    "/<int:group_id>",
    "mark",
    view_func=_admin_coord_instructor(login_required(AttendanceController.mark)),
    methods=["GET"],
)
attendance_bp.add_url_rule(
    "/<int:group_id>/salvar",
    "save",
    view_func=_admin_coord_instructor(login_required(AttendanceController.save)),
    methods=["POST"],
)
attendance_bp.add_url_rule(
    "/<int:group_id>/imprimir",
    "print_sheet",
    view_func=login_required(AttendanceController.print_sheet),
    methods=["GET"],
)
attendance_bp.add_url_rule(
    "/<int:group_id>/upload",
    "upload_sheet",
    view_func=_admin_coord_instructor(login_required(AttendanceController.upload_sheet)),
    methods=["POST"],
)
attendance_bp.add_url_rule(
    "/doc/<int:doc_id>",
    "serve_doc",
    view_func=login_required(AttendanceController.serve_doc),
    methods=["GET"],
)
