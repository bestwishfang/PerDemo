

#####################################################################
#                  Config Document
#####################################################################

class ConfigDoc(Document):
    filename = StringField(required=True)
    ac_crosstalk = ListField(default=None)
    dc_crosstalk = ListField(default=None)
    distortion = ListField(default=None)  # store file series of distortion_{num},dat
    distortion_width = ListField(default=None)
    hardware_offset = ListField(default=None)
    fidelity_matrix = ListField(default=None)  # store file fidelity_matrix_q0~q5.dat
    frequency_zamp_fitting = ListField(default=None)
    frequency_zamp_dc_fitting = ListField(default=None)
    union_readout = ListField(default=None)
    cz_pulse = DictField(default=None)
    instrument = DictField(default=None)
    qubit = DictField(default=None)
    two_qubit_readout = DictField(default=None)
    server = DictField(default=None)
    discriminator_bin = BinaryField(default=None)  # store bin file
    meta = {
        'collection': 'ConfigStore'
    }