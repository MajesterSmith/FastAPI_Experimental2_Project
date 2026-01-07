from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQL_ALCHEMY_DATABASE_URL,connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base = declarative_base()

class UserInput(Base):
    __tablename__ = "User_Input"
    id = Column(Integer, primary_key= True, index = True)
    user_email = Column(String, index = True)
    user_password = Column(String)

Base.metadata.create_all(bind = engine)