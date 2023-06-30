import random
import time

def binary_exponentiation(base, e, mod):
    result = 1
    base %= mod         # Reduce the base modulo mod
    while e:
        if e & 1:       # If e is odd
            result = (result * base) % mod      # Multiply result with base
        base = (base * base) % mod              # Square the base
        e >>= 1         # Divide e by 2
    return result

def check_composite(n, a, d, s):
    x = binary_exponentiation(a, d, n)
    if x == 1 or x == n - 1:
        return False
    for r in range(1, s):
        x = (x * x) % n
        if x == n - 1:
            return False
    return True

def miller_rabin_primality_test(n, k = 5):
    if n < 4:
        return n == 2 or n == 3

    s = 0
    d = n - 1
    while d & 1 == 0:
        d >>= 1
        s += 1

    for i in range(k):
        a = 2 + random.randint(0, n - 3)
        if check_composite(n, a, d, s):
            return False
    return True

# Generate a large prime p which is at least k bits long
def generate_prime_number(k):
    while True:
        p = random.getrandbits(k)
        if miller_rabin_primality_test(p, 5):
            return p

# Find a primitive root g using Euler's totient function for mod p. Take two parameters – min and max – both less than p. 
# Then g should be in the range [min,max]
def generate_primitive_root(p, min, max):
    phi = p - 1
    while True:
        g = random.randint(min, max)
        if binary_exponentiation(g, phi, p) == 1:
            return g

k = 256

p_start_time = time.perf_counter()
p = generate_prime_number(k)
p_time = time.perf_counter() - p_start_time
print("Time taken to generate prime number p :", p_time)

g_start_time = time.perf_counter()
g = generate_primitive_root(p, 2, p-2)
g_time = time.perf_counter() - g_start_time
print("Time taken to generate primitive root g :", g_time)

# generate random prime number a of given bit length k/2
a_start_time = time.perf_counter()
a = generate_prime_number(int(k/2))
a_time = time.perf_counter() - a_start_time
print("Time taken to generate random prime number a :", a_time)

b = generate_prime_number(int(k/2))

# Compute A = g^a (mod p)
A_start_time = time.perf_counter()
A = binary_exponentiation(g, a, p)
A_time = time.perf_counter() - A_start_time
print("Time taken to compute A :", A_time)

B = binary_exponentiation(g, b, p)

c1_start_time = time.perf_counter()
C1 = binary_exponentiation(B, a, p)
C2 = binary_exponentiation(A, b, p)
if C1 == C2:
    print("Private Key Shared :", C1)
c1_time = time.perf_counter() - c1_start_time
print("Time taken to compute C1 and C2 :", c1_time)