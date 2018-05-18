# _*_coding:utf-8_*_
from datetime import datetime

from scrapy_custom.http.request import Request

from .scheduler import Scheduler
from .downloader import Downloader
from .pipeline import Pipeline
from .spider import Spider
from scrapy_custom.middlewares import downloader_middlewares,spider_midllewares
from scrapy_custom.utils.log import logger

class Engine:
    def __init__(self,spider):
        self.spider = spider
        self.scheduler = Scheduler()
        self.downloader =Downloader()
        self.pipeline = Pipeline()
        self.spider_mid = spider_midllewares.SpiderMidlleware()
        self.downloader_mid  = downloader_middlewares.DownloaderMiddleware()


    def _start_engine(self):
        start_request = self.spider.start_request()
        # spider middleware
        start_request = self.spider_mid.process_request(start_request)
        self.scheduler.add_request(start_request)
        request = self.scheduler.get_request()

        # downloader middleware
        request = self.downloader_mid.process_request(request)
        response = self.downloader.get_response(request)
        # downloader middleware
        response = self.downloader_mid.process_response(response)


        ret = self.spider.parse(response)
        if isinstance(ret,Request):
            # spider middleware
            request = self.spider_mid.process_response(ret)
            self.scheduler.add_request(request)
        else:
            ret = self.spider_mid.process_response(ret)
            self.pipeline.process_item(ret)


    def start(self):
        start = datetime.now()  # 起始时间
        logger.info("开始运行时间：%s" % start)  # 使用日志记录起始运行时间
        self._start_engine()
        stop = datetime.now()  # 结束时间
        logger.info("开始运行时间：%s" % stop)  # 使用日志记录结束运行时间
        logger.info("耗时：%.2f" % (stop - start).total_seconds())  # 使用日志记录运行耗时