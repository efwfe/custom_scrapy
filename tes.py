# _*_coding:utf-8_*_

class A:
    def __init__(self):
        pass

    def pri(self):
        print("this is A")

class B(A):
    def __init__(self):
        pass

class C(A):
    def __init__(self):
        pass
    def pri(self):
        print('this is C')

class D(B,C):
    def __init__(self):
        pass

d = D()
d.pri()