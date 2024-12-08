def fun1():
    i = 0
    while True:
        yield i
        i += 1


g = fun1()
for i in range(10):
    print(next(g))
