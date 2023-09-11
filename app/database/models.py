from sqlalchemy import Column, Integer, String
from .database import Base

class Post(Base):
    __tablename__ = "posts"
    ID = Column(Integer, primary_key=True, index=True)
    field_1 = Column(String)
    author = Column(String)
    description = Column(String)
    my_numeric_field = Column(Integer)
