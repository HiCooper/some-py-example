# -*- coding: utf-8 -*-
# @File    : mix_config.py
# @Date    : 2019/11/26
# @Author  : HiCooper
# @Desc    : 混淆 配置文件
import json
import os

from util.AESUtil import AESUtil


def gen_encrypted_file(json_file_path, del_org_file=False):
    """
    根据json 文件生成对应的加密文件
    :param json_file_path: 原json 文件路径
    :param del_org_file: 是否删除原json文件
    :return:
    """
    if os.path.isfile(json_file_path) and json_file_path.endswith('.json'):
        with open(json_file_path, 'rb') as json_file:
            json_data = json.load(json_file)
            new_file_name = json_file_path.replace('json', 'data')
            print(new_file_name)
            data_str = json.dumps(json_data)
            f = open(new_file_name, 'wb')
            f.write(AESUtil.encrypt(data_str).encode('utf-8'))
            f.close()
            if del_org_file:
                os.remove(json_file_path)


def read_encrypted_file(data_file_path):
    """
    根据加密文件路径，读取原数据
    :param data_file_path:
    :return: python obj
    """
    if os.path.isfile(data_file_path) and data_file_path.endswith('.data'):
        with open(data_file_path, 'rb') as data_file:
            content = data_file.read().decode('utf-8')
            text = AESUtil.decrypt(content)
            result = json.loads(text)
            return result


def gen_all_json_file_encode_file():
    """
    根据目录将其下所有 `json` 文件 加密 成 新的文件 以 `.data` 结尾
    :return:
    """
    listdir = os.listdir('data')
    for file in listdir:
        file_path = './data/' + file
        if os.path.isfile(file_path) and file.endswith('.json'):
            gen_encrypted_file(file_path)


if __name__ == '__main__':
    gen_all_json_file_encode_file()
