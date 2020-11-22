from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = None
SqlAlchemyBase = declarative_base()


def create(environ):
    global engine, __maker
    if 'MYSQL_DBNAME' not in environ:
        engine = create_engine('sqlite:///users.db', echo=False)
    else:
        engine = create_engine(f'mysql+mysqldb://{environ["MYSQL_USERNAME"]}:{environ["MYSQL_PASSWORD"]}@localhost:3306/{environ["MYSQL_DBNAME"]}', pool_pre_ping=True)
    from . import __all_models
    SqlAlchemyBase.metadata.create_all(engine)
    __maker = sessionmaker(bind=engine)


def create_session():
    global __maker
    return __maker()
