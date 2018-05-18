# _*_coding:utf-8_*_
from datetime import datetime

from scrapy_custom.http.request import Request
from scrapy_custom.middlewares import downloader_middlewares, spider_midllewares
from scrapy_custom.utils.log import logger
from .downloader import Downloader
from .pipeline import Pipeline
from .scheduler import Scheduler


class Engine:
    def __init__(self, spiders):
        self.spiders = spiders
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.pipeline = Pipeline()
        self.spider_mid = spider_midllewares.SpiderMidlleware()
        self.downloader_mid = downloader_middlewares.DownloaderMiddleware()

        self.total_response_number = 0

    def _start_requests(self):

        for spider_name, spider in self.spiders.items():
            for start_request in spider.start_requests():
                start_request = self.spider_mid.process_request(start_request)
                # add name to the request && add to scheduler
                start_request.spider_name = spider_name
                self.scheduler.add_request(start_request)

    def _execute_request_response_item(self):
        request = self.scheduler.get_request()
        if request is None:
            return

        # downloader process request
        request = self.downloader_mid.process_request(request)
        # download the response
        response = self.downloader.get_response(request)
        response.meta = request.meta

        # downloader process response
        response = self.downloader_mid.process_response(response)

        # get the spider
        spider = self.spiders[request.spider_name]
        # user custom parse
        parse = getattr(spider, request.parse)
        results = parse(response)

        for result in results:
            if isinstance(result, Request):
                #  is Request back to scheduler
                result = self.spider_mid.process_request(result)
                self.scheduler.add_request(result)
            else:
                # pipeline solve the result
                result = self.spider_mid.process_response(result)
                self.pipeline.process_item(result)

        self.total_response_number += 1

    def _start_engine(self):
        self._start_requests()
        while True:
            self._execute_request_response_item()
            if self.total_response_number >= self.scheduler.total_request_number:
                break

    def start(self):
        start = datetime.now()  # 起始时间
        logger.info("开始运行时间：%s" % start)  # 使用日志记录起始运行时间
        self._start_engine()
        stop = datetime.now()  # 结束时间
        logger.info("停止运行时间：%s" % stop)  # 使用日志记录结束运行时间
        logger.info("耗时：%.2f" % (stop - start).total_seconds())  # 使用日志记录运行耗时
