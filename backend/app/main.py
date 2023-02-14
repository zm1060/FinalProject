'''API module
'''
import sqlalchemy as sa
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import scoped_session, sessionmaker
from backend.config import MySQLConfig
from backend.app.routers import base
from backend.db import Base



def create_app() -> FastAPI:
    '''Create FastAPI app
    Returns:
        FastAPI
    '''
    config = MySQLConfig()
    engine = sa.create_engine(
        f'mysql://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}?charset=utf8mb4',
        pool_size=20,
    )
    origins = ['*']
    sess = scoped_session(sessionmaker(engine))
    base.bind = engine
    base.query = sess.query_property()
    graphql_app = GraphQLApp(schema=schema)
    app = FastAPI(
        title="Eyes API",
        description="Eyes public opinion mining system API.",
        version="0.0.1",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app.include_router(base.router)

    return app


app = create_app()
