#Contains all the AES tables (app for appendix)
import app


#NOTE: In the following functions, text and key are 
#      assumed to be 4x4 tables of bytes, represented 
#      by a list. The indexing of these are as follows:
#
#               0    4    8    12
#               1    5    9    13
#               2    6   10    14
#               3    7   11    15
#
#      Please refer to app.py for specifics on the
#      tables used for encryption/decryption.


# Description: Returns the entry from box (16x16 table)
#              whose row is determined by the first 4
#              bits of byte, and whose column is
#              determined by the last 4 bits of byte.
def SubBytes(byte, box):
    return box[(byte >> 4)*16 + (byte & 0x0f)]


# Description: Permutes the rows of text via a left
#              circular shift of n for the nth row
#              (right circular shift for decryption).
#Note:         A permutation table is used to mimic
#              the left (or right) shift of each row.
def ShiftRows(text, matrix):
    temp = [text[matrix[i]] for i in range(16)]
    for i in range(16):
        text[i] = temp[i]


# Description: Performs matrix multiplication of an
#              encrypting (or decrypting) matrix and text.
# Note:        All addition operations here are replaced
#              by XOR(^). Arithmetic is done over
#              F[x]/(f(x)) where F = Z/(2**8)Z and
#              f(x) = x**8 + x**4 + x**3 + x + 1.
# Note:        Since addition operations are replaced by
#              XOR(^), we cannot simply multiply entries
#              in the matrix with the bytes in text, as
#              this uses addition between place values.
#              For example, 14 (0x0E) cannot be interpreted
#              as an integer partition (ex. 10 + 4) but
#              must be interpreted as (8 ^ 4 ^ 2).
def MixColumns(text, matrix):
    temp = [0 for i in range(16)]
    
    # Matrix Multiplication
    for i in range(16):
        for j in range(4):
            # Store matrix entry and text byte
            entry = matrix[4*(i % 4) + j]
            byte = text[4*int(i/4) + j]

            # Multiplication with XOR as addition
            while(entry):
                temp[i] ^= (entry & 1)*byte
                byte = ((byte << 1) & 0xff) ^ (byte >> 7)*0b11011
                entry = entry >> 1

    # Update text
    for i in range(16):
        text[i] = temp[i]


# Description: XORs every entry of text with the
#              corresponding entry in key.
def AddRoundKey(text, key):
    temp = [text[i] ^ key[i] for i in range(16)]
    for i in range(16):
        text[i] = temp[i]


# Description: Generates the key schedule for AES-128.
#              Returns a list of lists where each sublist 
#              represents a subkey in the same format as 
#              text, as described above.
def keyExpansion(key, decrypt = False):
    # Add first subkey
    subkeys = [[int((key >> 8*(15 - i)) & 0xff) for i in range(16)]]

    # Generate round keys
    for i in range(10):
        # AES g function
        nextKey = [SubBytes(subkeys[-1][-3], app.S) ^ app.RC[i],
                    SubBytes(subkeys[-1][-2], app.S),
                    SubBytes(subkeys[-1][-1], app.S),
                    SubBytes(subkeys[-1][-4], app.S)]       

        # Generate next round key
        for j in range(16):
            nextKey.append(nextKey[j] ^ subkeys[-1][j])

        # Add key to list
        subkeys.append(nextKey[4:])

    # Reverse key schedule and apply inverse mix cols for decryption
    if(decrypt):
        subkeys.reverse()
        for i in range(1, 10):
            MixColumns(subkeys[i], app.oMC)

    return subkeys


# Description: Encrypts (or decrypts) plaintext using key via AES.
# Note:        This algorithm uses AES-128, so we assume a plaintext
#              and key length of 128 bits and perform 10 rounds.             
def aes(plaintext, key, decrypt = False):
    ciphertext = 0

    # Put plaintext in list
    text = [int((plaintext >> 8*(15 - i)) & 0xff) for i in range(16)]

    # Choose correct matrices (encryption vs decryption)
    box = [app.oS, app.oSR, app.oMC] if decrypt else [app.S, app.SR, app.MC]

    # Get key schedule
    keySchedule = keyExpansion(key, decrypt)

    # Initial transformation
    AddRoundKey(text, keySchedule[0])

    # Rounds 1 - 9
    for i in range(9):        
        text = [SubBytes(text[j], box[0]) for j in range(16)] 
        ShiftRows(text, box[1])                             
        MixColumns(text, box[2])                          
        AddRoundKey(text, keySchedule[i + 1])          

    # Final Round (no MixColumns)
    text = [SubBytes(text[j], box[0]) for j in range(16)] 
    ShiftRows(text, box[1])                             
    AddRoundKey(text, keySchedule[10])               

    # Convert list back to integer
    for byte in text:
        ciphertext = (ciphertext << 8) | byte

    return ciphertext



