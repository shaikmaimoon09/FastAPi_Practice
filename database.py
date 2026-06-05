# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker



# db_url = "postgresql://postgres:Qwerty%401@localhost:5432/mydb"
# engine = create_engine(db_url)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)