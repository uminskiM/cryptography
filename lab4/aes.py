import base64
import json

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class AESCipher(object):

    def __init__(self):
        pass

    def encrypt(self, message, encryption_key):
        raise Exception('NotImplementedInterface')

    def decrypt(self, encrypted_message, encryption_key):
        raise Exception('NotImplementedInterface')


class AESCipherGCM(AESCipher):

    def __init__(self):
        super().__init__()
        self.header = b"header"

    def encrypt(self, message, encryption_key):
        aes = AES.new(encryption_key, AES.MODE_GCM)
        aes.update(self.header)
        # print('Message to be encrypted: ', message)
        ciphertext, tag = aes.encrypt_and_digest(message)
        json_k = ['nonce', 'header', 'ciphertext', 'tag']
        json_v = [base64.b64encode(x).decode('utf-8') for x in (aes.nonce, self.header, ciphertext, tag)]
        return dict(zip(json_k, json_v))

    def decrypt(self, encryption_result, encryption_key):
        b64 = json.loads(encryption_result)
        json_k = ['nonce', 'header', 'ciphertext', 'tag']
        jv = {k: base64.b64decode(b64[k]) for k in json_k}
        cipher = AES.new(encryption_key, AES.MODE_GCM, nonce=jv['nonce'])
        cipher.update(jv['header'])
        plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
        print("The message was: ", plaintext)
        return plaintext


class AESCipherCBC(AESCipher):

    def __init__(self):
        super().__init__()
        self.header = b"header"

    def encrypt(self, message, encryption_key):
        aes = AES.new(encryption_key, AES.MODE_CBC)
        # print('Message to be encrypted: ', message)
        ct_bytes = aes.encrypt(pad(message, AES.block_size))
        iv = base64.b64encode(aes.iv).decode('utf-8')
        ciphertext = base64.b64encode(ct_bytes).decode('utf-8')
        json_k = ['iv', 'ciphertext']
        json_v = [x for x in (iv, ciphertext)]
        return dict(zip(json_k, json_v))

    def encrypt_with_iv(self, message, encryption_key, iv):
        aes = AES.new(encryption_key, AES.MODE_CBC, iv=iv)
        return aes.encrypt(pad(message, AES.block_size, style='iso7816')), aes.iv

    def decrypt(self, encryption_result, encryption_key):
        b64 = json.loads(encryption_result)
        json_k = ['iv', 'ciphertext']
        jv = {k: base64.b64decode(b64[k]) for k in json_k}
        cipher = AES.new(encryption_key, AES.MODE_CBC, iv=jv['iv'])
        plaintext = unpad(cipher.decrypt(jv['ciphertext']), AES.block_size)
        print("The message was: ", plaintext)
        return plaintext


class AESCipherOFB(AESCipher):

    def __init__(self):
        super().__init__()
        self.header = b"header"

    def encrypt(self, message, encryption_key):
        aes = AES.new(encryption_key, AES.MODE_OFB)
        # print('Message to be encrypted: ', message)
        ct_bytes = aes.encrypt(message)
        iv = base64.b64encode(aes.iv).decode('utf-8')
        ciphertext = base64.b64encode(ct_bytes).decode('utf-8')
        json_k = ['iv', 'ciphertext']
        json_v = [x for x in (iv, ciphertext)]
        return dict(zip(json_k, json_v))

    def decrypt(self, encryption_result, encryption_key):
        b64 = json.loads(encryption_result)
        json_k = ['iv', 'ciphertext']
        jv = {k: base64.b64decode(b64[k]) for k in json_k}
        cipher = AES.new(encryption_key, AES.MODE_OFB, iv=jv['iv'])
        plaintext = cipher.decrypt(jv['ciphertext'])
        print("The message was: ", plaintext)
        return plaintext


class AESCipherCTR(AESCipher):

    def __init__(self):
        super().__init__()
        self.header = b"header"

    def encrypt(self, message, encryption_key):
        aes = AES.new(encryption_key, AES.MODE_CTR)
        # print('Message to be encrypted: ', message)
        ct_bytes = aes.encrypt(message)
        nonce = base64.b64encode(aes.nonce).decode('utf-8')
        ciphertext = base64.b64encode(ct_bytes).decode('utf-8')
        json_k = ['nonce', 'ciphertext']
        json_v = [x for x in (nonce, ciphertext)]
        return dict(zip(json_k, json_v))

    def decrypt(self, encryption_result, encryption_key):
        b64 = json.loads(encryption_result)
        json_k = ['nonce', 'ciphertext']
        jv = {k: base64.b64decode(b64[k]) for k in json_k}
        cipher = AES.new(encryption_key, AES.MODE_CTR, nonce=jv['nonce'])
        plaintext = cipher.decrypt(jv['ciphertext'])
        print("The message was: ", plaintext)
        return plaintext
