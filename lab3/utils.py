import random

from bitarray import bitarray


class Utils:
    @staticmethod
    def string_to_bits(some_string):
        return ''.join(format(ord(i), '08b') for i in some_string)

    @staticmethod
    def binary_string_from_number(number, length):
        return "{0:b}".format(number).zfill(length)

    @staticmethod
    def generate_random_key(power_of_two):
        return random.randint(0, 2 ** power_of_two - 1)

    @staticmethod
    def string_of_bits_to_bytes(some_string):
        return bitarray(some_string, 'big').tobytes()
