from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import models
from database.database import engine

from api import input, get_data


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(input.router)
app.include_router(get_data.router)
