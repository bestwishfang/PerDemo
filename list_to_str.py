# -*- coding: utf-8 -*-


import re


list1 = ['JCK72WA', 'JCK72WA','JCK65WA','JCK65WA','JCK65WA','JCK65WA','JCK65WA','JCK65WA',]
list2 = ['01', '12', '0A', '0A', '0B', '0B', '0C', '0D']
list3 = []
list4 = []

pattern = re.compile('^0[A-Z]$')
for i in list2:
    if i not in list3:
        res = pattern.match(i)
        if res:
            list3.append(res.group())

print(list3)
string = '|'.join(list3)

for j in list1:
    new_str = j + string
    if new_str not in list4:
        list4.append(new_str)

print(list4)
