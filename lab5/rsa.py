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
    # print('m e', m, e)
    d = modinv(e, m)
    return N, e, d, p, q


def enc(message, N, public_key):
    return pow(message, public_key, N)


def dec(ciphertext, N, private_key):
    return pow(ciphertext, private_key, N)


def fast_pow(ciphertext, N, private_key):
    private_key_bin = "{0:b}".format(private_key)
    private_key_len = len(private_key_bin)
    reductions = 0
    inner_reductions = 0
    result = ciphertext
    for j in range(1, private_key_len):
        result, was_reduction_done = mod_reduce(result ** 2, N)
        reductions = reductions + was_reduction_done
        if private_key_bin[j] == "1":
            result, was_reduction_done = mod_reduce(result * ciphertext, N)
            reductions = reductions + was_reduction_done
            inner_reductions = inner_reductions + 1
    return result, inner_reductions, reductions


def mod_reduce(a, b):
    reductions = 0
    if a >= b:
        a = a % b
        reductions = 1
    return a, reductions


def sign(message, N, private_key):
    sigma = pow(message, private_key, N)
    return sigma


def verify(message, signature, N, public_key):
    # print('m ** e % N', pow(message, public_key, N))
    return message == pow(signature, public_key, N)


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


# This is done according to the http://www.cs.jhu.edu/~fabian/courses/CS600.624/Timing-full.pdf, chapter 3.4
def timing_attack(N, private_key, public_key):
    # We know that the first bit of key is 1
    print('private_key: {0:b}'.format(private_key))
    print('cracked_key: 1', end='')
    cracked_key = '1'
    # We generate sample ciphertexts
    sample_ciphertexts = random.sample(range(2, N), 10000)
    # We perform the fast_pow over the ciphertexts and we receive the tuples of result, inner and outer reductions
    # Oracle querying
    ciphertexts_reductions_tuples = [fast_pow(ciphertext, N, private_key) for ciphertext in sample_ciphertexts]
    # We retrieve the number of outer reductions
    reductions = [c[2] for c in ciphertexts_reductions_tuples]

    for _ in range(len('{0:b}'.format(private_key)) - 2):  # minus 2 because we omit the first and the last bit
        # We create sets for two different oracles The sets distinguish what expression was calculated and with reduction or not
        m_1, m_2, m_3, m_4 = [], [], [], []

        for index in range(len(reductions)):
            ciphertext = sample_ciphertexts[index]

            temporary_value = fast_pow(ciphertext, N, int(f'{cracked_key}0', 2))[0]

            reduced_value, _ = mod_reduce(temporary_value * ciphertext, N)

            if mod_reduce(reduced_value ** 2, N)[1] == 1:
                m_4.append(index)
            else:
                m_3.append(index)

            if mod_reduce(temporary_value ** 2, N)[1] == 1:
                m_2.append(index)
            else:
                m_1.append(index)

        # We count the averages of reductions in particular sets
        avg_1 = sum(reductions[index] for index in m_1) / len(m_1)
        avg_2 = sum(reductions[index] for index in m_2) / len(m_2)
        avg_3 = sum(reductions[index] for index in m_3) / len(m_3)
        avg_4 = sum(reductions[index] for index in m_4) / len(m_4)

        # We count differences between two sets grouped by expression
        difference_1_2 = avg_1 - avg_2
        difference_3_4 = avg_3 - avg_4

        # We determine whether the bit is 0 or 1 by comparing the differences
        bit = ('0', '1')[difference_1_2 > difference_3_4]
        cracked_key += bit
        print(bit, end='')
    print('?')

    print('\nLet\'s brute force the last bit')
    cracked_one = cracked_key + '1'
    cracked_zero = cracked_key + '0'
    print('The possible keys are: ', cracked_one, cracked_zero)
    print('Let\'s take the random message, encrypt it with public key, and try to decrypt it by one of these two keys')
    ta_message = random_element_from_Z(N)
    ta_encrypted = enc(ta_message, N, public_key)
    print('message: {}, encrypted message: {}'.format(ta_message, ta_encrypted))
    decrypted_one = dec(ta_encrypted, N, int(cracked_one, 2))
    decrypted_zero = dec(ta_encrypted, N, int(cracked_zero, 2))
    proper_key = (cracked_one, cracked_zero)[decrypted_zero == ta_message]
    print('decrypted by key with 0 at the end: {}'.format(decrypted_zero))
    print('decrypted by key with 1 at the end: {}'.format(decrypted_one))
    print('The proper key is {}'.format(proper_key))


N, public_key, private_key, p, q = GenRSA("1111111111111111111")
message = random_element_from_Z(N)
signature = sign(message, N, private_key)
print('message, signature, N, public_key, verify(message, signature, N, public_key)')
print(message, signature, N, public_key, verify(message, signature, N, public_key), '\n')

encrypted = enc(message, N, public_key)
decrypted = dec(encrypted, N, private_key)
print('message, encrypted, decrypted')
print(message, encrypted, decrypted, '\n')
print('message, encrypted, decrypt_securely(encrypted, N, private_key, public_key)')
print(message, encrypted, decrypt_securely(encrypted, N, private_key, public_key), '\n')

s1, random_element = blind_signature_part_one(message, public_key, N)
s2 = sign(s1, N, private_key)
signature = blind_signature_part_two(s2, N, random_element)
print('s1, random_element, N')
print(s1, random_element, N, '\n')
print('s2')
print(s2, '\n')
print('message, signature, verify(message, signature, N, public_key)')
print(message, signature, verify(message, signature, N, public_key), '\n')

print('Timing attack presentation')
timing_attack(N, private_key, public_key)
