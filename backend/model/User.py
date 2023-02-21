from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class ProtectedUser(BaseModel):
    username: str
    hashed_password: str
