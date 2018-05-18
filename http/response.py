# _*_coding:utf-8_*_

class Response:
    def __init__(self,url,headers,status_code,body):
        '''
        :param url: request url
        :param method: GET POST
        :param status_code:
        :param data:
        :param params:
        '''
        self.url = url
        self.headers=headers
        self.status_code = status_code
        self.body = body
