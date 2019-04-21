def set_level(level_num):
    def set_func(func):
        def curr_func(*args, **kwargs):
            if level_num == 10:
                print('通过10级验证')
            elif level_num == 1:
                print('通过1级验证')
            ret = func(*args, **kwargs)
            return ret
        return curr_func

    return set_func # 这里返回装饰器函数 set_func 的引用


@set_level(10) # 代码的执行流程：（1）先执行set_level(10), 它的执行结果是：装饰器函数的引用（2）接着通过返回的装饰器函数进行装饰
def test1():
    print('-----test1------')
    return 10

@set_level(1)
def test2():
    print('-----test2------')
    return 9


if __name__ == '__main__':
    ret1 =  test1()
    ret2 = test2()
