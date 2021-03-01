import hashlib


def hash_item(str_obj):
    md5 = hashlib.md5()
    md5.update(str_obj.encode('utf-8'))
    sign = md5.hexdigest()
    return sign
