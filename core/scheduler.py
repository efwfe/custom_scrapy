# _*_coding:utf-8_*_

from queue import Queue

class Scheduler:
    def __init__(self):
        self.queue = Queue()
        self.total_request_number = 0

    def add_request(self,request):
        self.queue.put(request)
        self.total_request_number += 1

    def get_request(self):
        try:
            request = self.queue.get(False)
        except:
            return None
        else:
            return  request

    def _filter_request(self):
        pass