import numpy as np
import pandas as pd


detail = pd.read_excel('./meal_order_detail.xlsx')
print(detail)
print(detail.info())

print('='*100)
# 全为空的列 的list
null_list = []

# 获取列的非空数
res = detail.count()  # res 的类型 Series
res_index = res.index  # 获取res的index
for n, t in zip(res, res_index):
    if not n:
        null_list.append(t)

print(null_list)

ret = detail.drop(labels=null_list, axis=1, inplace=False)
print(ret)
print(ret.info())