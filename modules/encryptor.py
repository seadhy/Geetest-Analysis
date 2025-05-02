import time
import json
import rsa
import os
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


class Encryptor:
    MODULUS = '00C1E3934D1614465B33053E7F48EE4EC87B14B95EF88947713D25EECBFF7E74C7977D02DC1D9451F79DD5D1C10C29ACB6A9B4D6FB7D0A0279B6719E1772565F09AF627715919221AEF91899CAE08C0D686D748B20A3603BE2318CA6BC2B59706592A9219D0BF05C9F65023A21D2330807252AE0066D59CEEFA5F2748EA80BAB81'
    PUB_KEY = '10001'
    
    
    @staticmethod
    def generate_ts():
        return str(int(time.time() * 1000))
    
    @staticmethod
    def read_geetest(callback: str, response_text: str):
        result = response_text.lstrip(callback + "(").rstrip(')')

        return json.loads(result)
    
    @staticmethod
    def generate_aes_key(size: int = 8):
        return binascii.hexlify(os.urandom(size)).decode()
    
    @staticmethod
    def generate_rsa(aes_key: str):
        PublicKey = rsa.PublicKey(int(Encryptor.MODULUS, 16), int(Encryptor.PUB_KEY,16))
        rs = rsa.encrypt(aes_key.encode(), PublicKey)
        return rs.hex()
    
    @staticmethod
    def aes_encrypt(text, secKey, iv = b'0000000000000000', style='pkcs7'):
        encryptor = AES.new(secKey.encode('utf-8'), AES.MODE_CBC, iv)
        pad_pkcs7 = pad(text.encode('utf-8'), AES.block_size, style=style)
        ciphertext = encryptor.encrypt(pad_pkcs7)
        
        arr = []
        for byte in ciphertext:
            arr.append(byte)
        
        return arr
