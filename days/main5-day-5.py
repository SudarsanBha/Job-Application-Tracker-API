# Day 5: Update responses

# install Pydentic: pip install Pydentic
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from app.models import Base, Job
#import JobCreate from schemas
from app.schemas import JobCreate, JobResponse

#Keep Db SetUp
app = FastAPI()

#Create Tables
Base.metadata.create_all(bind=engine)

#Add/get DB session dependecy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Root EndPoint
@app.get("/")
def read_root():
    return {"message": "Hello World!! API is running"}

# Step 1: POST response
# CREATE jOb(POST with JSON body) 
@app.post("/jobs", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    new_job = Job(**job.model_dump())

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job

#Step 2: GET all responses
# Read all jobs
# Filter jobs(query params)
@app.get("/jobs", response_model=list[JobResponse])
def get_jobs(status: str = None, db: Session = Depends(get_db)):
    query = db.query(Job)

    if status:
        query = query.filter(Job.status == status)
    
    return query.all()

# step 3: GET one response
# Read Single job
@app.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job

# step 4: PUT responses
# UPDATE job(PUT)
@app.put("/jobs/{job_id}", response_model=JobResponse)
def update_job(job_id: int, job: JobCreate, db: Session = Depends(get_db)):
    existing_job = db.query(Job).filter(Job.id == job_id).first()

    if not existing_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    for key, value in job.model_dump().items():
        setattr(existing_job, key, value)

    db.commit()
    db.refresh(existing_job)

    return existing_job
    

# DELETE job
@app.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not Found")
    
    db.delete(job)
    db.commit()

    return {"message": "Job Deleted"}

# Step 5: Add Validation Rules: but already added at schemas.py : title: str = Field(..., min_length=2)