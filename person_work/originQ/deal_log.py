import re

import numpy as np

np.set_printoptions(suppress=True)


def read_lines(fp, mark_info):
    buffer = ''
    while True:
        while mark_info in buffer:
            pos = buffer.index(mark_info)
            yield buffer[:pos]
            buffer = buffer[pos + len(mark_info):]
        chunk = fp.read(4096)

        if not chunk:
            yield buffer
            break
        buffer += chunk


def deal_log(log_file, bit_list):
    max_bit = max((bit_list))
    length = max_bit + 1
    arr = np.full((5 * length, length), np.nan)
    target, bias = None, None

    mark_info = 'Run DC Crosstalk Experiment'
    pattern_bit = re.compile(r'target qubit: (\d), bias qubit: (\d)')
    pattern_osc_freq = re.compile(r'DC Crosstalk osc_freq=(.*?)MHZ')

    with open(log_file, mode='r', encoding='gbk') as fp:
        content = read_lines(fp, mark_info)
        for line in content:
            osc_freq_list = re.findall(pattern_osc_freq, line)
            if osc_freq_list:
                osc_freq_arr = np.array(osc_freq_list[1:], dtype=np.float64)
                if target and bias:
                    target, bias = int(target), int(bias)
                    # print(f'target: {target}, bias: {bias}')
                    arr[target * 5: (target + 1) * 5, bias] = osc_freq_arr

            res_bit = re.search(pattern_bit, line)
            if res_bit:
                target, bias = res_bit.group(1), res_bit.group(2)

    data_file = f'{log_file.rsplit(".", 1)[0]}_dc_crosstalk_osc_freq.dat'
    np.savetxt(data_file, arr, fmt='%10.1f')
    print(arr)
    return arr


if __name__ == '__main__':
    log_file = '20210609pyqcatlog.txt'
    bit_list = [0, 1, 2, 3, 4, 5]
    deal_log(log_file, bit_list)
