from sqlalchemy import Column, Integer, String
from database import Base

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    company = Column(String)
    status = Column(String)
    date_applied = Column(String)
    notes = Column(String)