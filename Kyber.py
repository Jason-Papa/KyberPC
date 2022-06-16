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
du = 10
dv = 4
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

def add_noise_v(v, P):
    noisy_v = []
    for vv in v:
        noise = R([2**(int(random.uniform(0,3))) if random.uniform(0,1) < P else 0 for _ in range(0, n)])
        noisy_v.append(vv + noise)
    return noisy_v
    
def add_noise_u(u, P):
    noisy_u = []
    for uu in u:
        noise = vector(R, k, [R([ 2**(int(random.uniform(0,9))) if random.uniform(0,1) < P else 0 for _ in range(0, n)]) for _ in range(k)])
        noisy_u.append(uu + noise)
    return noisy_u

def compress(poly, d):
    return R([round(int(coeff) * (2**d)/(q-1))  for coeff in poly])

def compress_u(polys, d):
    for i in range(k):
        polys[i] = compress(polys[i], d)
    return polys
    

def decompress(poly_list, d):
    return [R([round(int(coeff) * (q-1) /(2**d)) for coeff in poly]) for poly in poly_list]

def decompress_u(poly_list, d):
    for i in range(len(poly_list)):
        for j in range(k):
            poly_list[i][j] = decompress([poly_list[i][j]], d)[0]
    return poly_list
            

def decompress_list(lst, d):
    return [round(int(coeff) * (q-1) /(2**d)) for coeff in lst]
    

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
        v.append(compress( (r*t + e_2 + R(decompress_list(submessage, 1))) % fx, dv))
        u.append(compress_u((r*A + e_1) % fx, du))
    return u, v

def decrypt(u, v, sk, for_pc = False):
    message = []
    
    v = decompress(v, dv)
    u = decompress_u(u, du)
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
