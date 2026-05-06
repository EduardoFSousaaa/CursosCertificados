from flask import flash, redirect, render_template, url_for

from app.exceptions.app_errors import NotFoundError
from app.forms.training_form import TrainingForm
from app.services.training_service import TrainingService


class TrainingsController:
    @staticmethod
    def list_page():
        trainings = TrainingService.list_all()
        return render_template("pages/trainings/list.html", trainings=trainings)

    @staticmethod
    def form_page():
        return render_template("pages/trainings/form.html", form=TrainingForm())

    @staticmethod
    def create():
        form = TrainingForm()
        if form.validate_on_submit():
            TrainingService.create(form)
            flash("Treinamento cadastrado com sucesso!", "success")
        else:
            for field_name, errors in form.errors.items():
                label = getattr(form, field_name).label.text
                for error in errors:
                    flash(f"{label}: {error}", "danger")
        return redirect(url_for("trainings.list"))

    @staticmethod
    def detail(id: int):
        training = TrainingService.get_by_id(id)
        return render_template("pages/trainings/detail.html", training=training)

    @staticmethod
    def delete(id: int):
        try:
            TrainingService.remove(id)
            flash("Treinamento removido.", "warning")
        except NotFoundError:
            flash("Treinamento não encontrado.", "danger")
        return redirect(url_for("trainings.list"))
