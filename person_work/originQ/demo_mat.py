# -*- coding: utf-8 -*-

import time
import random

import numpy as np
import matplotlib.pyplot as plt


def plot_double_dynamic(x1_list, y1_list, x2_list, y2_list, figures: tuple = None,
                        x1_label=None, y1_label=None,
                        x2_label=None, y2_label=None,
                        title1=None, title2=None):
    if figures is None:
        figure, ax = plt.subplots(1, 2, figsize=(10, 5))
    else:
        if len(figures) == 2:
            figure, ax = figures
        else:
            raise ValueError('figures value error,  It must be two values')
    if x1_label:
        ax[0].set_xlabel(x1_label)
    if y1_label:
        ax[0].set_ylabel(y1_label)
    ax[0].plot(x1_list, y1_list, c='b')
    if title1:
        ax[0].set_title(title1)

    if x2_label:
        ax[1].set_xlabel(x2_label)
    if y2_label:
        ax[1].set_ylabel(y2_label)
    ax[1].plot(x2_list, y2_list, c='b')
    if title2:
        ax[1].set_title(title2)
    plt.pause(0.001)
    figure.canvas.draw()


def producer(length):
    count = 0
    while count < length:
        y1 = np.sin(random.randrange(0, 3))
        y2 = np.cos(random.randrange(0, 3))
        yield y1, y2
        count += 1


# def consumer(length, arr):
#     count = 0
#     y1_list = []
#     y2_list = []
#     figures = plt.subplots(2, 1, figsize=(6, 6))
#     while count < length:
#         y1, y2 = yield
#         y1_list.append(y1)
#         y2_list.append(y2)
#         x_list = arr[: count + 1]
#         plot_double_dynamic(x_list, y1_list, x_list, y2_list, figures=figures)
#         count += 1
#     plt.close()


def consumer(length, arr):
    count = 0
    y1_list = []
    y2_list = []
    figures = plt.subplots(2, 1, figsize=(6, 6))
    while count < length:
        y1, y2 = yield
        y1_list.append(y1)
        y2_list.append(y2)
        if count > 0:
            x_list = arr[count - 1: count + 1]
            new_y1_list = y1_list[count - 1:]
            new_y2_list = y2_list[count - 1:]
            plot_double_dynamic(x_list, new_y1_list, x_list,
                                new_y2_list, figures=figures)

        count += 1
    plt.close()


if __name__ == '__main__':

    start = time.time()
    length = 200
    arr = np.arange(length)
    p = producer(length)
    c = consumer(length, arr)
    count = 0
    for y1, y2 in p:
        if count == 0:
            c.__next__()
        else:
            c.send((y1, y2))
        count += 1

    print(f'time: {time.time() - start}')

"""
time: 47.987231731414795
time: 14.652785301208496
"""
