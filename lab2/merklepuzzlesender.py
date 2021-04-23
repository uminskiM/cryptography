import random
from bitarray import bitarray
from aes import AESCipher
from utils import Utils


class MerklePuzzleSender:

    def __init__(self, security_parameter):
        self.security_parameter = security_parameter
        self.key_length = 128
        self.ack_message_bits = '0' * (112 - security_parameter) + Utils.string_to_bits('OK')  # WARNING THIS CAN BE POTENTIAL PROBLEM
        self.identifiers = [i for i in range(2 ** security_parameter)]
        self.encryption_keys = [i for i in range(2 ** security_parameter)]
        self.keys = {}

    def generate_public_keys(self):
        aes_cipher = AESCipher()
        encrypted_messages = []
        for i in range(2 ** self.security_parameter):
            message_to_be_encrypted = bitarray(self.build_message(i), 'big').tobytes()
            encryption_key = self.build_encryption_key()
            encryption_result = aes_cipher.encrypt(message_to_be_encrypted, encryption_key)
            # decrypted_message = aes_cipher.decrypt(encryption_result, encryption_key)
            # print(message_to_be_encrypted == decrypted_message, '\n')
            encrypted_messages.append(encryption_result)
        # print(self.keys)
        return encrypted_messages

    def decode_message(self, identifier, message):
        key = self.keys[identifier]
        # print(identifier, key)
        decryption_result = AESCipher().decrypt(message, key)
        # print(decryption_result)

    def build_message(self, i):
        key = Utils.binary_string_from_number(Utils.generate_random_key(self.key_length), self.key_length)
        identifier = self.identifiers[random.randint(0, len(self.identifiers) - 1)]
        self.keys[i] = bitarray(key, 'big').tobytes()
        self.identifiers.remove(identifier)
        identifier = Utils.binary_string_from_number(identifier, self.security_parameter)
        message = identifier + key + self.ack_message_bits
        # print(len(message), len(identifier), len(key), len(self.ack_message_bits))
        return message

    def build_encryption_key(self):
        encryption_key_prefix = '1' * (self.key_length - self.security_parameter)
        encryption_key_number = self.encryption_keys[random.randint(0, len(self.encryption_keys) - 1)]
        self.encryption_keys.remove(encryption_key_number)
        encryption_key_suffix = Utils.binary_string_from_number(encryption_key_number, self.security_parameter)
        key = encryption_key_prefix + encryption_key_suffix
        return bitarray(key, 'big').tobytes()