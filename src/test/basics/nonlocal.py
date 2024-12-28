def test_wrapper(n):
    m = n
    obj = None

    def inner():
        nonlocal m
        m += 1
        nonlocal obj
        obj = m
        print(id(obj))
        return obj

    inner.ref = obj
    return inner


t = test_wrapper(2)
print(t())
print(t())
print(t.ref)
