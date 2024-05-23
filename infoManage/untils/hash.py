from django.conf import settings
import hashlib
import binascii


def md5(data_string):
    """md5加密"""
    obj = hashlib.md5(settings.SECRET_KEY.encode("utf-8"))
    obj.update(data_string.encode("utf-8"))
    return obj.hexdigest()


def pbkdf2(data_string):
    """pbkdf2加密"""
    # 把django SECRET_KEY作为盐
    salt = settings.SECRET_KEY.encode("utf-8")
    # 使用PBKDF2算法生成一个32字节的密钥
    key = hashlib.pbkdf2_hmac('sha256', data_string.encode("utf-8"), salt, 100000, dklen=32)
    return binascii.hexlify(key).decode()
