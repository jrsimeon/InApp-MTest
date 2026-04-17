import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

engine = create_engine(f"sqlite:///{os.path.join(BASE_DIR, 'Database', 'MovieInfo.db')}")

SessionLocal = sessionmaker(bind=engine)