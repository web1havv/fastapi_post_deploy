from fastapi import HTTPException, status, Depends, APIRouter
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db, engine

router = APIRouter(tags=['users'])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')
models.Base.metadata.create_all(bind=engine)


@router.post('/users', status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the plain-text password
    hashed_password = pwd_context.hash(user.password)
    print("Hashed Password:", hashed_password)

    # Update the user object with the hashed password
    user.password = hashed_password

    new_user = models.User(**user.dict())
    print("New User Password:", new_user.password)

    # Add and commit the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    print('User CREATED SUCCESSFULLY')

    return new_user


@router.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    print("reached here")
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'invalid user, user not found')
    return user
