from datetime import datetime

from app.extensions import db
from app.utils.enums import AssessmentType, GradeStatus, QuestionType


class Assessment(db.Model):
    __tablename__ = "assessments"

    id = db.Column(db.Integer, primary_key=True)
    training_id = db.Column(db.Integer, db.ForeignKey("trainings.id"), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    type = db.Column(
        db.Enum(AssessmentType, native_enum=False, length=20),
        nullable=False,
        default=AssessmentType.QUESTIONNAIRE,
    )
    grade_weight = db.Column(db.Numeric(4, 2), nullable=True)
    applied_on = db.Column(db.Date, nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    questions = db.relationship(
        "Question", backref="assessment", lazy="select", cascade="all, delete-orphan",
        order_by="Question.order_number",
    )
    grades = db.relationship("AssessmentGrade", backref="assessment", lazy="select", cascade="all, delete-orphan")
    created_by = db.relationship("User", foreign_keys=[created_by_id])

    def __repr__(self) -> str:
        return f"<Assessment {self.title!r}>"


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey("assessments.id"), nullable=False, index=True)
    statement = db.Column(db.Text, nullable=False)
    type = db.Column(
        db.Enum(QuestionType, native_enum=False, length=20),
        nullable=False,
        default=QuestionType.MULTIPLE_CHOICE,
    )
    image_url = db.Column(db.String(500), nullable=True)
    order_number = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    options = db.relationship(
        "QuestionOption", backref="question", lazy="select", cascade="all, delete-orphan",
        order_by="QuestionOption.order_number",
    )
    answers = db.relationship("StudentAnswer", backref="question", lazy="select", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Question #{self.order_number} assessment_id={self.assessment_id}>"


class QuestionOption(db.Model):
    __tablename__ = "question_options"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False, index=True)
    text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False, default=False)
    order_number = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self) -> str:
        return f"<QuestionOption question_id={self.question_id} correct={self.is_correct}>"


class StudentAnswer(db.Model):
    __tablename__ = "student_answers"
    __table_args__ = (
        db.UniqueConstraint("enrollment_id", "question_id", name="uq_answer_enrollment_question"),
    )

    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey("enrollments.id"), nullable=False, index=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False, index=True)
    option_id = db.Column(db.Integer, db.ForeignKey("question_options.id"), nullable=True)
    text_answer = db.Column(db.Text, nullable=True)
    answered_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    option = db.relationship("QuestionOption")

    def __repr__(self) -> str:
        return f"<StudentAnswer enrollment_id={self.enrollment_id} question_id={self.question_id}>"


class AssessmentGrade(db.Model):
    __tablename__ = "assessment_grades"
    __table_args__ = (
        db.UniqueConstraint("enrollment_id", "assessment_id", name="uq_grade_enrollment_assessment"),
    )

    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey("enrollments.id"), nullable=False, index=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey("assessments.id"), nullable=False, index=True)
    grade = db.Column(db.Numeric(5, 2), nullable=True)
    status = db.Column(
        db.Enum(GradeStatus, native_enum=False, length=15),
        nullable=False,
        default=GradeStatus.PENDING,
    )
    notes = db.Column(db.Text, nullable=True)
    graded_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    graded_by = db.relationship("User", foreign_keys=[graded_by_id])

    def __repr__(self) -> str:
        return f"<AssessmentGrade enrollment_id={self.enrollment_id} grade={self.grade}>"
