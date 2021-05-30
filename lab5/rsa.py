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
    n = len(w)
    N, p, q = GenModulus(w)
    m = (p - 1) * (q - 1)
    e = 2 ** 16 + 1
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


def sign(m, N, d):
    sigma = m ** d % N
    return sigma


def verify(m, s, N, e):
    return s == (m ** e % N)


def random_element_from_Z(N):
    g = N
    while math.gcd(g, N) != 1:
        g = random.randint(2, N)
    return g


def blind_signature_part_one(m, e, N):
    r = random_element_from_Z(N)
    return (m * r ** e) % N, r


def blind_signature_part_two(s, e, N, r):
    r_inv = modinv(r, N)
    return s * r_inv % N


def decSec(c, N, d, e):
    r = random_element_from_Z(N)
    mp = dec((c * (r ** e % N)) % N, N, d)
    r_inv = modinv(r, N)
    return (mp * r_inv) % N


N, e, d, p, q = GenRSA("11111111")
m = random_element_from_Z(N)
s = sign(m, N, d)
print(verify(m, s, N, e))

c = enc(m, N, e)
d = dec(c, N, d)
print(m, c, d)

c = enc(m, N, e)
d = decSec(c, N, d, e)
print(m, c, d)
