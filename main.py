# FastAPI with SQL Integration
# CRUD Operations / HTTP Requests
# Create - POST
# Read  - GET
# Update - PUT
# Delete - DELETE
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base  # base model for SQLAlchemy
from sqlalchemy.orm import sessionmaker, Session

from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Integration with SQL Demo")

# ---------------- Database setup; Business/DB Interaction Layer ------------------------
# connection to the actual database; bridge to SQLite:
engine = create_engine("sqlite:///users.db", connect_args={"check_same_thread": False})
# factory for creating sessions; sessions are used to talk to the database (query, insert, update, delete operations):
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# SQLAlchemy class to define database models:
Base = declarative_base()  # base class to build DB model around


# -------------------- Database Layer ------------------------
# SQLAlchemy ORM Model
class User(Base):
    __tablename__ = "users"  # Defines table name in the database

    # columns in the user table with constraints provided:
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    role = Column(String(100), nullable=False)


# links model to our engine:
Base.metadata.create_all(engine)  # looks at all classes that inherit from Base; for User class, it creates the actual
# users table inside users.db if it does not exist


# -------------------- API Layer --------------------------------

# Create Pydantic Models; API models of what is sent and received

# UserCreate: shape of data the API expects when a client sends a request
class UserCreate(BaseModel):
    # id not defined here because clients do not send IDs when creating users, the database generates it
    name: str
    email: str
    role: str


# UserResponse: defines shape of data the API returns in responses
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True  # allows Pydantic to convert SQLAlchemy ORM objects into Pydantic models automatically


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


get_db()


# Endpoints

@app.get("/")
def root():
    return {"message": "Intro to FastAPI with SQL Demo"}


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    # to receive a user we need to query the DB to fetch a user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    return user


@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # query to check if email exists in database:
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=404, detail="User already exists!")
    # Create a new user
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()  # always commit after a change to the database is made
    db.refresh(new_user)

    return new_user
