


def load_qubit_data(file):
    with open(file, mode='r', encoding='utf-8') as fp:
        data = json.load(fp)
    sample = data.get('sample')

    for info, values in data.items():
        if info.startswith('qubit'):
            bit = info.split()[1]
            qubit = QubitStoreDoc()
            qubit.bit = bit
            qubit.sample = sample

            for key, value in values.items():
                if key == 'XYwave':
                    qubit.XYwave = XYWaveDoc()
                    for subkey, subvalue in value.items():
                        setattr(qubit.XYwave, subkey, subvalue)
                elif key == 'Zwave':
                    qubit.Zwave = ZWaveDoc()
                    for subkey, subvalue in value.items():
                        setattr(qubit.Zwave, subkey, subvalue)
                elif key == 'union_readout':
                    qubit.union_readout = UnionReadoutDoc()
                    for subkey, subvalue in value.items():
                        setattr(qubit.union_readout, subkey, subvalue)
                else:
                    setattr(qubit, key, value)
            qubit.save()


def init_qubit(bit):
    xy_wave_init = {
            "Xpi": 0.772,
            "Xpi2": 0.3827,
            "Ypi": 0.5,
            "Ypi2": 0.9,
            "Zpi": 0.7,
            "drive_IF": 466.667,
            "delta": -240,
            "detune_pi": -9.3103,
            "detune_pi2": -9.953800000000001,
            "alpha": 1,
            "offset": 5,
            "time": 20
        }
    z_wave_init = {
            "width": 100,
            "amp": 1
        }
    union_readout_init = {
            "probe_IF": 553.1,
            "index": [480.000000, 1760.000000],
            "amp": 0.300000
        }
    qubit_info_init = {
        "sample": "D:\\Qubit\\D4",
        "bit": bit,
        "probe_freq": 6545.72,
        "probe_power": -24,
        "drive_freq": 5429.197,
        "drive_power": -19,
        "sample_delay": 600,
        "sample_width": 800,
        "dc": -0.692937,
        "T1": 10000,
        "T2": 2000,
        "XYwave": XYWaveDoc(**xy_wave_init),
        "Zwave": ZWaveDoc(**z_wave_init),
        "z_dc_channel": 1,
        "xy_channel": 5,
        "z_flux_channel": 1,
        "readout_channel": 1,
        "union_readout": UnionReadoutDoc(**union_readout_init)
    }

    qubit_doc = QubitStoreDoc(**qubit_info_init)
    qubit_doc.save()
    return qubit_doc



"""
{
    "_id" : ObjectId("606414327253b87349f62388"),
    "sample" : "D:\\Qubit\\D4",
    "bit" : 0,
    "probe_freq" : 6545.72,
    "probe_power" : -24.0,
    "drive_freq" : 5429.197,
    "drive_power" : -19.0,
    "sample_delay" : 600,
    "sample_width" : 800,
    "dc" : -0.69301,
    "T1" : 10000.0,
    "T2" : 2000.0,
    "XYwave" : {
        "Xpi" : 0.772,
        "Xpi2" : 0.3827,
        "Ypi" : 0.5,
        "Ypi2" : 0.9,
        "Zpi" : 0.7,
        "drive_IF" : 466.667,
        "delta" : -240.0,
        "detune_pi" : -9.3103,
        "detune_pi2" : -9.9538,
        "alpha" : 1,
        "offset" : 5,
        "time" : 20
    },
    "Zwave" : {
        "width" : 100.0,
        "amp" : 1.0
    },
    "z_dc_channel" : 1,
    "xy_channel" : 5,
    "z_flux_channel" : 1,
    "readout_channel" : 1,
    "union_readout" : {
        "probe_IF" : 553.1,
        "index" : [ 
            480.0, 
            1760.0
        ],
        "amp" : 0.3
    },
    "create_time" : ISODate("2021-03-31T14:18:26.079Z")
}
"""