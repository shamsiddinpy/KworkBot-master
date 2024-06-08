import datetime
import os
from dotenv import load_dotenv
from sqlalchemy import DateTime, create_engine
from sqlalchemy.orm import declarative_base, mapped_column, Session

load_dotenv()
Base = declarative_base()


class Config:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_CONFIG = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(Config().DB_CONFIG)
session = Session(engine)


class AbstractClass(Base):
    __abstract__ = True
    create_at = mapped_column(DateTime, default=datetime.datetime.utcnow)
    updated_at = mapped_column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
