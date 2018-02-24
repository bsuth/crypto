# To get byte size of key in RC4
import sys

# Description: Generates a sequence of pseudo-random numbers
#              using a Linear Congruential Generator. Follows
#              the relation X_{n+1} = (a * X_n) mod m.
# Note:        For convenience and choice limitations, a and m
#              are default initialized to 7^5 and 2^{31} - 1.
def LCG(seed, num_random, a = 7**5, m = 2**31 - 1):
    for i in range(num_random):
        seed = (a * seed) % m
        print(seed)


# Description: An implementation of the Blum Blum Shub PRNG.
#              p and q MUST be  large primes that are 3 mod 4
#              and the seed must be relatively prime to these.
#              (Think about Legendre Symbol/quadratic residues)
def BBS(seed, num_random, p, q):
    # Calculate modulus and seed
    n = p * q
    seed = (seed**2) % n

    # Generate bits
    for i in range(num_random):
        seed = (seed**2) % n
        print(seed & 1)


# Description: An implementation of the RC4 PRNG.
def RC4(key, num_random):
    # Initialize vectors
    S = [i for i in range(255)]
    T = [(key >> i % sys.getsizeof(key)) & 1 for i in range(255)]

    # Permute S with pseudorandom swaps
    j = 0
    for i in range(255):
        # Next permutation
        j = (j + S[i] + T[i]) % 256

        # Swap
        temp = S[i]
        S[i] = S[j]
        S[j] = temp

    # Generate numbers
    j = k = 0
    for i in range(num_random):
        # Next pair to swap
        j = (j + 1) % 256
        k = (k + S[j]) % 256
        
        # Swap
        temp = S[j]
        S[j] = S[k]
        S[k] = temp

        # Next number
        print(S[(S[j] + S[k]) % 256])
