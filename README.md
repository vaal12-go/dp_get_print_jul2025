# DP get & print 

Simple containerized application, which implements modular website scraping of country/region population data and summarizing the results.
Application utilizes postgres DB for data storage.

## Technology considerations
1. Python application with pluggable scraping modules using python asyncio for web requests

    1. Abstract class based architecture. Concrete scraping classes should be descendants of the datafetchers.BaseFetcher abstract class.
    1. Instantiation of the scraping classes is done dynamically (see FETCHER_BACKEND_LIST in fetchers_list)
1. Postgres (non async psycopg2) database layer:
        
    1. SQLModel (which is pydantic based) for writing data
    1. Direct SQL query via psycopg2 for summarizing the data

1. Docker compose containerization

## Datasources types

Datasource for summarizing the data are set by the DATA_PRINT_SELECTOR environment variable for print_data container (see compose.yaml). If not set, then default values will be used - `WIKIPEDIATABLE_STATISTICAL_2022`.

Format of the variable is the following `[datasource]_[region type]_[data year]`.
Available values for each field (depending on data provided by each datasource):
* Datasource: `WIKIPEDIATABLE`
    * Available region types:
        * `CONTINENTAL`
        * `STATISTICAL`
    * Available years:
        * `2022`
        * `2023`
* Datasource: `STATISTICTIMES`
    * Region type available is only one: `CONTINENT`
    * Available years:
        * `2023`
        * `2024`

## Updates

* 29Jul2025:
    * Added STATISTICTIMES datasource
    * Non async parts of fetchers are covered with tests.
    * As compose.yaml is build simplistically, run `docker compose build` before running new version

## Further improvements
1. Scraping module for statisticstimes.com - DONE
1. Better tests coverage to cover fetching and parsing routines
    1. Partially done. Async parts of fetchers still to be covered.
1. DB structure optimization

    1. Database structure is driven by the models.*.py SQLModel classes (country and region)
    1. Some DB structure review (mostly normalization) would be granted:
        
        1. Create separate 'datasource' model
        1. Country - region relation may be done via intermediate table (as currently country names are duplicated for all region type and year).
        1. Adding indexes for region ids would be needed (in case of higher data loads)
        1. More constraints can be added to the DB, but as SQLModel is a pydantic model, maybe validation on the python model level would be sufficient (esp. if more data would flow into DB, validating before DB INSERT/UPDATE scales better)

    1. DB access strategy to be reviewed (e.g. make deletion of data and it's generation to be one transaction)

        1. Move DB writes/reads to [async posgres driver](https://github.com/MagicStack/asyncpg) 

## Deployment

1. Clone repository
1. If you are upgrading (e.g. used this application before) run `docker compose build` before running new version so containers are rebuit.
1. Run `docker compose up get_data` from the cloned repository directory. This will create postgres container and run container which will download data from the web and populate the DB.
1. Change DATA_PRINT_SELECTOR environment variable for print_data service in the compose.yaml for desired datasource, region type and datapoint year (for a list of possible values see python-app/.env file comments)
1. Run `docker compose up print_data` for summarized data to be printed to the console.


    