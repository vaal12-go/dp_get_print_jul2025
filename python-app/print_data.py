import os
from dotenv import dotenv_values, load_dotenv
from psycopg2 import connect
from psycopg2.extras import RealDictCursor

from prettytable import PrettyTable


REGION_SQL_QUERY = '''
    SELECT 
        regions_grouped.name as "Reg. name", 
        regions_grouped.sum_population as "Total popul.",
		max_country.name as "Max. country",
		regions_grouped.max_population as "Max. popul.",
		min_country.name as "Min. country",
		regions_grouped.min_population as "Min. popul."
    FROM (
        SELECT region.id as region_id, region.name as name, SUM(country.population) as sum_population,
                    MIN(country.population) as min_population, MAX(country.population) as max_population
        FROM region
        JOIN country ON
            region.id = country.region_id
        WHERE
            -- region.datasource = 'WIKIPEDIA_TABLE'
            region.datasource = %(datasource)s
            AND
            region.type = %(region_type)s
            AND
            region.data_year = %(data_year)s
        GROUP BY region.id, region.name
    ) as regions_grouped
JOIN country as max_country 
	ON
      max_country.region_id = regions_grouped.region_id
      AND
      max_country.population = regions_grouped.max_population
JOIN country as min_country 
	ON
      min_country.region_id = regions_grouped.region_id
      AND
      min_country.population = regions_grouped.min_population
ORDER BY "Reg. name"
'''


def print_query_row(qrow):
    print(
        f"Region:{qrow["Reg. name"]} Total population:{qrow["Total popul."]}",
        f"\n\tSmallest country:{qrow["Min. country"]} population:{qrow["Min. popul."]}",
        f"\n\tLargest country:{qrow["Max. country"]} population:{qrow["Max. popul."]}"
    )


def parse_data_print_selector(selector_str: str) -> tuple[str, str, int]:
    selector_arr = selector_str.split('_')
    if len(selector_arr) != 3:
        raise Exception(
            f"DATA_PRINT_SELECTOR environment variable should have 3 components (see python-app/.env file for explanation and possible values). Provided value:{selector_str}")
    return {
        'datasource': selector_arr[0],
        'region_type': selector_arr[1],
        'data_year': int(selector_arr[2])}


if __name__ == "__main__":
    postgres_host = os.getenv("POSTGRES_HOST")
    if postgres_host is None:
        config = dotenv_values(".env")
        postgres_host = config["POSTGRES_HOST"]
        postgres_port = config["POSGRES_PORT"]
        postgres_user = config["POSTGRES_USER"]
        postgres_pass = config["POSTGRES_PASSWORD"]
        postgres_db_name = config["POSTGRES_DB_NAME"]
        print_selector = config["DATA_PRINT_SELECTOR"]
    else:
        postgres_port = os.getenv("POSGRES_PORT")
        postgres_user = os.getenv("POSTGRES_USER")
        postgres_pass = os.getenv("POSTGRES_PASSWORD")
        postgres_db_name = os.getenv("POSTGRES_DB_NAME")
        print_selector = os.getenv("DATA_PRINT_SELECTOR")

    if print_selector is None:
        print("DATA_PRINT_SELECTOR env variable is not provided. Using default:WIKIPEDIATABLE_STATISTICAL_2022")
        print_selector = 'WIKIPEDIATABLE_STATISTICAL_2022'

    print('Effective DATA_PRINT_SELECTOR:>>', print_selector)
    prnt_selectors_params = parse_data_print_selector(print_selector)

    conn = connect(
        database=postgres_db_name,
        user=postgres_user,
        password=postgres_pass,
        host=postgres_host,
        port=postgres_port)

    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(REGION_SQL_QUERY, prnt_selectors_params)

    table = None
    try:
        terminal_dimensions = os.get_terminal_size()
        if terminal_dimensions[0] >= 91:
            table = PrettyTable()
    except Exception as e:
        # the terminal in docker does not support getting size - will print without table
        pass

    row_count = 0
    while True:
        row = cursor.fetchone()
        if row is None:
            break

        if row_count == 0 and table is not None:
            table.field_names = row.keys()
            table._max_width = {"Reg. name": 10,
                                "Total popul.": 11,
                                "Min. country": 15,
                                "Min. popul.": 8,
                                "Max. popul.": 15,
                                "Max. country": 11
                                }
        if table is not None:
            row_data = [row[key] for key in row.keys()]
            table.add_row(row_data)
        else:
            print_query_row(row)

        row_count += 1

    if table is not None:
        print(table)
    print(f"Total regions:{row_count}")

    conn.commit()
    conn.close()
