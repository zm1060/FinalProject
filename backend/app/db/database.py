from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = f'mysql+mysqlconnector://root:Zm.1575098153@mysql:3306/fast?charset=utf8&auth_plugin=mysql_native_password'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True
)
# In the above code, the SQLALCHEMY_DATABASE_URL is set to mysql+mysqlconnector://root:your_password@mysql:3306/your_database, where mysql is the hostname of the MySQL service in the Docker Compose network. This URL specifies the database driver, username, password, hostname, port, and database name.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
