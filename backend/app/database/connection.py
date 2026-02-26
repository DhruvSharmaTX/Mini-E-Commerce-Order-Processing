import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()  # read value from .env 

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False) # connects to MySQL

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Created database session

Base = declarative_base() # used by models to create table


def get_db():  # dependency for routes
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        