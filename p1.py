import sys
from process import Process
from rand48 import Rand48

class Params(object):
    def __init__(self, n, seed, lam, upper_bound, t_cs, alpha, t_slice, rr_add):
        self.n = int(n)
        self.seed = int(seed)
        self.lam = float(lam)
        self.upper_bound = int(upper_bound)
        self.t_cs = int(t_cs)
        self.alpha = float(alpha)
        self.t_slice = int(t_slice)
        self.rr_add = rr_add

if len(sys.argv) == 9:
    params = Params(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])
else:
    params = Params(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], "END")

processes = []
ran = Rand48(params.seed)
for i in range(params.n):
    processes.append(Process(chr(i + 65), params, ran))

# FCFS
time = 0
while(1):
    break 
    time += 1

processes = []
ran = Rand48(params.seed)
for i in range(params.n):
    processes.append(Process(chr(i + 65), params, ran))

# SJF
time = 0
while(1):
    print("TODO")
    break
    time += 1

processes = []
ran = Rand48(params.seed)
for i in range(params.n):
    processes.append(Process(chr(i + 65), params, ran))

# SRT
time = 0
while(1):
    print("TODO")
    break
    time += 1

processes = []
ran = Rand48(params.seed)
for i in range(params.n):
    processes.append(Process(chr(i + 65), params, ran))

# RR
time = 0
while(1):
    print("TODO")
    break
    time += 1