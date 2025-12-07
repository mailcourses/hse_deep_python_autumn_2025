import random

import cffi


def test_sum():
    ffi = cffi.FFI()
    lib = ffi.dlopen("../fib_ctypes/libfibutils.so")

    ffi.cdef("int sum(int* arr, int len);")

    arr = random.sample(range(-1000, 1000), 100)
    c_arr = ffi.new("int[]", arr)

    res = lib.sum(c_arr, len(arr))
    print(f"{res=}, {res == sum(arr)=}")


def test_compile():
    ffi = cffi.FFI()
    ffi.cdef("int mult(int a, int b, int c);")

    ffi.set_source(
        "multutil",
        """
        int mult(int a, int b, int c)
        {
           return a * b * c;
        }
        """
    )
    ffi.compile()


def test_mult():
    import multutil

    print(f"{multutil.lib.mult(4, 9, 17)=}, {4 * 9 * 17=}")



if __name__ == "__main__":
    test_sum()
    test_compile()
    test_mult()

