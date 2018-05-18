# _*_coding:utf-8_*_
class DownloaderMiddleware:

    def process_request(self,request):
        print('downloader is ready')
        return request

    def process_response(self,response):
        print('downloader is off')
        return response