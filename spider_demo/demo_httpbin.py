from pprint import pprint

import requests


url = 'http://httpbin.org/post'
data = {
    'server_ip': "10.10.12.147",
    'flows': {
        'initial_flow': [],
        'tunable_flow': [],
        'cavity_detecte_flow': [],
        'qubit_detecte_flow': [],
        'pi_pulse_detecte_flow': ["rabi_scan_amp_node"],
        'readout_calibrate_flow': ["probe_freq_cali_node", "probe_power_cali_node", "single_shot_node"],
        'qubit_freq_calibrate_flow': [],
        'qubit_optimizate_flow': [],
    },
}


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36z",
}

ret_data = requests.post(url, data=data, headers=headers).json()

print('ret data: ')
pprint(ret_data)

print('*' * 100)
json_data = requests.post(url, json=data, headers=headers).json()

print('json data: ')
pprint(json_data)
