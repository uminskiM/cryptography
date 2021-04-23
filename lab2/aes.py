import base64
import json

from Crypto.Cipher import AES


class AESCipher:

    def __init__(self):
        self.header = b"header"

    def encrypt(self, message, encryption_key):
        aes = AES.new(encryption_key, AES.MODE_GCM)
        aes.update(self.header)
        # print('Message to be encrypted: ', message)
        ciphertext, tag = aes.encrypt_and_digest(message)
        json_k = ['nonce', 'header', 'ciphertext', 'tag']
        json_v = [base64.b64encode(x).decode('utf-8') for x in (aes.nonce, self.header, ciphertext, tag)]
        result = json.dumps(dict(zip(json_k, json_v)))
        return result

    def decrypt(self, encryption_result, encryption_key):
        b64 = json.loads(encryption_result)
        json_k = ['nonce', 'header', 'ciphertext', 'tag']
        jv = {k: base64.b64decode(b64[k]) for k in json_k}
        cipher = AES.new(encryption_key, AES.MODE_GCM, nonce=jv['nonce'])
        cipher.update(jv['header'])
        plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
        print("The message was: ", plaintext)
        return plaintext

    def is_proper_key(self, encryption_result, encryption_key):
        b64 = json.loads(encryption_result)
        json_k = ['nonce', 'header', 'ciphertext', 'tag']
        jv = {k: base64.b64decode(b64[k]) for k in json_k}
        cipher = AES.new(encryption_key, AES.MODE_GCM, nonce=jv['nonce'])
        cipher.update(jv['header'])

        is_proper_key = False
        try:
            cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
            is_proper_key = True
        except ValueError:
            pass
        return is_proper_key
