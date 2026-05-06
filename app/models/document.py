from datetime import datetime

from app.extensions import db
from app.utils.enums import DocumentType


class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(
        db.Enum(DocumentType, native_enum=False, length=15),
        nullable=False,
        default=DocumentType.PDF,
    )
    url = db.Column(db.String(1000), nullable=False)
    size_bytes = db.Column(db.BigInteger, nullable=True)
    training_id = db.Column(db.Integer, db.ForeignKey("trainings.id"), nullable=True, index=True)
    uploader_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    is_archived = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Document {self.name!r}>"
