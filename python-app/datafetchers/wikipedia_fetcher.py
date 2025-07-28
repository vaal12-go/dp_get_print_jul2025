from sqlalchemy.engine.base import Engine

from .base_fetcher import BaseFetcher, DebugOption
from .fetcher_utils import async_fetch_url

from models.region import Region
from models.country import Country

from bs4 import BeautifulSoup


def parse_wiki_integer(number_str: str) -> int:
    replaced_str = number_str.replace(',', '')
    return int(replaced_str)


REGION_TYPE_CONTINENTAL = "CONTINENTAL"
REGION_TYPE_STATISTICAL = "STATISTICAL"

WIKI_COUNTRIES_PAGE_URL = 'https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_(United_Nations)&oldid=1215058959'


class WikipediaFetcher(BaseFetcher):
    def __init__(self, db_engine: Engine,
                 debug_option: DebugOption = DebugOption.NONE,
                 debug_file: str = None) -> None:
        super().__init__(db_engine, debug_option, debug_file)
        self.datasource = "WIKIPEDIATABLE"

    def get_region_country(self, region_name, region_type, region_year,
                           country_name, populaton) -> tuple[Country, Region]:
        ret_reg = Region()
        ret_reg.datasource = self.datasource
        ret_reg.name = region_name
        ret_reg.type = region_type
        ret_reg.data_year = region_year

        ret_ctry = Country()
        ret_ctry.datasource = self.datasource
        ret_ctry.name = country_name
        ret_ctry.population = populaton

        return (ret_ctry, ret_reg)

    def objects_from_row(self, country: str,
                         population2022: int, population2023: int,
                         region_continental: str, region_statistical: str) -> list(tuple[Country, Region]):
        ret = []
        rc_tuple = self.get_region_country(
            region_continental, REGION_TYPE_CONTINENTAL, 2022,
            country, population2022
        )
        ret.append(rc_tuple)

        rc_tuple = self.get_region_country(
            region_statistical, REGION_TYPE_STATISTICAL, 2022,
            country, population2022
        )
        ret.append(rc_tuple)

        rc_tuple = self.get_region_country(
            region_continental, REGION_TYPE_CONTINENTAL, 2023,
            country, population2023
        )
        ret.append(rc_tuple)

        rc_tuple = self.get_region_country(
            region_statistical, REGION_TYPE_STATISTICAL, 2023,
            country, population2023
        )
        ret.append(rc_tuple)
        return ret

    def wiki_table_country_generator(self, html_page):
        soup = BeautifulSoup(html_page, 'html.parser')
        table = soup.find(
            "div", id='mw-content-text').find('table').find('tbody')
        rows = table.find_all("tr")
        i = 1
        for row in rows:
            table_cells = row.find_all('td')
            if table_cells is not None \
                    and \
                    len(table_cells) == 6:

                a_tags = table_cells[0].find_all('a')

                country_name = a_tags[0].text
                if len(a_tags) > 1 and \
                        '[' not in a_tags[1].text:
                    country_name = f"{country_name} ({a_tags[1].text})"

                if country_name is not None:
                    if country_name == "World":
                        self.print_message('Skipping "country" "World"')
                        continue
                else:
                    continue

                try:
                    parsed_population2022 = parse_wiki_integer(
                        table_cells[1].string)
                    parsed_population2023 = parse_wiki_integer(
                        table_cells[2].string)
                except Exception as e:
                    self.print_message(
                        f"Skipping country {country_name} due to exception:\n\t{e}")
                    continue

                i += 1
                if table_cells[4].find('a') is not None:
                    region_cont = table_cells[4].find('a').string
                    region_stat = table_cells[5].find('a').string

                    yield self.objects_from_row(
                        country_name,
                        parsed_population2022, parsed_population2023,
                        region_cont, region_stat)
        self.print_message(f"Total rows processed:{i}")

    async def get_data(self) -> None:
        wiki_html = await async_fetch_url(
            WIKI_COUNTRIES_PAGE_URL,
            debug_option=self.debug_option, debug_file=self.debug_file)
        return self.wiki_table_country_generator(wiki_html)
