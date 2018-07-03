from functools import partial

def add(x, y):
    return x + y

add2 = partial(add, 2)


print(add2(3))