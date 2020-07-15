import sys
from process import Process
from rand48 import Rand48
from print_sim import p_sim, end
from params import Params
from algorithms import round_robin

if len(sys.argv) == 9:
    params = Params(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])
else:
    params = Params(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], "END")

# FCFS
processes = []
ran = Rand48(params.seed)
ran.srand(params.seed)
for i in range(params.n):
    processes.append(Process(chr(i + 65), params, ran))

# RR
round_robin(processes, params, True)

processes = []
ran = Rand48(params.seed)
ran.srand(params.seed)
for i in range(params.n):
    processes.append(Process(chr(i + 65), params, ran))

# SJF
Q = []
time = 0
while(1):
    p_sim(time, processes, Q, params, "SJF")
    break
    time += 1

processes = []
ran = Rand48(params.seed)
ran.srand(params.seed)
for i in range(params.n):
    processes.append(Process(chr(i + 65), params, ran))

# SRT
Q = []
time = 0
while(1):
    p_sim(time, processes, Q, params, "SRT")
    break
    time += 1


# RR
processes = []
ran = Rand48(params.seed)
ran.srand(params.seed)
for i in range(params.n):
    processes.append(Process(chr(i + 65), params, ran))

round_robin(processes, params)

#end([0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0])
