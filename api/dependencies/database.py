"""SQLAlchemy connection setup and request-scoped sessions."""
import os
from sqlalchemy import create_engine, event
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import conf


SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL") or URL.create(
    "mysql+pymysql",
    username=conf.user,
    password=conf.password,
    host=conf.host,
    port=conf.port,
    database=conf.database,
    query={"charset": "utf8mb4"},
)

is_sqlite = str(SQLALCHEMY_DATABASE_URL).startswith("sqlite")
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False} if is_sqlite else {},
)

# SQLite tests need actual foreign-key enforcement, like MySQL provides.
if is_sqlite:
    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
