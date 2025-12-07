int fib_rec_c(int n)
{
    if (n <= 2)
        return 1;

    return fib_rec_c(n - 1) + fib_rec_c(n - 2);
}


int fib_iter_c(int n)
{
    int a = 0, b = 1;
    for (int i; i < n; ++i)
    {
        int tmp = b;
        b = a + b;
        a = tmp;
    }
    return a;
}


int sum(int *arr, int len)
{
    int res = 0;
    for (int i = 0; i < len; ++i)
    {
        res += arr[i];
    }
    return res;
}
