import logging
import os
import signal
import sys
from dotenv import load_dotenv
import requests
import urllib3

load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

USER_AGENT = os.getenv(
    'USER_AGENT',
    default=(
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    )
)


def run_urls(urls):
    """Проходим по урлам."""
    for url in urls:
        if not url.startswith(('https://', 'http://')):
            url = 'https://' + url

        try:
            requests.get(
                url,
                headers={'User-Agent': USER_AGENT},
                timeout=3,
                verify=False,
                allow_redirects=False
            )
        except Exception as e:
            logging.error(e)


def read_urls(filename):
    """Читаем урлы из файла."""
    urls = set()

    with open(filename, 'r', encoding='UTF-8') as file:
        for line in file:
            urls.add(line.strip())

    return urls


def signal_handler(signal, frame) -> None:
    """Если остановлен принудительно (Ctrl+C)."""
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logging.getLogger().setLevel(logging.DEBUG)

    run_urls(read_urls('urls.txt'))
