from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = None
SqlAlchemyBase = declarative_base()

def create():
    global engine, __maker
    engine = create_engine('sqlite:///users.db', echo=False)
    from . import __all_models
    SqlAlchemyBase.metadata.create_all(engine)
    __maker = sessionmaker(bind=engine)

def create_session():
    global __maker
    return __maker()
