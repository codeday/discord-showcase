from os import getenv

from sqlalchemy import *
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
postgres_db = {
    "drivername": "postgres",
    "username": getenv("DB_USERNAME", "discord-showcase"),
    "password": getenv("DB_PASSWORD"),
    "database": getenv("DB_DB", "discord-showcase"),
    "host": getenv("DB_HOST", "postgres-master-pg.service.consul"),
    "port": 5432,
}
postgres_url = URL(**postgres_db)
engine = create_engine(postgres_url)
metadata = MetaData()

Base = declarative_base(bind=engine, metadata=metadata)


class Pod(Base):
    __tablename__ = "pods"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    tc_id = Column(String, nullable=False)
    mentor = Column(String, nullable=False)
    teams = relationship("Team", back_populates="team", cascade="all, delete")


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    pod =


def session_creator() -> Session:
    session = sessionmaker(bind=engine)
    return session()


global_session: Session = session_creator()
