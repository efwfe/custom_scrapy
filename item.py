# _*_coding:utf-8_*_

class Item:
    def __init__(self,data):
        self._data = data

    @property
    def data(self):
        return self._data