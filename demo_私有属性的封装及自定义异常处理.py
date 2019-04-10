class ValueTypeError(Exception):
    def __init__(self):
        self.show_error()

    def show_error(self):
        print('值类型错误')


class MyClass(object):
    def __init__(self):
        self.__money = 0

    def get_money(self):
        return self.__money

    def set_money(self, val):
        if isinstance(val, int):
            self.__money = val
        else:
            raise ValueTypeError


myClass = MyClass()
m = myClass.get_money()
print(m)
var_money = '11'
try:
    myClass.set_money(var_money)
except ValueTypeError as err:
    print(err)

m = myClass.get_money()
print(m)