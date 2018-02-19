#Description: Takes the text given by cipher and
#             computes the index of coincidence.
def getIoC(cipher):
    #Default initialize analysis dictionary
    from collections import defaultdict
    analysis = defaultdict(int)
    IoC = 0

    #Analyze text
    for i in range(len(cipher)):
        analysis[cipher[i]] += 1

    #Calculate IoC and return
    for char in analysis:
        IoC += analysis[char]**2
    return IoC / len(cipher)**2


#Description: Takes the text given by cipher and prints
#             the most likely Viginere keyword lengths.
def getKeyLengths(cipher):
    print("\n---Possible Keyword Lengths---")
    IoC = 0

    #Calculate average IoC's
    for i in range(1, len(cipher)):
        for j in range(i):
            IoC += getIoC(cipher[j::i])
        IoC /= i

        #Standard English IoC: ~0.067
        #Current Difference Cutoff: 0.005
        if(abs(IoC - 0.067) < 0.005):
            print("Keylength: ", i, "Percent Match: ", end='')
            print(100*(0.067 - abs(IoC - 0.067)) / 0.067, "%")


#Description: Encrypts the text given by cipher and
#             prints result to stdout.
def encrypt(cipher):
    key = input("\nPlease enter the keyword: ").upper()
    choice = input("Are you decrypting (y/n)? ")
    encrypt = ''

    #Change key for decryption
    if(choice == 'y'):
        temp = ''
        for i in range(len(key)):
            temp += chr((65 - ord(key[i])) % 26 + 65)
        key = temp

    #Encryption
    for i in range(len(cipher)):
        encrypt += chr((ord(cipher[i]) + ord(key[i % len(key)]) - 2*65) % 26 + 65)

    print('\n', encrypt, '\n')


if __name__ == "__main__":
    print("\nVigenere Cipher Analysis")
    print("------------------------")
    choice = 0

    while(True):
        #Main menu
        print("1) Index of Coincidence")
        print("2) Keyword Lengths")
        print("3) Encrypt/Decrypt")
        print("4) Exit")
        choice = input("Please select an option: ")

        #Check for exit
        if(choice == '4'):
            break

        #Get cipher text
        try:
            cipher = open(input("Enter file name: "), "r").read().upper().replace('\n', '')
        except:
            print("Couldn't open file. Exiting program.")
            exit()

        #Execute selected function
        if(choice == '1'):
            print("Index of Coincidence: ", getIoC(cipher), "\n")
        elif(choice == '2'):
            getKeyLengths(cipher)
        elif(choice == '3'):
            encrypt(cipher)

    #Clean up and exit
    exit()
