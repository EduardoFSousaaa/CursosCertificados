import enum


class UserRole(enum.Enum):
    ADMIN = "admin"
    COORDINATOR = "coordinator"
    INSTRUCTOR = "instructor"
    STUDENT = "student"


class TrainingStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Shift(enum.Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"

    @property
    def label(self) -> str:
        return {
            Shift.MORNING: "Manhã (08:00 – 12:00)",
            Shift.AFTERNOON: "Tarde (14:00 – 18:00)",
            Shift.EVENING: "Noite (19:00 – 22:00)",
        }[self]

    @property
    def starts_at(self) -> str:
        return {"morning": "08:00", "afternoon": "14:00", "evening": "19:00"}[self.value]

    @property
    def ends_at(self) -> str:
        return {"morning": "12:00", "afternoon": "18:00", "evening": "22:00"}[self.value]


class EnrollmentStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class FinalConcept(enum.Enum):
    APPROVED = "approved"
    FAILED = "failed"
    PENDING = "pending"
    EXCUSED = "excused"


class AssessmentType(enum.Enum):
    TECHNICAL_TEST = "technical_test"
    QUESTIONNAIRE = "questionnaire"
    PRACTICAL = "practical"


class QuestionType(enum.Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    ESSAY = "essay"


class GradeStatus(enum.Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    GRADED = "graded"

    @property
    def label(self) -> str:
        return {
            GradeStatus.PENDING: "Pendente",
            GradeStatus.SUBMITTED: "Enviado",
            GradeStatus.GRADED: "Corrigido",
        }[self]


class DocumentType(enum.Enum):
    FORM = "form"
    CSV = "csv"
    IMAGE = "image"
    PDF = "pdf"
    LINK = "link"


class EnrollmentRequestStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
