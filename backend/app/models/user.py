from sqlalchemy import Column, String, Integer
from pydantic import BaseModel
from app.db.database import Base, engine

class User(Base):
    __tablename__ = 'users'  # 数据库表名
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    password = Column(String(200))


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


if __name__ == '__main__':
    Base.metadata.create_all(engine)