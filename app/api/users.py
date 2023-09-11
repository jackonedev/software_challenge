from fastapi import APIRouter, Depends, HTTPException, status
from database import models
from database.database import get_db
from schemas.users import UserOut, UserCreate
from utils.utils import hash_password


router = APIRouter(
    prefix="/users",
    tags=['Authentication']
)




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db=Depends(get_db)):
    
    # Verificar que el usuario no exista
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    hashed_psw = hash_password(user.password)
    user.password = hashed_psw
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db=Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
    return db_user