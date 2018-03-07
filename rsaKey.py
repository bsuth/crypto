# Used for PRNG purposes.
import random


# Description: An implementation of the Miller-Rabin
#              primality test up to 99.9% accuracy.
# Note:        Assumed that n is sufficiently
#              large (for randint function).
def MillerRabin(n):
    # Check parity
    if(not n % 2):
        return False

    # Find k, odd q such that n-1 = (2^k)q
    k = 1
    q = (n - 1) // 2
    while(not q % 2):
        k += 1
        q //= 2

    # Conduct 10 tests for 99.9% accuracy (1 - 1/(2^10))
    for i in range(10):
        a = random.randint(2, n - 2)

        # Check gcd
        if(gcd(a, n) != 1):
            return False

        # Check primality conditions
        if(a**q % n != 1) and (n-1 not in [a**((2**j)*q) % n for j in range(k)]):
            return False

    # All tests passed
    return True


# Description: An implementation of the Euclidean
#              algorithm to find the gcd of a and b.
def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


# Decription: Finds the inverse of a mod m using
#             the Extended Euclidean Algorithm.
def modInvHelper(m, a, r1, r2):
    return (a, m % a, r2, -(m // a) * r2 + r1)
def modInverse(m, a):
    newM = m 
    newA = a
    r1 = 0
    r2 = 1

    while(a*r2 % m != 1):
        newM, newA, r1, r2 = modInvHelper(newM, newA, r1, r2)

    return r2 % m


# Description: Generates an RSA public/private key pair.
# Note:        For simplicity, the sizes of p and q are
#              quite limited. This is, of course, by no
#              means secure and is only for conceptual
#              understanding purposes.
def genKey():
    p = q = e = 0

    # Find p and q
    while(not MillerRabin(p)):
        p = random.randint(1, 65536)
    while(not MillerRabin(q)):
        q = random.randint(1, 65536)

    n = p * q
    phin = (p-1) * (q-1)

    # Find e and d
    while(gcd(phin, e) != 1):
        e = random.randint(1, 65536)
    d = modInverse(phin, e)

    print(p, q)
    print("Private key: ", d)
    print("Public key: (", e, ", ", n, ")")
