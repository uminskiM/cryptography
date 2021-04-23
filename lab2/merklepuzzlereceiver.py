import random

from bitarray import bitarray

from utils import Utils
from aes import AESCipher


class MerklePuzzleReceiver:

    def __init__(self, security_parameter, public_keys):
        self.key_length = 128
        self.security_parameter = security_parameter
        self.public_keys = public_keys
        self.message = b"Hello"
        self.suffix_numbers = [i for i in range(0, 2 ** security_parameter - 1)]

    def respond(self):
        number = random.randint(0, 2 ** self.security_parameter - 1)
        # print('random number ', number)
        public_key = self.public_keys[number]
        key = self.brute_forced_key(public_key)
        decryption_result = AESCipher().decrypt(public_key, key)
        message = bin(int(decryption_result.hex(), 16))[2:].zfill(256)
        message_key = message[self.security_parameter:-(128-self.security_parameter)]
        # print('Responding with encryption of message key ', Utils.string_of_bits_to_bytes(message_key))
        # print(message)
        # print(message_key, len(message_key))
        # print(number)
        # print(bin(int(decryption_result.hex(), 16))[2:].zfill(256))
        return number, AESCipher().encrypt(self.message, Utils.string_of_bits_to_bytes(message_key))

    def brute_forced_key(self, public_key):
        is_key_proper = False
        while not is_key_proper:
            key = self.generate_random_key()
            aes = AESCipher()
            is_key_proper = aes.is_proper_key(public_key, key)
            if is_key_proper:
                # print('Brute forced key ', key)
                return key

    def generate_random_key(self):
        prefix = '1' * (self.key_length - self.security_parameter)
        suffix_number = self.suffix_numbers[random.randint(0, len(self.suffix_numbers)-1)]
        self.suffix_numbers.remove(suffix_number)
        binary_suffix = Utils.binary_string_from_number(suffix_number, self.security_parameter)
        # print('Generated key ', prefix + binary_suffix)
        key = bitarray(prefix + binary_suffix, 'big').tobytes()
        return key
