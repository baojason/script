#!/usr/bin/python3
class c:
    def __init__(self,a):
        self.__m1__ = a
    def getA(self):
        return self.__m1__
    def setA(self, a):
        self.__m1__=a
def f(a):
    print("type(a) is c = ", type(a) is c)
    print("a and x are aliasing =", a is x)
    print("a =", a.getA())
    print("a isinstance of c = ", isinstance(a,c))
    a.setA(20)

if __name__ == '__main__':
    x = c(10)
    print("x = ", x.getA())
    f(x)
    print("x = ", x.getA())
