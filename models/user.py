from sqlalchemy import Column, Integer, String,ForeignKey,Boolean
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key = True)
    fullname = Column(String,nullable = False)
    email = Column(String,nullable = False,unique = True)
    hashed_password = Column(String,nullable = False)
    created_at = Column(TIMESTAMP(timezone = True),nullable = False,server_default = text('now()'))


