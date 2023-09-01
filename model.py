from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from config import sql_connect

DATABASE_URL = sql_connect

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, index=True)
    chat_id         = Column(String, index=True)
    user_first_name = Column(String)
    user_last_name  = Column(String)
    user_name       = Column(String)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    product_price = Column(Float)
    product_img = Column(String)
    product_article = Column(Integer)


class Orders(Base):
    __tablename__ = "orders"

    id          = Column(Integer, primary_key=True, index=True)
    chat_id     = Column(String, index=True)
    product_id  = Column(Integer)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)