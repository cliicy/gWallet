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
    dapi = info['api']
    dsecret = info['secret']
    tt = CryptoUtil().base64_decrypt(dapi)
    api = CryptoUtil().decrypt(tt)
    tts = CryptoUtil().base64_decrypt(dsecret)
    secret = CryptoUtil().decrypt(tts)
    return [api, secret]


if __name__ == '__main__':
    # 从命令行运行没有出错 在pycharm里运行会有错： from cryptography.hazmat.bindings._openssl import ffi, lib
    # ImportError: DLL load failed: 找不到指定的模块。
    # invalid accout
    # ss_api = "0a5ba5fe-2ce4-4f2a-b308-1f6f17d3e6ec"
    # ss_secret = "82B69BD2B7DBBABF726D046C37C7969F"

    # invalid accout
    # ss_api = "bb025326-6429af53-37f866f1-3793f"
    # ss_secret = "5d9560ca-993c7690-790f0503-21a70"

    ss_api = "05a75e18-3286baaf-b9397b90-5cecc"
    ss_secret = "b1887276-ebd2705c-f961a929-32ed7"

    api_key = CryptoUtil().base64_encrypt(CryptoUtil().encrypt(ss_api))
    print('after api encrypt:', api_key)
    secret_key = CryptoUtil().base64_encrypt(CryptoUtil().encrypt(ss_secret))
    print('after secret encrypt:', secret_key)

    tapi_key = CryptoUtil().base64_decrypt(api_key)
    v1_api_key = CryptoUtil().decrypt(tapi_key)
    print('before api encrypt:', v1_api_key)
    tsecret_key = CryptoUtil().base64_decrypt(secret_key)
    v1_secret_key = CryptoUtil().decrypt(tsecret_key)
    print('before secret encrypt:', v1_secret_key)

    pass

