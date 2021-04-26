import time
from decryptor import Decryptor
from keygenerator import KeyGenerator
from encryptor import Encryptor
from shamirattack import ShamirAttack

if __name__ == "__main__":
    secret_message = 423653242436532365
    security_parameter = 64
    keygen = KeyGenerator(security_parameter)
    private_key, public_key = keygen.generate_keys()
    encryptor = Encryptor(public_key, secret_message)
    ciphertext = encryptor.encrypt(security_parameter)
    decryptor = Decryptor(private_key)
    decryptor.decrypt(ciphertext)
    attack = ShamirAttack(ciphertext, public_key)
    # start = time.time()
    # attack.perform_attack()
    # duration = time.time() - start
    # print('Duration ', duration)

    start = time.time()
    attack.perform_attack_2()
    duration = time.time() - start
    print('Duration ', duration)
