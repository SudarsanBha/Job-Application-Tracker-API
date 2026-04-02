from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models import Job
from app.schemas import JobCreate, JobResponse
from app.dependencies.db import get_db

router = APIRouter(prefix="/jobs", tags=["Jobs"])

# CREATE
@router.post("/", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    new_job = Job(**job.model_dump())

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


# READ ALL
@router.get("/", response_model=list[JobResponse])
def get_jobs(status: str = None, db: Session = Depends(get_db)):
    query = db.query(Job)

    if status:
        query = query.filter(Job.status == status)

    return query.all()


# READ ONE
@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found!")
    
    return job


# UPDATE
@router.put("/{job_id}", response_model=JobResponse)
def update_job(job_id: int, job: JobCreate, db: Session = Depends(get_db)):
    existing_job = db.query(Job).filter(Job.id == job_id).first()

    if not existing_job:
        raise HTTPException(status_code=404, detail="Job not found!")
    

    for key, value in job.model_dump().items():
        setattr(existing_job, key, value)

    db.commit()
    db.refresh(existing_job)
    
    return existing_job


# DELETE
@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found!")
    
    db.delete(job)
    db.commit()

    return {"message" : "Job Deleted!"}