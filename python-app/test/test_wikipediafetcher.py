import unittest
import hashlib

from datafetchers.wikipedia_fetcher import WikipediaFetcher
from datafetchers.fetcher_utils import DebugOption
from test.utils_for_test import hash_array_tuple_tree

# To run:
#   uv run python -m unittest test.test_wikipediafetcher


# [x]: combine those 2 functions to generic hasher of arrays, which uses __str__ when meets an object


class WikipediaFetcherTest(unittest.TestCase):
    def test_get_region_country(self):
        debug_options_arguments = (DebugOption.NONE, None)
        wk_fetcher = WikipediaFetcher(None, *debug_options_arguments)
        res_tuple = wk_fetcher.get_region_country("TEST_REGION", "TEST_REGION_TYPE", 1970,
                                                  "TEST_COUNTRY", 123)
        str_hash = hashlib.sha256()
        hash_array_tuple_tree(str_hash, res_tuple)

        self.assertEqual(
            str_hash.hexdigest(),
            '5e9c8ed2c80aa527634bd8c7baf093b143e250115cb106e28e231a00f2e3897d'
        )

    def test_wiki_table_country_generator(self):
        debug_options_arguments = (DebugOption.NONE, None)
        wk_fetcher = WikipediaFetcher(None, *debug_options_arguments)

        with open("test/test_data/wiki_countries_23Jul2025.html", 'rb') as testF:
            test_html = testF.read()
            array_gen = wk_fetcher.wiki_table_country_generator(
                test_html)

            str_hash = hashlib.sha256()
            hash_array_tuple_tree(str_hash, array_gen)
            # print('test_wikipediafetcher:52 str_hash.hexdigest():>>',
            #       str_hash.hexdigest())
            self.assertEqual(
                str_hash.hexdigest(),
                '6a14e6eed4affd757c99f928c43967edbf7f4a2f0175dcd7ba92824e6f6f1ee9'
            )
