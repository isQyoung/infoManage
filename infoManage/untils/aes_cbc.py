from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from .hash import pbkdf2
from django.conf import settings

# 使用django SECRET_KEY，经过pbkdf2哈希后得到32个字节的key
secret_key = settings.SECRET_KEY
key = pbkdf2(secret_key)[:32]


def encrypt(data):
    # 加密
    # print(key.encode('utf-8'))
    data = str(data)
    # print(data)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    encrypted_data = iv + ct
    # print(encrypted_data)
    return encrypted_data


def decrypt(data):
    # 解密
    iv = b64decode(data[:24])
    ct = b64decode(data[24:])
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    decrypted_data = pt.decode()
    return decrypted_data


def check_text(data):
    # 验证传入的字符串是不是已加密的
    try:
        decrypt(data)
        return True
    except Exception or BaseException:
        return False
