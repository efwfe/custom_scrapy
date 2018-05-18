# _*_coding:utf-8_*_
class SpiderMidlleware:
    def process_request(self,request):
        print('spider middleware on')
        return request

    def process_response(self, response):

        print('spider middleware off')

        return response