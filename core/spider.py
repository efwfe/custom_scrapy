# _*_coding:utf-8_*_
from scrapy_custom.http.request import Request
from scrapy_custom.item import Item

class Spider:

    start_url = "http://www.baidu.com"

    def start_request(self):
        return Request(self.start_url)


    def parse(self,response):
        return Item(response.body)
