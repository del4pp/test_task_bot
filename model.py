from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from config import sql_connect

DATABASE_URL = sql_connect

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, index=True)
    cat_id          = Column(String, index=True)
    user_first_name = Column(String)
    user_last_name  = Column(String)
    user_name       = Column(String)