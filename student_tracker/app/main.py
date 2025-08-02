from fastapi import FastAPI
from .database import engine
from .models import models
from .api import api

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
