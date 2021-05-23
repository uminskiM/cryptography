import json

from Crypto.Random import get_random_bytes

import aes

import unittest


class MyTestCase(unittest.TestCase):
    def test_gcm_encrypts_and_decrypts_correctly(self):
        mode = aes.AESCipherGCM()
        message = b"message"
        key = get_random_bytes(16)
        encrypted = mode.encrypt(message, key)
        plaintext = mode.decrypt(json.dumps(encrypted), key)
        self.assertEqual(b"message", plaintext)

    def test_ofb_encrypts_and_decrypts_correctly(self):
        mode = aes.AESCipherOFB()
        message = b"message"
        key = get_random_bytes(16)
        encrypted = mode.encrypt(message, key)
        plaintext = mode.decrypt(json.dumps(encrypted), key)
        self.assertEqual(b"message", plaintext)

    def test_cbc_encrypts_and_decrypts_correctly(self):
        mode = aes.AESCipherCBC()
        message = b"message"
        key = get_random_bytes(16)
        encrypted = mode.encrypt(message, key)
        plaintext = mode.decrypt(json.dumps(encrypted), key)
        self.assertEqual(b"message", plaintext)

    def test_ctr_encrypts_and_decrypts_correctly(self):
        mode = aes.AESCipherCTR()
        message = b"message"
        key = get_random_bytes(16)
        encrypted = mode.encrypt(message, key)
        plaintext = mode.decrypt(json.dumps(encrypted), key)
        self.assertEqual(b"message", plaintext)


if __name__ == '__main__':
    unittest.main()
