from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DB = os.getenv("DB")

SQLALCHEMY_DATABASE_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{HOST}:{PORT}/{DB}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
