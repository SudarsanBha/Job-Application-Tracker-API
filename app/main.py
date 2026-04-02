from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import jobs

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(jobs.router)

@app.get("/")
def root():
    return {"message" : "Hello World! API is running!!"}
