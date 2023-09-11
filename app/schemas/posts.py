from pydantic import BaseModel, ConfigDict

class PostBase(BaseModel):
    field_1: str
    author: str
    description: str
    my_numeric_field: int

class PostCreate(PostBase):
    pass

class Post(BaseModel):
    ID: int
    field_1: str
    author: str
    description: str
    my_numeric_field: int
    model_config = ConfigDict(from_attributes=True)
