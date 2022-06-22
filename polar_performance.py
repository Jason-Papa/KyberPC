import numpy as np
from polarcodes import *
import time
# initialise polar code

start_time = time.time()
PC = PolarCode(256, 144)
PC.construction_type = 'bb'

# mothercode construction
design_SNR  = 37.55
Construct(PC, design_SNR)

m = np.random.randint(2, size=PC.K)
PC.set_message(m)

Encode(PC)
encode_time = time.time() - start_time

# transmit the codeword
AWGN(PC, design_SNR)
# decode the received codeword
Decode(PC)
decode_time = time.time() - start_time - encode_time
total_time = time.time() - start_time

print(f"encoding = {encode_time}, decode = {decode_time}, total = {total_time}")