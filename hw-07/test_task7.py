""" Файл для тестирования """


import asyncio
import sys
import aiohttp
import pytest


from fetcher import read_urls_from_file, parse_args, run
from fetcher import fetch_url


@pytest.mark.asyncio
async def test_fetch_url_success():
    """Сценарий успешного фетчинга"""
    sem = asyncio.Semaphore(1)
    with open('urls.txt', encoding='utf-8') as f:
        url = f.read().split('\n')[-1]
    async with aiohttp.ClientSession() as session:

        text = await fetch_url(url, session, sem)
        assert text is not None
        assert 'decoreo.ru' in text


@pytest.mark.asyncio
async def test_fetch_url_fail():
    """Сценарий не успешного фетчинга"""
    sem = asyncio.Semaphore(1)
    async with aiohttp.ClientSession() as session:
        url = "https://some-weird-link/"
        text = await fetch_url(url, session, sem)
        assert text is None


def test_read_urls_from_file():
    """Тестирует функцию чтения урлов из файла"""
    with open('urls.txt', encoding='utf-8') as f:
        old_urls = f.read().split('\n')
    with open('test_urls.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(old_urls))
    urls = read_urls_from_file(f.name)
    assert urls == old_urls


def test_parse_args(monkeypatch):
    """Тестирует парсинг аргументов командной строки"""
    test_args = ["fetcher.py", "5", "urls.txt"]
    monkeypatch.setattr(sys, "argv", test_args)
    args = parse_args()
    assert args.concurrency == 5
    assert args.urlfile == "urls.txt"


@pytest.mark.asyncio
async def test_run(tmp_path):
    """Тестирует функцию run."""
    file = tmp_path / "urls.txt"
    lurl = "https://geotargetly.com/"
    file.write_text(lurl)
    urls = read_urls_from_file(str(file))
    await run(urls, 1)
