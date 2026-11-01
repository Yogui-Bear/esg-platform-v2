from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cif = Column(String, unique=True, index=True, nullable=False)
    sector = Column(String, nullable=False)
    employees = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    assessments = relationship("ESGAssessment", back_populates="company")

class ESGAssessment(Base):
    __tablename__ = "esg_assessments"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    score_environmental = Column(Float, nullable=False)
    score_social = Column(Float, nullable=False)
    score_governance = Column(Float, nullable=False)
    total_score = Column(Float, nullable=False)
    rating = Column(String, nullable=False)
    raw_metrics = Column(JSON, nullable=False)
    recommendations = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    company = relationship("Company", back_populates="assessments")
