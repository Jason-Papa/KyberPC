import numpy as np
from polarcodes import *
import time
import matplotlib.pyplot as plt
# initialise polar code


tests = 100000
SNR_list = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]
BLER_list = []
for design_SNR in SNR_list:
    start_time = time.time()
    BLER = 0
    PC = PolarCode(256, 144)
    PC.construction_type = 'bb'

    
    Construct(PC, design_SNR)

    m = np.random.randint(2, size=PC.K)
    PC.set_message(m)

    Encode(PC)

    for i in range(tests):
        
        # transmit the codeword
        AWGN(PC, design_SNR)
        # decode the received codeword
        Decode(PC)
        decoded = (PC.message_received)
        if any(decoded != m):
            BLER += 1.0/tests
        
    print(BLER, design_SNR)
    BLER_list.append(BLER)

plt.plot(SNR_list, BLER_list)

plt.xlabel("SNR (dB)")
plt.ylabel("BLER")
plt.title("Block Error Rate vs Signal to Noise Ratio for (256,144) Polar Code ")
plt.show()