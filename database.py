from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()


db_url = os.get_env("DB_URL")

engine = create_engine(db_url)
session = sessionmaker(autocommit= False, bind=engine)