import des
import aes

if __name__ == "__main__":
    plaintext = 0x02468aceeca86420
    key = 0x0f1571c947d9e859
    print(hex(des.decrypt(des.encrypt(plaintext, key), key)))
