from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user

from app.extensions import db
from app.forms.assessment_form import AssessmentForm
from app.models.training import Training
from app.repositories.assessment_repository import AssessmentRepository
from app.repositories.training_repository import TrainingRepository
from app.services.assessment_service import AssessmentService, PASSING_GRADE
from app.utils.enums import QuestionType


class AssessmentController:

    # ── Admin ────────────────────────────────────────────────────────────

    @staticmethod
    def list_page(training_id: int):
        training = TrainingRepository.find_by_id_or_404(training_id)
        assessments = AssessmentRepository.find_by_training(training_id)
        return render_template(
            "pages/assessments/list.html",
            training=training,
            assessments=assessments,
            form=AssessmentForm(),
        )

    @staticmethod
    def create(training_id: int):
        training = TrainingRepository.find_by_id_or_404(training_id)
        form = AssessmentForm()
        if form.validate_on_submit():
            assessment = AssessmentService.create(training_id, form)
            flash("Avaliação criada. Adicione as questões.", "success")
            return redirect(url_for("assessments.questions", assessment_id=assessment.id))
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", "danger")
        return redirect(url_for("assessments.list_page", training_id=training_id))

    @staticmethod
    def questions(assessment_id: int):
        assessment = AssessmentRepository.find_by_id_or_404(assessment_id)
        return render_template(
            "pages/assessments/questions.html",
            assessment=assessment,
            training=assessment.training,
            QuestionType=QuestionType,
        )

    @staticmethod
    def add_question(assessment_id: int):
        assessment = AssessmentRepository.find_by_id_or_404(assessment_id)
        statement = request.form.get("statement", "").strip()
        q_type = request.form.get("type", QuestionType.MULTIPLE_CHOICE.value)

        if not statement:
            flash("O enunciado não pode ser vazio.", "danger")
            return redirect(url_for("assessments.questions", assessment_id=assessment_id))

        options = []
        if q_type == QuestionType.MULTIPLE_CHOICE.value:
            correct_idx = request.form.get("correct_option", "0")
            for i in range(1, 6):
                text = request.form.get(f"option_{i}", "").strip()
                if text:
                    options.append({"text": text, "is_correct": str(i) == correct_idx})
            if len(options) < 2:
                flash("Informe ao menos 2 opções para questão de múltipla escolha.", "danger")
                return redirect(url_for("assessments.questions", assessment_id=assessment_id))
            if not any(o["is_correct"] for o in options):
                flash("Marque a opção correta.", "danger")
                return redirect(url_for("assessments.questions", assessment_id=assessment_id))

        AssessmentService.add_question(assessment, statement, q_type, options)
        flash("Questão adicionada.", "success")
        return redirect(url_for("assessments.questions", assessment_id=assessment_id))

    @staticmethod
    def delete_question(assessment_id: int, question_id: int):
        question = AssessmentRepository.find_question_or_404(question_id)
        if question.assessment_id != assessment_id:
            abort(404)
        AssessmentRepository.delete_question(question)
        flash("Questão removida.", "warning")
        return redirect(url_for("assessments.questions", assessment_id=assessment_id))

    @staticmethod
    def results(assessment_id: int):
        assessment = AssessmentRepository.find_by_id_or_404(assessment_id)
        if current_user.is_instructor and assessment.training.instructor_id != current_user.id:
            abort(403)
        grades = AssessmentRepository.find_all_grades(assessment_id)
        return render_template(
            "pages/assessments/results.html",
            assessment=assessment,
            training=assessment.training,
            grades=grades,
            passing_grade=PASSING_GRADE,
        )

    # ── Aluno ────────────────────────────────────────────────────────────

    @staticmethod
    def take(assessment_id: int):
        assessment = AssessmentRepository.find_by_id_or_404(assessment_id)
        enrollment = AssessmentRepository.find_enrollment_for_student(
            assessment.training_id, current_user.id
        )
        if enrollment is None:
            flash("Você não está inscrito neste treinamento.", "danger")
            return redirect(url_for("trainings.list"))

        existing_grade = AssessmentRepository.find_grade(enrollment.id, assessment_id)
        if existing_grade and existing_grade.grade is not None:
            return redirect(url_for("assessments.result", assessment_id=assessment_id))

        return render_template(
            "pages/assessments/take.html",
            assessment=assessment,
            training=assessment.training,
            QuestionType=QuestionType,
        )

    @staticmethod
    def submit(assessment_id: int):
        assessment = AssessmentRepository.find_by_id_or_404(assessment_id)
        enrollment = AssessmentRepository.find_enrollment_for_student(
            assessment.training_id, current_user.id
        )
        if enrollment is None:
            abort(403)

        existing_grade = AssessmentRepository.find_grade(enrollment.id, assessment_id)
        if existing_grade and existing_grade.grade is not None:
            return redirect(url_for("assessments.result", assessment_id=assessment_id))

        AssessmentService.submit_answers(assessment, enrollment, request.form)
        return redirect(url_for("assessments.result", assessment_id=assessment_id))

    @staticmethod
    def result(assessment_id: int):
        assessment = AssessmentRepository.find_by_id_or_404(assessment_id)
        enrollment = AssessmentRepository.find_enrollment_for_student(
            assessment.training_id, current_user.id
        )
        if enrollment is None:
            abort(403)

        grade = AssessmentRepository.find_grade(enrollment.id, assessment_id)
        answers = {
            a.question_id: a
            for a in AssessmentRepository.find_answers(enrollment.id, assessment_id)
        }
        return render_template(
            "pages/assessments/result.html",
            assessment=assessment,
            training=assessment.training,
            grade=grade,
            answers=answers,
            passing_grade=PASSING_GRADE,
            passed=AssessmentService.passed(grade.grade if grade else None),
            QuestionType=QuestionType,
        )
