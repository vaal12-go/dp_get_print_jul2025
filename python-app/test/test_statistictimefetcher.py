import unittest
import hashlib
import types


from datafetchers.statistictimes_fetcher import StatisticTimesFetcher
from datafetchers.fetcher_utils import DebugOption
from test.utils_for_test import hash_array_tuple_tree

# To run:
# uv run python -m unittest test.test_statistictimefetcher


class StatisticTimesFetcherTest(unittest.TestCase):
    def test_objects_from_data(self):
        debug_options_arguments = (DebugOption.NONE, None)
        st_fetcher = StatisticTimesFetcher(None, *debug_options_arguments)
        res_tuple = st_fetcher.objects_from_data("TEST_COUNTRY", 123,
                                                 "TEST_REGION",  1970)

        str_hash = hashlib.sha256()
        hash_array_tuple_tree(str_hash, res_tuple)

        print('test_statistictimefetcher:21 str_hash.hexdigest():>>',
              str_hash.hexdigest())

        self.assertEqual(
            str_hash.hexdigest(),
            'd0874bc37f5eceecc49f1da4fa8cc604c5637084feec321d93436332ff6741c9'
        )

    def test_stattimes_country_generator(self):
        debug_options_arguments = (DebugOption.NONE, None)
        st_fetcher = StatisticTimesFetcher(None, *debug_options_arguments)

        with open("test/test_data/statistictimes_page_28Jul2025.html", 'rb') as testF:
            test_html = testF.read()
            array_gen = st_fetcher.stattimes_country_generator(
                test_html)

            str_hash = hashlib.sha256()
            hash_array_tuple_tree(str_hash, array_gen)
            # print('test_wikipediafetcher:52 str_hash.hexdigest():>>',
            #       str_hash.hexdigest())
            self.assertEqual(
                str_hash.hexdigest(),
                '4f61e2a8ff51dc01daadd045dda36f529169dbb91c6e8e55eb26fc0823a76ddd'
            )
