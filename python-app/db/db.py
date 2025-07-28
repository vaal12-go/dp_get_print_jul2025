import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session, select

from models.region import Region
from models.country import Country


def init_db(echo=False):
    postgres_host = os.getenv("POSTGRES_HOST")

    if postgres_host is None:
        load_dotenv()

    postgres_host = os.getenv("POSTGRES_HOST")
    postgres_port = os.getenv("POSGRES_PORT")
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_pass = os.getenv("POSTGRES_PASSWORD")
    postgres_db_name = os.getenv("POSTGRES_DB_NAME")

    postgres_url = f"postgresql://{postgres_user}:{postgres_pass}@{postgres_host}:5432/{postgres_db_name}"
    # TODO: add DEBUG_SQL_VERBOSE variable, which will control echo of the db_engine
    db_engine = create_engine(postgres_url, echo=echo)
    SQLModel.metadata.create_all(db_engine)
    return db_engine
