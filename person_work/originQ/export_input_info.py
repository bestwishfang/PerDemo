# -*- coding: utf-8 -*-
import os
import json
import tkinter
from tkinter import filedialog
from datetime import datetime

import yaml
from mongoengine import connect, disconnect
from mongoengine import (
    Document, StringField,
    ListField, FloatField,
    IntField, EmbeddedDocument,
    EmbeddedDocumentField, DateTimeField,
    BinaryField, ReferenceField, BooleanField,
    DictField, FileField
)


class XYWaveDoc(EmbeddedDocument):
    Xpi = FloatField(default=0.8)
    Xpi2 = FloatField(default=0.4)
    Ypi = FloatField(default=None, null=True)
    Ypi2 = FloatField(default=None, null=True)
    Zpi = FloatField(default=None, null=True)
    drive_IF = FloatField(default=466.667)
    delta = FloatField(default=-240.0)
    detune_pi = FloatField(default=0)
    detune_pi2 = FloatField(default=0)
    alpha = IntField(default=1)
    offset = IntField(default=5)
    time = IntField(default=20)


class ZWaveDoc(EmbeddedDocument):
    width = FloatField(default=None, null=True)
    amp = FloatField(default=None, null=True)


class UnionReadoutDoc(EmbeddedDocument):
    probe_IF = FloatField(default=None, null=True)
    index = ListField(default=[])
    amp = FloatField(default=None, null=True)


class QubitStoreDoc(Document):
    bit = IntField(required=True)
    sample = StringField(default=None, null=True)
    tunable = BooleanField(default=False)
    goodness = BooleanField(default=False)
    probe_freq = FloatField(default=None, null=True)
    probe_power = FloatField(default=None, null=True)
    drive_freq = FloatField(default=None, null=True)
    drive_power = FloatField(default=None, null=True)
    tls_freq = FloatField(default=None, null=True)
    anharmonicity = FloatField(default=-240, null=True)
    sample_delay = IntField(default=500)
    sample_width = IntField(default=500)
    dc = FloatField(min_value=-5, max_value=5, default=None, null=True)
    dc_max = FloatField(default=0, min_value=-5, max_value=5)
    dc_min = FloatField(default=0, min_value=-5, max_value=5)
    T1 = FloatField(default=20000)
    T2 = FloatField(default=10000)
    XYwave = EmbeddedDocumentField(XYWaveDoc)
    Zwave = EmbeddedDocumentField(ZWaveDoc)
    z_dc_channel = IntField(default=None, null=True)
    xy_channel = IntField(default=None, null=True)
    z_flux_channel = IntField(default=None, null=True)
    readout_channel = IntField(default=None, null=True)
    union_readout = EmbeddedDocumentField(UnionReadoutDoc)
    create_time = DateTimeField(default=datetime.now)
    meta = {
        'collection': 'QubitStore'
    }


def save_qubit(yaml_file):
    print(f'\nQubit yaml file: {yaml_file}')
    with open(yaml_file, mode='r', encoding='utf-8') as fp:
        data = yaml.safe_load(fp)

    qubit_store = QubitStoreDoc()
    qubit_store.XYwave = XYWaveDoc()
    qubit_store.Zwave = ZWaveDoc()
    qubit_store.union_readout = UnionReadoutDoc()

    for key, value in data.items():
        if key == 'XYwave':
            for subkey, subvalue in value.items():
                setattr(qubit_store.XYwave, subkey, subvalue)
        elif key == 'Zwave':
            for subkey, subvalue in value.items():
                setattr(qubit_store.Zwave, subkey, subvalue)
        elif key == 'union_readout':
            for subkey, subvalue in value.items():
                setattr(qubit_store.union_readout, subkey, subvalue)
        elif key == '_id' or key == 'create_time':
            pass
        else:
            setattr(qubit_store, key, value)
    qubit_store.save()
    print(f'Save q{qubit_store.bit} info to QubitStore success, id: {qubit_store.id}')


def export_qubit(bit=None, qubit_id=None, export_path=None):
    """
    Export qubit info from QubitStore.
    If qubit_id, search qubit info by qubit_id.
    If not qubit_id, and if bit, select the most recent qubit info by bit.
    Args:
        bit (int):  bit number
        qubit_id (str):  QubitStore id value, eg: qubit_id='60d00d8c3bf402fce2a597a4'
        export_path (str): export yaml to directory

    """
    if qubit_id:
        qubit_doc = QubitStoreDoc.objects.get(id=qubit_id)
    else:
        if bit is None:
            raise ValueError(f'bit and qubit_id are None!')
        qubit_doc = QubitStoreDoc.objects.filter(bit=bit).order_by('-create_time').first()
    print(f'Export qubit info from QubitStore, id: {qubit_doc.id}')
    json_data = qubit_doc.to_json()
    dict_data = json.loads(json_data)

    if export_path:
        if not os.path.exists(export_path):
            os.makedirs(export_path)
    else:
        export_path = os.getcwd()
    time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    file = f'{export_path}/q{qubit_doc.bit}_{time_str}.yaml'

    with open(file, mode='w', encoding='utf-8') as fp:
        yaml.safe_dump(dict_data, fp, allow_unicode='utf-8', sort_keys=False)
    print(f'Export q{qubit_doc.bit} info to yaml file success, file: {file}')


def import_click():
    # 将 yaml 文件中 qubit 导入数据库
    yaml_file = filedialog.askopenfilename(title=r'Select qubit yaml file', initialdir=os.getcwd())
    save_qubit(yaml_file)


def export_click():
    bit_lb = tkinter.Label(window, text='bit', width=16, height=2)
    bit_lb.pack()

    bit_en = tkinter.Entry(window, show=None, font=('Arial', 10), width=32)
    bit_en.pack()

    qubit_id_lb = tkinter.Label(window, text='qubit store id', width=16, height=2)
    qubit_id_lb.pack()

    qubit_id_en = tkinter.Entry(window, show=None, font=('Arial', 10), width=32)
    qubit_id_en.pack()

    def export_sure():
        bit = bit_en.get()
        qubit_id = qubit_id_en.get()

        # 从数据库导出 qubit
        if bit or qubit_id:
            err_lb['text'] = ''
            if bit:
                bit = int(bit)
            print(f'\nExport qubit bit: {bit}, id: {qubit_id}')
            export_qubit(bit=bit, qubit_id=qubit_id, export_path=os.getcwd())
        else:
            err_lb['text'] = f'Error: bit and qubit store id are None!'

    err_lb = tkinter.Label(window, text='', fg="#FF0000", width=32, height=1)
    err_lb.pack()

    sure_btn = tkinter.Button(window, text="Export", width=8, height=2, command=export_sure)
    sure_btn.pack()


if __name__ == '__main__':
    mongodb_ip = '127.0.0.1'  # 设置自己的 MongoDB ip
    connect('measuresystem', host=mongodb_ip, port=27017)

    window = tkinter.Tk()
    window.title('Import or Export Qubit Information')
    window.geometry("600x400")

    lb = tkinter.Label(window, text='', width=16, height=2)
    lb.pack()

    import_btn = tkinter.Button(window, text="Import Qubit", width=16, height=2, command=import_click)
    import_btn.pack()

    lb = tkinter.Label(window, text='', width=16, height=2)
    lb.pack()

    export_btn = tkinter.Button(window, text="Export Qubit", width=16, height=2, command=export_click)
    export_btn.pack()

    window.mainloop()

    disconnect()
