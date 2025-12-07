import time
import ctypes

import cffi
from fib_native import fib_rec_py, fib_iter_py
from fib_cython import fib_rec_cyth, fib_iter_cyth
from fib_c_api import fib_rec_c_api, fib_iter_c_api


def calc_native(n_rec, n_iter):
    t1 = time.perf_counter()
    res = fib_rec_py(n_rec)
    t2 = time.perf_counter()

    print(f"[python] recursive {res=}, {n_rec=}, tt={t2 - t1}")

    t1 = time.perf_counter()
    res = fib_iter_py(n_iter)
    t2 = time.perf_counter()

    print(f"[python] iterative {res=}, {n_iter=}, tt={t2 - t1}")
    print("\n----------")


def calc_ctypes(n_rec, n_iter):
    libfib = ctypes.CDLL("./fib_ctypes/libfibutils.so")

    libfib.fib_rec_c.argtypes = (ctypes.c_int,)
    libfib.fib_rec_c.restype = ctypes.c_int

    libfib.fib_iter_c.argtypes = (ctypes.c_int,)
    libfib.fib_iter_c.restype = ctypes.c_int

    t1 = time.perf_counter()
    res = libfib.fib_rec_c(n_rec)
    t2 = time.perf_counter()

    print(f"[ctypes] recursive {res=}, {n_rec=}, tt={t2 - t1}")

    t1 = time.perf_counter()
    res = libfib.fib_iter_c(n_iter)
    t2 = time.perf_counter()

    print(f"[ctypes] iterative {res=}, {n_iter=}, tt={t2 - t1}")
    print("\n----------")


def calc_cffi(n_rec, n_iter):
    ffi = cffi.FFI()
    lib = ffi.dlopen("./fib_ctypes/libfibutils.so")

    ffi.cdef("int fib_rec_c(int n);")
    ffi.cdef("int fib_iter_c(int n);")

    t1 = time.perf_counter()
    res = lib.fib_rec_c(n_rec)
    t2 = time.perf_counter()

    print(f"[cffi] recursive {res=}, {n_rec=}, tt={t2 - t1}")

    t1 = time.perf_counter()
    res = lib.fib_iter_c(n_iter)
    t2 = time.perf_counter()

    print(f"[cffi] iterative {res=}, {n_iter=}, tt={t2 - t1}")
    print("\n----------")


def calc_c_api(n_rec, n_iter):
    t1 = time.perf_counter()
    res = fib_rec_c_api(n_rec)
    t2 = time.perf_counter()

    print(f"[c-api] recursive {res=}, {n_rec=}, tt={t2 - t1}")

    t1 = time.perf_counter()
    res = fib_iter_c_api(n_iter)
    t2 = time.perf_counter()

    print(f"[c-api] iterative {res=}, {n_iter=}, tt={t2 - t1}")
    print("\n----------")


def calc_cython(n_rec, n_iter):
    t1 = time.perf_counter()
    res = fib_rec_cyth(n_rec)
    t2 = time.perf_counter()

    print(f"[cython] recursive {res=}, {n_rec=}, tt={t2 - t1}")

    t1 = time.perf_counter()
    res = fib_iter_cyth(n_iter)
    t2 = time.perf_counter()

    print(f"[cython] iterative {res=}, {n_iter=}, tt={t2 - t1}")
    print("\n----------")


if __name__ == "__main__":
    N_REC = 40
    N_ITER = 45

    calc_native(N_REC, N_ITER)
    calc_ctypes(N_REC, N_ITER)
    calc_cffi(N_REC, N_ITER)
    calc_c_api(N_REC, N_ITER)
    calc_cython(N_REC, N_ITER)
