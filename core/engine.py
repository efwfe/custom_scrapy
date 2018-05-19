# _*_coding:utf-8_*_
from datetime import datetime
import importlib
from scrapy_custom.http.request import Request
from scrapy_custom.utils.log import logger
from .downloader import Downloader
from .scheduler import Scheduler
from scrapy_custom.conf.settings import SPIDERS,PIPELINES,SPIDER_MIDDLEWARES, \
    DOWNLOADER_MIDDLEWARES


class Engine:
    def __init__(self):

        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.spiders = self._auto_import_instances(SPIDERS,is_spider=True)
        self.pipelines = self._auto_import_instances(PIPELINES)
        # self.spider_mid = spider_midllewares.SpiderMidlleware()
        # self.downloader_mid = downloader_middlewares.DownloaderMiddleware()
        self.spider_mids = self._auto_import_instances(SPIDER_MIDDLEWARES)
        self.downloader_mids = self._auto_import_instances(DOWNLOADER_MIDDLEWARES)

        self.total_response_number = 0
        self.total_request_number = 0

    def _auto_import_instances(self, path, is_spider = False):
        instances = []
        if is_spider:
            instances = {}
        for p in path:
            module_path = p.rsplit('.',1)[0]
            cls_name = p.rsplit('.',1)[-1]

            ret = importlib.import_module(module_path)
            cls = getattr(ret, cls_name)
            if is_spider:
                instances[cls.name] = cls()
            else:
                instances.append(cls())
        return instances


    def _start_requests(self):
        # 添加请求到调度器
        for spider_name, spider in self.spiders.items():
            for start_request in spider.start_requests():
                # spider middleware
                for spider_mid in self.spider_mids:
                    start_request = spider_mid.process_request(start_request)
                # add name to the request && add to scheduler
                start_request.spider_name = spider_name
                self.scheduler.add_request(start_request)

    def _execute_request_response_item(self):
        request = self.scheduler.get_request()
        if request is None:
            return

        # downloader process request
        for downloader_mid in self.downloader_mids:
             request = downloader_mid.process_request(request)
        # download the response
        response = self.downloader.get_response(request)
        response.meta = request.meta

        # downloader process response
        for downloader_mid in self.downloader_mids:
            response = downloader_mid.process_response(response)

        # get the spider
        spider = self.spiders[request.spider_name]
        # user custom parse
        parse = getattr(spider, request.parse)
        results = parse(response)

        for result in results:
            if isinstance(result, Request):
                #  is Request back to scheduler
                for spider_mid in self.spider_mids:
                    result = spider_mid.process_request(result)
                self.scheduler.add_request(result)
                self.total_request_number += 1
            else:
                # pipeline solve the result
                for spider_mid in self.spider_mids:
                    result = spider_mid.process_response(result)
                for pipeline in self.pipelines:
                    pipeline.process_item(result, spider)

        self.total_response_number += 1

    def _start_engine(self):
        self._start_requests()
        while True:
            self._execute_request_response_item()
            if self.total_response_number >= self.total_request_number:
                break

    def start(self):
        start = datetime.now()  # 起始时间
        logger.info("开始运行时间：%s" % start)  # 使用日志记录起始运行时间
        self._start_engine()
        stop = datetime.now()  # 结束时间
        logger.info("停止运行时间：%s" % stop)  # 使用日志记录结束运行时间
        logger.info("耗时：%.2f" % (stop - start).total_seconds())  # 使用日志记录运行耗时
