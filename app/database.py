import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SETTINGS_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'settings.json')

with open(SETTINGS_FILE_PATH, 'r') as file:
    settings = json.load(file)

db_settings = settings['database']
SQLALCHEMY_DATABASE_URL = (
    f"mysql+mysqlconnector://{db_settings['username']}:{db_settings['password']}@"
    f"{db_settings['host']}:{db_settings['port']}/{db_settings['dbname']}"
)

# SQLAlchemy 설정
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)