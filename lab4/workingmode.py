import random
import string


import utils
from bitarray import bitarray

import aes


class WorkingMode(object):

    def __init__(self):
        pass

    def run(self):
        raise Exception('NotImplementedException')

    @staticmethod
    def resolve_aes_instance(encryption_mode) -> aes.AESCipher:
        if encryption_mode == 'GCM':
            return aes.AESCipherGCM()
        elif encryption_mode == 'OFB':
            return aes.AESCipherOFB()
        elif encryption_mode == 'CBC':
            return aes.AESCipherCBC()
        elif encryption_mode == 'CTR':
            return aes.AESCipherGCM()
        raise Exception('Incorrect encryption mode')


class EncryptionOracleWorkingMode(WorkingMode):

    def __init__(self, key: string, encryption_mode: string):
        WorkingMode.__init__(self)
        self.key = key
        self.aes_instance: aes.AESCipher = self.resolve_aes_instance(encryption_mode)

    def run(self):
        messages = []
        while True:
            message = input('Enter the message to be encrypted. \'exit\' command exists the program: ')
            if message == 'exit':
                break
            messages.append(bitarray(utils.Utils.string_to_bits(message), 'big').tobytes())
        encrypted_messages = []
        for message in messages:
            ciphertext = self.aes_instance.encrypt(message, self.key)
            encrypted_messages.append(ciphertext['ciphertext'])
        print(encrypted_messages)
        return encrypted_messages


class ChallengeWorkingMode(WorkingMode):

    def __init__(self, key: string, encryption_mode: string):
        WorkingMode.__init__(self)
        self.key = key
        self.aes_instance = self.resolve_aes_instance(encryption_mode)

    def run(self):
        first_message = input('Enter first message: ')
        second_message = input('Enter second message: ')
        messages = [bitarray(utils.Utils.string_to_bits(first_message), 'big').tobytes(),
                    bitarray(utils.Utils.string_to_bits(second_message), 'big').tobytes()]
        random_bit = random.randint(0, 1)
        ciphertext = self.aes_instance.encrypt(messages[random_bit], self.key)
        print(ciphertext['ciphertext'])
        return ciphertext
