import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Unless DB_CONNECTION_STRING is defined, put the database in the application root
engine = create_engine(
    os.environ.get(
        'DB_CONNECTION_STRING',
        f'sqlite:///{os.path.dirname(os.path.dirname(os.path.dirname(__file__)))}/sample.sqlite3'
    )
)

# Start the database session here
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from app.models.authentication import User, Role, RolesUsers
    Base.metadata.create_all(bind=engine)