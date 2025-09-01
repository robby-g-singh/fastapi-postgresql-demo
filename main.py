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
# Endpoints


@app.get("/")
def root():
    return {"message": "Intro to FastAPI with SQL Demo"}
