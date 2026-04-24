import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# engine = create_engine(f"sqlite:///{os.path.join(BASE_DIR, 'Database', 'MovieInfo.db')}")
engine = create_engine("postgresql+psycopg2://postgres:jrs%23321@localhost:5432/inapp_db")

SessionLocal = sessionmaker(bind=engine)