# _*_coding:utf-8_*_
import requests
from scrapy_custom.http.response import Response

class Downloader:
    def get_response(self,request):
        if request.method.upper() =="GET":
            resp = requests.get(request.url,headers=request.headers,params=request.params)
        elif request.method.upper() =="POST":
            resp = requests.post(request.url,headers=request.headers,params=request.params,data=request.data)
        else:
            raise Exception("not support the method")

        return Response(resp.url,resp.headers,resp.status_code,resp.content)