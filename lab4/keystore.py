import binascii
import utils
import jks
import getpass

from bitarray import bitarray


class KeyLoader(object):

    def __init__(self, path_to_keystore):
        self.path_to_keystore = path_to_keystore

    def load_key(self, key_identifier):
        keystore_pass = getpass.getpass("Enter the password to the keystore: ")
        keystore = jks.KeyStore.load(self.path_to_keystore, keystore_pass)

        key_pass = getpass.getpass("Enter the password to the key: ")
        keystore.entries[key_identifier].decrypt(key_pass)
        key_structure = keystore.secret_keys[key_identifier]
        # print(key_structure.alias, key_structure.algorithm, key_structure.key_size, "".join("{:02x}".format(b) for b in bytearray(key_structure.key)))
        key_to_print = "".join("{:02x}".format(b) for b in bytearray(key_structure.key))
        key_as_number = int(key_to_print, 16)
        key_as_bits = utils.Utils.binary_string_from_number(key_as_number, 256)
        # print(utils.Utils.binary_string_from_number(key_as_number, 256), len(utils.Utils.binary_string_from_number(key_as_number, 256)))
        # print(bitarray(key_as_bits, 'big'))
        return bitarray(key_as_bits, 'big').tobytes()
