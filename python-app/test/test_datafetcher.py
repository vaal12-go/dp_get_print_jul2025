import unittest
from datafetchers.base_fetcher import BaseFetcher, DebugOption

# To run:
#   uv run python -m unittest tests.datafetcher_tests
#   uv run python -m unittest discover -v


class DataFetchersTest(unittest.TestCase):
    def test_constructor_debug(self):
        with self.assertRaises(Exception):
            fetcher = BaseFetcher(
                debug_option=DebugOption.NONE, debug_file="somefile.txt")


if __name__ == '__main__':
    unittest.main()
