# -*- coding: utf-8 -*-


import re
import numpy as np
import pandas as pd


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', 100)


def re_split_col(arr):
    pattern = re.compile(r'(\d+)')
    ret = [pattern.split(string) for string in arr]
    data = [[str_list[0], ''.join(str_list[0:3]), ''.join(str_list[3:])] for str_list in ret]
    data = pd.DataFrame(data=np.array(data))
    return data


def get_digit_index(arr):
    digit_index = [True if string.isdigit() else False for string in arr]
    return digit_index


def get_alnum_index(arr):
    alnum_index = [True if not string.isdigit() else False for string in arr]
    return alnum_index


def process_digit(series):
    x = series[0]
    y = series[1]
    num = int(y)
    if num % 2 != 0:
        string = '|'.join((x + y, x + str(num + 1).zfill(2)))
    else:
        string = '|'.join((x + str(num - 1).zfill(2), x + str(num - 1).zfill(2)))
    return string


def create_new_data(series):
    one = series[0] + series[1][0]
    two = series[1][1]
    new_series = pd.Series(data=(one, two))
    return new_series


def process_alnum(data):
    new_data = data.apply(func=create_new_data, axis=1)
    new_data.columns = ['one', 'two']
    grouped = new_data.groupby(['one', 'two'])
    series = grouped.size()
    arr = series.index.values

    new_series = pd.Series()
    for string, i in arr:
        if string not in new_series.index:
            new_series[string] = i
        else:
            new_series[string] += '|' + i
    new_data['three'] = np.array([string + new_series[string] for string in new_data['one']])
    return new_data['three']


def process_dev_col(data):
    sou_digit_index = get_digit_index(data['SouTwo'].values)
    data.loc[sou_digit_index, 'SouDev'] = data.loc[sou_digit_index, ['SouOne', 'SouTwo']].apply(func=process_digit,
                                                                                                axis=1)

    sou_alnum_index = get_alnum_index(data['SouTwo'].values)
    data.loc[sou_alnum_index, 'SouDev'] = process_alnum(data.loc[sou_alnum_index, ['SouOne', 'SouTwo']])

    des_digit_index = get_digit_index(data['DesTwo'].values)
    data.loc[des_digit_index, 'DesDev'] = data.loc[des_digit_index, ['DesOne', 'DesTwo']].apply(func=process_digit,
                                                                                                axis=1)

    des_alnum_index = get_alnum_index(data['DesTwo'].values)
    data.loc[des_alnum_index, 'DesDev'] = process_alnum(data.loc[des_alnum_index, ['DesOne', 'DesTwo']])


def judge_sou_des(series):
    flag = False
    if series[0] == series[1]:
        flag = True
    return flag


def process_park(series):
    pattern = re.compile('^[A-Z]{2}')
    new_series = pd.Series()
    for index, string in series.items():
        if pattern.match(string).group() == 'NF':
            new_series[index] = 'NF'
        else:
            new_series[index] = 'BF'

    return new_series


def main():
    data = pd.read_csv('./decice_name.csv')
    data[['SouDev', 'SouArea']] = data['DEVNAME'].str.split('-', n=1, expand=True)
    data[['DesDev', 'DesArea']] = data['PEERDEVNAME'].str.split('-', n=1, expand=True)

    data[['SouPark', 'SouOne', 'SouTwo']] = re_split_col(data['SouDev'].values)
    data[['DesPark', 'DesOne', 'DesTwo']] = re_split_col(data['DesDev'].values)

    process_dev_col(data)

    sou_des_index = data[['SouDev', 'DesDev']].apply(func=judge_sou_des, axis=1)
    if np.any(sou_des_index):
        pattern = re.compile(r'.*')
        new_data = data.loc[sou_des_index, ['DEVNAME', 'PEERDEVNAME', 'SouOne', 'SouTwo', 'DesOne', 'DesTwo']]
        new_data.replace(pattern, np.nan, inplace=True)
        data.loc[sou_des_index, ['DEVNAME', 'PEERDEVNAME', 'SouOne', 'SouTwo', 'DesOne', 'DesTwo']] = new_data

    data[['SouPark', 'DesPark']] = data.loc[:, ['SouPark', 'DesPark']].apply(func=process_park, axis=1)

    sec_data = data.copy(deep=True)
    sec_data.rename(columns={
                                'SouDev': 'DesDev',
                                'SouArea': 'DesArea',
                                'SouPark': 'DesPark',
                                'DesDev': 'SouDev',
                                'DesArea': 'SouArea',
                                'DesPark': 'SouPark',
                             },
                    inplace=True)

    con_data = pd.concat((data, sec_data), axis=0, join='inner', ignore_index=True)
    con_data.drop_duplicates(inplace=True)
    con_data['timerange'] = ''
    print(con_data)


if __name__ == '__main__':
    main()
