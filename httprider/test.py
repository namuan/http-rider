import logging
from threading import Thread
from multiprocessing import Process
import requests
import urllib.request

logging.basicConfig(format="%(threadName)-10s - %(message)s", level=logging.DEBUG)


def thread_get(delay, url):
    s = requests.Session()
    logging.debug(f"Making request with {delay} seconds delay")
    r = s.get(url)
    logging.debug(f"Received Response - {r.status_code}")


def thread_urllib(delay, url):
    logging.debug(f"Making request with {delay} seconds delay")
    with urllib.request.urlopen(url) as response:
        j = response.read()
        logging.debug(f"Received Response - {j}")


# host = "https://httpbin.org"
host = "http://localhost:8000"

worker_thread = thread_get

t1 = Process(target=worker_thread, args=(10, f"{host}/delay/10"))
t1.start()

t2 = Process(target=worker_thread, args=(3, f"{host}/delay/3"))
t2.start()

t3 = Process(target=worker_thread, args=(15, f"{host}/delay/15"))
t3.start()
