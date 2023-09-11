from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database.database import get_db
from database import models
from schemas import posts

from auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/get_data",
    tags=["Posts"]
)

@router.get("/{id}", response_model=posts.Post)
async def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.ID == id).first()
    if db_post is None:
        return JSONResponse(status_code=404, content={"error": f"id {id} no válido"})
    return db_post