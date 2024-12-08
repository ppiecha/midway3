print(eval("2 + 2"))


def add(a, b):
    return a + b


print("add", eval("add(3, 1)"))

from itertools import count, takewhile

print(list(takewhile(lambda pair: pair[0] < 6, (p for p in enumerate(count(1, 0))))))

a = """
def test_it()2:
    return [1, 2, 3, 4]
"""
try:
    exec(a)
except Exception as e:
    print(str(e))
    print(e.args)
# l = test_it()
# print(l)
