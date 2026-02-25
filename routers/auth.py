from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from database import get_db
from models import User
from schemas import Token, UserCreate
from auth import create_access_token, verify_password, get_password_hash, get_current_user
from utils.audit import log_action

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    log_action(db, user.id, "LOGIN", f"User {form_data.username} logged in")
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
def register(
    user: UserCreate, 
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Only admin can manage users and roles"
        )
    
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed = get_password_hash(user.password)
    db_user = User(
        username=user.username, 
        hashed_password=hashed, 
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    log_action(db, current_user.id, "REGISTER_USER", 
               f"Created user {user.username} with role {user.role}")
    
    return {"msg": "User created successfully"}