from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Student).filter(models.Student.email == student.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = utils.hash_password(student.password)
    new_student = models.Student(
        full_name=student.full_name,
        email=student.email,
        password_hash=hashed_pw,
        student_id=student.student_id
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {"message": "Registration successful"}

@router.post("/login", response_model=schemas.TokenResponse)
def login(student: schemas.StudentLogin, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.email == student.email).first()
    if not db_student or not utils.verify_password(student.password, db_student.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = utils.create_access_token(data={"sub": db_student.email})
    return {"access_token": access_token, "token_type": "bearer"}
