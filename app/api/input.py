from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from database.database import get_db
from database import models
from schemas import posts


router = APIRouter(
    prefix="/input",
    tags=["Posts"]
)


@router.get("/")
async def root():
    return {"data": "Hola mundo desde input"}