# _*_coding:utf-8_*_
from queue import Queue
from hashlib import sha1
import w3lib.url

from scrapy_custom.utils.log import logger


def utf8_string(string):
    if isinstance(string, str):
        return string.encode('utf-8')
    else:
        return string

class Scheduler:
    def __init__(self):
        self.queue = Queue()
        self._filter_container = set()
        self.total_request_number = 0
        self.repeat_request_number = 0

    def add_request(self,request):
        fp = self._gen_fp(request)
        if self._filter_request(fp, request):
            self.queue.put(request)
            self._filter_container.add(request)
            self.total_request_number +=1
        else:
            self.repeat_request_number += 1

    def get_request(self):
        try:
            request = self.queue.get(False)
        except:
            return None
        else:
            return  request

    def _filter_request(self, fp, request):
        if fp not in self._filter_container:
            logger.info("重复请求:%s"%request.url)
            return True
        else:
            return False

    def _gen_fp(self, request):
        url = w3lib.url.canonicalize_url(request.url)
        method = request.method.upper()
        params = request.params if request.params is not None else {}
        params = sorted(params.items(), key=lambda x:x[0])

        data = request.data if request.data is not None else {}
        data = sorted(data.items(), key=lambda x:x[0])

        s1 = sha1()
        s1.update(utf8_string(url))
        s1.update(utf8_string(method))
        s1.update(utf8_string(str(params)))
        s1.update(utf8_string(str(data)))

        fp = s1.hexdigest()
        return fp

