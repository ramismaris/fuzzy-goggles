import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import text

load_dotenv()

DATABASE_USER = os.getenv('POSTGRES_USER')
DATABASE_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DATABASE_HOST = 'localhost'
DATABASE_NAME = os.getenv('POSTGRES_DB')
DATABASE_PORT = os.getenv('POSTGRES_PORT')
DATABASE_URL = (
    f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
)

PATH_TO_FILE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/tests/backup.sql'

engine = create_engine(DATABASE_URL, echo=True)

with engine.connect() as con:
    with open(PATH_TO_FILE) as file:
        query = text(file.read())
        con.execute(query)

    con.commit()
