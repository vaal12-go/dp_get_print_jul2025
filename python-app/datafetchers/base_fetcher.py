from abc import ABC, abstractmethod
from enum import Enum
import random
import asyncio

from .fetcher_utils import DebugOption
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql.expression import Select
from sqlmodel import Session, select, delete, SQLModel
from models.region import Region
from models.country import Country


def delete_and_insert(db_session: Session, statement: Select, new_object: SQLModel) -> None:
    existing_obj = db_session.exec(statement).first()
    if existing_obj is not None:
        db_session.delete(existing_obj)
    db_session.add(new_object)
    db_session.commit()


def get_or_insert(db_session: Session, statement: Select, new_object: SQLModel) -> SQLModel:
    existing_obj = db_session.exec(statement).first()
    if existing_obj is None:
        db_session.add(new_object)
        db_session.commit()
        existing_obj = new_object
    return existing_obj


class BaseFetcher(ABC):
    def __init__(self, db_engine: Engine,
                 debug_option: DebugOption = DebugOption.NONE,
                 debug_file: str = None) -> None:
        self.debug_option = debug_option
        if (self.debug_option == DebugOption.NONE) \
                and \
                (debug_file is not None):
            raise Exception(
                'BaseFetcher class is created with DebugOption.DEBUG_OPTION_NONE and debug_file which is not None.')
        self.debug_file = debug_file
        self.db_engine = db_engine
        self.datasource = "GENERIC"

    @abstractmethod
    async def get_data(self) -> None:
        pass

    def delete_data_for_datasource(self, db_session: Session) -> None:
        countries_statement = delete(Country).where(
            Country.datasource == self.datasource)
        db_session.exec(countries_statement)

        regions_stmt = delete(Region).where(
            Region.datasource == self.datasource)
        db_session.exec(regions_stmt)
        db_session.commit()

    def print_message(self, msg: str) -> None:
        print(f"[{self.datasource}] fetcher:{msg}")

    async def fetch_data_to_db(self) -> None:
        self.print_message("Starting")
        counter = 0
        with Session(self.db_engine, expire_on_commit=False) as session:
            self.delete_data_for_datasource(session)
            for country_reg_list in await self.get_data():
                for country_reg in country_reg_list:
                    (country, reg) = country_reg
                    reg = get_or_insert(session,
                                        select(Region).where(Region.name == reg.name).
                                        where(Region.type == reg.type).
                                        where(Region.datasource ==
                                              reg.datasource).
                                        where(Region.data_year ==
                                              reg.data_year),
                                        reg)

                    country.region_id = reg.id

                    # TODO: delete and insert probably may be removed with complete clean of data for datasource
                    delete_and_insert(session,
                                      select(Country).where(Country.name == country.name).
                                      where(Country.datasource == country.datasource).
                                      where(Country.region_id == reg.id),
                                      country
                                      )
                    counter += 1
        self.print_message("Finished")
        return
