from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    student_id = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())

    assignments = relationship("Assignment", back_populates="student")

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    filename = Column(String)
    original_text = Column(Text)
    topic = Column(String)
    academic_level = Column(String)
    word_count = Column(Integer)
    uploaded_at = Column(TIMESTAMP, server_default=func.now())

    student = relationship("Student", back_populates="assignments")
    analysis = relationship("AnalysisResult", back_populates="assignment", uselist=False)

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    suggested_sources = Column(Text)
    plagiarism_score = Column(Float)
    research_suggestions = Column(Text)
    citation_recommendations = Column(Text)
    confidence_score = Column(Float)
    analyzed_at = Column(TIMESTAMP, server_default=func.now())

    assignment = relationship("Assignment", back_populates="analysis")
