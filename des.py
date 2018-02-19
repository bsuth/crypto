# Contains all the DES tables (app for appendix)
import app

# Description: Permutes (or expands/shrinks) the text via the bit
#              placements designated in the box.
def permute(text, box):
    result = 0
    for i in range(len(box)):
        result = (result << 1) | ((text >> box[i]) & 1)
    return result


# Description: Returns a list containing all the subkeys.
def keySchedule(key, rounds, decrypt):
    subkeys = []

    #Permutation Choice 1
    key = permute(key, app.PC1)

    # Generate subkeys
    for i in range(rounds):
        #Split the key into halves
        L = key >> 28
        R = key & 0xfffffff

        #Circular Left Shifts on halves
        L = ((L << app.LS[i]) + (L >> (28 - app.LS[i]))) & 0xfffffff
        R = ((R << app.LS[i]) + (R >> (28 - app.LS[i]))) & 0xfffffff

        # Mend and Permutation Choice 2
        key = (L << 28) | R
        subkeys.append(permute(key, app.PC2))

    # Reverse key schedule if decrypting
    if(decrypt):
        subkeys.reverse()

    return subkeys


# Description: Returns text after one round of DES
def desRound(text, subkey):
    temp = 0

    # Load the S-Boxes
    sBoxes = [app.S1, app.S2, app.S3, app.S4,
              app.S5, app.S6, app.S7, app.S8]

    #First 32 bits of text
    newL = text & 0xffffffff

    #Expansion/Permutation and XOR
    newR = permute(newL, app.E) ^ subkey

    #S-boxes
    for j in range(8):
        bits = (newR >> 6*(7-j)) & 0x3f #S-Box 6 bit input
        sRow = 2*(bits >> 5) + (bits & 1) #Last and first bit
        sColumn = (bits & 0x1e) >> 1 #Middle 4 bits
        temp = (temp << 4) | sBoxes[j][sRow*16 + sColumn] #S-box output

    #Permutation and XOR
    newR = permute(temp, app.P) ^ (text >> 32)

    #Finish round
    return (newL << 32) | newR


# Description: Takes in two 64-bit numbers (as plaintext and key)
#              and applies the DEA. Returns the encrypted text.
def des(plaintext, key, rounds = 16, decrypt = False):
    # Get key schedule
    subkeys = keySchedule(key, rounds, decrypt)
 
    #Initial Permutation
    ciphertext = permute(plaintext, app.IP)

    #DES Rounds
    for i in range(rounds):
        ciphertext = desRound(ciphertext, subkeys[i])

    #Flip and Inverse Initial Permutation
    ciphertext = ((ciphertext & 0xffffffff) << 32) | (ciphertext >> 32)
    return permute(ciphertext, app.oIP)
