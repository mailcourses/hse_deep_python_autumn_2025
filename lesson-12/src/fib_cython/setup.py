from setuptools import setup
from Cython.Build import cythonize


def main():
    setup(
        name="fib_cython",
        version="5.1.1",
        ext_modules=cythonize(["fib_cython.pyx"]),
    )


if __name__ == "__main__":
    main()
