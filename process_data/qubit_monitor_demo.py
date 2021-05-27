# -*- coding: utf-8 -*-

"""
__date:         2021/05/12
__author:       ssfang
__corporation:  OriginQuantum
__usage:

"""
import os
import re
import time
import threading
from queue import Queue
from datetime import datetime

import yaml
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)


def process_data(file_q, data_q):
    while not file_q.empty():
        file_path = file_q.get()
        with open(file_path, mode='r', encoding='utf-8') as fp:
            data = yaml.safe_load(fp)

        create_time = data.get('create_time').get('$date')
        local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(create_time * 1e-3))
        new_data = {
            'bit': data.get('bit'),
            'probe_freq': data.get('probe_freq'),
            'probe_power': data.get('probe_power'),
            'drive_freq': data.get('drive_freq'),
            'drive_power': data.get('drive_power'),
            'dc_max': data.get('dc_max'),
            'dc_min': data.get('dc_min'),
            'T1': data.get('T1'),
            'T2': data.get('T2'),
            'create_time': local_time,
        }
        data_q.put(new_data)


def process_path(path_q, file_q):
    pattern = re.compile(r'^q(.*?)yaml$')
    while not path_q.empty():
        target_path = path_q.get()
        ret_path_list = os.listdir(target_path)
        if 'qubit_data' in ret_path_list:
            new_path = f'{target_path}/qubit_data'
            file_list = os.listdir(new_path)
            for file in file_list:
                if pattern.match(file):
                    file_path = f'{new_path}/{file}'
                    file_q.put(file_path)


def get_all_qubit_yaml(data_path, file_q):
    path_list = os.listdir(data_path)
    path_q = Queue()
    for new_path in path_list:
        target_path = data_path + '/' + new_path
        if os.path.isdir(target_path):
            path_q.put(target_path)

    threading_list = []
    for i in range(5):
        t = threading.Thread(target=process_path, args=(path_q, file_q))
        threading_list.append(t)
        t.start()

    for t in threading_list:
        t.join()


def plot_special(x, y, title, ylabel, color, bit):
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel(f'{ylabel}')
    plt.plot(x, y,
             marker='o',
             color=color,
             label=f'q{bit}')
    plt.grid(True)
    plt.legend()


def plot_operate(df, bit_list, save_path):
    color_list = ['r', 'b', 'g', 'c', 'm', 'y']

    for index, bit in enumerate(bit_list):
        new_df = df.loc[df['bit'] == bit, :]
        new_df = new_df.sort_values(by='create_time')

        time_series = pd.to_datetime(new_df['create_time'])
        probe_freq_series = new_df['probe_freq']
        drive_freq_series = new_df['drive_freq']
        probe_power_series = new_df['probe_power']
        drive_power_series = new_df['drive_power']
        dc_max_series = new_df['dc_max']
        dc_min_series = new_df['dc_min']
        T1_series = new_df['T1']
        T2_series = new_df['T2']

        new_index = index % len(color_list)
        plt.figure(figsize=(20, 24))
        plt.subplot(4, 2, 1)
        plot_special(time_series, probe_freq_series, 'Probe Frequency', 'Frequency(MHz)', color_list[new_index], bit)

        plt.subplot(4, 2, 2)
        plot_special(time_series, drive_freq_series, 'Drive Frequency', 'Frequency(MHz)', color_list[new_index], bit)

        plt.subplot(4, 2, 3)
        plot_special(time_series, probe_power_series, 'Probe Power', 'Power(dB)', color_list[new_index], bit)

        plt.subplot(4, 2, 4)
        plot_special(time_series, drive_power_series, 'Drive Power', 'Power(dB)', color_list[new_index], bit)

        plt.subplot(4, 2, 5)
        plot_special(time_series, dc_max_series, 'Dc Max', 'Voltage(V)', color_list[new_index], bit)

        plt.subplot(4, 2, 6)
        plot_special(time_series, dc_min_series, 'Dc Min', 'Voltage(V)', color_list[new_index], bit)

        plt.subplot(4, 2, 7)
        plot_special(time_series, T1_series, 'T1', 'Delay(ns)', color_list[new_index], bit)

        plt.subplot(4, 2, 8)
        plot_special(time_series, T2_series, 'T2', 'Delay(ns)', color_list[new_index], bit)

        # plt.show()
        time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        png_name = f'{save_path}/qubit_data/q{bit}_monitor_{time_str}.png'
        plt.savefig(png_name)
        plt.close('all')


def qubit_monitor(data_path, save_path, bit_list):
    """
    Monitor qubit some info,
    monitor field : probe_freq, drive_freq,
                    probe_power, drive_power,
                    dc_max, dc_min,
                    T1, T2
    Args:
        data_path (str): read data path, normal `config/exp.yaml` system.save_path
        save_path (str): save png path, normal `config/exp.yaml` f'{system.save_path}/{system.chip_num}'
        bit_list (list): list of bit, normal `config/exp.yaml` system.bit_list

    """
    file_q = Queue()
    data_q = Queue()
    get_all_qubit_yaml(data_path, file_q)

    threading_list = []
    for i in range(5):
        t = threading.Thread(target=process_data, args=(file_q, data_q))
        threading_list.append(t)
        t.start()

    for t in threading_list:
        t.join()

    data_list = []
    while not data_q.empty():
        data_list.append(data_q.get())

    df = pd.DataFrame(data_list)
    print(df)

    plot_operate(df, bit_list, save_path)


if __name__ == '__main__':
    data_path = r'D:\ssfang'  # exp.yaml system.save_path
    save_path = r'D:\ssfang\D4-6bit_0512_dag_1'
    bit_list = [0, 1, 2, 3, 4, 5]  # exp.yaml system.bit_list
    qubit_monitor(data_path, save_path, bit_list)
