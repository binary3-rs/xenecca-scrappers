from os import getenv

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

load_dotenv()

db_type = getenv("DB_TYPE")
db_username = getenv("DB_USERNAME")
db_password = getenv("DB_PASSWORD")
db_endpoint = getenv("DB_ENDPOINT")
db_name = getenv("DB_NAME")
engine = create_engine(
    f"{db_type}://{db_username}:{db_password}@{db_endpoint}/{db_name}", echo=False
)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
db = sqlalchemy
