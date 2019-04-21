def func1(func3):
    def func2(*args, **kwargs):
        print('添加功能代码逻辑1')
        ret = func3(*args, **kwargs)
        print('添加功能代码逻辑2')
        return ret

    return func2

@func1
def test():
    print('----a-----')
    return 5

if __name__ == '__main__':
    ret = test()
    print(ret)