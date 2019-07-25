import logging

handlers = [
    logging.StreamHandler()
]

logging.basicConfig(
    handlers=handlers,
    format='%(asctime)s - %(filename)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)
logging.captureWarnings(capture=True)

from threading import Thread

import requests
from requests.adapters import HTTPAdapter


def thread_get(name, url):
    s = requests.Session()
    s.mount('https://', HTTPAdapter(pool_connections=10, pool_maxsize=10))
    logging.info(f"Thread: {name}")
    s.get(url)


for i in range(20):
    t1 = Thread(target=thread_get, args=(i, 'http://127.0.0.1:8000/delay/1',))
    t1.start()

t2 = Thread(target=thread_get, args=(20, 'http://127.0.0.1:8000/delay/3',))
t2.start()
# t2.join()
#
# t3 = Thread(target=thread_get, args=(3, 'http://127.0.0.1:8000/delay/3',))
# t4 = Thread(target=thread_get, args=(4, 'http://127.0.0.1:8000/delay/3',))
#
# t3.start()
# t4.start()
