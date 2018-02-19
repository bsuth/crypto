#Contains all the AES tables (app for appendix)
import app


#NOTE: In the following 4 functions (SubBytes, ShiftRows,
#      MixColumns, and AddRoundKey), text is assumed to
#      be a 4x4 table of bytes, represented by a list.
#      The indexing of text in the list is as follows:
#
#               0    4    8    12
#               1    5    9    13
#               2    6   10    14
#               3    7   11    15
#
#      Please refer to app.py for specifics on the tables
#      used for encryption/decryption.


# Description: Substitutes the bytes in text via
#              byte-wise matrix multiplication
#              together with an offset.
# Note:        All addition operations here are
#              replaced by XOR(^).
def SubBytes(text, matrix, vec):
    for i in range(16):
        # Convert ith byte to bits
        byte = [int(bit) for bit in format(text[i], '08b')]
        
        # Transform bits via matrix operations
        text[i] = 0
        for j in range(8):
            text[i] = (text[i] << 1) ^ vec[j]
            for k in range(8):
                text[i] ^= (matrix[8*j + k] * byte[k])


# Description: Permutes the rows of text via a left
#              circular shift of n for the nth row.
#Note:         We use a permutation table to create
#              a permutation of the original text,
#              then set text to the new permutation.
def ShiftRows(text, matrix):
    for i in range(16):
        text.append(text[matrix[i]])
    text = text[16:]


# Description: Performs matrix multiplication of an
#              encrypting (or decrypting) matrix and text.
#Note:         All addition operations here are replaced
#              by XOR(^). Arithmetic is done over
#              F[x]/(f(x)) where F = Z/(2**8)Z and
#              f(x) = x**8 + x**4 + x**3 + x + 1.
def MixColumns(text, matrix):
    # Default initialize another block
    for i in range(16):
        text.append(0)

    for i in range(16):
        for j in range(4):
            # Transform byte via matrix multiplication
            temp = matrix[4*(i % 4) + j] * text[4*int(i/4) + j]
            text[16 + i] ^= temp & 0xff

            # Working in x**8 + x**4 + x**3 + x + 1
            overflow = temp >> 8
            modulus = 27 # 11011
            while(overflow):
                text[16 + i] ^= (overflow & 1) * modulus
                modulus = modulus << 1
                overflow = overflow >> 1

    # Remove old text
    text = text[16:]


# Description: XORs every entry of text with the
#              corresponding entry in key.
def AddRoundKey(text, key):
    for i in range(16):
        text[i] ^=  key[i]
