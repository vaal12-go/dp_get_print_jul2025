from bs4 import BeautifulSoup

from sqlalchemy.engine.base import Engine
from .base_fetcher import BaseFetcher, DebugOption
from .fetcher_utils import async_fetch_url

from models.region import Region
from models.country import Country
from datafetchers.fetcher_utils import parse_wiki_integer


STATISTICTIMES_COUNTRIES_PAGE_URL = 'https://statisticstimes.com/demographics/countries-by-population.php'

REGION_TYPE = "CONTINENT"


class StatisticTimesFetcher(BaseFetcher):
    def __init__(self, db_engine: Engine,
                 debug_option: DebugOption = DebugOption.NONE,
                 debug_file: str = None) -> None:
        super().__init__(db_engine, debug_option, debug_file)
        self.datasource = "STATISTICTIMES"

    def objects_from_data(self, country: str,
                          population: int, region_name: str, data_year: int) -> tuple[Country, Region]:
        reg = Region()
        reg.name = region_name
        reg.type = REGION_TYPE
        reg.data_year = data_year
        reg.datasource = self.datasource

        ctry = Country()
        ctry.name = country
        ctry.population = population
        ctry.datasource = self.datasource

        return (ctry, reg)

    def stattimes_country_generator(self, html_page):
        soup = BeautifulSoup(html_page, 'html.parser')
        table = soup.find(
            "table", id='table_id').find('tbody')
        rows = table.find_all("tr")
        i = 0

        for row in rows:
            cells = row.find_all('td')
            if cells is not None \
                    and len(cells) == 9:
                country_name = cells[0].find('a').text
                population2023 = parse_wiki_integer(
                    cells[1].text
                )
                population2024 = parse_wiki_integer(
                    cells[3].text
                )
                region_name = cells[8].text
                i += 1
                yield [
                    self.objects_from_data(
                        country_name, population2023, region_name, 2023),
                    self.objects_from_data(
                        country_name, population2024, region_name, 2024),
                ]

        self.print_message(f"Total countries parsed:{i}")

    async def get_data(self) -> None:
        self.print_message("Retrieving data from the web.")
        page_html = await async_fetch_url(
            STATISTICTIMES_COUNTRIES_PAGE_URL,
            debug_option=self.debug_option, debug_file=self.debug_file)
        self.print_message("Web data retrieved. Starting parsing.")
        return self.stattimes_country_generator(page_html)
