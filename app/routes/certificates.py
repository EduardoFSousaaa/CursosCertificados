from flask import Blueprint

from app.controllers.certificate_controller import CertificateController
from app.guards.auth import login_required, role_required
from app.utils.enums import UserRole

certificates_bp = Blueprint("certificates", __name__)

_admin_coord = role_required(UserRole.ADMIN, UserRole.COORDINATOR)

certificates_bp.add_url_rule(
    "/treinamento/<int:training_id>",
    "admin_list",
    view_func=_admin_coord(login_required(CertificateController.admin_list)),
    methods=["GET"],
)
certificates_bp.add_url_rule(
    "/<int:enrollment_id>/emitir",
    "issue",
    view_func=_admin_coord(login_required(CertificateController.issue)),
    methods=["POST"],
)
certificates_bp.add_url_rule(
    "/<int:enrollment_id>/enviar-email",
    "send_email",
    view_func=_admin_coord(login_required(CertificateController.send_email)),
    methods=["POST"],
)
certificates_bp.add_url_rule(
    "/<int:enrollment_id>/download",
    "download",
    view_func=login_required(CertificateController.download),
    methods=["GET"],
)
