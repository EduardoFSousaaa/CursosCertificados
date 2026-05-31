from app.extensions import db
from app.models.assessment import Assessment, AssessmentGrade, Question, StudentAnswer
from app.models.enrollment import Enrollment
from app.models.class_group import ClassGroup


class AssessmentRepository:
    @staticmethod
    def find_by_id(id: int) -> Assessment | None:
        return db.session.get(Assessment, id)

    @staticmethod
    def find_by_id_or_404(id: int) -> Assessment:
        return db.get_or_404(Assessment, id)

    @staticmethod
    def find_by_training(training_id: int) -> list[Assessment]:
        return (
            Assessment.query
            .filter_by(training_id=training_id)
            .order_by(Assessment.applied_on.asc())
            .all()
        )

    @staticmethod
    def save(assessment: Assessment) -> Assessment:
        db.session.add(assessment)
        db.session.commit()
        return assessment

    @staticmethod
    def delete(assessment: Assessment) -> None:
        db.session.delete(assessment)
        db.session.commit()

    @staticmethod
    def find_question_or_404(id: int) -> Question:
        return db.get_or_404(Question, id)

    @staticmethod
    def save_question(question: Question) -> Question:
        db.session.add(question)
        db.session.commit()
        return question

    @staticmethod
    def delete_question(question: Question) -> None:
        db.session.delete(question)
        db.session.commit()

    @staticmethod
    def find_grade(enrollment_id: int, assessment_id: int) -> AssessmentGrade | None:
        return AssessmentGrade.query.filter_by(
            enrollment_id=enrollment_id,
            assessment_id=assessment_id,
        ).first()

    @staticmethod
    def find_all_grades(assessment_id: int) -> list[AssessmentGrade]:
        return (
            AssessmentGrade.query
            .filter_by(assessment_id=assessment_id)
            .all()
        )

    @staticmethod
    def find_enrollment_for_student(training_id: int, student_id: int) -> Enrollment | None:
        return (
            Enrollment.query
            .join(ClassGroup, Enrollment.class_group_id == ClassGroup.id)
            .filter(
                ClassGroup.training_id == training_id,
                Enrollment.student_id == student_id,
            )
            .first()
        )

    @staticmethod
    def find_answers(enrollment_id: int, assessment_id: int) -> list[StudentAnswer]:
        question_ids = db.session.query(Question.id).filter_by(assessment_id=assessment_id)
        return StudentAnswer.query.filter(
            StudentAnswer.enrollment_id == enrollment_id,
            StudentAnswer.question_id.in_(question_ids),
        ).all()
