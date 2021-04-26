import math
import random

from privatekey import PrivateKey


class KeyGenerator:

    def __init__(self, security_parameter):
        self.security_parameter = security_parameter
        self.superincreasing_sequence = []
        self.q = None
        self.r = None

    def generate_keys(self):
        return self.generate_private_key(), self.generate_public_key()

    def generate_private_key(self):
        return PrivateKey(self.generate_superincreasing_sequence(), self.choose_random_q(), self.choose_r_coprime_to_q())

    def generate_public_key(self):
        pubkey = [self.superincreasing_sequence[i] * self.r % self.q for i in range(0, len(self.superincreasing_sequence))]
        # print('Public key: ', pubkey)
        return pubkey

    def generate_superincreasing_sequence(self):
        for i in range(0, self.security_parameter):
            number = random.randint(2 ** (i + self.security_parameter - 1) + 1, 2 ** (i + self.security_parameter))
            while (number <= sum(self.superincreasing_sequence)):
                number = random.randint(max(2 ** (i + self.security_parameter - 1), sum(self.superincreasing_sequence)) + 1, 2 ** (i + self.security_parameter))
            assert number > sum(self.superincreasing_sequence)
            self.superincreasing_sequence.append(number)
        # print('Superincreasing sequence: ', self.superincreasing_sequence)
        print('Sequence length: ', len(self.superincreasing_sequence))
        return self.superincreasing_sequence

    def choose_random_q(self):
        self.q = random.randint(2 ** (self.security_parameter * 2 + 1) + 1, 2 ** (self.security_parameter * 2 + 2) - 1)
        print('Q: ', self.q)
        return self.q

    def choose_r_coprime_to_q(self):
        self.r = random.randint(2, self.q)
        while math.gcd(self.q, self.r) != 1:
            self.r = random.randint(0, 2 ** (2 * self.security_parameter))
        print('Q, R, gcd(Q, R)', self.q, self.r, math.gcd(self.q, self.r))
        return self.r