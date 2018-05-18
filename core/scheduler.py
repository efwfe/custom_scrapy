# _*_coding:utf-8_*_

from queue import Queue

class Scheduler:
    def __init__(self):
        self.queue = Queue()

    def add_request(self,request):
        self.queue.put(request)

    def get_request(self):
        return self.queue.get()

    def _filter_request(self):
        pass