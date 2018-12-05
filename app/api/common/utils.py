# -*- coding:utf-8 -*-
from cryptography.fernet import Fernet
import base64
import hashlib


class CryptoConfig(object):
    account_cipher_key = "PJ7TgEt2PmiUCxUlAdmEld2iCPauEy66iAoP0gB0DD4="


class JwtConfig(object):
    SECRET_KEY = "dfyg"


class CryptoUtil(object):
    @staticmethod
    def encrypt(text):
        cipher_key = CryptoConfig.account_cipher_key.encode('utf-8')
        cipher = Fernet(cipher_key)
        return str(cipher.encrypt(text.encode(encoding='utf-8')), 'utf-8')

    @staticmethod
    def decrypt(text):
        cipher_key = CryptoConfig.account_cipher_key.encode('utf-8')
        cipher = Fernet(cipher_key)
        return str(cipher.decrypt(text.encode(encoding='utf-8')), 'utf-8')

    @staticmethod
    def md5_encrypt(text):
        m = hashlib.md5()
        bytes = text.encode(encoding='utf-8')
        m.update(bytes)
        return m.hexdigest()

    @staticmethod
    def base64_encrypt(text):
        encrypt_str = base64.b64encode(text.encode('utf-8'))
        return str(encrypt_str, 'utf-8')

    @staticmethod
    def base64_decrypt(text):
        decode_str = base64.b64decode(text.encode('utf-8'))
        return str(decode_str, 'utf-8')


class FormateUtil(object):
    """
    格式转化类
    """

    @staticmethod
    def atrribute_to_str(dict):
        """
        字典值转str
        :param dict:
        :return:
        """
        if dict.__contains__("_sa_instance_state"):
            dict.pop("_sa_instance_state")
        for key, value in dict.items():
            if value is None:
                continue
            if value == 0E-8:
                value = 0
            dict[key] = str(value)
        return dict


def get_apikeys(info):
    api = info['api']
    secret = info['secret']
    tt = CryptoUtil().base64_decrypt(api)
    api = CryptoUtil().decrypt(tt)
    tts = CryptoUtil().base64_decrypt(secret)
    secret = CryptoUtil().decrypt(tts)
    return [api, secret]


if __name__ == '__main__':
    # 从命令行运行没有出错 在pycharm里运行会有错： from cryptography.hazmat.bindings._openssl import ffi, lib
    # ImportError: DLL load failed: 找不到指定的模块。
    # ss_secret = ""
    # ss_api = ""
    #
    # api_key = CryptoUtil().base64_encrypt(CryptoUtil().encrypt(ss_api))
    # print('after api encrypt:', api_key)
    # secret_key = CryptoUtil().base64_encrypt(CryptoUtil().encrypt(ss_secret))
    # print('after secret encrypt:', secret_key)
    # #
    # tapi_key = CryptoUtil().base64_decrypt(api_key)
    # v1_api_key = CryptoUtil().decrypt(tapi_key)
    # print('before api encrypt:', v1_api_key)
    # tsecret_key = CryptoUtil().base64_decrypt(secret_key)
    # v1_secret_key = CryptoUtil().decrypt(tsecret_key)
    # print('before secret encrypt:', v1_secret_key)

    pass

