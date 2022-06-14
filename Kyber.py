from sage.all import parent, ZZ, vector, PolynomialRing, GF
from sage.all import log, ceil, randint, set_random_seed, random_vector, matrix, floor
import numpy as np
import random 

# Kyber parameters
n = 256
q = 3329
k = 3
eta1 = 2
eta2 = 2
Fq = GF(q)
Rq = PolynomialRing(Fq, "x")
R, x = PolynomialRing(ZZ, "x").objgen()
fx = R([1]+[0]*(n-1)+[1])

def B(eta):
    return sum(np.random.randint(0,2,eta) - np.random.randint(0,2,eta))

def string_to_bits(s):
    bits_message = []
    for letter in s:
        for i in range(6, -1, -1):
            bits_message.append(ord(letter)>>i & 1)
    return bits_message

def bits_to_string(b):
    s = []
    if len(b)==0:
        return ""
    sub = b[:7]
    i=0
    while not (sub == [0]*7) and i < len(b)//7:
        s.append(chr(int(''.join(str(item) for item in sub), 2)))
        i+=1      
        sub = b[7*i:7*i+7]   
    return "".join(s)

def map_q_to_01(polynomial):
    new_coeffs = [(coeff + q//4) % q for coeff in polynomial]
    return [int(new_coeff)*(2/q) - 0.5 for new_coeff in new_coeffs ]

def add_noise_v(v, SNR):
    noisy_v = []
    for vv in v:
        signal_power_db = 10*np.log10(q**2/4)
        noise_power_db = signal_power_db - SNR
        noise = R([round(random.normalvariate(0, 10**(noise_power_db/10))) for _ in range(0, n)])
        noisy_v.append(vv + noise)
    return noisy_v
    
def add_noise_u(u, SNR):
    noisy_u = []
    for uu in u:
        signal_power_db = 10*np.log10(q**2/4)
        noise_power_db = signal_power_db - SNR
        noise = vector(R, k, [R([ round(random.normalvariate(0, 10**(noise_power_db/10))) for _ in range(n)]) for _ in range(k)])
        noisy_u.append(uu + noise)
    return noisy_u

def generate_keys():
    A = matrix(Rq, k, k, [Rq.random_element(degree=n-1) for _ in range(k*k)])
    e = vector(R, k, [R([(B(eta1)) for _ in range(n)]) for _ in range(k)])
    s = vector(R, k, [R([(B(eta1)) for _ in range(n)]) for _ in range(k)])
    t = ( A*s + e) % fx

    return (A, t), s # (pk), sk


def encrypt(message, pk):
    A, t = pk
    if type(message) == str:
        message = string_to_bits(message)
    
    message = list(message)
    message = [message[i:i+256] for i in range(0, len(message), 256)]
    u, v = [], []
    r = vector(R, k, [R([(B(eta1)) for _ in range(n)]) for _ in range(k)])
    e_1 = vector(R, k, [R([(B(eta2)) for _ in range(n)]) for _ in range(k)])
    e_2 = R([(B(eta2)) for _ in range(n)])
    for submessage in message:
        u.append((r*A + e_1) % fx)
        v.append((r*t + e_2 + q//2 * R(submessage)) % fx)
    return u, v

def decrypt(u, v, sk, for_pc = False):
    message = []
    for i in range(0, len(v)):
        decrypted_message = (v[i] - sk*u[i]) % fx
        if for_pc:
            message.append(map_q_to_01(decrypted_message))
        else:
            message.append([int(coef > q//4 and coef < 3*q//4) for coef in decrypted_message])
    if for_pc:
        return np.array([bit for submessage in message for bit in submessage])
    else:
        all_messages = [bit for submessage in message for bit in submessage]
        return "".join([bits_to_string(bits) for bits in [all_messages[i:i+7] for i in range(0, len(all_messages), 7)] ])