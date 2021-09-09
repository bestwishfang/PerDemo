# -*- coding: utf-8 -*-
import os
from functools import partial

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, leastsq
from scipy.signal import find_peaks, savgol_filter


def get_file_list(dir_path, target_file_list=None):
    if target_file_list is None:
        target_file_list = []

    dir_list = os.listdir(dir_path)
    for dir_name in dir_list:
        new_path = os.path.join(dir_path, dir_name)
        if os.path.isdir(new_path):
            file_list = get_file_list(new_path, target_file_list)
            for file in file_list:
                if file not in target_file_list:
                    target_file_list.append(file)
        else:
            if 'DistortionT1 P0_P1.dat' in dir_name:
                target_file_list.append(new_path)

    return target_file_list


def smooth(x, window_len=11, window='hanning'):
    """smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the
        signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are
        minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window; should be an
            odd integer
        window: the type of window from 'flat', 'hanning', 'hamming',
            'bartlett', 'blackman'
        flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman,
    numpy.convolve
    scipy.signal.lfilter

    """
    if int(window_len) & 0x1 == 0:
        window_len += 1

    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")

    if window_len < 3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError(
            "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s = np.r_[x[window_len - 1:0:-1], x, x[-1:-window_len:-1]]

    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')

    else:
        w = eval('np.' + window + '(window_len)')
    y = np.convolve(w / w.sum(), s, mode='valid')

    # Cut edges of y since a mirror image is used
    edge = (window_len - 1) / 2
    edge = int(edge)
    return y[edge:-edge]


def initial_lorentz_fit_args_p0(x_list, y_list):
    index_list, properties = find_peaks(y_list, height=0.2, width=0)
    print(f'index_list: {index_list}\n'
          f'properties: {properties}')

    peak_value_list = properties.get('peak_heights')
    peak_width_list = properties.get('width_heights')
    peak_start_list = properties.get('left_bases')
    peak_end_list = properties.get('right_bases')

    max_index = np.argmax(peak_value_list)
    start_index = peak_start_list[max_index]
    end_index = peak_end_list[max_index]

    # a = np.max(peak_value_list)
    a = 0.01
    b = np.mean(y_list)
    c = x_list[index_list[max_index]]
    d = 0.01
    # d = peak_width_list[max_index]

    fit_args_p0 = [a, b, c, d]
    return start_index, end_index, fit_args_p0


def lorentz_one(f, A, offset, f0, kappa):
    val = offset + A / np.pi * (kappa / ((f - f0) ** 2 + kappa ** 2))
    return val


def lorentz_other(x, A, y0, x0, w):
    y = y0 + 2 * A / np.pi * (w / (4 * (x - x0) ** 2 + w ** 2))
    return y


def _residuals(p, y, x, func):
    return y - func(x, *p)


def RMSE(x, y1, y2):
    variances = list(map(lambda x, y: (x - y) ** 2, y1, y2))
    variance = np.sum(variances)
    rmse = np.sqrt(variance / len(x))
    # print(variance)
    return rmse


def least_sq_fit_step(xdata, ydata, p0, func):
    y = ydata
    x = xdata
    num = 0
    # f0 = 0.01
    _residuals_attach = partial(_residuals, func=func)
    plsq = leastsq(_residuals_attach, p0, args=(y, x))
    p = plsq[0]
    y2 = func(x, *p)
    rmse = RMSE(x, y, y2)

    while (rmse > 1e-3) and (num < 1000):
        plsq = leastsq(_residuals, p, args=(y, x, func))
        p = plsq[0]
        y2 = func(x, *p)
        rmse = RMSE(x, y, y2)
        num += 1

    print(f'fit times {num}')
    print(f'fit rmse {rmse}')
    return p, rmse, y2


def plot_data(x_list, y_list, smooth_y_list, fit_y_list, title):
    font_dict = {
        'fontfamily': 'Times New Roman',
        'fontweight': 'bold',
        'fontsize': 36
    }

    font_label = {
        'family': 'Times New Roman',
        'weight': 'normal',
        'size': 24,
    }

    fig, axs = plt.subplots(figsize=(16, 9))
    axs.plot(x_list, y_list, marker='o', linewidth=1.5, alpha=1.0)
    axs.plot(x_list, smooth_y_list, marker='o', linewidth=1.5, alpha=1.0)
    axs.plot(x_list, fit_y_list, marker='o', linewidth=1.5, alpha=1.0)

    line_labels = ['real', 'smooth', 'fit']
    axs.tick_params(axis='both', which='major', labelsize=24)
    axs.legend(labels=line_labels, loc='upper right', prop=font_label)
    axs.set_title(title, **font_dict)
    axs.set_xlabel('Z offset', **font_dict)
    axs.set_ylabel('P1', **font_dict)
    axs.grid(True)

    plt.show()
    # plt.pause(0.001)
    # fig.canvas.flush_events()


if __name__ == '__main__':
    # data_path = r'E:\WorkDoc\202109\0908_ZZ_24bit_BUS3_Q4'
    data_path = r'E:\WorkDoc\202109\20210908_144419_Q4_IterationTimes0'
    file_list = get_file_list(data_path)

    for file_name in file_list:
        data = np.loadtxt(file_name)
        z_offset_arr, p1_arr = data[:, 0], data[:, 2]

        # smooth
        smooth_p1_arr = smooth(p1_arr)
        # smooth_p1_arr = savgol_filter(p1_arr, window_length=11, polyorder=5)

        # fit
        start_index, end_index, fit_args_p0 = initial_lorentz_fit_args_p0(z_offset_arr, smooth_p1_arr)
        new_x_list = z_offset_arr[start_index: end_index + 1]
        new_y_list = smooth_p1_arr[start_index: end_index + 1]
        new_p0, rmse, fit_y_list = least_sq_fit_step(new_x_list, new_y_list, fit_args_p0, lorentz_one)
        fit_y_list = np.hstack((smooth_p1_arr[: start_index], fit_y_list, smooth_p1_arr[end_index + 1:]))

        offset = round(new_p0[2], 6)
        png_title = f'offset: {offset}'

        # plot
        plot_data(z_offset_arr, p1_arr, smooth_p1_arr, fit_y_list, png_title)
