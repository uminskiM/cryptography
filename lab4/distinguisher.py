import random
import sys

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from aes import AESCipherCBC


def xor(first_bytestream, second_bytestream):
    second_bytestream = second_bytestream[:len(first_bytestream)]
    first_as_int = int.from_bytes(first_bytestream, sys.byteorder)
    second_as_int = int.from_bytes(second_bytestream, sys.byteorder)
    xor_result = first_as_int ^ second_as_int
    return xor_result.to_bytes(len(first_bytestream), sys.byteorder)


def generate_iv():
    iv_as_number = int(get_random_bytes(16).hex(), 16)
    while True:
        yield iv_as_number.to_bytes(16, 'big')
        iv_as_number = iv_as_number + 1


class EncryptionOracle(object):

    def __init__(self):
        self.encryption_key = get_random_bytes(32)
        self.iv_generator = generate_iv()
        self.random_bit = None

    def encode(self, message):
        aes = AESCipherCBC()
        return aes.encrypt_with_iv(message, self.encryption_key, next(self.iv_generator))

    def challenge(self, first_message, second_message):
        aes = AESCipherCBC()
        self.random_bit = random.randint(0, 1)
        messages = [first_message, second_message]
        message = messages[self.random_bit]
        return aes.encrypt_with_iv(message, self.encryption_key, next(self.iv_generator))


class CPADistinguisher(object):

    def __init__(self):
        self.oracle = EncryptionOracle()

    def distinguish(self):
        first_message_part_one = get_random_bytes(AES.block_size)
        first_message_part_two = get_random_bytes(AES.block_size)
        first_message = self.build_message(first_message_part_one, first_message_part_two)
        first_ciphertext, first_iv = self.oracle.encode(first_message)
        incremented_first_iv = (int(first_iv.hex(), 16) + 1).to_bytes(16, 'big')

        xored_part = xor(xor(first_message_part_one, first_iv), incremented_first_iv)
        second_message_part_two = get_random_bytes(AES.block_size)
        message_with_xor = self.build_message(xored_part, second_message_part_two)

        second_message_part_one = get_random_bytes(AES.block_size)
        assert xored_part != second_message_part_one
        second_message = self.build_message(second_message_part_one, second_message_part_two)

        second_ciphertext, second_iv = self.oracle.challenge(message_with_xor, second_message)
        if second_ciphertext[:AES.block_size] == first_ciphertext[:AES.block_size]:
            chosen_bit = 0
        else:
            chosen_bit = 1
        if self.oracle.random_bit == chosen_bit:
            # print('CPA distinguisher won!')
            return 1
        else:
            # print('CPA distinguisher lost!')
            return 0

    @staticmethod
    def build_message(message_part_one, message_part_two):
        return message_part_one + message_part_two


if __name__ == "__main__":
    tries = 10000
    winnings = 0
    for i in range(0, tries):
        distinguisher = CPADistinguisher()
        winnings += distinguisher.distinguish()
    print('CPA distinguisher won {0} out of {1} attempts.'.format(winnings, tries))
