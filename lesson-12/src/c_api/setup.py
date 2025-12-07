from setuptools import setup, Extension


def main():
    setup(
        name="fib_c_api",
        version="3.1.5",
        ext_modules=[Extension("fib_c_api", ["fibcapi.c"])]
    )


if __name__ == "__main__":
    main()
