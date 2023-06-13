import datetime as dt
from distutils.util import strtobool
import json
import logging
import os
import signal
import sys
from dotenv import load_dotenv
import requests
import urllib3

load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ALLOW_REDIRECTS = strtobool(os.getenv('ALLOW_REDIRECTS', default='False'))
USER_AGENT = os.getenv(
    'USER_AGENT',
    default=(
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    )
)
RUNS_NUMBER = int(os.getenv('RUNS_NUMBER', default='1'))


def run_urls(urls):
    """Проходим по урлам."""
    global urls_count

    for url in urls:
        if not url.startswith(('https://', 'http://')):
            url = 'https://' + url

        try:
            requests.get(
                url,
                headers={'User-Agent': USER_AGENT},
                timeout=3,
                verify=False,
                allow_redirects=ALLOW_REDIRECTS
            )
            urls_count += 1
        except Exception as e:
            logging.error(e)


def read_urls(filename):
    """Читаем урлы из файла."""
    urls = []

    with open(filename, 'r', encoding='UTF-8') as file:
        for line in file:
            urls.append(line.strip())

    return urls


def write_json() -> None:
    '''Сохраняем стату в json-файлик.'''
    finish = dt.datetime.now()

    info['start_time'] = start_time
    info['finish_time'] = finish.strftime("%Y.%m.%d-%H:%M:%S")
    info['running_time'] = str(
        dt.datetime.combine(finish, finish.time())
        - dt.datetime.combine(start, start.time())
    )
    info['visited_urls_count'] = urls_count

    with open(f'info-{start_time}.json', 'w', encoding='utf-8') as file:
        json.dump(info, file, indent=4)


def signal_handler(signal, frame) -> None:
    """Если остановлен принудительно (Ctrl+C)."""
    write_json()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


if __name__ == '__main__':
    start = dt.datetime.now()
    start_time = start.strftime("%Y.%m.%d-%H:%M:%S")

    info = {}
    urls_count = 0

    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logging.getLogger().setLevel(logging.DEBUG)

    for _ in range(RUNS_NUMBER):
        run_urls(read_urls('urls.txt'))
    
    write_json()
