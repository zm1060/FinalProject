from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config.config import SQLALCHEMY_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True
)
# In the above code, the SQLALCHEMY_DATABASE_URL is set to mysql+mysqlconnector://root:your_password@mysql:3306/your_database, where mysql is the hostname of the MySQL service in the Docker Compose network. This URL specifies the database driver, username, password, hostname, port, and database name.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
