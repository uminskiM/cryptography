from decryptor import Decryptor
from keygenerator import KeyGenerator
from encryptor import Encryptor

if __name__ == "__main__":
    secret_message = 324654634562435437345764587689
    security_parameter = 100
    keygen = KeyGenerator(security_parameter)
    private_key, public_key = keygen.generate_keys()
    encryptor = Encryptor(public_key, secret_message)
    ciphertext = encryptor.encrypt(security_parameter)
    decryptor = Decryptor(private_key)
    decryptor.decrypt(ciphertext)