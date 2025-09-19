import time

def timeit(inner):
    def timer(*args, **kwargs):
        start = time.time()
        try:
            res = inner(*args, **kwargs)
        finally:
            finish = time.time()
            print(f"Measure: {finish - start}!")
        return res
    return timer


@timeit
def summator(a, b):
    time.sleep(1)
    return a + b
    
def summutor_1(a, b):
    time.sleep(1)
    return a + b
summator_1 = timeit(summutor_1)


print(summator(1, 10))


def meancall(k):
    lst = []
    def timeit(inner):
        def timer(*args, **kwargs):
            start = time.time()
            try:
                res = inner(*args, **kwargs)
            finally:
                finish = time.time()
                lst.append(finish - start)
                mid = sum(lst[-k:]) / len(lst[-k:])
                print(f"Mean time ({k} times): {mid}")
            return res
        return timer
    return timeit
    


@meancall(k=5)
def summator(a, b):
    time.sleep(1)
    return a + b
    
summator(1, 2)
summator(1, 2)
summator(1, 2)
summator(1, 2)
summator(1, 2)
summator(1, 2)


def add_1(a, b):
    time.sleep(1)
    return a + b
add_1 = meancall(k=2)(add_1)



