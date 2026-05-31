from flask import Blueprint

from app.controllers.enrollment_controller import EnrollmentController
from app.guards.auth import login_required, role_required
from app.utils.enums import UserRole

enrollments_bp = Blueprint("enrollments", __name__)

_admin_coord = role_required(UserRole.ADMIN, UserRole.COORDINATOR)
_admin_coord_instructor = role_required(UserRole.ADMIN, UserRole.COORDINATOR, UserRole.INSTRUCTOR)

# Rotas públicas — sem login
enrollments_bp.add_url_rule(
    "/<token>",
    "public_form",
    view_func=EnrollmentController.public_form,
    methods=["GET"],
)
enrollments_bp.add_url_rule(
    "/<token>/enviar",
    "submit",
    view_func=EnrollmentController.submit,
    methods=["POST"],
)
enrollments_bp.add_url_rule(
    "/<token>/sucesso",
    "success",
    view_func=EnrollmentController.success,
    methods=["GET"],
)

# Rotas admin
enrollments_bp.add_url_rule(
    "/<int:training_id>/admin",
    "admin_list",
    view_func=_admin_coord_instructor(login_required(EnrollmentController.admin_list)),
    methods=["GET"],
)
enrollments_bp.add_url_rule(
    "/<int:training_id>/admin/<int:req_id>/aprovar",
    "approve",
    view_func=_admin_coord(login_required(EnrollmentController.approve)),
    methods=["POST"],
)
enrollments_bp.add_url_rule(
    "/<int:training_id>/admin/<int:req_id>/rejeitar",
    "reject",
    view_func=_admin_coord(login_required(EnrollmentController.reject)),
    methods=["POST"],
)
