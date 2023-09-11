from enum import Enum
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session


from database.database import get_db
from database import models
from schemas import posts


router = APIRouter(
    prefix="/input",
    tags=["Posts"]
)


class QueryType(str, Enum):
    field_1 = "field_1"
    author = "author"
    description = "description"


@router.post("/{query}")
async def create_post(query: str, post: posts.PostCreate, db: Session = Depends(get_db)):
    try:
        query_type = QueryType(query)
    except ValueError:
        return JSONResponse(status_code=400, content={"error": f"{query} no es un campo válido para convertir a mayúsculas"})

    if query_type == QueryType.field_1:
        post.field_1 = post.field_1.upper()
    elif query_type == QueryType.author:
        post.author = post.author.upper()
    elif query_type == QueryType.description:
        post.description = post.description.upper()

    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return JSONResponse(status_code=201, content={"id": db_post.ID})
