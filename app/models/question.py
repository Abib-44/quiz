from sqlalchemy import Column, Text, DateTime, text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
import enum

class QuestionType(str, enum.Enum):
    multiple = "multiple"
    truefalse = "truefalse"

class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question = Column(Text, nullable=False)
    type = Column(Enum(QuestionType), nullable=False)
    options = Column(Text, nullable=True)
    answer = Column(Text, nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("category.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=text("now()"))