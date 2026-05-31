from datetime import datetime

from flask_login import current_user

from app.extensions import db
from app.forms.assessment_form import AssessmentForm
from app.models.assessment import (
    Assessment, AssessmentGrade, Question, QuestionOption, StudentAnswer,
)
from app.models.enrollment import Enrollment
from app.repositories.assessment_repository import AssessmentRepository
from app.utils.enums import AssessmentType, GradeStatus, QuestionType

PASSING_GRADE = 7.0


class AssessmentService:
    @staticmethod
    def create(training_id: int, form: AssessmentForm) -> Assessment:
        assessment = Assessment(
            training_id=training_id,
            title=form.title.data.strip(),
            description=form.description.data.strip() if form.description.data else None,
            type=AssessmentType(form.type.data),
            applied_on=form.applied_on.data,
            created_by_id=current_user.id,
        )
        return AssessmentRepository.save(assessment)

    @staticmethod
    def add_question(assessment: Assessment, statement: str, q_type: str, options: list[dict]) -> Question:
        """options: list of {text, is_correct} — only for MULTIPLE_CHOICE."""
        next_order = max((q.order_number for q in assessment.questions), default=0) + 1
        question = Question(
            assessment_id=assessment.id,
            statement=statement.strip(),
            type=QuestionType(q_type),
            order_number=next_order,
        )
        db.session.add(question)
        db.session.flush()

        if question.type == QuestionType.MULTIPLE_CHOICE:
            for i, opt in enumerate(options, start=1):
                text = opt.get("text", "").strip()
                if not text:
                    continue
                db.session.add(QuestionOption(
                    question_id=question.id,
                    text=text,
                    is_correct=opt.get("is_correct", False),
                    order_number=i,
                ))

        db.session.commit()
        return question

    @staticmethod
    def submit_answers(assessment: Assessment, enrollment: Enrollment, raw_answers: dict) -> AssessmentGrade:
        """raw_answers: {question_id: option_id_or_text_str}"""
        for question in assessment.questions:
            value = raw_answers.get(str(question.id))
            if value is None:
                continue

            if question.type == QuestionType.MULTIPLE_CHOICE:
                try:
                    option_id = int(value)
                except (ValueError, TypeError):
                    option_id = None
                answer = StudentAnswer(
                    enrollment_id=enrollment.id,
                    question_id=question.id,
                    option_id=option_id,
                )
            else:
                answer = StudentAnswer(
                    enrollment_id=enrollment.id,
                    question_id=question.id,
                    text_answer=str(value).strip(),
                )
            db.session.add(answer)

        db.session.flush()

        grade_value, status = AssessmentService._auto_grade(assessment, enrollment.id)

        grade_record = AssessmentGrade(
            enrollment_id=enrollment.id,
            assessment_id=assessment.id,
            grade=grade_value,
            status=status,
        )
        db.session.add(grade_record)
        db.session.commit()
        return grade_record

    @staticmethod
    def _auto_grade(assessment: Assessment, enrollment_id: int) -> tuple[float | None, GradeStatus]:
        mc_questions = [q for q in assessment.questions if q.type == QuestionType.MULTIPLE_CHOICE]
        if not mc_questions:
            return None, GradeStatus.PENDING

        correct_ids = {
            opt.question_id
            for q in mc_questions
            for opt in q.options
            if opt.is_correct
        }
        answers = {
            a.question_id: a
            for a in StudentAnswer.query.filter(
                StudentAnswer.enrollment_id == enrollment_id,
                StudentAnswer.question_id.in_([q.id for q in mc_questions]),
            ).all()
        }

        correct_count = sum(
            1 for q in mc_questions
            if answers.get(q.id) and answers[q.id].option_id in {
                opt.id for opt in q.options if opt.is_correct
            }
        )
        grade = round((correct_count / len(mc_questions)) * 10, 2)
        return grade, GradeStatus.GRADED

    @staticmethod
    def passed(grade: float | None) -> bool:
        return grade is not None and float(grade) >= PASSING_GRADE
