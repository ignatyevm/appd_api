from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import redis

import config

engine = create_engine(config.db_url, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

redis_session = redis.StrictRedis(host='127.0.0.1', port=6379, password='admin12345', decode_responses=True)

def init_db():
    import models
    Base.metadata.create_all(bind=engine)