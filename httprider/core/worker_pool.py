from PyQt5.QtCore import QThreadPool

from httprider.external.rest_api_connector import RestApiConnector


class WorkerPool:
    thread_pool = QThreadPool()

    def __init__(self, max_threads):
        self.thread_pool.setMaxThreadCount(max_threads)

    def schedule(self, worker):
        self.thread_pool.start(worker)

    def shutdown(self):
        self.thread_pool.clear()
        self.thread_pool.waitForDone(msecs=2)


class ThreadPool:
    ct: RestApiConnector = None

    def schedule_task(self, exchange, on_success, on_failure):
        ct = RestApiConnector(exchange)
        ct.start()

    def shutdown(self):
        pass


single_worker = WorkerPool(1)
