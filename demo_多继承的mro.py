class D(object):
    pass


class E(object):
    pass


class F(object):
    pass


class C(F, D):
    pass


class B(E, D):
    pass


class A(B, C):
    pass


if __name__ == '__main__':
    print(A.__mro__)