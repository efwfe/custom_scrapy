# _*_coding:utf-8_*_
from scrapy_custom.http.request import Request
from scrapy_custom.item import Item

class Spider:

    start_urls =[]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)



    def parse(self,response):
        yield Item(response.body)
