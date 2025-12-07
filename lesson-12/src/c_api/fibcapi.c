#include <Python.h>


int fib_rec_inner(int n)
{
    if (n <= 2)
        return 1;

    return fib_rec_inner(n - 1) + fib_rec_inner(n - 2);
}


int fib_iter_inner(int n)
{
    int a = 0, b = 1;
    for (int i = 0; i < n; ++i)
    {
        int tmp = b;
        b = a + b;
        a = tmp;
    }
    return a;
}


PyObject* fib_rec_c_api(PyObject* self, PyObject* args)
{
    int n;
    if (!PyArg_ParseTuple(args, "i", &n))
        return NULL;

    int res = fib_rec_inner(n);
    return PyLong_FromLong(res);
}


PyObject* fib_iter_c_api(PyObject* self, PyObject* args)
{
    int n;
    if (!PyArg_ParseTuple(args, "i", &n))
        return NULL;

    int res = fib_iter_inner(n);
    return PyLong_FromLong(res);
}


static PyMethodDef methods[] = {
    {"fib_rec_c_api", fib_rec_c_api, METH_VARARGS, "N-th fib number recursive"},
    {"fib_iter_c_api", fib_iter_c_api, METH_VARARGS, "N-th fib number iterative"},
    {NULL, NULL, 0, NULL},
};


static struct PyModuleDef module_fib_c_api = {
    PyModuleDef_HEAD_INIT, "fib_c_api", NULL, -1, methods
};


PyMODINIT_FUNC PyInit_fib_c_api()
{
    return PyModule_Create( &module_fib_c_api );
}
