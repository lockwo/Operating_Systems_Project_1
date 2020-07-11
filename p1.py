import sys
from process import Process

class Params(object):
    def __init__(self, n, seed, lam, upper_bound, t_cs, tau, t_slice, rr_add):
        self.n = int(n)
        self.seed = int(seed)
        self.lam = int(lam)
        self.upper_bound = int(upper_bound)
        self.t_cs = int(t_cs)
        self.tau = int(tau)
        self.t_slice = int(t_slice)
        self.rr_add = rr_add

if len(sys.argv) == 9:
    params = Params(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])
else:
    params = Params(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], "END")

processes = []
for i in range(params.n):
    processes.append(Process(chr(i + 65), params))

# FCFS
time = 0
while(1):




    time += 1

# SJF
time = 0
while(1):




    time += 1

# SRT
time = 0
while(1):




    time += 1

# RR
time = 0
while(1):




    time += 1
