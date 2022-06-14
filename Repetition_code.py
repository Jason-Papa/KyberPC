import numpy as np
def repetition_encode(m):
    return list(np.repeat(m, 3))

def repetition_decode(c):
    return [int(sum(c[i:i+3])>2) for i in range(0, len(c), 3) ]

def zero_padding(m, n):
    while len(m)< n:
        m = m + [0]
    return m