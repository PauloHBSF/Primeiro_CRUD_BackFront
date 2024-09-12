from sqlalchemy import create_engine, URL
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

load_dotenv()


drivername='postgresql+psycopg2'
username=os.getenv('POSTGRES_USER')
password=os.getenv('POSTGRES_PASSWORD')
database=os.getenv('POSTGRES_DB')
host=os.getenv('HOST_DB')


uri = f"{drivername}://{username}:{password}@{host}/{database}"
print("-"*40)
print("*"*40)
print("-"*40)
print("*"*40)
print(uri)
print("*"*40)
print("-"*40)
print("*"*40)
print("-"*40)
engine = create_engine(uri)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

