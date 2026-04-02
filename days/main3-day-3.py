from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from app.models import Base, Job

# step 2: Keep Db SetUp
app = FastAPI()

#Create Tables
Base.metadata.create_all(bind=engine)

#: step 3 Add/get DB session dependecy
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

# step: 4 Create Job
@app.post("/jobs")
def create_job(
    title: str,
    company: str,
    status: str,
    date_applied: str,
    notes: str,
    db: Session = Depends(get_db)
):
    job = Job(
        title = title,
        company = company,
        status = status,
        date_applied = date_applied,
        notes = notes
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    return job

#Step 5: Read all jobs
@app.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()

# Step 6: Read Single job
@app.get("/jobs/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job
    
# Step 7: DELETE job
@app.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not Found")
    
    db.delete(job)
    db.commit()

    return {"message": "Job Deleted"}