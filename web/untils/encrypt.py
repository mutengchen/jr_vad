import base64
import traceback

from Crypto.Cipher import Salsa20

# 解密方
KEY = b'0123456789012345'

# 加密
def cry_pass(pass_str):
    try:
        if(not pass_str or len(pass_str)<=0):
            return ""
        plaintext = bytes(pass_str, 'utf-8') # 明文
        cipher = Salsa20.new(key=KEY)
        msg = cipher.nonce + cipher.encrypt(plaintext)  # 消息=随机数+密文
    except:
        return ""
    return base64.b64encode(msg).decode('UTF-8')


# 解密
def decode_pass(pass_str):
    try:
        if (not pass_str or len(pass_str) <= 0):
            return ""
        pass_str = base64.b64decode(pass_str)
        msg_nonce = pass_str[:8]
        ciphertext = pass_str[8:]
        cipher = Salsa20.new(key=KEY, nonce=msg_nonce)
        plaintext = cipher.decrypt(ciphertext)
    except:
        return ""
    return plaintext.decode('UTF-8')
