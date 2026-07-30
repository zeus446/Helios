from app.database import Base
from sqlalchemy import Column,Integer,String,ForeignKey,Boolean

class UserPreferences(Base):
    __tablename__ = "preferences"

    id = Column(Integer,nullable=False,primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False,unique=True)
    job_title = Column(String, nullable=False)
    location = Column(String,nullable=False)
    remote_only=  Column(Boolean,default=False)
    employment_type = Column(String,nullable=False)

