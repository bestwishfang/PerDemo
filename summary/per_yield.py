# -*- coding: utf-8 -*-
import random


def producer():
    while True:
        num = random.randint(10, 100)
        print(f'Product: {num}')
        yield num


def consumer():
    while True:
        x = yield
        print(f'Consume: {x}')


if __name__ == '__main__':
    p = producer()
    c = consumer()
    start = c.__next__()
    print(f'c start: {start}')
    for j in p:
        c.send(j)
