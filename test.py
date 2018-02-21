import des
import aes

if __name__ == "__main__":
    plaintext = 0x0123456789abcdeffedcba9876543210
    #plaintext = 0xff0b844a0853bf7c6934ab4364148fb9
    key = 0x0f1571c947d9e8590cb7add6af7f6798
    print(hex(aes.aes(plaintext, key)))
