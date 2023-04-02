import os

# RabbitMQ Configuration
# rabbitmq is container's name
# if you want to run it local, you should set it too localhost
# BROKER_URL = 'pyamqp://admin:admin@rabbitmq//'

BROKER_URL = 'amqp://admin:admin@localhost:5672/'
BACKEND_URL = 'rpc://'
# BACKEND_URL = 'amqp://guest:guest@localhost:5672/'
REDIS_BACKEND_URL = 'redis://localhost:6379/0'
# Database Configuration
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Zm.1575098153")
# DB_HOST = os.getenv("DB_HOST", "mysql")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "fast")
DB_CHARSET = os.getenv("DB_CHARSET", "utf8")
DB_AUTH_PLUGIN = os.getenv("DB_AUTH_PLUGIN", "mysql_native_password")

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}&auth_plugin={DB_AUTH_PLUGIN}"
