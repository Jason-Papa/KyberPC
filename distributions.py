## approach 1
from sage.all import parent, ZZ, vector, PolynomialRing, GF
from sage.all import log, ceil, randint, set_random_seed, random_vector, matrix, floor
import matplotlib.pyplot as plt
import time

def B(eta):
    r = 0
    for i in range(eta):
        r += randint(0, 1) - randint(0, 1)
    return r

def find_mean_variance(q):
    no_of_samples = sum(q.values())
    expected, variance = 0,0
    
    for k,v in q.items():
        expected += k*v / no_of_samples

    for k,v in q.items():
        variance += (k-expected)**2*v / no_of_samples
    return expected, variance


n = 256
q = 3329
eta = 2
k = 3
R, x = PolynomialRing(ZZ, "x").objgen()
f = R([1]+[0]*(n-1)+[1])
iterations_list =  [10, 100, 1000, 10000, 20000, 30000, 50000, 100000]
print("Kyber768")
for iterations in iterations_list:
    vals = {}
    start_time = time.time()
    for _ in range (iterations):
        N = 0
        e = vector(R, k, [R([(B(eta)) for _ in range(n)]) for _ in range(k)])
        s = vector(R, k, [R([(B(eta)) for _ in range(n)]) for _ in range(k)])
        r  = vector(R, k, [R([(B(eta)) for _ in range(n)]) for _ in range(k)])
        e1 = vector(R, k, [R([(B(eta)) for _ in range(n)]) for _ in range(k)])
        e2 = R([(B(eta)) for _ in range(n)])

        N = (e*r - s*e1 + e2 )% f
        for nn in N:
            if nn in vals.keys():
                vals[nn] += 1
            else:
                vals[nn] = 1

    minimum = min(vals)
    maximum = max(vals)
    x = []
    y = []
    total = sum(list(vals.values()))
    for i in range(minimum, maximum+1):
        if i in vals.keys():
            x.append(i)
            y.append(vals[i]/total)
    print(iterations,n,total)

    plt.plot(x, y)

    plt.xlabel("Outcome")
    plt.ylabel("Probability")
    plt.title("Distribution of N with "+str(iterations) +" trials ")
    plt.show()
    m, var = (find_mean_variance(vals))
    print(f"Number of trials = {iterations}, Mean = {float(m)}, Variance = {float(var)}")
###############################################################################################3
k=4
print("Kyber1024")
for iterations in iterations_list:
    vals = {}
    start_time = time.time()
    for _ in range (iterations):
        N = 0
        e = vector(R, k, [R([(B(eta)) for _ in range(n)]) for _ in range(k)])
        s = vector(R, k, [R([(B(eta)) for _ in range(n)]) for _ in range(k)])
        r  = vector(R, k, [R([(B(eta)) for _ in range(n)]) for _ in range(k)])
        e1 = vector(R, k, [R([(B(eta)) for _B in range(n)]) for _ in range(k)])
        e2 = R([(B(eta)) for _ in range(n)])

        N = (e*r - s*e1 + e2 )% f
        for nn in N:
            if nn in vals.keys():
                vals[nn] += 1
            else:
                vals[nn] = 1

    minimum = min(vals)
    maximum = max(vals)
    x = []
    y = []
    total = sum(list(vals.values()))
    for i in range(minimum, maximum+1):
        if i in vals.keys():
            x.append(i)
            y.append(vals[i]/total)
    print(iterations,n,total)

    plt.plot(x, y)

    plt.xlabel("Outcome")
    plt.ylabel("Probability")
    plt.title("Distribution of N with "+str(iterations) +" trials")
    plt.show()
    m, var = (find_mean_variance(vals))
    print(f"Number of trials = {iterations}, Mean = {float(m)}, Variance = {float(var)}")
##################################################################################################3
k = 2
print("Kyber512")
for iterations in iterations_list:
    start_time = time.time()
    vals = {}
    for _ in range (iterations):
        N = 0
        e = vector(R, k, [R([(B(3)) for _ in range(n)]) for _ in range(k)])
        s = vector(R, k, [R([(B(3)) for _ in range(n)]) for _ in range(k)])
        r  = vector(R, k, [R([(B(3)) for _ in range(n)]) for _ in range(k)])
        e1 = vector(R, k, [R([(B(2)) for _ in range(n)]) for _ in range(k)])
        e2 = R([(B(2)) for _ in range(n)])

        N = (e*r - s*e1 + e2 )% f
        for nn in N:
            if nn in vals.keys():
                vals[nn] += 1
            else:
                vals[nn] = 1

    minimum = min(vals)
    maximum = max(vals)
    x = []
    y = []
    total = sum(list(vals.values()))
    for i in range(minimum, maximum+1):
        if i in vals.keys():
            x.append(i)
            y.append(vals[i]/total)
    print(iterations,n,total)

    plt.plot(x, y)

    plt.xlabel("Outcome")
    plt.ylabel("Probability")
    plt.title("Distribution of N with "+str(iterations) +" trials")
    plt.show()
    m, var = (find_mean_variance(vals))
    print(f"Number of trials = {iterations}, Mean = {float(m)}, Variance = {float(var)}")