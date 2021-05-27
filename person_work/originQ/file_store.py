import os
import re
import json
import pickle
import configparser

import numpy as np
from typing import Union

from ..log import pyqlog
from ..database.ODM import ConfigDoc
from .iqprobability import IQdiscriminator


class SetConfig:
    def __init__(self, configname):
        self.configName = configname
        self.rc = configparser.ConfigParser()
        self.rc.read(self.configName)

    def read_config(self, section, option):
        value = self.rc.get(section, option)
        return value

    def write_config(self, section, option, value):
        if not self.rc.has_section(section):
            self.rc.add_section(section)
            self.__write_config_file()
        self.rc.set(section, option, value)
        self.__write_config_file()

    def delete_section(self, section, option=None):
        if option is None:
            self.rc.remove_section(section)
        else:
            self.rc.remove_option(section, option)
        self.__write_config_file()

    def __write_config_file(self):
        with open(self.configName, 'w') as fw:
            self.rc.write(fw)


class ConfigStoreMap(object):
    postfix_list = ['dat', 'json', 'bin']
    pattern = re.compile(r'(distortion_width|distortion|fidelity_matrix)')

    def __init__(self, file_name):
        """
        self.filename is a config file name,
        self._file is a config file name without a postfix,
        self._postfix is a postfix of config file name,
        self._config_doc is an object of ConfigDoc.

        Args:
            file_name (str):  config file name, likes `dc_crosstalk.dat`

        """
        self.filename = file_name
        self._file = None
        self._postfix = None
        self._config_doc = None
        self._initial()

    def _initial(self):
        self._file, self._postfix = self.filename.rsplit('.', 1)
        config_doc_list = ConfigDoc.objects.filter(filename=self.filename)
        if config_doc_list:
            self._config_doc = config_doc_list[0]
        else:
            self._config_doc = ConfigDoc()
            self._config_doc.filename = self.filename

    def read_config(self):
        """
        Read from MongoDB ConfigStore, specific config info by self._config_doc.

        Returns:
            data : config info, may be a np.array, dict or IQdiscriminator object.

        """
        try:
            data = None
            if self._postfix in self.postfix_list:
                if self._postfix == 'bin':
                    data = pickle.loads(self._config_doc.discriminator_bin)
                elif self._postfix == 'json':
                    data = dict(getattr(self._config_doc, self._file))
                elif self._postfix == 'dat':
                    ret = self.pattern.search(self.filename)
                    if ret:
                        attr = ret.group(1)
                    else:
                        attr = self._file
                    data = np.array(getattr(self._config_doc, attr))
            else:
                pyqlog.warning(f'Not Support Postfix with {self._postfix}!!! Not in {self.postfix_list}')
            return data
        except Exception as err:
            pyqlog.error(f'Query config by {self.filename} from ConfigStore Error!!! {err}')

    def write_config(self, value: Union[list, dict, np.ndarray, IQdiscriminator] = None):
        """
        Write a value to MongDB ConfigStore,
        the corresponding self._config_doc's field is determined by self._file and self._postfix.

        Args:
            value (Union[list, dict, np.ndarray, IQdiscriminator]):
                the value specifically written to the database.

        """
        try:
            if self._postfix in self.postfix_list:
                if self._postfix == 'bin':
                    value = value if value is not None else ''
                    self._config_doc.discriminator_bin = pickle.dumps(value)
                elif self._postfix == 'json':
                    value = value if value is not None else {}
                    setattr(self._config_doc, self._file, value)
                elif self._postfix == 'dat':
                    value = value if value is not None else []
                    value = np.array(value).tolist()
                    ret = self.pattern.search(self.filename)
                    if ret:
                        attr = ret.group(1)
                    else:
                        attr = self._file
                    setattr(self._config_doc, attr, value)

                self._config_doc.save()
            else:
                print(f'{self.filename} postfix not in {self.postfix_list}.')
        except Exception as err:
            pyqlog.error(f'Save config file {self.filename} to Store error!!! {err}')

    def save_config(self):
        """
        Save self._config_doc to MongDB ConfigStore.

        """
        self._config_doc.save()


def save_config_to_store(config_dir=None):
    """Save batch config file to MongoDB ConfigStore.
    Support the file postfix with dat, json, bin.
    Just save one object about file name to ConfigStore.
    First, query by file name, if exist update, else create a new object.

    Args:
        config_dir: dir name of config files
    """
    if not config_dir:
        config_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/config'
        print(f'config dir: {config_dir}')
    file_list = os.listdir(config_dir)
    for file in file_list:
        file_path = f'{config_dir}/{file}'
        if os.path.isfile(file_path):
            write_file_to_store(file_path)


def write_file_to_store(file_path):
    """Save one config file to MongoDB ConfigStore.

    Args:
        file_path: file path, likes {work_dir}/instrument.json
    """
    postfix_list = ['dat', 'json', 'bin']
    pattern = re.compile(r'(distortion_width|distortion|fidelity_matrix)')

    file = file_path.replace('\\', '/').rsplit('/', 1)[-1]
    try:
        file_name, postfix = file.rsplit('.', 1)
        if postfix in postfix_list:
            config_doc_list = ConfigDoc.objects.filter(filename=file)
            if config_doc_list:
                config_doc = config_doc_list[0]
            else:
                config_doc = ConfigDoc()
                config_doc.filename = file

            if postfix == 'bin':
                with open(file_path, mode='rb') as fp:
                    discriminator_bin = fp.read()
                config_doc.discriminator_bin = discriminator_bin
            elif postfix == 'json':
                with open(file_path, mode='r', encoding='utf-8') as fp:
                    data = json.load(fp)
                setattr(config_doc, file_name, data)
            elif postfix == 'dat':
                value = np.loadtxt(file_path).tolist()
                ret = pattern.search(file)
                if ret:
                    attr = ret.group(1)
                else:
                    attr = file_name
                setattr(config_doc, attr, value)

            config_doc.save()
        else:
            print(f'{file_path} postfix not in {postfix_list}.')
    except Exception as err:
        pyqlog.error(f'Save config file {file_path} to Store error!!! {err}')


def read_store_by_filename(file_path):
    """
    Read some info from ConfigStore.
    Args:
        file_path: file name or file path, recommend likes instrument.json

    Returns:
        data:
    """
    postfix_list = ['dat', 'json', 'bin']
    pattern = re.compile(r'(distortion_width|distortion|fidelity_matrix)')

    file = file_path.replace('\\', '/').rsplit('/', 1)[-1]
    try:
        file_name, postfix = file.rsplit('.', 1)
        config_doc_list = ConfigDoc.objects.filter(filename=file)
        if config_doc_list:
            config_doc = config_doc_list[0]
            if postfix == 'bin':
                data = config_doc.discriminator_bin
            elif postfix == 'json':
                data = getattr(config_doc, file_name)
            elif postfix == 'dat':
                ret = pattern.search(file)
                if ret:
                    attr = ret.group(1)
                else:
                    attr = file_name
                data = getattr(config_doc, attr)
            else:
                print(f'Not Support Postfix with {postfix}!!! Not in {postfix_list}')
                data = None
            return data
        else:
            pyqlog.warning(f'ConfigStore not found {file} info!!!')
    except Exception as err:
        pyqlog.error(f'Query config by {file} from ConfigStore Error!!! {err}')
