from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing_extensions import Annotated
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemas import users
from database.database import get_db
from database import models
from utils.utils import verify
from auth import oauth2


router = APIRouter(
    prefix="/login",
    tags=['Authentication']
    )


@router.post('/', response_model=users.Token)
def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
          db: Annotated[Session, Depends(get_db)]
          ):
    user = db.query(models.User).filter(
        models.User.username == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
