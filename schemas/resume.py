from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy import Column, Integer, Text, JSON, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# =====================================================================
# 1. THE DATABASE MODEL (SQLAlchemy)
# =====================================================================
class Master_resume_DB(Base):
    __tablename__ = "master_resumes"

    user_id = Column(Integer, primary_key=True, index=True)
    raw_text = Column(Text, nullable=False)
    structured_data = Column(JSON, nullable=False) 
    created_at = Column(DateTime, default=datetime.utcnow)

# =====================================================================
# 2. THE AI PARSING SUB-SCHEMAS (Pydantic - Made Highly Defensive)
# =====================================================================
class PersonalInfo(BaseModel):
    name: str
    email: Optional[str] = None
    phoneno: Optional[str] = None
    Linked_in: Optional[str] = None
    portfolio: Optional[str] = None

class WorkExperience(BaseModel):
    company: str
    title: str
    dates: Optional[str] = None
    responsiblities: List[str] = Field(default_factory=list)

class project(BaseModel):
    name: str
    tech_stack: List[str] = Field(default_factory=list)
    link: Optional[str] = None

class Education(BaseModel):
    shcool: str  # Intentionally preserved your original layout typo
    degree: str
    year: Optional[str] = None

class certifications(BaseModel):
    issuer: str
    degree: str
    proof: Optional[str] = None  # 👈 Fixed: Now allows missing/null data safely
    link: Optional[str] = None
    year: Optional[str] = None   # 👈 Fixed: Now allows missing/null data safely

class publications(BaseModel):
    publication_type: str
    name: str
    place_of_publication: Optional[str] = None
    link: Optional[str] = None
    date: Optional[str] = None
    contribution: List[str] = Field(default_factory=list)

class acheivements(BaseModel):
    name: str
    level: str
    date: Optional[str] = None

class volunteering(BaseModel):
    name_org: str
    responsibilities: Optional[str] = None

# =====================================================================
# 3. THE MASTER AI TARGET SCHEMA
# =====================================================================
class structure_resume(BaseModel):
    personal_info: PersonalInfo
    education: List[Education] = Field(default_factory=list)
    experiences: List[WorkExperience] = Field(default_factory=list)
    projects: List[project] = Field(default_factory=list)
    Publications: List[publications] = Field(default_factory=list)
    Acheivements: List[acheivements] = Field(default_factory=list)
    certificates: List[certifications] = Field(default_factory=list)
    Volunteering: Optional[volunteering] = None