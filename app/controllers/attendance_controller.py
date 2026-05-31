import os
from datetime import date

from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename

from flask import abort

from app.extensions import db
from app.models.class_group import ClassGroup
from app.models.document import Document
from app.repositories.attendance_repository import AttendanceRepository
from app.services.attendance_service import AttendanceService
from app.utils.enums import DocumentType


def _check_instructor_owns_group(group: ClassGroup) -> None:
    """Aborts 403 if the current user is an instructor not assigned to this training."""
    if current_user.is_instructor and group.training.instructor_id != current_user.id:
        abort(403)

_ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "webp"}


def _upload_dir() -> str:
    path = os.path.join(current_app.root_path, "..", "instance", "uploads", "attendance")
    os.makedirs(path, exist_ok=True)
    return os.path.abspath(path)


class AttendanceController:
    @staticmethod
    def mark(group_id: int):
        group = db.get_or_404(ClassGroup, group_id)
        _check_instructor_owns_group(group)

        raw_date = request.args.get("data")
        selected_date: date | None = None
        if raw_date:
            try:
                selected_date = date.fromisoformat(raw_date)
            except ValueError:
                pass

        attendance_map: dict = {}
        if selected_date:
            attendance_map = AttendanceService.get_session(group_id, selected_date)

        past_dates = AttendanceRepository.dates_with_records(group_id)

        uploaded_docs = Document.query.filter_by(
            training_id=group.training_id,
        ).filter(Document.name.like(f"presença_turma_{group_id}_%")).order_by(
            Document.created_at.desc()
        ).all()

        return render_template(
            "pages/attendance/mark.html",
            group=group,
            training=group.training,
            enrollments=group.enrollments,
            selected_date=selected_date,
            attendance_map=attendance_map,
            past_dates=past_dates,
            uploaded_docs=uploaded_docs,
        )

    @staticmethod
    def save(group_id: int):
        group = db.get_or_404(ClassGroup, group_id)
        _check_instructor_owns_group(group)

        raw_date = request.form.get("class_date")
        if not raw_date:
            flash("Informe a data da aula.", "danger")
            return redirect(url_for("attendance.mark", group_id=group_id))
        try:
            class_date = date.fromisoformat(raw_date)
        except ValueError:
            flash("Data inválida.", "danger")
            return redirect(url_for("attendance.mark", group_id=group_id))

        present_ids = {int(v) for v in request.form.getlist("present")}
        AttendanceService.save(group.enrollments, class_date, present_ids)
        flash(f"Presença de {class_date.strftime('%d/%m/%Y')} registrada.", "success")
        return redirect(url_for("attendance.mark", group_id=group_id, data=class_date.isoformat()))

    @staticmethod
    def print_sheet(group_id: int):
        group = db.get_or_404(ClassGroup, group_id)

        raw_date = request.args.get("data")
        selected_date: date | None = None
        attendance_map: dict = {}
        if raw_date:
            try:
                selected_date = date.fromisoformat(raw_date)
                attendance_map = AttendanceService.get_session(group_id, selected_date)
            except ValueError:
                pass

    @staticmethod
    def upload_sheet(group_id: int):
        group = db.get_or_404(ClassGroup, group_id)
        file = request.files.get("file")
        if not file or not file.filename:
            flash("Selecione um arquivo.", "danger")
            return redirect(url_for("attendance.mark", group_id=group_id))

        ext = file.filename.rsplit(".", 1)[-1].lower()
        if ext not in _ALLOWED_EXTENSIONS:
            flash("Formato não permitido. Use PDF, PNG ou JPG.", "danger")
            return redirect(url_for("attendance.mark", group_id=group_id))

        label = request.form.get("label", "").strip() or date.today().isoformat()
        safe_label = secure_filename(label)
        filename = f"presenca_turma_{group_id}_{safe_label}.{ext}"
        file.save(os.path.join(_upload_dir(), filename))

        doc = Document(
            name=f"presença_turma_{group_id}_{label}",
            type=DocumentType.PDF if ext == "pdf" else DocumentType.IMAGE,
            url=filename,
            training_id=group.training_id,
            uploader_id=current_user.id,
        )
        db.session.add(doc)
        db.session.commit()
        flash("Lista de presença anexada.", "success")
        return redirect(url_for("attendance.mark", group_id=group_id))

    @staticmethod
    def serve_doc(doc_id: int):
        from flask import send_file, abort as _abort
        doc = db.get_or_404(Document, doc_id)
        path = os.path.join(_upload_dir(), doc.url)
        if not os.path.exists(path):
            _abort(404)
        return send_file(path)

    @staticmethod
    def print_sheet(group_id: int):
        group = db.get_or_404(ClassGroup, group_id)

        raw_date = request.args.get("data")
        selected_date: date | None = None
        attendance_map: dict = {}
        if raw_date:
            try:
                selected_date = date.fromisoformat(raw_date)
                attendance_map = AttendanceService.get_session(group_id, selected_date)
            except ValueError:
                pass

        return render_template(
            "pages/attendance/print.html",
            group=group,
            training=group.training,
            enrollments=group.enrollments,
            selected_date=selected_date,
            attendance_map=attendance_map,
            today=date.today(),
        )
