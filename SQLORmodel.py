# import os
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class TitleBasics(Base):
    __tablename__ = "title_basics"

    tconst = Column(String, primary_key=True)
    titleType = Column(String)
    primaryTitle = Column(String)
    originalTitle = Column(String)
    isAdult = Column(Integer)          # 0 or 1
    startYear = Column(Integer)
    endYear = Column(Integer)
    runtimeMinutes = Column(Integer)
    genres = Column(String)


class NameBasics(Base):
    __tablename__ = "name_basics"

    nconst = Column(String, primary_key=True)
    primaryName = Column(String)
    birthYear = Column(Integer)
    deathYear = Column(Integer)
    primaryProfession = Column(String)
    knownForTitles = Column(String)


class TitlePrincipals(Base):
    __tablename__ = "title_principals"

    tconst = Column(String, ForeignKey("title_basics.tconst"), primary_key=True)
    nconst = Column(String, ForeignKey("name_basics.nconst"), primary_key=True)


