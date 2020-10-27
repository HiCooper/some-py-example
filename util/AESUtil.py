# -*- coding: utf-8 -*-
# @File    : AESUtil.py
# @Date    : 2019/11/25
# @Author  : HiCooper
# @Desc    : AES 加密解密
import base64

from Crypto import Random
from Crypto.Cipher import AES

# 明文分块大小，补足则补齐
BS = AES.block_size
# 加密密钥：It must be 16, 24 or 32 bytes long (respectively for *AES-128*,*AES-192* or *AES-256*)
private_key = 'p6ltpjBktik7C5HH17kxbPR0DQJBqITk'


def pad(s):
    """
    补齐为16的倍数
    :param s:
    :return:
    """
    return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)


def un_pad(s):
    """
    去除补位
    :param s:
    :return:
    """
    return s[0:-s[-1]]


class AESUtil(object):

    @staticmethod
    def encrypt(data_str):
        """
        使用密钥key，加密字符串
        :param data_str: 待加密数据
        :return: 密文字符串
        """
        key_encode = private_key.encode('utf-8')
        bs = AES.block_size
        iv = Random.new().read(bs)
        cipher = AES.new(key_encode, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(pad(data_str).encode('utf-8'))).decode('utf-8')

    @staticmethod
    def decrypt(encrypt_data_str):
        """
        使用密钥key，解密已加密字符串，返回明文字符串
        :param encrypt_data_str: 已加密字符串
        :return: 明文字符串
        """
        key_encode = private_key.encode('utf-8')
        bs = AES.block_size
        data = base64.b64decode(encrypt_data_str.encode('utf-8'))
        if len(data) <= bs:
            return data
        iv = data[:bs]
        cipher = AES.new(key_encode, AES.MODE_CBC, iv)
        return un_pad(cipher.decrypt(data[bs:])).decode("utf-8")


if __name__ == '__main__':
    text = 'hello, here is data info!wow awesome...'
    encrypt_data = AESUtil.encrypt(text)
    print('encrypt_data:', encrypt_data)

    decrypt_data = AESUtil.decrypt(encrypt_data)
    print('decrypt_data:', decrypt_data)
