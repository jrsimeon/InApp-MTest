# import os
from sqlalchemy import Column, String, create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class TitleBasics(Base):
    __tablename__ = "title_basics"

    tconst = Column(String, primary_key=True)
    primaryTitle = Column(String)
    originalTitle = Column(String)
    titleType = Column(String)

class NameBasics(Base):
    __tablename__ = "name_basics"

    nconst = Column(String, primary_key=True)
    primaryName = Column(String)
    knownForTitles = Column(String)

