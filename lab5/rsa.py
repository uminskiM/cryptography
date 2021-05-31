import math
import random
from sympy import randprime, isprime, Mod


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('does not exist')
    else:
        return x % m


def GenModulus(w):
    n = len(w) // 2
    p = randprime(2 ** n, 2 ** (n + 1))
    q = randprime(2 ** n, 2 ** (n + 1))
    N = p * q
    return N, p, q


def GenRSA(w):
    N, p, q = GenModulus(w)
    m = (p - 1) * (q - 1)
    e = 2 ** 16 + 1
    print('m e', m, e)
    d = modinv(e, m)
    return N, e, d, p, q


def enc(x, N, e):
    return x ** e % N


def dec(c, N, d):
    return c ** d % N


def fast_pow(c, N, d):
    d_bin = "{0:b}".format(d)
    d_len = len(d_bin)
    reductions = 0
    h = 0
    x = c
    for j in range(1, d_len):
        x, r = mod_reduce(x ** 2, N)
        reductions = reductions + r
        if d_bin[j] == "1":
            x, r = mod_reduce(x * c, N)
            reductions = reductions + r
            h = h + 1
    return x, h, reductions


def mod_reduce(a, b):
    reductions = 0
    if a >= b:
        a = a % b
        reductions = 1
    return a, reductions


def sign(message, N, private_key):
    sigma = message ** private_key % N
    return sigma


def verify(message, signature, N, public_key):
    print('m ** e % N', message ** public_key % N)
    return message == (signature ** public_key % N)


def random_element_from_Z(N):
    g = N
    while math.gcd(g, N) != 1:
        g = random.randint(2, N)
    return g


def blind_signature_part_one(message, public_key, N):
    random_element = random_element_from_Z(N)
    return (message * (random_element ** public_key) % N) % N, random_element


def blind_signature_part_two(signature, N, random_element):
    r_inv = modinv(random_element, N)
    return signature * r_inv % N


def decrypt_securely(ciphertext, N, private_key, public_key):
    random_element = random_element_from_Z(N)
    intermediate_decryption = dec((ciphertext * (random_element ** public_key % N)) % N, N, private_key)
    random_inversed = modinv(random_element, N)
    return (intermediate_decryption * random_inversed) % N


N, public_key, private_key, p, q = GenRSA("11111111111111111")
message = random_element_from_Z(N)
signature = sign(message, N, private_key)
print(message, signature, N, public_key, verify(message, signature, N, public_key))

encrypted = enc(message, N, public_key)
decrypted = dec(encrypted, N, private_key)
print(message, encrypted, decrypted)
print(message, encrypted, decrypt_securely(encrypted, N, private_key, public_key))

s1, random_element = blind_signature_part_one(message, public_key, N)
s2 = sign(s1, N, private_key)
signature = blind_signature_part_two(s2, N, random_element)
print(s1, random_element, N)
print(s2)
print(message, signature, verify(message, signature, N, public_key))
