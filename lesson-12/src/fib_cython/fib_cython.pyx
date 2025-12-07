cpdef int fib_rec_cyth(int n):
    if n <= 2:
        return 1

    return fib_rec_cyth(n - 1) + fib_rec_cyth(n - 2)


cpdef int fib_iter_cyth(int n):
    cdef int a = 0
    cdef int b = 1

    for _ in range(n):
        a, b = b, a + b

    return a
