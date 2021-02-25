# -*- coding: utf-8 -*-


def factorial_func(n: int):
    if isinstance(n, int) and n < 0:
        raise ValueError('Number n must be an integer and n is not an negative!')

    res = 1
    while n >= 2:
        res *= n
        n -= 1
    return res


def fib_func(n):
    if isinstance(n, int) and n < 1:
        raise ValueError('Number n must be a positive integer!')

    a, b = 1, 1
    while n > 2:
        a, b = b, a + b
        n -= 1
    return b
