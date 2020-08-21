# -*- coding: utf-8 -*-


import os
import re
import shutil
from queue import Queue
from threading import Thread


def load_features(file):
    with open(file, mode='r', encoding='utf-8') as fp:
        features_list = fp.readlines()
    return [feature.strip('\n') for feature in features_list]


def valid_feature(q, feature_list, pattern):
    while not q.empty():
        pakeage_path = q.get()
        file_list = os.listdir(pakeage_path)
        for file in file_list:
            ret = file.rsplit('.', 1)
            if pattern.match(file) and ret[0] not in feature_list:
                print(file)
                file_path = pakeage_path + '\\' + file
                os.remove(file_path)
        new_file_list = os.listdir(pakeage_path)
        if len(new_file_list) == 3:
            shutil.rmtree(pakeage_path)


def select_features(features_path, feature_list):
    q = Queue()
    threading_list = []
    pakeages_list = os.listdir(features_path)
    pattern = re.compile(r'^PNF_|^SCP_')

    for pakeage in pakeages_list:
        pakeage_path = features_path + '\\' + pakeage
        q.put(pakeage_path)

    for i in range(4):
        t = Thread(target=valid_feature, args=(q, feature_list, pattern))
        threading_list.append(t)
        t.start()
    for t in threading_list:
        t.join()


def main():
    feature_file = './usg12000_vcmu_om'
    features_path = r'D:\WorkDocument\SimulateEnv\VCMU_12000_0821\feature'
    feature_list = load_features(feature_file)
    select_features(features_path, feature_list)


if __name__ == '__main__':
    main()
