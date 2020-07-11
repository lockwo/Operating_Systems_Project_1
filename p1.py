import sys

class Params(object):
    def __init__(self, n, seed, lam, upper_bound, t_cs, tau, t_slice, rr_add):
        self.n = n
        self.seed = seed
        self.lam = lam
        self.upper_bound = upper_bound
        self.t_cs = t_cs
        self.tau = tau
        self.t_slice = t_slice
        self.rr_add = rr_add

if len(sys.argv) == 9:
    params = Params(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])
else:
    params = Params(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], "END")

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
