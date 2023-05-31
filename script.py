import logging
import signal
import sys
import requests


def run_urls(urls):
    """Проходим по урлам."""
    for url in urls:
        if not url.startswith(('https://', 'http://')):
            url = 'https://' + url

        try:
            requests.get(url, timeout=3, verify=False)
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
