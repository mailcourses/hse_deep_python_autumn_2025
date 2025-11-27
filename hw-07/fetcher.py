"""Async URL fetcher: для асинхронной обкачки урлов"""

import argparse
import ssl
import asyncio
import aiohttp


async def fetch_url(url, session, sem):
    """
    Асинхронно скачивает старницу
    Через semaphor контролирует кол-во одновременных запросов
    """
    async with sem:
        try:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            async with session.get(url, ssl=ssl_context) as resp:
                text = await resp.text()
                print(f"Fetched {url}")
                return text
        except (asyncio.TimeoutError,
                aiohttp.client_exceptions.ClientConnectorDNSError) as e:
            print(f"Error fetching {url}: {e}")
            return None


async def fetch_batch_urls(urls, session, sem):
    """
    Асинхронно запускает все задачи на обкачку урлов + вывод
    """
    tasks = [
        asyncio.create_task(fetch_url(url, session, sem))
        for url in urls
    ]
    result = await asyncio.gather(*tasks)
    for i, text in enumerate(result):
        if text is not None:
            print(f"Result {i}: {text[:100]}")


def read_urls_from_file(filename):
    """
    Считывает урлы из файла
    """
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def parse_args():
    """
    Собирает аргументы командной строки
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("concurrency", type=int)
    parser.add_argument("urlfile", type=str)
    return parser.parse_args()


async def run(urls, concurrency):
    """
    Создаёт объекты семафор и aiohttp, запускает обкачку urlов
    """
    sem = asyncio.Semaphore(concurrency)
    async with aiohttp.ClientSession() as session:
        await fetch_batch_urls(urls, session, sem)


def main():
    """
    Точка входа. Собираем аргументы командной строки, считываем данные
    И запускаем асинхронное выполнение задач
    """
    args = parse_args()
    urls = read_urls_from_file(args.urlfile)
    asyncio.run(run(urls, args.concurrency))


if __name__ == "__main__":
    main()
