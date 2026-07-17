from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey,JSON
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class MasterResume(Base):
    __tablename__ = "master_resumes"
    id = Column(Integer,primary_key = True)
    user_id = Column(Integer,ForeignKey('users.id'),nullable= False)
    raw_text = Column(String, nullable=False)
    structured_data = Column(JSON,nullable = False)
    created_at = Column(TIMESTAMP(timezone = True),nullable = False,server_default = text('now()'))


class TailoredResume(Base):
    __tablename__ = "tailored_resumes"
    id = Column(Integer,primary_key = True)
    master_resume_id = Column(Integer, ForeignKey('master_resumes.id'))
    user_id = Column(Integer,ForeignKey('users.id'),nullable= False)
    job_description = Column(String,nullable = False)   
    job_title = Column(String)
    company_name = Column(String)
    tailored_content = Column(JSON)
    tailoring_notes = Column(JSON)
    ats_score = Column(Integer,nullable = False)
    created_at = Column(TIMESTAMP(timezone = True),nullable = False,server_default = text('now()'))







