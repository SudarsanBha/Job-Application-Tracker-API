from fastapi import FastAPI
from database import engine
from app.models import Base, Job

app = FastAPI()

#Create Tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello World!! API is running"}
