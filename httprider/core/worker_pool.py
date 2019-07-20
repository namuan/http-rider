from PyQt5.QtCore import QThreadPool


class WorkerPool:
    thread_pool = QThreadPool()

    def __init__(self, max_threads):
        self.thread_pool.setMaxThreadCount(max_threads)

    def schedule(self, worker):
        self.thread_pool.start(worker)

    def shutdown(self):
        self.thread_pool.clear()
        self.thread_pool.waitForDone(msecs=2)


single_worker = WorkerPool(1)
