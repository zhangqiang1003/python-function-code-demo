def func1(func):
    def n_func(*args, **kwargs):
        print('执行func1装饰器的逻辑-开始')
        ret = func(*args, **kwargs)
        print('执行func1装饰器的逻辑-结束')
        return ret

    return n_func


def func2(func):
    def n_func(*args, **kwargs):
        print('执行func2装饰器的逻辑-开始')
        ret = func(*args, **kwargs)
        print('执行func2装饰器的逻辑-结束')
        return ret

    return n_func


@func2
@func1
def test(*args, **kwargs):
    print('这是一个测试：读个装饰器装饰一个函数')

if __name__ == '__main__':
    test()
