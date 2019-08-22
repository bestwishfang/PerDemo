import time

print(time.time())
li = [1, 34, 56, 78, 34, 23, 34, 56]
new_list = [x for x in li if li.count(x) == 1]
print(new_list)
