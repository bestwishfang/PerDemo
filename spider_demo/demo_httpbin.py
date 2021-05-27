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

ret_data = requests.post(url, data=data).json()

print('ret data: ')
pprint(ret_data)

print('*' * 100)
json_data = requests.post(url, json=data).json()

print('json data: ')
pprint(json_data)
