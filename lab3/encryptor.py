import utils

class Encryptor:

    def __init__(self, public_key, message_number):
        self.public_key = public_key
        self.message_number = message_number

    def encrypt(self, security_parameter):
        message_binary = utils.Utils.binary_string_from_number(self.message_number, security_parameter)
        assert len(message_binary) == len(self.public_key)
        ciphertext = sum([int(message_binary[i]) * self.public_key[i] for i in range(0, len(message_binary))])
        print('Ciphertext ', ciphertext)
        return ciphertext


