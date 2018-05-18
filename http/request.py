# _*_coding:utf-8_*_

class Request:
    def __init__(self,url,method='GET',headers=None,params=None,data=None,parse='parse'):
        '''
        :param url: request url
        :param method: GET OR POST
        :param headers:
        '''
        self.url = url
        self.method = method
        self.headers = headers
        self.data = data
        self.params = params
        self.parse = parse
        self.meta = None

