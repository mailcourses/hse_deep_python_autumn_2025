import unittest
from unittest import mock
import asyncio

import fetcher


class TestFetcher(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        print("asyncSetUp")

    async def asyncTearDown(self):
        print("asyncTearDown")

    async def test_fetch_url(self):
        with mock.patch("fetcher.aiohttp.ClientSession.get") as mget:
            text_mock = mock.AsyncMock(return_value="orig_text")
            resp_mock = mock.AsyncMock(text=text_mock)
            mget.return_value.__aenter__.return_value = resp_mock

            result = await fetcher.fetch_url("fake_url")

            self.assertEqual("orig_text", result)

            expected_calls = [
                mock.call("fake_url"),
                mock.call().__aenter__(),
                mock.call().__aenter__().text(),
                mock.call().__aexit__(None, None, None),
            ]            
            self.assertEqual(expected_calls, mget.mock_calls)

    async def test_fetch_url_with_error(self):
        with mock.patch("fetcher.aiohttp.ClientSession.get") as mget:
            mget.side_effect = ValueError("Failed connection")

            with self.assertRaises(ValueError) as err:
                await fetcher.fetch_url("fake_url")

            expected_calls = [
                mock.call("fake_url"),
            ]            
            self.assertEqual(expected_calls, mget.mock_calls)

    async def test_fetch_batch_urls(self):
        resps = {f"url_{i}": f"resp_{i}" for i in range(1, 4)}

        with mock.patch("fetcher.aiohttp.ClientSession.get") as mget:
            text_mock = mock.AsyncMock(side_effect=resps.values())
            resp_mock = mock.AsyncMock(text=text_mock)
            mget.return_value.__aenter__.return_value = resp_mock

            result = await fetcher.fetch_batch_urls(resps.keys())

            self.assertEqual(list(resps.values()), result)
            self.assertEqual(["resp_1", "resp_2", "resp_3"], result)

            expected_calls = []

            for url in resps:
                 expected_calls.extend(
                     [
                         mock.call(url),
                         mock.call().__aenter__(),
                         mock.call().__aenter__().text(),
                         mock.call().__aexit__(None, None, None),
                     ]
                 )
            self.assertEqual(expected_calls, mget.mock_calls)


if __name__ == "__main__":
    unittest.main()
