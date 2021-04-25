

class Decryptor:

    def __init__(self, private_key):
        self.private_key = private_key

    def decrypt(self, ciphertext):
        r_inverse = pow(self.private_key.r, -1, self.private_key.q)
        ciphertext_prim = ciphertext * r_inverse % self.private_key.q
        X = self.knapsack(ciphertext_prim)
        message = sum([2 ** (len(self.private_key.sequence) - X[i] - 1) for i in range(0, len(X))])
        print('Decrypted message: ', message)
        return message

    def knapsack(self, ciphertext_prim):
        X = []
        while True:
            for i in reversed(self.private_key.sequence):
                if i <= ciphertext_prim:
                    ciphertext_prim = ciphertext_prim - i
                    X.append(self.private_key.sequence.index(i))
                    break
            if ciphertext_prim <= 0:
                break
        return X



