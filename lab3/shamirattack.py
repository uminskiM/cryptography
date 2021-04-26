import numpy as np
import olll

from fpylll import *

class ShamirAttack:

    def __init__(self, ciphertext, public_key):
        self.ciphertext = ciphertext
        self.public_key = public_key

    # def perform_attack(self):
    #     matrix = np.identity(len(self.public_key) + 1)
    #     vector = self.public_key.copy()
    #     vector.append(-self.ciphertext)
    #     transposed_vector = np.array(vector)
    #     matrix[:, -1] = transposed_vector
    #     reduced_matrix = olll.reduction(matrix, 0.75)
    #     binary_row = self.get_binary_row(reduced_matrix)[:-1]
    #     binary_row.reverse()
    #     # print(matrix)
    #     # print(reduced_matrix)
    #     cracked_message = 0
    #     for i in range(0, len(binary_row)):
    #         if binary_row[i] == 1:
    #             cracked_message = cracked_message + 2 ** i
    #     print('Cracked message ', cracked_message)

    def perform_attack_2(self):
        size = len(self.public_key)
        matrix = IntegerMatrix.identity(size+1)
        for i in range(size):
            matrix[i, size] = int(self.public_key[i])
        matrix[size, size] = -self.ciphertext
        L = LLL.reduction(matrix)
        matrix_binary_row = self.get_binary_row(L)
        binary_row = []
        for i in range(0, len(matrix_binary_row)-1):
            binary_row.append(matrix_binary_row[i])
        cracked_message = 0
        binary_row.reverse()
        for i in range(0, len(binary_row)):
            if binary_row[i] == 1:
                cracked_message = cracked_message + 2 ** i
        print('Cracked message ', cracked_message)

    def get_binary_row(self, matrix):
        for row in matrix:
            is_binary = True
            for value in row:
                if value != 0 and value != 1:
                    is_binary = False
                    break
            if is_binary:
                return row
        return None
