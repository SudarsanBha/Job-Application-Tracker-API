'''
from pydantic import BaseModel

class JobCreate(BaseModel):
    title:str
    company: str
    status: str
    date_applied: str
    notes: str
'''

#Day-5: Update 
from pydantic import BaseModel, Field
from typing import Optional

# Input schema for creating/ updating
class JobCreate(BaseModel):
    title: str = Field(..., min_length=2)
    company: str = Field(..., min_length=2)
    status: str
    date_applied: str
    notes: Optional[str] = None

#Output schema (What API rturns)
class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    status: str
    date_applied: str
    notes: Optional[str]

    
    class Config:
        from_attributes = True # Important for SQLAlchemy