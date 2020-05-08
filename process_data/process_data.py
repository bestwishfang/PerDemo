# -*- coding: utf-8 -*-


import re
import numpy as np
import pandas as pd


def re_split_col(arr):
    pattern = re.compile(r'(\d+)')
    ret = [pattern.split(string) for string in arr]
    data = [[str_list[0], ''.join(str_list[0:3]), ''.join(str_list[3:])] for str_list in ret]
    data = np.array(data)
    print(data)
    data = pd.DataFrame(data=data)
    return data


def main():
    data = pd.read_csv('./decice_name.csv')
    data[['SouDev', 'SouArea']] = data['DEVNAME'].str.split('-', n=1, expand=True)
    data[['DesDev', 'DesArea']] = data['PEERDEVNAME'].str.split('-', n=1, expand=True)

    data[['SouPark', 'SouOne', 'SouTwo']] = re_split_col(data['SouDev'].values)

    data[['DesPark', 'DesOne', 'DesTwo']] = re_split_col(data['DesDev'].values)

    print(data.columns)
    print(data.head())




if __name__ == '__main__':
    main()

"""
Index(['DEVNAME', 'T.INTTYPE||T.ININUM', 'PEERDEVNAME',
       'T.PEERINTTYPE||T.PEERINTNUM'],
      dtype='object')
====================
        DEVNAME T.INTTYPE||T.ININUM   PEERDEVNAME T.PEERINTTYPE||T.PEERINTNUM
0  JCK72WA01-A1  GigabitEthernet0/1  JCK65RT0A-C1          GigabitEthernet3/1
1  JCK72WA01-A1  GigabitEthernet0/2  JCK65RT0B-C1          GigabitEthernet3/1
2  JCK72WA02-A1  GigabitEthernet0/1  JCK65RT0A-C1          GigabitEthernet3/2
3  JCK72WA02-A1  GigabitEthernet0/2  JCK65RT0B-C1          GigabitEthernet3/2
4  JCK31BL11-C1       FastEthernet0  JCK31BL12-C1               FastEthernet0

Index(['DEVNAME', 'T.INTTYPE||T.ININUM', 'PEERDEVNAME',
       'T.PEERINTTYPE||T.PEERINTNUM', 'SouDev', 'SouArea', 'DesDev', 'DesArea',
       'SouPark', 'SouOne', 'SouTwo', 'DesPark', 'DesOne', 'DesTwo'],
      dtype='object')
        DEVNAME T.INTTYPE||T.ININUM   PEERDEVNAME  ... DesPark   DesOne DesTwo
0  JCK72WA01-A1  GigabitEthernet0/1  JCK65RT0A-C1  ...     JCK  JCK65RT     0A
1  JCK72WA01-A1  GigabitEthernet0/2  JCK65RT0B-C1  ...     JCK  JCK65RT     0B
2  JCK72WA02-A1  GigabitEthernet0/1  JCK65RT0A-C1  ...     JCK  JCK65RT     0A
3  JCK72WA02-A1  GigabitEthernet0/2  JCK65RT0B-C1  ...     JCK  JCK65RT     0B
4  JCK31BL11-C1       FastEthernet0  JCK31BL12-C1  ...     JCK  JCK31BL     12

[5 rows x 14 columns]


"""
