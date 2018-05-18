# _*_coding:utf-8_*_
import json
import re

from lxml import etree


class Response:
    def __init__(self, url, headers, status_code, body):
        '''
        :param url: request url
        :param method: GET POST
        :param status_code:
        :param data:
        :param params:
        '''
        self.url = url
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def xpath(self, rule):
        '''
        :param rule: xpath规则
        :return: xpath object
        '''
        html = etree.HTML(self.body)
        return html.xpath(rule)

    @property
    def json(self):
        return json.loads(self.body)

    def re_findall(self, rule, data=None):
        '''
        :param rule: re匹配规则
        :param data:
        :return: re result
        '''
        if data is None:
            data = self.body
        return re.findall(rule, data)
