# 使用的技能：装饰器传参
# 应用场景 - 路由的实现


# 定义一个空字典
URL_FUNC_DICT = dict()

# 定义一个可传参数的装饰器
def route(url):
    def decorator_func(func):
        URL_FUNC_DICT[url] = func
        def curr_func(*args, **kwargs):
            ret = func(*args, **kwargs)
            return ret
        return curr_func
    return decorator_func # 返回装饰器函数的引用


@route('index')
def index():
    print('------这是index----')


@route('login')
def login():
    print('----------login---------')


@route('register')
def register():
    print('---------register---------')


def main():
    route = input('请输入路由地址')

    '''
    如果if...elif...elif...的条件比较多，这种代码实现肯定不合适

    if route == 'index':
        index()
    elif route == 'login':
        login()
    elif route == 'register':
        register()
    else:
        print('-----没有找到你要查看的路由-----')
    '''

    # 更优质的实现方式，使用 带参数的装饰器 配合 字典
    URL_FUNC_DICT[route]()


if __name__ == '__main__':
    main()

