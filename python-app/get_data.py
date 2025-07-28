import aiofiles
import aiohttp
import asyncio
import time
import importlib

from datafetchers.base_fetcher import BaseFetcher
from datafetchers.wikipedia_fetcher import WikipediaFetcher
from datafetchers.fetcher_utils import DebugOption
from db.db import init_db
from fetchers_list import FETCHER_BACKEND_LIST


def instantiate_class(module_name: str, class_name: str, *instance_args):
    module = importlib.import_module(module_name)
    class_ = getattr(module, class_name)
    return class_(*instance_args)


async def main():
    db_eng = None
    try:
        db_eng = init_db(False)
    except Exception as e:
        print("Exception connecting to the database:")
        print(e)
        exit(1)

    tasks = []

    debug_options_arguments = (DebugOption.NONE, None)
    try:
        for fetcher_class_tuple in FETCHER_BACKEND_LIST:
            fetcher_obj = instantiate_class(*fetcher_class_tuple,
                                            db_eng, *debug_options_arguments)
            tasks.append(asyncio.create_task(fetcher_obj.fetch_data_to_db()))
        # tasks = (asyncio.create_task(fetcher.fetch_data_to_db())
        #          for fetcher in FETCHER_BACKEND_LIST)
        results = await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Exception collecting data:\n\t{e}")

asyncio.run(main())
