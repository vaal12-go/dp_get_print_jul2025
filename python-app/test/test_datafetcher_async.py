import asyncio
import unittest
from datafetchers.base_fetcher import BaseFetcher, DebugOption
from datafetchers.fetcher_utils import async_fetch_url

# TODO: add string and file hashing functions to test against hashes


class BaseFetcherAsyncTest(unittest.IsolatedAsyncioTestCase):
    async def test_async_fetch_url(self):
        result = await async_fetch_url('https://api.restful-api.dev/objects/7')
        self.assertEqual(
            result,
            b'{"id":"7","name":"Apple MacBook Pro 16","data":{"year":2019,"price":1849.99,"CPU model":"Intel Core i9","Hard disk size":"1 TB"}}'
        )

    async def test_async_fetch_url_save_file(self):
        result = await async_fetch_url('https://api.restful-api.dev/objects/7')
        self.assertEqual(
            result,
            b'{"id":"7","name":"Apple MacBook Pro 16","data":{"year":2019,"price":1849.99,"CPU model":"Intel Core i9","Hard disk size":"1 TB"}}'
        )


if __name__ == '__main__':
    unittest.main()
