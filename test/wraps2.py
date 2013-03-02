import time
import functools
 
def timeit(func):
    @functools.wraps(func)
    def wrapper(*args):
        start = time.clock()
        func(*args)
        end =time.clock()
        print 'used:', end - start
    return wrapper
 
@timeit
def foo(x):
    print 'in foo()',x
 
foo(1111)
print foo.__name__